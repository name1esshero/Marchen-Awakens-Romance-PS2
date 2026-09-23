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
NODE_NAME_PREFIX_SIZE = 4
NODE_NAME_SLOT_SIZE = 0x40
NODE_FIXED_REGION_SIZE = 192
NODE_REPEAT_BLOCK_SIZE = 112


def _parse_node_records(raw: bytes, table_end: int):
    """Recognize the corpus-observed fixed-name AT animation-node envelope.

    Each observed node starts with a u32 64-byte name-slot length and a
    zero-padded CP932 name slot. The next node (or EOF) bounds its record.
    Across the recovered corpus, the remaining record extent is always a
    192-byte opaque region followed by zero or more 112-byte opaque blocks.
    Their internal field meanings are deliberately not inferred here.
    """
    starts = []
    for offset in range(table_end, len(raw) - NODE_NAME_PREFIX_SIZE - NODE_NAME_SLOT_SIZE + 1, 4):
        if int.from_bytes(raw[offset:offset + NODE_NAME_PREFIX_SIZE], 'little') != NODE_NAME_SLOT_SIZE:
            continue
        slot_start = offset + NODE_NAME_PREFIX_SIZE
        slot = raw[slot_start:slot_start + NODE_NAME_SLOT_SIZE]
        terminator = slot.find(b'\0')
        if terminator <= 0 or any(slot[terminator + 1:]):
            continue
        name_raw = slot[:terminator]
        try:
            name = name_raw.decode('cp932')
        except UnicodeDecodeError:
            continue
        if not name.isprintable():
            continue
        starts.append((offset, name, name_raw, slot))

    if not starts:
        return None

    nodes = []
    for index, (offset, name, name_raw, slot) in enumerate(starts):
        end = starts[index + 1][0] if index + 1 < len(starts) else len(raw)
        record_size = end - offset
        data_size = record_size - NODE_NAME_PREFIX_SIZE - NODE_NAME_SLOT_SIZE
        if data_size < NODE_FIXED_REGION_SIZE or (
                data_size - NODE_FIXED_REGION_SIZE) % NODE_REPEAT_BLOCK_SIZE:
            return None
        nodes.append({
            'index': index,
            'offset': offset,
            'size': record_size,
            'name': name,
            'original_name': name,
            'name_hex': name_raw.hex(),
            'name_slot_hex': slot.hex(),
            'opaque_data_hex': raw[offset + NODE_NAME_PREFIX_SIZE + NODE_NAME_SLOT_SIZE:end].hex(),
            'opaque_fixed_region_bytes': NODE_FIXED_REGION_SIZE,
            'opaque_repeat_block_bytes': NODE_REPEAT_BLOCK_SIZE,
            'opaque_repeat_block_count': (data_size - NODE_FIXED_REGION_SIZE) // NODE_REPEAT_BLOCK_SIZE,
        })

    return {
        'state': 'validated_envelope',
        'preamble_hex': raw[table_end:starts[0][0]].hex(),
        'record_count': len(nodes),
        'nodes': nodes,
        'basis': (
            'Every node has a u32 64-byte CP932 name slot; consecutive name slots '
            'and EOF bound records whose post-name extents are 192 + 112*n bytes. '
            'This validates record envelopes only, not the opaque fields.'
        ),
    }


def _encode_slot(name: str, original_name: str, original_slot_hex: str, capacity: int) -> bytes:
    if name == original_name:
        slot = bytes.fromhex(original_slot_hex)
        if len(slot) != capacity:
            raise ValueError('stored name slot has an invalid size')
        return slot
    try:
        encoded = name.encode('cp932')
    except UnicodeEncodeError as exc:
        raise ValueError(f'name is not encodable as CP932: {name!r}') from exc
    if not encoded or b'\0' in encoded or len(encoded) >= capacity:
        raise ValueError(f'name must encode to 1..{capacity - 1} bytes without NUL')
    return encoded + b'\0' + bytes(capacity - len(encoded) - 1)


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
            'original_name': name,
            'name_hex': name_raw.hex(),
            'name_slot_hex': record.hex(),
            'following_field': int.from_bytes(
                raw[trailer_offset:trailer_offset + REFERENCE_TRAILER_SIZE],
                'little'),
        })

    node_envelope = _parse_node_records(raw, table_end)
    post_table = raw[table_end:]

    return {
        'magic': 'AT  ',
        'field_04': field_04,
        'texture_reference_count': reference_count,
        'reference_record_size': record_size,
        'reference_stride': record_stride,
        'reference_table_end': table_end,
        'file_size': len(raw),
        'header_hex': raw[:HEADER_SIZE].hex(),
        'references': references,
        'post_table_size': len(raw) - table_end,
        'post_table_sha256': hashlib.sha256(post_table).hexdigest(),
        'node_envelope': node_envelope,
        'opaque_post_table_hex': post_table.hex() if node_envelope is None else None,
    }


def rebuild(parsed: dict) -> bytes:
    """Rebuild an AT resource without changing reference or node extents.

    Opaque node data, reference trailer words, and any preamble are preserved
    from the editable hex fields. Same-size byte edits are permitted, but
    reference/node counts and node extents cannot change through this bounded
    writer because their runtime semantics are not recovered.
    """
    try:
        header = bytearray.fromhex(parsed['header_hex'])
        references = parsed['references']
        if len(header) != HEADER_SIZE or not isinstance(references, list):
            raise ValueError('invalid stored AT header or reference list')
        if header[:4] != b'AT  ':
            raise ValueError('stored AT header magic was modified')
        if len(references) != parsed.get('texture_reference_count'):
            raise ValueError('texture-reference count changes are not supported')
        if len(references) > 0xFFFFFFFF:
            raise ValueError('too many AT texture references')
        header[8:12] = len(references).to_bytes(4, 'little')
        header[12:16] = TEXTURE_NAME_RECORD_SIZE.to_bytes(4, 'little')

        table = bytearray()
        for row in references:
            original_slot = bytes.fromhex(row['name_slot_hex'])
            if len(original_slot) != TEXTURE_NAME_RECORD_SIZE:
                raise ValueError('stored texture-reference name slot has an invalid size')
            name_slot = _encode_slot(
                row['name'], row.get('original_name', row['name']),
                original_slot.hex(),
                TEXTURE_NAME_RECORD_SIZE)
            following = int(row['following_field'])
            if not 0 <= following <= 0xFFFFFFFF:
                raise ValueError('texture-reference trailing field is outside u32')
            table.extend(name_slot)
            table.extend(following.to_bytes(4, 'little'))

        envelope = parsed.get('node_envelope')
        if envelope is None:
            post_table = bytes.fromhex(parsed['opaque_post_table_hex'])
        else:
            nodes = envelope.get('nodes')
            if not isinstance(nodes, list) or len(nodes) != envelope.get('record_count'):
                raise ValueError('AT node count changes are not supported')
            post = bytearray.fromhex(envelope['preamble_hex'])
            for node in nodes:
                data = bytes.fromhex(node['opaque_data_hex'])
                if len(data) < NODE_FIXED_REGION_SIZE or (
                        len(data) - NODE_FIXED_REGION_SIZE) % NODE_REPEAT_BLOCK_SIZE:
                    raise ValueError('AT node opaque data has an unsupported extent')
                if len(data) + NODE_NAME_PREFIX_SIZE + NODE_NAME_SLOT_SIZE != node.get('size'):
                    raise ValueError('AT node record growth or shrinkage is not supported')
                name_slot = _encode_slot(
                    node['name'], node.get('original_name', node['name']),
                    node['name_slot_hex'], NODE_NAME_SLOT_SIZE)
                post.extend(NODE_NAME_SLOT_SIZE.to_bytes(4, 'little'))
                post.extend(name_slot)
                post.extend(data)
            post_table = bytes(post)

        return bytes(header) + bytes(table) + post_table
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f'invalid editable AT representation: {exc}') from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, nargs='?')
    parser.add_argument('--output-json', type=Path,
                        help='write the editable structural representation here')
    parser.add_argument('--build-json', type=Path,
                        help='rebuild an AT resource from an edited JSON representation')
    parser.add_argument('--output', type=Path,
                        help='binary output path used with --build-json')
    args = parser.parse_args()
    try:
        if args.build_json:
            if args.source or args.output_json or not args.output:
                parser.error('--build-json requires --output and cannot be combined with a source or --output-json')
            with args.build_json.open(encoding='utf-8') as stream:
                result = rebuild(json.load(stream))
            args.output.write_bytes(result)
            print(f'Wrote {len(result)} bytes to {args.output}')
            return 0
        if args.output:
            parser.error('--output is only valid with --build-json')
        if not args.source:
            parser.error('provide a source AT file or --build-json')
        result = parse(args.source.read_bytes())
        if args.output_json:
            args.output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n',
                                        encoding='utf-8')
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
