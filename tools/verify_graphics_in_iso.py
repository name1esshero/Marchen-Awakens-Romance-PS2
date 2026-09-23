"""Reparse English RTX3 overrides from a built ISO and compare exact TXC bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import assets
import bpe
import graphics
import ui_bundle
from bootstrap import read_at


class IsoReader:
    """Read one logical asset path through the observed ISO/archive tables."""

    def __init__(self, image):
        self.image = Path(image)
        self.stream = self.image.open('rb')
        _, entries = assets.disc_entries(self.stream, self.image.stat().st_size)
        self.disc_entries = {entry['name']: entry for entry in entries}

    def close(self):
        self.stream.close()

    def read(self, logical_path):
        parts = logical_path.split('!/')
        if len(parts) < 2 or parts[0] != 'disc':
            raise ValueError(f'unsupported logical ISO path: {logical_path}')
        try:
            current = self.disc_entries[parts[1]]
        except KeyError as exc:
            raise ValueError(f'ISO member is missing: {parts[1]}') from exc
        base, size = current['offset'], current['size']
        for name in parts[2:]:
            parsed = assets.archive(self.stream, base, size)
            if parsed is None:
                raise ValueError(f'not a recognized archive before {name}: {logical_path}')
            _, _, entries = parsed
            matches = [entry for entry in entries if entry['name'] == name]
            if len(matches) != 1:
                raise ValueError(f'archive member {name!r} matched {len(matches)} entries')
            current = matches[0]
            base += current['offset']
            size = current['size']
        return read_at(self.stream, base, size)


def _sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def _bundle_member(raw, source):
    decoded = bpe.decode(raw)
    parsed = ui_bundle.parse(decoded)
    matches = [entry for entry in parsed['entries']
               if ui_bundle._entry_filename(entry) == source]
    if len(matches) != 1:
        raise ValueError(f'UI bundle member {source!r} matched {len(matches)} entries')
    entry = matches[0]
    return decoded[entry['offset']:entry['offset'] + entry['size']]


def verify(image, graphics_root, overrides_dir, workspace):
    graphics_root = Path(graphics_root)
    overrides_dir = Path(overrides_dir)
    workspace = Path(workspace)
    index_raw = (graphics_root / graphics.INDEX_NAME).read_bytes()
    index = json.loads(index_raw)
    report = json.loads((graphics_root / 'build-report.json').read_text(encoding='utf-8'))
    if report.get('source_index_sha256') != _sha256(index_raw):
        raise ValueError('graphics build report refers to a stale index')
    rows = {row['key']: row for row in index['entries']}
    changed = {entry['key']: entry for entry in report.get('changed', [])}
    english = report.get('english_overrides', [])
    if len(set(english)) != len(english):
        raise ValueError('duplicate English override key in graphics build report')

    reader = IsoReader(image)
    verified_bytes = 0
    try:
        for key in english:
            if key not in rows:
                raise ValueError(f'English override is absent from graphics index: {key}')
            row = rows[key]
            english_path = graphics.english_variant_path(graphics_root / row['image'])
            if not english_path.is_file():
                raise ValueError(f'English TGA is missing: {english_path}')

            if row.get('source_kind') == 'standalone':
                actual = reader.read(row['logical_path'])
                record = changed.get(key)
                if record and record.get('language') == 'eng':
                    expected_path = overrides_dir / 'standalone' / row['source_path']
                else:
                    expected_path = workspace / row['source_path']
            elif row.get('source_kind') == 'bundle':
                packed = reader.read(row['asset_path'])
                actual = _bundle_member(packed, row['source'])
                record = changed.get(key)
                relative = Path(row['bundle_dir']) / row['source']
                if record and record.get('language') == 'eng':
                    expected_path = overrides_dir / relative
                else:
                    expected_path = workspace / relative
            else:
                raise ValueError(f'unsupported graphics source kind for {key}: '
                                 f'{row.get("source_kind")}')

            expected = expected_path.read_bytes()
            if len(actual) != len(expected) or actual != expected:
                raise ValueError(f'ISO TXC differs from {expected_path}: {key}')
            if record and record.get('language') == 'eng':
                digest = _sha256(actual)
                if digest != record.get('override_sha256'):
                    raise ValueError(f'ISO TXC hash differs from build report: {key}')
            elif _sha256(actual) != row['source_sha256']:
                raise ValueError(f'unchanged English entry differs from source hash: {key}')
            verified_bytes += len(actual)
            print(f'PASS {key}: {len(actual)} bytes, sha256={_sha256(actual)}')
    finally:
        reader.close()

    print(json.dumps(dict(image=str(image), english_overrides=len(english),
                          verified_txc_bytes=verified_bytes), indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', type=Path)
    parser.add_argument('--graphics-root', type=Path, default=Path('graphics'))
    parser.add_argument('--overrides-dir', type=Path,
                        default=Path('build/graphics-overrides'))
    parser.add_argument('--workspace', type=Path, default=Path('extracted/assets'))
    args = parser.parse_args()
    try:
        verify(args.image, args.graphics_root, args.overrides_dir, args.workspace)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
