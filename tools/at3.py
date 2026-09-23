#!/usr/bin/env python3
"""Inspect the observed AT3 header and fixed-width texture-name records."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


HEADER_SIZE = 0x10
TEXTURE_NAME_RECORD_SIZE = 0x40
REFERENCE_TRAILER_SIZE = 4


def parse(raw: bytes) -> dict:
    if len(raw) < HEADER_SIZE:
        raise ValueError('truncated AT3 header')
    if raw[:4] != b'AT  ':
        raise ValueError('not an AT3 resource (expected AT two-space magic)')
    field_04 = int.from_bytes(raw[4:8], 'little')
    reference_count = int.from_bytes(raw[8:12], 'little')
    record_size = int.from_bytes(raw[12:16], 'little')
    if record_size != TEXTURE_NAME_RECORD_SIZE:
        raise ValueError(f'unsupported AT3 reference record size {record_size}')
    record_stride = record_size + REFERENCE_TRAILER_SIZE
    table_end = HEADER_SIZE + reference_count * record_stride
    if table_end > len(raw):
        raise ValueError('AT3 texture-name table exceeds file size')

    references = []
    for index in range(reference_count):
        offset = HEADER_SIZE + index * record_stride
        record = raw[offset:offset + record_size]
        trailer_offset = offset + record_size
        terminator = record.find(b'\0')
        if terminator < 0:
            raise ValueError(f'AT3 reference {index} has no NUL terminator')
        name_raw = record[:terminator]
        try:
            name = name_raw.decode('cp932')
        except UnicodeDecodeError as exc:
            raise ValueError(f'AT3 reference {index} is not valid CP932') from exc
        references.append({
            'index': index,
            'offset': offset,
            'name': name,
            'name_hex': name_raw.hex(),
            'following_field': int.from_bytes(
                raw[trailer_offset:trailer_offset + REFERENCE_TRAILER_SIZE],
                'little'),
        })

    return {
        'magic': 'AT  ',
        'field_04': field_04,
        'texture_reference_count': reference_count,
        'reference_record_size': record_size,
        'reference_stride': record_stride,
        'reference_table_end': table_end,
        'file_size': len(raw),
        'references': references,
        'post_table_size': len(raw) - table_end,
        'post_table_sha256': hashlib.sha256(raw[table_end:]).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    args = parser.parse_args()
    try:
        result = parse(args.source.read_bytes())
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
