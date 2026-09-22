"""Compare explicitly selected ELF sections byte-for-byte; never mutates input."""
import argparse
from pathlib import Path
from bootstrap import elf_sections


def compare(reference, candidate, names):
    original = {s['name']: s for s in elf_sections(reference)['sections']}
    rebuilt = {s['name']: s for s in elf_sections(candidate)['sections']}
    total = 0
    if not names or len(set(names)) != len(names):
        raise ValueError('expected nonempty unique section selection')
    for name in names:
        a, b = original[name], rebuilt[name]
        if a['type'] != 1 or b['type'] != 1 or a['size'] == 0:
            raise ValueError(f'{name}: expected nonempty PROGBITS')
        left = reference[a['offset']:a['offset'] + a['size']]
        right = candidate[b['offset']:b['offset'] + b['size']]
        if left != right:
            raise ValueError(f'{name}: byte mismatch ({len(left)} vs {len(right)} bytes)')
        total += len(left)
    return total


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('reference', type=Path)
    parser.add_argument('candidate', type=Path)
    parser.add_argument('selection', type=Path)
    args = parser.parse_args()
    names = args.selection.read_text().splitlines()
    count = compare(args.reference.read_bytes(), args.candidate.read_bytes(), names)
    print(f'PASS: {len(names)} selected sections, {count} identical bytes; not a full ELF comparison')
