"""Download the pinned research compiler into an ignored local directory.

Uses the decomp.me compiler distribution. No system installation or baseline
updates. Download/hash failure aborts before extraction; existing installs are
not overwritten. Requires a host capable of running Linux i386 executables.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import tarfile
import urllib.request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=Path('config/ee_compiler.json'))
    parser.add_argument('--destination', type=Path, default=Path('.tools/ee-gcc2.96'))
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    if args.destination.exists():
        raise ValueError('destination exists; use a new directory to avoid overwriting tools')
    with urllib.request.urlopen(config['url'], timeout=60) as response:
        data = response.read(config['archive_size'] + 1)
    if len(data) != config['archive_size'] or hashlib.sha256(data).hexdigest() != config['sha256']:
        raise ValueError('compiler archive does not match the pinned size/hash')
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:xz') as archive:
        archive.extractall(args.destination, filter='data')
    print(f"Installed research compiler {config['version']} in {args.destination}")


if __name__ == '__main__':
    main()
