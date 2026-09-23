"""Decode and rewrap the observed 16-byte BPE resource wrapper.

The wrapper is observed in the game's menu .b resources. Re-encoding uses a
literal identity table, so it is valid but intentionally does not compress.
"""
import argparse
from pathlib import Path
import struct
import sys

MAGIC = b'BPE\0'
HEADER_SIZE = 16
TABLE_SIZE = 256
MAX_OUTPUT_SIZE = 64 * 1024 * 1024
MAX_STACK_SIZE = 256


def decode(raw, max_output=MAX_OUTPUT_SIZE):
    """Decode one wrapped BPE resource, rejecting malformed or stale sizes."""
    if len(raw) < HEADER_SIZE or raw[:4] != MAGIC:
        raise ValueError('not an observed BPE resource')
    table_size, packed_size, output_size = struct.unpack_from('<III', raw, 4)
    if table_size != TABLE_SIZE:
        raise ValueError(f'unsupported BPE table size {table_size}')
    if packed_size != len(raw) - HEADER_SIZE:
        raise ValueError('BPE payload size does not match wrapper')
    if output_size > max_output:
        raise ValueError(f'BPE output size {output_size} exceeds limit {max_output}')

    payload = memoryview(raw)[HEADER_SIZE:]
    pos = 0
    output = bytearray()

    def read_byte():
        nonlocal pos
        if pos >= len(payload):
            raise ValueError('truncated BPE payload')
        value = payload[pos]
        pos += 1
        return value

    while pos < len(payload):
        count = read_byte()
        left = list(range(TABLE_SIZE))
        right = [0] * TABLE_SIZE
        code = 0

        # Each count encodes a run of literal entries followed by pair entries.
        while True:
            if count > 127:
                code += count - 127
                count = 0
            if code >= TABLE_SIZE:
                break
            for _ in range(count + 1):
                if code >= TABLE_SIZE:
                    raise ValueError('BPE translation table overflows')
                first = read_byte()
                left[code] = first
                if first != code:
                    right[code] = read_byte()
                code += 1
                if code > TABLE_SIZE:
                    raise ValueError('BPE translation table overflows')
            if code >= TABLE_SIZE:
                break
            count = read_byte()

        block_size = (read_byte() << 8) | read_byte()
        for _ in range(block_size):
            stack = [read_byte()]
            while stack:
                symbol = stack.pop()
                if symbol == left[symbol]:
                    output.append(symbol)
                    if len(output) > output_size:
                        raise ValueError('BPE output exceeds declared size')
                else:
                    if len(stack) + 2 > MAX_STACK_SIZE:
                        raise ValueError('BPE expansion stack exceeds limit')
                    # LIFO: push right then left to emit the pair in order.
                    stack.append(right[symbol])
                    stack.append(left[symbol])

    if len(output) != output_size:
        raise ValueError(f'BPE output size {len(output)} differs from declared {output_size}')
    return bytes(output)


def encode(raw):
    """Wrap bytes in valid BPE blocks using an identity translation table.

    This prioritizes correctness and insertion over compression ratio.
    """
    if len(raw) > 0xFFFFFFFF:
        raise ValueError('BPE output exceeds 32-bit wrapper size')
    payload = bytearray()
    for start in range(0, len(raw), 0xFFFF):
        block = raw[start:start + 0xFFFF]
        # Skip 128 entries, emit literal code 128, then skip the remaining 127.
        payload.extend((255, 128, 254))
        payload.extend(struct.pack('>H', len(block)))
        payload.extend(block)
    if len(payload) > 0xFFFFFFFF:
        raise ValueError('BPE payload exceeds 32-bit wrapper size')
    return MAGIC + struct.pack('<III', TABLE_SIZE, len(payload), len(raw)) + payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('decode', 'encode'):
        command = sub.add_parser(name)
        command.add_argument('source', type=Path)
        command.add_argument('output', type=Path)
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise ValueError('output already exists')
        raw = args.source.read_bytes()
        result = decode(raw) if args.command == 'decode' else encode(raw)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(result)
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
