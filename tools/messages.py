"""Extract and rebuild the observed Japanese message-table candidate."""
import argparse
import json
from pathlib import Path
import struct
import sys

HEADER_SIZE = 8
ENTRY_SIZE = 12


def parse(data):
    if len(data) < HEADER_SIZE:
        raise ValueError('message table is shorter than its header')
    count = struct.unpack_from('<I', data)[0]
    table_end = HEADER_SIZE + count * ENTRY_SIZE
    if table_end > len(data):
        raise ValueError('message table records exceed file size')

    records = []
    offsets = []
    for i in range(count):
        kind, key, offset = struct.unpack_from('<III', data, HEADER_SIZE + i * ENTRY_SIZE)
        offsets.append(offset)
        records.append(dict(kind=kind, key=key))

    if not count:
        if table_end != len(data):
            raise ValueError('empty message table has trailing data')
        return dict(format='observed-msg-v1', header_hex=data.hex(), entries=[])
    if offsets[0] != table_end - HEADER_SIZE:
        raise ValueError('first message does not follow the record table')
    if any(a >= b for a, b in zip(offsets, offsets[1:])):
        raise ValueError('message offsets are not strictly increasing')

    for i, entry in enumerate(records):
        start = HEADER_SIZE + offsets[i]
        end = HEADER_SIZE + (offsets[i + 1] if i + 1 < count else len(data) - HEADER_SIZE)
        if start < table_end or end > len(data) or start >= end:
            raise ValueError('message extent is outside the string area')
        raw = data[start:end]
        if raw[-1:] != b'\0' or b'\0' in raw[:-1]:
            raise ValueError('message must have one terminal NUL and no embedded NUL')
        try:
            entry['text'] = raw[:-1].decode('cp932')
        except UnicodeDecodeError as exc:
            raise ValueError(f'message {i} is not valid CP932') from exc

    return dict(format='observed-msg-v1', header_hex=data[:HEADER_SIZE].hex(), entries=records)


def build(document):
    if document.get('format') != 'observed-msg-v1':
        raise ValueError('unsupported message document format')
    try:
        header = bytes.fromhex(document['header_hex'])
        entries = document['entries']
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError('invalid message document') from exc
    if len(header) != HEADER_SIZE or not isinstance(entries, list):
        raise ValueError('invalid message header or entry list')
    if len(entries) > 0xffffffff:
        raise ValueError('too many message entries')
    out = bytearray(header)
    struct.pack_into('<I', out, 0, len(entries))
    out.extend(b'\0' * (len(entries) * ENTRY_SIZE))
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ValueError(f'invalid message entry {i}')
        kind, key, text = entry.get('kind'), entry.get('key'), entry.get('text')
        if (not isinstance(kind, int) or not 0 <= kind <= 0xffffffff
                or not isinstance(key, int) or not 0 <= key <= 0xffffffff
                or not isinstance(text, str) or '\0' in text):
            raise ValueError(f'invalid message entry {i}')
        try:
            encoded = text.encode('cp932')
        except UnicodeEncodeError as exc:
            raise ValueError(f'message {i} contains characters not representable in CP932') from exc
        offset = len(out) - HEADER_SIZE
        if offset > 0xffffffff:
            raise ValueError('message data exceeds 32-bit offsets')
        struct.pack_into('<III', out, HEADER_SIZE + i * ENTRY_SIZE, kind, key, offset)
        out.extend(encoded)
        out.append(0)
    return bytes(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    extract = sub.add_parser('extract')
    extract.add_argument('source', type=Path)
    extract.add_argument('output', type=Path)
    rebuild = sub.add_parser('build')
    rebuild.add_argument('source', type=Path)
    rebuild.add_argument('output', type=Path)
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise ValueError('output already exists')
        if args.command == 'extract':
            result = json.dumps(parse(args.source.read_bytes()), ensure_ascii=False, indent=2) + '\n'
            args.output.write_text(result, encoding='utf-8')
        else:
            result = build(json.loads(args.source.read_text(encoding='utf-8')))
            args.output.write_bytes(result)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
