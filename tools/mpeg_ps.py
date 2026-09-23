"""Parse and losslessly reassemble the observed sectorized MPEG-1 program streams."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import sys

SECTOR_SIZE = 2048
PACK_HEADER_SIZE = 12
PACK_START = b'\x00\x00\x01\xba'
PROGRAM_END = b'\x00\x00\x01\xb9'


def _validate_pack_header(raw: bytes, offset: int) -> None:
    header = raw[offset + 4:offset + PACK_HEADER_SIZE]
    if len(header) != PACK_HEADER_SIZE - 4 or header[0] & 0xF0 != 0x20:
        raise ValueError(f'unsupported or truncated MPEG pack header at {offset:#x}')
    # MPEG-1 SCR and mux-rate marker bits. The observed corpus uses this
    # 12-byte pack form; MPEG-2 pack headers are deliberately not guessed.
    if not (header[0] & 1 and header[2] & 1 and header[4] & 1 and header[7] & 1):
        raise ValueError(f'invalid MPEG-1 pack marker bits at {offset:#x}')


def parse(raw: bytes) -> dict:
    """Validate all pack/PES extents and the final sector trailer.

    This contract is intentionally limited to the observed MOVIE.AFS corpus:
    MPEG-1 12-byte pack headers at each 2048-byte sector boundary, nonzero
    length-delimited packets, a program-end code at the start of the last
    sector, and 2044 trailing 0xff bytes.
    """
    if len(raw) < 2 * SECTOR_SIZE or len(raw) % SECTOR_SIZE:
        raise ValueError('MPEG program stream size is not a multi-sector extent')

    cursor = 0
    segments = []
    packet_counts = Counter()
    packet_bytes = Counter()
    pack_count = 0
    end_offset = None
    terminal_fill_bytes = 0

    while cursor < len(raw):
        if raw[cursor:cursor + 4] == PACK_START:
            if cursor % SECTOR_SIZE:
                raise ValueError(f'MPEG pack header is not sector-aligned at {cursor:#x}')
            if cursor + PACK_HEADER_SIZE > len(raw):
                raise ValueError(f'truncated MPEG pack header at {cursor:#x}')
            _validate_pack_header(raw, cursor)
            segments.append((cursor, PACK_HEADER_SIZE, 'pack', None))
            pack_count += 1
            cursor += PACK_HEADER_SIZE
            continue

        if raw[cursor:cursor + 4] == PROGRAM_END:
            end_offset = cursor
            if cursor != len(raw) - SECTOR_SIZE:
                raise ValueError('program-end code is not at the start of the final sector')
            segments.append((cursor, 4, 'program_end', None))
            cursor += 4
            terminal_fill = raw[cursor:]
            if len(terminal_fill) != SECTOR_SIZE - 4 or any(
                    byte != 0xFF for byte in terminal_fill):
                raise ValueError('final program-stream sector is not the observed 0xff trailer')
            terminal_fill_bytes = len(terminal_fill)
            segments.append((cursor, terminal_fill_bytes, 'terminal_ff', None))
            cursor = len(raw)
            break

        if raw[cursor:cursor + 3] != b'\x00\x00\x01' or cursor + 6 > len(raw):
            raise ValueError(f'expected MPEG pack/packet start code at {cursor:#x}')
        stream_id = raw[cursor + 3]
        if stream_id < 0xBB:
            raise ValueError(f'unsupported MPEG control/start code {stream_id:#04x} at {cursor:#x}')
        packet_length = struct.unpack_from('>H', raw, cursor + 4)[0]
        if packet_length == 0:
            raise ValueError(f'zero-length MPEG packet is outside the observed contract at {cursor:#x}')
        packet_end = cursor + 6 + packet_length
        sector_end = (cursor // SECTOR_SIZE + 1) * SECTOR_SIZE
        if packet_end > sector_end:
            raise ValueError(f'MPEG packet crosses its sector boundary at {cursor:#x}')
        if packet_end > len(raw):
            raise ValueError(f'MPEG packet extends past EOF at {cursor:#x}')
        segments.append((cursor, packet_end - cursor, 'packet', stream_id))
        packet_counts[stream_id] += 1
        packet_bytes[stream_id] += packet_end - cursor
        cursor = packet_end

    if end_offset is None:
        raise ValueError('missing MPEG program-end code')
    if pack_count != len(raw) // SECTOR_SIZE - 1:
        raise ValueError('pack-header count does not match the observed one-pack-per-data-sector layout')
    if cursor != len(raw) or not segments:
        raise ValueError('MPEG packet extents do not cover the complete resource')

    # The parser walks adjacent ranges in source order; make that invariant
    # explicit because the census uses complete parser coverage for this span.
    covered = 0
    for offset, size, _, _ in segments:
        if offset != covered or size <= 0:
            raise ValueError('MPEG packet extents contain a gap, overlap, or empty segment')
        covered += size
    if covered != len(raw):
        raise ValueError('MPEG packet extents do not partition the complete resource')

    return {
        'format': 'MPEG-1 program stream (observed sectorized variant)',
        'file_size': len(raw),
        'sha256': hashlib.sha256(raw).hexdigest(),
        'sector_size': SECTOR_SIZE,
        'sector_count': len(raw) // SECTOR_SIZE,
        'pack_header_count': pack_count,
        'packet_count': sum(packet_counts.values()),
        'packet_counts_by_stream_id': {
            f'0x{stream_id:02x}': count for stream_id, count in sorted(packet_counts.items())
        },
        'packet_bytes_by_stream_id': {
            f'0x{stream_id:02x}': count for stream_id, count in sorted(packet_bytes.items())
        },
        'program_end_offset': end_offset,
        'terminal_ff_bytes': terminal_fill_bytes,
        'structural_bytes': covered,
        'segments': segments,
        'limits': [
            'PES payloads, timestamps, codec headers and audio/video frame data remain opaque.',
            'This validates the observed 2048-byte sectorized MPEG-1 program-stream layout; it does not prove PlayStation runtime acceptance of a replacement stream.',
        ],
    }


def rebuild(parsed: dict, raw: bytes) -> bytes:
    """Reassemble the exact indexed extents after checking the source hash."""
    if len(raw) != parsed.get('file_size'):
        raise ValueError('source size does not match MPEG packet manifest')
    if hashlib.sha256(raw).hexdigest() != parsed.get('sha256'):
        raise ValueError('source SHA-256 does not match MPEG packet manifest')
    output = bytearray(len(raw))
    cursor = 0
    try:
        for offset, size, _kind, _stream_id in parsed['segments']:
            if offset != cursor or size <= 0 or offset + size > len(raw):
                raise ValueError('invalid MPEG editable segment table')
            output[cursor:cursor + size] = raw[offset:offset + size]
            cursor += size
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f'invalid MPEG packet representation: {exc}') from exc
    if cursor != len(raw):
        raise ValueError('MPEG packet segments do not cover the source')
    rebuilt = bytes(output)
    # Also validate that the source matches the segment boundaries recorded in
    # the representation, rather than trusting edited JSON offsets.
    current = parse(rebuilt)
    if [(a, b, c, d) for a, b, c, d in current['segments']] != parsed['segments']:
        raise ValueError('MPEG segment table disagrees with the parsed source')
    return rebuilt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output-json', type=Path,
                        help='write packet-boundary and stream-ID inventory')
    parser.add_argument('--rebuild', type=Path,
                        help='reassemble the validated source into this output file')
    args = parser.parse_args()
    try:
        raw = args.source.read_bytes()
        parsed = parse(raw)
        if args.rebuild:
            rebuilt = rebuild(parsed, raw)
            args.rebuild.write_bytes(rebuilt)
            print(f'Wrote {len(rebuilt)} bytes to {args.rebuild}')
        if args.output_json:
            args.output_json.write_text(json.dumps(parsed, indent=2) + '\n',
                                        encoding='utf-8')
        print(f"{args.source}: {parsed['file_size']:,} bytes, "
              f"{parsed['pack_header_count']:,} pack headers, "
              f"{parsed['packet_count']:,} length-bounded packets")
        return 0
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
