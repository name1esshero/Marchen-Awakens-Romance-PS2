"""Create and apply a tracked translation catalogue for the observed message table."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import messages


def entry_id(kind, key, occurrence):
    return f'msg-k{kind:08x}-i{key:08x}-o{occurrence:03d}'


def occurrences(entries):
    seen = {}
    result = []
    for entry in entries:
        pair = (entry['kind'], entry['key'])
        occurrence = seen.get(pair, 0)
        seen[pair] = occurrence + 1
        result.append(occurrence)
    return result


def create(document):
    raw = messages.build(document)
    rows = []
    for index, (entry, occurrence) in enumerate(zip(document['entries'], occurrences(document['entries']))):
        kind, key = entry['kind'], entry['key']
        rows.append(dict(
            id=entry_id(kind, key, occurrence),
            record_index=index,
            kind=kind,
            key=key,
            occurrence=occurrence,
            original=entry['text'],
            translation=None,
            context='System message table; runtime call site not traced.',
            notes='',
            status='untranslated',
        ))
    return dict(
        format='marps2-message-catalog-v1',
        resource='disc!/_DATA.YFS;1!/data/common.pac!/_msg.dat',
        source_sha256=hashlib.sha256(raw).hexdigest(),
        source_format=document['format'],
        header_hex=document['header_hex'],
        entries=rows,
    )


def validate_catalog(catalog):
    if catalog.get('format') != 'marps2-message-catalog-v1':
        raise ValueError('unsupported message catalogue format')
    if catalog.get('resource') != 'disc!/_DATA.YFS;1!/data/common.pac!/_msg.dat':
        raise ValueError('catalogue resource identity does not match the supported table')
    try:
        digest = catalog['source_sha256']
        bytes.fromhex(digest)
        entries = catalog['entries']
        header = bytes.fromhex(catalog['header_hex'])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError('invalid message catalogue') from exc
    if len(digest) != 64 or len(header) != messages.HEADER_SIZE or not isinstance(entries, list):
        raise ValueError('invalid catalogue digest, header, or entries')
    seen_ids = set()
    for row in entries:
        if not isinstance(row, dict):
            raise ValueError('catalogue entry must be an object')
        required = ('id', 'kind', 'key', 'occurrence', 'original', 'translation', 'status')
        if any(key not in row for key in required):
            raise ValueError('catalogue entry is missing required fields')
        identifier = entry_id(row['kind'], row['key'], row['occurrence'])
        if row['id'] != identifier or identifier in seen_ids:
            raise ValueError('catalogue IDs must uniquely match kind/key/occurrence')
        seen_ids.add(identifier)
        if not isinstance(row['original'], str) or '\0' in row['original']:
            raise ValueError(f'invalid original text for {identifier}')
        translation = row['translation']
        if translation is not None and (not isinstance(translation, str) or '\0' in translation):
            raise ValueError(f'invalid translation for {identifier}')
        expected = 'translated' if translation else 'untranslated'
        if row['status'] != expected:
            raise ValueError(f'status does not match translation for {identifier}')
        for field in ('kind', 'key', 'occurrence', 'record_index'):
            if field in row and (not isinstance(row[field], int) or row[field] < 0):
                raise ValueError(f'invalid {field} for {identifier}')


def apply(document, catalog):
    validate_catalog(catalog)
    if document.get('format') != catalog.get('source_format') or document.get('header_hex') != catalog['header_hex']:
        raise ValueError('message source format/header differs from catalogue')
    if hashlib.sha256(messages.build(document)).hexdigest() != catalog['source_sha256']:
        raise ValueError('message source hash differs from catalogue original')
    base_entries = document.get('entries')
    rows = catalog['entries']
    if len(base_entries) != len(rows):
        raise ValueError('message source entry count differs from catalogue')
    counts = {}
    output = dict(document)
    output['entries'] = [dict(entry) for entry in base_entries]
    for index, (entry, row) in enumerate(zip(base_entries, rows)):
        pair = (entry['kind'], entry['key'])
        occurrence = counts.get(pair, 0)
        counts[pair] = occurrence + 1
        if (row['kind'], row['key'], row['occurrence'], row.get('record_index'), row['original']) != (
                entry['kind'], entry['key'], occurrence, index, entry['text']):
            raise ValueError(f'message source does not match catalogue row {row["id"]}')
        output['entries'][index]['text'] = row['translation'] or row['original']
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    make = sub.add_parser('create')
    make.add_argument('source', type=Path, help='editable messages JSON from tools/messages.py')
    make.add_argument('output', type=Path)
    apply_parser = sub.add_parser('apply')
    apply_parser.add_argument('source', type=Path)
    apply_parser.add_argument('catalog', type=Path)
    apply_parser.add_argument('output', type=Path)
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise ValueError('output already exists')
        document = json.loads(args.source.read_text(encoding='utf-8'))
        if args.command == 'create':
            result = create(document)
            content = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(content, encoding='utf-8')
        else:
            catalog = json.loads(args.catalog.read_text(encoding='utf-8'))
            result = apply(document, catalog)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
