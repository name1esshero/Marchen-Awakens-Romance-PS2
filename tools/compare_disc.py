"""Independent streaming byte comparison against a pinned reference image.

Exit 0: authenticated exact match; 1: mismatch; 2: input/authentication error.
The complete images are read, even after a mismatch. No baseline is modified.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

CHUNK = 1024 * 1024


def compare(reference, rebuilt, expected_hash, sample_limit=16):
    hashes = [hashlib.sha256(), hashlib.sha256()]
    lengths = [0, 0]
    differing = 0
    samples = []
    offset = 0
    with reference.open('rb') as left, rebuilt.open('rb') as right:
        while True:
            a, b = left.read(CHUNK), right.read(CHUNK)
            if not a and not b:
                break
            for i, data in enumerate((a, b)):
                hashes[i].update(data)
                lengths[i] += len(data)
            if a != b:
                for i in range(max(len(a), len(b))):
                    av = a[i] if i < len(a) else None
                    bv = b[i] if i < len(b) else None
                    if av != bv:
                        differing += 1
                        if len(samples) < sample_limit:
                            samples.append(dict(offset=offset + i, reference=av, rebuilt=bv))
            offset += max(len(a), len(b))
    authenticated = hashes[0].hexdigest() == expected_hash
    return dict(authenticated=authenticated, match=authenticated and differing == 0,
                reference_size=lengths[0], rebuilt_size=lengths[1],
                reference_sha256=hashes[0].hexdigest(), rebuilt_sha256=hashes[1].hexdigest(),
                differing_bytes=differing, first_differences=samples)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rebuilt', type=Path)
    parser.add_argument('--reference', type=Path, default=Path('baserom.iso'))
    parser.add_argument('--hash-file', type=Path, default=Path('config/reference.sha256'))
    parser.add_argument('--json', type=Path, help='write comparison evidence to a new file')
    args = parser.parse_args()
    try:
        result = compare(args.reference, args.rebuilt, args.hash_file.read_text().split()[0])
        if args.json:
            with args.json.open('x') as out:
                json.dump(result, out, indent=2)
                out.write('\n')
        print(json.dumps(result, indent=2))
        if not result['authenticated']:
            print('ERROR: reference does not match pinned SHA-256', file=sys.stderr)
            return 2
        print('PASS: complete image is byte-identical' if result['match'] else 'FAIL: images differ')
        return 0 if result['match'] else 1
    except (OSError, ValueError, IndexError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
