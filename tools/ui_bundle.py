"""Lossless parser and editor for the observed menu UI resource bundle table."""
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import struct
import sys

import bpe

HEADER_SIZE = 16
RECORD_SIZE = 32
ALIGNMENT = 16
MAX_ENTRIES = 65535
KNOWN_HEADER = b'\x01\x01\x00\x00'


def parse(raw):
    """Parse one observed bundle, rejecting unsafe or overlapping extents."""
    if len(raw) < HEADER_SIZE:
        raise ValueError('truncated UI bundle header')
    count = struct.unpack_from('<I', raw)[0]
    if count > MAX_ENTRIES:
        raise ValueError('UI bundle entry count exceeds limit')
    if raw[4:8] != KNOWN_HEADER:
        raise ValueError('unknown UI bundle header variant')
    table_end = HEADER_SIZE + count * RECORD_SIZE
    if table_end > len(raw):
        raise ValueError('truncated UI bundle entry table')

    entries = []
    extents = []
    for index in range(count):
        record_offset = HEADER_SIZE + index * RECORD_SIZE
        record = raw[record_offset:record_offset + RECORD_SIZE]
        name = record[:16].split(b'\0', 1)[0]
        kind = record[16:20]
        size, offset, flags = struct.unpack_from('<III', record, 20)
        if not name or b'\0' in name or not kind.strip(b'\0'):
            raise ValueError(f'invalid UI bundle entry {index} name/type')
        if offset < table_end or offset % ALIGNMENT:
            raise ValueError(f'UI bundle entry {index} has invalid data offset')
        if size > len(raw) or offset > len(raw) - size:
            raise ValueError(f'UI bundle entry {index} lies outside source')
        extents.append((offset, offset + size, index))
        entries.append(dict(index=index, record_offset=record_offset,
                             name_hex=name.hex(), kind_hex=kind.hex(),
                             size=size, offset=offset, flags=flags))

    extents.sort()
    for previous, current in zip(extents, extents[1:]):
        if current[0] < previous[1]:
            raise ValueError(f'overlapping UI bundle entries {previous[2]} and {current[2]}')

    return dict(header_hex=raw[:HEADER_SIZE].hex(), source_size=len(raw),
                source_sha256=hashlib.sha256(raw).hexdigest(), table_end=table_end,
                entries=entries)


def _entry_filename(entry):
    name = bytes.fromhex(entry['name_hex']).decode('ascii', errors='replace')
    kind = bytes.fromhex(entry['kind_hex']).rstrip(b'\0').decode('ascii', errors='replace')
    safe_name = re.sub(r'[^A-Za-z0-9_.-]+', '_', name).strip('._') or 'unnamed'
    safe_kind = re.sub(r'[^A-Za-z0-9_.-]+', '_', kind).strip('._') or 'raw'
    return f"{entry['index']:04d}_{safe_name}.{safe_kind}.bin"


def _member_path(source_root, name):
    relative = Path(name)
    if relative.is_absolute() or '..' in relative.parts or not relative.parts:
        raise ValueError('unsafe UI bundle member path')
    return source_root / relative


def extract(raw, destination, manifest_path):
    """Extract members plus a source-hash-anchored manifest."""
    manifest = parse(raw)
    destination.mkdir(parents=True, exist_ok=True)
    for entry in manifest['entries']:
        filename = _entry_filename(entry)
        entry['source'] = filename
        member_path = destination / filename
        if not member_path.exists():
            member_path.write_bytes(raw[entry['offset']:entry['offset'] + entry['size']])
        entry['source_sha256'] = hashlib.sha256(
            raw[entry['offset']:entry['offset'] + entry['size']]).hexdigest()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n',
                             encoding='utf-8')
    return manifest


def has_edits(manifest, source_root, overrides_root=None):
    """Validate extracted members and optional out-of-tree replacements."""
    edited = False
    for entry in manifest.get('entries', []):
        path = _member_path(source_root, entry['source'])
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        edited |= digest != entry.get('source_sha256')
        if overrides_root is not None:
            override = _member_path(overrides_root, entry['source'])
            if override.is_file():
                override_digest = hashlib.sha256(override.read_bytes()).hexdigest()
                edited |= override_digest != entry.get('source_sha256')
    return edited


def rebuild(original, manifest, source_root, overrides_root=None):
    """Apply member edits, appending grown members and updating table offsets."""
    parsed = parse(original)
    if parsed['source_sha256'] != manifest.get('source_sha256'):
        raise ValueError('UI bundle differs from extracted manifest source')
    if parsed['header_hex'] != manifest.get('header_hex'):
        raise ValueError('UI bundle header differs from extracted manifest')
    if len(parsed['entries']) != len(manifest.get('entries', [])):
        raise ValueError('UI bundle entry count differs from extracted manifest')

    result = bytearray(original)
    tail = len(result)
    changed = False
    for current, saved in zip(parsed['entries'], manifest['entries']):
        for key in ('index', 'record_offset', 'name_hex', 'kind_hex', 'size', 'offset', 'flags'):
            if current[key] != saved.get(key):
                raise ValueError(f'UI bundle entry {current["index"]} metadata drift: {key}')
        member_path = _member_path(source_root, saved['source'])
        member = member_path.read_bytes()
        member_digest = hashlib.sha256(member).hexdigest()
        override_path = (_member_path(overrides_root, saved['source'])
                         if overrides_root is not None else None)
        if override_path is not None and override_path.is_file():
            override = override_path.read_bytes()
            override_digest = hashlib.sha256(override).hexdigest()
            base_changed = member_digest != saved.get('source_sha256')
            override_changed = override_digest != saved.get('source_sha256')
            if base_changed and override_changed:
                raise ValueError(f'conflicting UI member and override edits: {saved["source"]}')
            if override_changed:
                member = override
                member_digest = override_digest
        if member_digest == saved.get('source_sha256'):
            continue
        changed = True
        record_offset = saved['record_offset']
        if len(member) > saved['size']:
            offset = (tail + ALIGNMENT - 1) // ALIGNMENT * ALIGNMENT
            result.extend(b'\0' * (offset - tail))
            result.extend(member)
            tail = offset + len(member)
        else:
            offset = saved['offset']
            result[offset:offset + len(member)] = member
        struct.pack_into('<II', result, record_offset + 20, len(member), offset)

    if not changed:
        return original
    return bytes(result)


def audit(root):
    """Validate every extracted bundle and unchanged member round-trip."""
    root = Path(root)
    rows = json.loads((root / 'catalog.json').read_text(encoding='utf-8'))
    census_path = root / 'census.json'
    root_census = (json.loads(census_path.read_text(encoding='utf-8'))
                   if census_path.exists() else {})
    result = dict(version=1, evidence_date=date.today().isoformat(),
                  reference_sha256=root_census.get('reference_sha256'),
                  scope='Prepared workspace bundles accepted by the observed menu resource-table parser',
                  schema=dict(count='u32le@0', header_marker_hex=KNOWN_HEADER.hex(),
                              record_size=RECORD_SIZE, name='16 bytes', type='4 bytes',
                              size='u32le@record+20', offset='u32le@record+24',
                              flags='u32le@record+28; observed zero, semantics unresolved',
                              member_alignment=ALIGNMENT),
                  bundle_count=0, resource_count=0, decoded_bytes=0,
                  type_counts={}, untouched_exact_rebuilds=0, edited_bundles=0,
                  unparsed=[])
    for row in rows:
        if not row.get('ui_bundle_source'):
            continue
        decoded = _member_path(root, row['bpe_source']).read_bytes()
        manifest = json.loads(_member_path(root, row['ui_bundle_source']).read_text(encoding='utf-8'))
        member_root = _member_path(root, row['ui_bundle_dir'])
        parsed = parse(decoded)
        rebuilt = rebuild(decoded, manifest, member_root)
        edited = has_edits(manifest, member_root)
        if not edited and rebuilt != decoded:
            raise ValueError(f'untouched UI bundle does not rebuild exactly: {row["name"]}')
        result['bundle_count'] += 1
        result['resource_count'] += len(parsed['entries'])
        result['decoded_bytes'] += len(decoded)
        for entry in parsed['entries']:
            kind = bytes.fromhex(entry['kind_hex']).rstrip(b'\0').decode('ascii', errors='replace')
            result['type_counts'][kind] = result['type_counts'].get(kind, 0) + 1
        if edited:
            result['edited_bundles'] += 1
        else:
            result['untouched_exact_rebuilds'] += 1
    prepared_census_path = root / 'prepared-census.json'
    if prepared_census_path.exists():
        result['unparsed'] = json.loads(prepared_census_path.read_text(encoding='utf-8')).get(
            'ui_bundle_unparsed', [])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    extract_parser = sub.add_parser('extract')
    extract_parser.add_argument('source', type=Path)
    extract_parser.add_argument('destination', type=Path)
    extract_parser.add_argument('manifest', type=Path)
    build_parser = sub.add_parser('build')
    build_parser.add_argument('source', type=Path)
    build_parser.add_argument('manifest', type=Path)
    build_parser.add_argument('members', type=Path)
    build_parser.add_argument('output', type=Path)
    audit_parser = sub.add_parser('audit')
    audit_parser.add_argument('workspace', type=Path)
    audit_parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'extract':
            raw = args.source.read_bytes()
            extract(raw, args.destination, args.manifest)
        elif args.command == 'build':
            if args.output.exists():
                raise ValueError('output already exists')
            original = args.source.read_bytes()
            manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_bytes(rebuild(original, manifest, args.members))
        else:
            result = audit(args.workspace)
            output = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
            if args.output:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(output, encoding='utf-8')
            else:
                print(output, end='')
    except (OSError, ValueError, KeyError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
