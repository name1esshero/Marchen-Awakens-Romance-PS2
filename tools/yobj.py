#!/usr/bin/env python3
"""Inspect and losslessly rebuild the observed YOBJ envelopes used by YMP."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys


HEADER_SIZE = 0x40
POF0_MAGIC = b'POF0'


def _u32(raw: bytes, offset: int) -> int:
    return int.from_bytes(raw[offset:offset + 4], 'little')


def _decode_pof0(payload: bytes, header_base: int, pof0_offset: int) -> tuple[list[int], bytes]:
    """Decode the observed delta-coded pointer-slot list and zero tail."""
    positions = []
    cursor = 0
    previous = header_base
    while cursor < len(payload):
        first = payload[cursor]
        tag = first & 0xC0
        if tag == 0:
            padding = payload[cursor:]
            if any(padding):
                raise ValueError('YOBJ POF0 has a nonzero invalid tag')
            return positions, padding
        if tag == 0x40:
            encoded_value = first & 0x3F
            width = 1
        elif tag == 0x80:
            if cursor + 2 > len(payload):
                raise ValueError('truncated two-byte YOBJ POF0 value')
            encoded_value = ((first & 0x3F) << 8) | payload[cursor + 1]
            width = 2
        else:
            if cursor + 4 > len(payload):
                raise ValueError('truncated four-byte YOBJ POF0 value')
            encoded_value = ((first & 0x3F) << 24) | (payload[cursor + 1] << 16) | (
                payload[cursor + 2] << 8) | payload[cursor + 3]
            width = 4
        delta = encoded_value * 4
        if delta == 0:
            raise ValueError('YOBJ POF0 contains a zero pointer-slot delta')
        previous += delta
        if previous % 4 or previous < header_base or previous + 4 > pof0_offset:
            raise ValueError('YOBJ POF0 pointer slot is unaligned or outside model data')
        positions.append(previous)
        cursor += width
    return positions, b''


def _encode_pof0(positions: list[int], header_base: int) -> bytes:
    """Encode pointer-slot positions using the corpus-observed POF0 deltas."""
    encoded = bytearray()
    previous = header_base
    for position in positions:
        delta = position - previous
        if delta <= 0 or delta & 3:
            raise ValueError('YOBJ POF0 pointer slots must be strictly increasing and aligned')
        value = delta // 4
        if value <= 0x3F:
            encoded.append(0x40 | value)
        elif value <= 0x3FFF:
            encoded.extend((0x8000 | value).to_bytes(2, 'big'))
        elif value <= 0x3FFFFFFF:
            encoded.extend((0xC0000000 | value).to_bytes(4, 'big'))
        else:
            raise ValueError('YOBJ POF0 pointer-slot delta exceeds the observed encoding')
        previous = position
    while len(encoded) % 4:
        encoded.append(0)
    return bytes(encoded)


def parse(raw: bytes) -> dict:
    if raw[:4] == b'YOBJ':
        yobj_offset = 0
        variant = 'YOBJ'
    elif raw[:8] == b'DUMY\0\0\0\0' and raw[8:12] == b'YOBJ':
        yobj_offset = 8
        variant = 'DUMY_YOBJ'
    else:
        raise ValueError('unsupported YOBJ prefix')

    header_base = yobj_offset + 8
    if len(raw) < header_base + HEADER_SIZE:
        raise ValueError('truncated YOBJ header')
    pof0_relative_a = _u32(raw, yobj_offset + 4)
    pof0_relative_b = _u32(raw, header_base + 4)
    if pof0_relative_a != pof0_relative_b:
        raise ValueError('YOBJ duplicate POF0 offsets disagree')
    pof0_offset = header_base + pof0_relative_b
    if pof0_offset < header_base + HEADER_SIZE or pof0_offset + 8 > len(raw):
        raise ValueError('YOBJ POF0 extent is outside the file')
    if raw[pof0_offset:pof0_offset + 4] != POF0_MAGIC:
        raise ValueError('YOBJ POF0 offset does not point to POF0')
    pof0_length = _u32(raw, pof0_offset + 4)
    if pof0_offset + 8 + pof0_length != len(raw):
        raise ValueError('YOBJ POF0 length does not end at EOF')

    counts = [
        _u32(raw, header_base + 0x10),
        _u32(raw, header_base + 0x14),
        _u32(raw, header_base + 0x18),
        _u32(raw, header_base + 0x2C),
    ]
    offsets = [
        _u32(raw, header_base + 0x1C),
        _u32(raw, header_base + 0x20),
        _u32(raw, header_base + 0x24),
        _u32(raw, header_base + 0x28),
    ]
    offset_targets = []
    for value in offsets:
        target = header_base + value if value else None
        if target is not None and not header_base + HEADER_SIZE <= target <= pof0_offset:
            raise ValueError('YOBJ header table offset points outside the model body')
        offset_targets.append(target)

    pof0_payload = raw[pof0_offset + 8:]
    pointer_slots, pof0_padding = _decode_pof0(pof0_payload, header_base, pof0_offset)
    pointer_values = []
    for slot in pointer_slots:
        value = _u32(raw, slot)
        target = header_base + value if value else None
        if target is not None and not header_base + HEADER_SIZE <= target <= pof0_offset:
            raise ValueError('YOBJ POF0-listed value points outside the model body')
        pointer_values.append({'slot_offset': slot, 'relative_value': value,
                               'target_offset': target})

    # Almost the entire POF0 byte stream is reproduced canonically by encoding
    # the decoded slots. The single recovered basebone variant has additional
    # all-zero opaque tail bytes; preserve those instead of discarding them.
    canonical = _encode_pof0(pointer_slots, header_base)
    if pof0_payload[:len(canonical)] != canonical or any(pof0_payload[len(canonical):]):
        raise ValueError('YOBJ POF0 encoding does not match the observed delta form')

    body_start = header_base + HEADER_SIZE
    return {
        'format': 'YOBJ',
        'variant': variant,
        'file_size': len(raw),
        'sha256': hashlib.sha256(raw).hexdigest(),
        'yobj_offset': yobj_offset,
        'header_base': header_base,
        'header_counts_uninterpreted': counts,
        'header_offsets_uninterpreted': offsets,
        'header_offset_targets': offset_targets,
        'body_start': body_start,
        'body_size': pof0_offset - body_start,
        'pof0_offset': pof0_offset,
        'pof0_size': len(raw) - pof0_offset,
        'pof0_payload_size': pof0_length,
        'pof0_reference_count': len(pointer_slots),
        'pof0_reference_slots': pointer_slots,
        'pof0_reference_values': pointer_values,
        'pof0_zero_tail_bytes': len(pof0_padding),
        'prefix_hex': raw[:header_base].hex(),
        'header_hex': raw[header_base:body_start].hex(),
        'opaque_body_hex': raw[body_start:pof0_offset].hex(),
        'pof0_hex': raw[pof0_offset:].hex(),
        'limits': [
            'Header count/offset labels are kept numeric; mesh, bone, material and object semantics are not asserted by this parser.',
            'The body between the fixed header and POF0 remains opaque. POF0-listed values are bounded references, but this parser does not prove which offsets the runtime adjusts or support safe model growth.',
        ],
    }


def rebuild(parsed: dict) -> bytes:
    try:
        raw = (bytes.fromhex(parsed['prefix_hex']) + bytes.fromhex(parsed['header_hex']) +
               bytes.fromhex(parsed['opaque_body_hex']) + bytes.fromhex(parsed['pof0_hex']))
        rebuilt = parse(raw)
        if rebuilt['file_size'] != len(raw):
            raise ValueError('rebuilt YOBJ size changed during parse')
        return raw
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f'invalid editable YOBJ representation: {exc}') from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, nargs='?')
    parser.add_argument('--output-json', type=Path,
                        help='write the bounded YOBJ representation here')
    parser.add_argument('--build-json', type=Path,
                        help='rebuild a YOBJ file from an edited JSON representation')
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
            parser.error('provide a source YOBJ/YMP file or --build-json')
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
    raise SystemExit(main())
