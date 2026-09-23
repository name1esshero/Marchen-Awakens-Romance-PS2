"""Export editable RTX3 images and stage non-destructive UI-bundle overrides."""
import argparse
from collections import Counter
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

import rtx3


SUPPORTED = {
    rtx3.PSMT4: 'psmt4',
    rtx3.PSMT8: 'psmt8',
    rtx3.PSMT8H: 'psmt8h',
    rtx3.PSMT4HL: 'psmt4hl',
    rtx3.PSMT4HH: 'psmt4hh',
    rtx3.PSMCT32: 'psmct32',
}
INDEX_NAME = 'index.json'
INDEX_VERSION = 4
OVERRIDES_MARKER = '.generated-by-marps2-graphics'
OVERRIDES_MARKER_TEXT = 'Generated RTX3 overrides; safe to replace.\n'
STANDALONE_MANIFEST = 'standalone-txc-overrides.json'


def _sha256(data):
    return hashlib.sha256(data).hexdigest()


def english_variant_path(image_path):
    """Return the sibling English raster name for a source TGA."""
    image_path = Path(image_path)
    stem = image_path.stem
    if stem.endswith('_jp'):
        stem = stem[:-3]
    return image_path.with_name(f'{stem}_eng{image_path.suffix}')


def _safe_relative(value):
    path = Path(value)
    if path.is_absolute() or not path.parts or '..' in path.parts:
        raise ValueError(f'unsafe graphics workspace path: {value}')
    return path


def _name_from_entry(entry):
    raw = bytes.fromhex(entry['name_hex']).split(b'\0', 1)[0]
    return raw.decode('ascii', errors='replace')


def _source_path(workspace, row):
    if row.get('source_kind') == 'standalone':
        return workspace / _safe_relative(row['source_path'])
    return workspace / _safe_relative(row['bundle_dir']) / _safe_relative(row['source'])


def _image_name_for_standalone(row, category):
    source = _safe_relative(row['source_path'])
    # Extracted archive IDs make repeated TXC names unambiguous while keeping
    # the original resource name visible to artists browsing a flat folder.
    ids = [part.removesuffix('.asset') for part in source.parts[:-1]]
    ids.append(source.stem)
    stable_id = '_'.join(ids)
    raw_name = row['key'].rsplit('!/', 1)[-1].rsplit('/', 1)[-1]
    stem = Path(raw_name).stem
    safe_stem = re.sub(r'[^A-Za-z0-9_.-]+', '_', stem).strip('._') or 'texture'
    return (Path(category) / f'{stable_id}_{safe_stem}_jp.tga').as_posix()


def _raw_psm(raw):
    if len(raw) < 16 or raw[:4] != rtx3.MAGIC:
        return None
    return (int.from_bytes(raw[8:16], 'little') >> 20) & 0x3F


def _image_support(info):
    if info['psm'] in rtx3.INDEXED_PSMS:
        return None
    if info['psm'] == rtx3.PSMCT32:
        if info['width'] % 64 or info['height'] % 32:
            return 'PSMCT32 dimensions do not meet the evidenced page geometry'
        return None
    return 'pixel storage mode has no evidence-backed editable TGA conversion'


def _asset_paths(workspace):
    catalog_path = Path(workspace) / 'catalog.json'
    if not catalog_path.exists():
        return {}
    catalog = json.loads(catalog_path.read_text(encoding='utf-8'))
    return {row['ui_bundle_dir']: row['name'] for row in catalog
            if row.get('ui_bundle_dir')}


def _category(name, asset_path):
    """Use resource/bundle names for broad, human-readable asset groups."""
    text = f'{name} {Path(asset_path).stem}'.lower()
    tokens = set(re.findall(r'[a-z0-9]+', text))
    if 'title' in tokens or 'ttlprts' in tokens:
        return 'title'
    if 'icon' in tokens or 'iconguide' in tokens:
        return 'icon'
    if 'card' in tokens or any(re.fullmatch(r'\d+card', token) for token in tokens):
        return 'cards'
    if any(token.startswith(('arm', 'weapon')) for token in tokens):
        return 'weapons'
    if (tokens & {'char', 'chara', 'character', 'characters', 'chr', 'mych',
                  'face', 'faces', 'chsface', 'voice', 'voi', 'acter'} or
            any(token.startswith(('char2d', 'chara', 'character')) for token in tokens)):
        return 'characters'
    if tokens & {'eff', 'effect', 'effects', 'flare', 'flash', 'thunder',
                  'rainbow', 'flame', 'flear'} or any(
            token.startswith(('eff', 'effect', 'flare', 'flash', 'thunder',
                              'rainbow', 'flame', 'flear')) for token in tokens):
        return 'effects'
    if tokens & {'font', 'fnt', 'text', 'txt', 'subtitle'}:
        return 'text'
    if tokens & {'map', 'maps', 'hdmp', 'maze'}:
        return 'maps'
    if tokens & {'bg', 'background', 'sky', 'shopbg'}:
        return 'backgrounds'
    if tokens & {'stage', 'wall', 'door', 'pillar', 'piller', 'gate', 'arch',
                  'tower', 'yane', 'teras', 'kaidan', 'indoor', 'geo', 'lab',
                  'laby', 'environment', 'environmental'}:
        return 'environments'
    return 'user_interface'


def _discover(workspace):
    workspace = Path(workspace)
    asset_paths = _asset_paths(workspace)
    found = []
    for manifest_path in sorted(workspace.rglob('*.bundle.json')):
        manifest_rel = manifest_path.relative_to(workspace)
        bundle_dir = manifest_path.with_name(
            manifest_path.name.removesuffix('.bundle.json') + '.resources')
        bundle_rel = bundle_dir.relative_to(workspace)
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        for entry in manifest.get('entries', []):
            kind = bytes.fromhex(entry['kind_hex']).rstrip(b'\0').decode('ascii', errors='replace')
            if kind != 'txc':
                continue
            member_name = _safe_relative(entry['source'])
            source_rel = bundle_rel / member_name
            source_path = workspace / source_rel
            raw = source_path.read_bytes()
            source_hash = _sha256(raw)
            if source_hash != entry.get('source_sha256'):
                raise ValueError(f'TXC member differs from its bundle manifest: {source_rel}')
            try:
                info = rtx3.parse(raw)
                psm = info['psm']
                psm_name = SUPPORTED.get(psm, f'psm{psm}')
                asset_path = asset_paths.get(bundle_rel.as_posix(), '')
                category = _category(_name_from_entry(entry), asset_path)
                image_rel = None
                reason = _image_support(info)
                if reason is None:
                    asset_id = bundle_rel.parent.name.removesuffix('.asset')
                    bundle_id = bundle_rel.name.removesuffix('.resources')
                    source_stem = member_name.name.removesuffix('.txc.bin')
                    if not source_stem.endswith('_jp'):
                        source_stem += '_jp'
                    image_name = f'{asset_id}_{bundle_id}_{source_stem}.tga'
                    image_rel = Path(category) / image_name
                else:
                    reason = 'pixel storage mode has no evidence-backed TGA conversion'
            except ValueError as exc:
                info = None
                psm = None
                psm_name = 'unresolved'
                asset_path = asset_paths.get(bundle_rel.as_posix(), '')
                category = _category(_name_from_entry(entry), asset_path)
                image_rel = None
                reason = str(exc)
            found.append(dict(
                key=f'{bundle_rel.as_posix()}!/{member_name.as_posix()}',
                bundle_manifest=manifest_rel.as_posix(),
                bundle_dir=bundle_rel.as_posix(),
                source=member_name.as_posix(),
                source_sha256=source_hash,
                name=_name_from_entry(entry),
                asset_path=asset_path,
                category=category,
                psm=psm,
                psm_name=psm_name,
                rtx3_parse_valid=info is not None,
                width=info['width'] if info else None,
                height=info['height'] if info else None,
                image=image_rel.as_posix() if image_rel else None,
                unsupported_reason=reason,
                source_kind='bundle',
            ))

    catalog_path = workspace / 'catalog.json'
    if catalog_path.exists():
        catalog = json.loads(catalog_path.read_text(encoding='utf-8'))
        for catalog_row in catalog:
            logical_path = catalog_row.get('name', '')
            if (not logical_path.lower().endswith('.txc') or
                    catalog_row.get('ui_bundle_dir')):
                continue
            source_rel = _safe_relative(catalog_row['source'])
            source_path = workspace / source_rel
            raw = source_path.read_bytes()
            source_hash = _sha256(raw)
            name = logical_path.rsplit('!/', 1)[-1].rsplit('/', 1)[-1]
            asset_path = logical_path.rsplit('!/', 1)[0] if '!/' in logical_path else ''
            category = _category(Path(name).stem, asset_path)
            info = None
            psm = _raw_psm(raw)
            psm_name = f'psm{psm}' if psm is not None else 'unresolved'
            image_rel = None
            reason = None
            try:
                info = rtx3.parse(raw)
                psm = info['psm']
                psm_name = SUPPORTED.get(psm, f'psm{psm}')
                reason = _image_support(info)
                if reason is None:
                    image_rel = _image_name_for_standalone(
                        dict(source_path=source_rel.as_posix(), key=logical_path), category)
            except ValueError as exc:
                reason = str(exc)
            found.append(dict(
                key=f'standalone:/{source_rel.as_posix()}',
                logical_path=logical_path,
                source_path=source_rel.as_posix(),
                source_sha256=source_hash,
                source_kind='standalone',
                name=Path(name).stem,
                asset_path=asset_path,
                category=category,
                psm=psm,
                psm_name=psm_name,
                rtx3_parse_valid=info is not None,
                width=info['width'] if info else None,
                height=info['height'] if info else None,
                image=image_rel,
                unsupported_reason=reason,
            ))
    return found


def export(workspace, graphics_root):
    """Create missing TGA exports without overwriting user-edited images."""
    workspace = Path(workspace).resolve()
    graphics_root = Path(graphics_root).resolve()
    graphics_root.mkdir(parents=True, exist_ok=True)
    index_path = graphics_root / INDEX_NAME
    previous = None
    if index_path.exists():
        previous = json.loads(index_path.read_text(encoding='utf-8'))
        if previous.get('version') not in (2, 3, INDEX_VERSION):
            raise ValueError('unsupported graphics index version')
    old_by_key = {row['key']: row for row in previous.get('entries', [])} if previous else {}

    entries = []
    exported = 0
    discovered = _discover(workspace)
    image_paths = [row['image'] for row in discovered if row['image']]
    if len(image_paths) != len(set(image_paths)):
        raise ValueError('graphics image filename collision; refusing ambiguous exports')
    for row in discovered:
        old = old_by_key.get(row['key'])
        if old:
            for field in ('source_sha256', 'psm', 'width', 'height'):
                if old.get(field) != row.get(field):
                    raise ValueError(f'graphics source changed since export: {row["key"]} ({field})')
            if old.get('image') != row.get('image') and old.get('image'):
                old_image = graphics_root / _safe_relative(old['image'])
                new_image = (graphics_root / _safe_relative(row['image'])
                             if row.get('image') else None)
                if (new_image is None or not old_image.is_file() or
                        _sha256(old_image.read_bytes()) != old.get('image_sha256')):
                    raise ValueError(f'cannot safely move edited or missing graphics baseline: {row["key"]}')
                if new_image.exists():
                    raise ValueError(f'graphics category migration would overwrite: {row["image"]}')
                old_english = english_variant_path(old_image)
                new_english = english_variant_path(new_image)
                move_english = old_english.exists()
                if move_english and new_english.exists():
                    raise ValueError(f'graphics category migration would overwrite: {new_english}')
                new_image.parent.mkdir(parents=True, exist_ok=True)
                old_image.replace(new_image)
                if move_english:
                    old_english.replace(new_english)
        if row['image']:
            image_path = graphics_root / _safe_relative(row['image'])
            if image_path.exists():
                if not old:
                    raise ValueError(f'image exists without a graphics index record: {row["image"]}')
                row['image_sha256'] = old['image_sha256']
            else:
                source_path = _source_path(workspace, row)
                decode = rtx3.decode_rgba(source_path.read_bytes())
                image_path.parent.mkdir(parents=True, exist_ok=True)
                image_path.write_bytes(rtx3.write_tga(*decode))
                row['image_sha256'] = _sha256(image_path.read_bytes())
                exported += 1
        entries.append(row)

    missing_old = set(old_by_key) - {row['key'] for row in entries}
    if missing_old:
        raise ValueError(f'prepared workspace lost indexed graphics members: {sorted(missing_old)[:3]}')
    document = dict(version=INDEX_VERSION, updated=date.today().isoformat(),
                    workspace=str(workspace), entries=entries)
    temp = index_path.with_suffix('.json.tmp')
    temp.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(index_path)
    print(json.dumps(dict(index=str(index_path), resources=len(entries),
                          exported_images=exported,
                          unresolved=sum(not row['image'] for row in entries)), indent=2))
    return document


def _load_index(graphics_root):
    path = Path(graphics_root) / INDEX_NAME
    document = json.loads(path.read_text(encoding='utf-8'))
    if document.get('version') != INDEX_VERSION:
        raise ValueError('unsupported graphics index version')
    return document


def _reset_overrides(workspace, graphics_root, overrides):
    if (overrides == workspace or overrides.is_relative_to(workspace) or
            workspace.is_relative_to(overrides) or overrides == graphics_root or
            graphics_root.is_relative_to(overrides)):
        raise ValueError(f'unsafe graphics override output directory: {overrides}')
    if overrides.exists():
        if not overrides.is_dir():
            raise ValueError(f'graphics override output is not a directory: {overrides}')
        marker = overrides / OVERRIDES_MARKER
        if any(overrides.iterdir()):
            if not marker.is_file() or marker.read_text(encoding='utf-8') != OVERRIDES_MARKER_TEXT:
                raise ValueError(f'refusing to replace unrecognized output directory: {overrides}')
            shutil.rmtree(overrides)
        else:
            overrides.rmdir()
    overrides.mkdir(parents=True, exist_ok=True)
    (overrides / OVERRIDES_MARKER).write_text(OVERRIDES_MARKER_TEXT, encoding='utf-8')


def build(workspace, graphics_root, overrides_dir=None):
    """Import changed TGAs into a separate resource-override tree."""
    workspace = Path(workspace).resolve()
    graphics_root = Path(graphics_root).resolve()
    document = _load_index(graphics_root)
    overrides = (Path(overrides_dir).resolve() if overrides_dir else
                 graphics_root / 'overrides')
    _reset_overrides(workspace, graphics_root, overrides)
    changed = []
    unresolved = []
    english_overrides = []
    standalone_overrides = []
    for row in document['entries']:
        if not row.get('image'):
            unresolved.append(row['key'])
            continue
        source_path = _source_path(workspace, row)
        original = source_path.read_bytes()
        if _sha256(original) != row['source_sha256']:
            raise ValueError(f'TXC source changed since graphics export: {row["key"]}')
        image_path = graphics_root / _safe_relative(row['image'])
        english_path = english_variant_path(image_path)
        selected_path = english_path if english_path.exists() else image_path
        is_english = selected_path == english_path
        replacement = selected_path.read_bytes()
        if is_english:
            english_overrides.append(row['key'])
        elif _sha256(replacement) == row['image_sha256']:
            continue
        rebuilt = rtx3.encode_tga(original, replacement)
        if len(rebuilt) != len(original):
            raise ValueError(f'RTX3 image edit changed texture size: {row["key"]}')
        if rebuilt == original:
            continue
        if row.get('source_kind') == 'standalone':
            target = _safe_relative(row['source_path']).as_posix()
            output = overrides / 'standalone' / _safe_relative(target)
        else:
            target = None
            output = (overrides / _safe_relative(row['bundle_dir']) /
                      _safe_relative(row['source']))
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(rebuilt)
        record = dict(key=row['key'], language='eng' if is_english else 'base',
                      image=selected_path.relative_to(graphics_root).as_posix(),
                      source_sha256=row['source_sha256'],
                      override_sha256=_sha256(rebuilt), bytes=len(rebuilt))
        changed.append(record)
        if target is not None:
            standalone_overrides.append(dict(
                target=target, source_sha256=row['source_sha256'],
                override_sha256=record['override_sha256'], bytes=len(rebuilt),
                key=row['key']))

    (overrides / STANDALONE_MANIFEST).write_text(
        json.dumps(dict(version=1, entries=standalone_overrides), indent=2) + '\n',
        encoding='utf-8')

    report = dict(version=INDEX_VERSION, updated=date.today().isoformat(),
                  source_index_sha256=_sha256(
                      (graphics_root / INDEX_NAME).read_bytes()),
                  changed=changed, english_overrides=english_overrides,
                  unresolved=unresolved)
    report_path = graphics_root / 'build-report.json'
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n',
                           encoding='utf-8')
    print(json.dumps(dict(changed_resources=len(changed),
                          unresolved_resources=len(unresolved),
                          overrides=str(overrides)), indent=2))
    return report


def audit(workspace, graphics_root):
    """Report source authenticity, image presence and local edits."""
    workspace = Path(workspace).resolve()
    graphics_root = Path(graphics_root).resolve()
    document = _load_index(graphics_root)
    counts = Counter()
    edited = []
    english_overrides = []
    for row in document['entries']:
        if not row.get('image'):
            counts[f'unresolved:{row["psm_name"]}'] += 1
            continue
        counts[row['psm_name']] += 1
        source = _source_path(workspace, row)
        if _sha256(source.read_bytes()) != row['source_sha256']:
            raise ValueError(f'TXC source hash mismatch: {row["key"]}')
        image = graphics_root / _safe_relative(row['image'])
        image_raw = image.read_bytes()
        width, height = rtx3.tga_dimensions(image_raw)
        if (width, height) != (row['width'], row['height']):
            raise ValueError(f'edited image dimensions changed: {row["image"]}')
        if _sha256(image_raw) != row['image_sha256']:
            edited.append(row['key'])
        english = english_variant_path(image)
        if english.exists():
            width, height = rtx3.tga_dimensions(english.read_bytes())
            if (width, height) != (row['width'], row['height']):
                raise ValueError(f'English TGA dimensions changed: {english}')
            english_overrides.append(row['key'])
    result = dict(version=INDEX_VERSION, source_resources=len(document['entries']),
                  image_resources=sum(count for name, count in counts.items()
                                      if not name.startswith('unresolved:')),
                  counts=dict(sorted(counts.items())),
                  edited_images=len(edited), edited=edited,
                  english_overrides=len(english_overrides),
                  english_override_keys=english_overrides)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('export', 'build', 'audit'):
        command = sub.add_parser(name)
        command.add_argument('workspace', type=Path)
        command.add_argument('graphics_root', type=Path)
        if name == 'build':
            command.add_argument('--overrides-dir', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'export':
            export(args.workspace, args.graphics_root)
        elif args.command == 'build':
            build(args.workspace, args.graphics_root, args.overrides_dir)
        else:
            audit(args.workspace, args.graphics_root)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
