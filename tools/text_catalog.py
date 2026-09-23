"""Create and apply lossless CP932 TSV translation catalogues."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ENCODING = 'cp932'


def split_records(raw):
    records = []
    for part in raw.splitlines(keepends=True):
        if part.endswith(b'\r\n'):
            body, ending = part[:-2], b'\r\n'
        elif part.endswith((b'\r', b'\n')):
            body, ending = part[:-1], part[-1:]
        else:
            body, ending = part, b''
        try:
            cells = body.decode(ENCODING).split('\t')
        except UnicodeDecodeError as exc:
            raise ValueError('TSV contains invalid CP932') from exc
        records.append((cells, ending))
    if not raw:
        return []
    return records


def row_id(index, cells, id_column):
    if id_column is None:
        return f'row-{index:04d}'
    if id_column >= len(cells) or not cells[id_column]:
        raise ValueError(f'row {index} has no value in ID column {id_column}')
    return f'key-{cells[id_column]}'


def create(raw, resource, columns, id_column=None):
    records = split_records(raw)
    if not records:
        raise ValueError('empty TSV is unsupported')
    if not isinstance(resource, str) or not resource:
        raise ValueError('resource path is required')
    if not columns or any(not isinstance(col, int) or col < 0 for col in columns):
        raise ValueError('at least one non-negative translation column is required')
    if len(set(columns)) != len(columns):
        raise ValueError('translation columns must be unique')
    if id_column is not None and (not isinstance(id_column, int) or id_column < 0):
        raise ValueError('ID column must be non-negative')
    seen = set()
    rows = []
    for i, (cells, ending) in enumerate(records):
        identifier = row_id(i, cells, id_column)
        if identifier in seen:
            raise ValueError(f'duplicate stable row ID {identifier!r}')
        seen.add(identifier)
        if any(col >= len(cells) for col in columns):
            raise ValueError(f'row {i} has fewer than {max(columns) + 1} columns')
        rows.append(dict(id=identifier, original_cells=cells,
                         translations={str(col): None for col in columns if cells[col]},
                         line_ending=ending.decode('ascii')))
    return dict(format='marps2-cp932-tsv-v1', resource=resource,
                source_sha256=hashlib.sha256(raw).hexdigest(), encoding=ENCODING,
                columns=columns, id_column=id_column, rows=rows)


def validate(catalog):
    if catalog.get('format') != 'marps2-cp932-tsv-v1' or catalog.get('encoding') != ENCODING:
        raise ValueError('unsupported text catalogue format or encoding')
    resource, digest, columns, rows = (catalog.get('resource'), catalog.get('source_sha256'),
                                       catalog.get('columns'), catalog.get('rows'))
    if not isinstance(resource, str) or not resource:
        raise ValueError('invalid catalogue resource')
    try:
        bytes.fromhex(digest)
    except (TypeError, ValueError) as exc:
        raise ValueError('invalid source hash') from exc
    if len(digest) != 64 or not isinstance(columns, list) or not columns or not isinstance(rows, list):
        raise ValueError('invalid catalogue hash, columns, or rows')
    if any(not isinstance(c, int) or c < 0 for c in columns) or len(columns) != len(set(columns)):
        raise ValueError('invalid or duplicate translation columns')
    if not rows:
        raise ValueError('empty catalogue is unsupported')
    id_column = catalog.get('id_column')
    if id_column is not None and (not isinstance(id_column, int) or id_column < 0):
        raise ValueError('invalid ID column')
    ids = set()
    for i, row in enumerate(rows):
        if not isinstance(row, dict) or not isinstance(row.get('original_cells'), list):
            raise ValueError(f'invalid catalogue row {i}')
        cells = row['original_cells']
        if not all(isinstance(cell, str) for cell in cells):
            raise ValueError(f'invalid original cell in row {i}')
        identifier = row_id(i, cells, id_column)
        if row.get('id') != identifier or identifier in ids:
            raise ValueError(f'invalid or duplicate row ID at row {i}')
        ids.add(identifier)
        ending = row.get('line_ending')
        if ending not in ('', '\n', '\r', '\r\n'):
            raise ValueError(f'invalid line ending in row {i}')
        translations = row.get('translations')
        if not isinstance(translations, dict):
            raise ValueError(f'invalid translations map in row {i}')
        for key, value in translations.items():
            try:
                col = int(key)
            except (TypeError, ValueError) as exc:
                raise ValueError(f'invalid translation column in row {i}') from exc
            if (str(col) != key or col not in columns or col >= len(cells)
                    or (value is not None and not isinstance(value, str))
                    or (value is not None and '\0' in value)):
                raise ValueError(f'invalid translation value in row {i}, column {key}')
            if value is not None:
                try:
                    value.encode(ENCODING)
                except UnicodeEncodeError as exc:
                    raise ValueError(f'translation at row {i}, column {key} is not CP932-encodable') from exc


def apply(raw, catalog):
    validate(catalog)
    if hashlib.sha256(raw).hexdigest() != catalog['source_sha256']:
        raise ValueError('TSV source hash differs from catalogue original')
    records = split_records(raw)
    rows = catalog['rows']
    if len(records) != len(rows):
        raise ValueError('TSV row count differs from catalogue')
    output = bytearray()
    for i, ((cells, _), row) in enumerate(zip(records, rows)):
        if cells != row['original_cells']:
            raise ValueError(f'TSV source cells differ from catalogue at row {i}')
        if row_id(i, cells, catalog.get('id_column')) != row['id']:
            raise ValueError(f'TSV row identity differs from catalogue at row {i}')
        for key, translation in row['translations'].items():
            if translation is not None:
                cells[int(key)] = translation
        try:
            output.extend('\t'.join(cells).encode(ENCODING))
        except UnicodeEncodeError as exc:
            raise ValueError(f'updated TSV row {i} is not CP932-encodable') from exc
        output.extend(row['line_ending'].encode('ascii'))
    return bytes(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    make = sub.add_parser('create')
    make.add_argument('source', type=Path)
    make.add_argument('output', type=Path)
    make.add_argument('--resource', required=True)
    make.add_argument('--columns', required=True, help='comma-separated zero-based translation columns')
    make.add_argument('--id-column', type=int)
    rebuild = sub.add_parser('apply')
    rebuild.add_argument('source', type=Path)
    rebuild.add_argument('catalog', type=Path)
    rebuild.add_argument('output', type=Path)
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise ValueError('output already exists')
        if args.command == 'create':
            columns = [int(value) for value in args.columns.split(',')]
            document = create(args.source.read_bytes(), args.resource, columns, args.id_column)
            output = json.dumps(document, ensure_ascii=False, indent=2) + '\n'
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output, encoding='utf-8')
        else:
            document = json.loads(args.catalog.read_text(encoding='utf-8'))
            output = apply(args.source.read_bytes(), document)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_bytes(output)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
