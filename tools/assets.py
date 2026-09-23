"""Lossless asset workspace. Export is explicit research; build uses workspace only.

Observed YFS/PAC and AFS tables, not a universal archive implementation.
Unknown leaves remain binary; relocation updates container tables, not game code.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import tempfile

from bootstrap import inventory, read_at, record, SECTOR
import messages
import message_catalog
import text_catalog
import bpe
import ui_bundle
try:
    from . import movies as movie_tools
    from . import sofdec
except ImportError:  # Support direct execution of sibling tools.
    import movies as movie_tools
    import sofdec

CHUNK = 1024 * 1024
GRAPHICS_STANDALONE_MANIFEST = 'standalone-txc-overrides.json'


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def safe(root, name):
    root = Path(os.path.abspath(root))
    relative = Path(name)
    if relative.is_absolute() or '..' in relative.parts or not relative.parts:
        raise ValueError('unsafe workspace path')
    return root / relative


def name_string(b):
    return b.split(b'\0', 1)[0].decode('cp932')


def member(name, offset, size, offset_field=None, size_field=None, unit=1):
    return dict(name=name, offset=offset, size=size, offset_field=offset_field,
                size_field=size_field, unit=unit)


def graphics_override_state(overrides):
    """Load hash-anchored edits for TXCs that are archive leaves."""
    if overrides is None:
        return None
    manifest_path = safe(overrides, GRAPHICS_STANDALONE_MANIFEST)
    if not manifest_path.is_file():
        return dict(root=Path(overrides).resolve(), entries={}, applied=set())
    document = json.loads(manifest_path.read_text(encoding='utf-8'))
    if document.get('version') != 1 or not isinstance(document.get('entries'), list):
        raise ValueError('unsupported standalone graphics override manifest')
    entries = {}
    for entry in document['entries']:
        target = Path(entry.get('target', ''))
        if target.is_absolute() or not target.parts or '..' in target.parts:
            raise ValueError('unsafe standalone graphics override target')
        target = target.as_posix()
        if target in entries:
            raise ValueError(f'duplicate standalone graphics override target: {target}')
        for field in ('source_sha256', 'override_sha256'):
            digest = entry.get(field, '')
            if len(digest) != 64 or any(ch not in '0123456789abcdef' for ch in digest):
                raise ValueError(f'invalid standalone graphics {field}')
        if not isinstance(entry.get('bytes'), int) or entry['bytes'] < 0:
            raise ValueError('invalid standalone graphics override length')
        entries[target] = entry
    return dict(root=Path(overrides).resolve(), entries=entries, applied=set())


def archive(stream, base, size):
    h = read_at(stream, base, min(size, 16))
    entries = []
    if h[:4] == b'YFS\0':
        nd, nf = struct.unpack_from('<HH', h, 4)
        end = 8 + nd * 64 + nf * 36
        if end > size:
            raise ValueError('YFS table outside file')
        table = read_at(stream, base, end)
        owners = {}
        for i in range(nd):
            p = 8 + i * 64
            directory = name_string(table[p:p + 60])
            count, first = struct.unpack_from('<HH', table, p + 60)
            if first + count > nf:
                raise ValueError('YFS directory range')
            for j in range(first, first + count):
                if j in owners:
                    raise ValueError('YFS duplicate owner')
                owners[j] = directory
        if len(owners) != nf:
            raise ValueError('YFS unowned member')
        for i in range(nf):
            p = 8 + nd * 64 + i * 36
            length, offset, unknown = struct.unpack_from('<III', table, p + 24)
            if unknown:
                raise ValueError('YFS unknown member flags')
            entries.append(member(owners[i] + name_string(table[p:p + 24]),
                                  offset, length, p + 28, p + 24))
        kind, align = 'YFS', 2048
    elif h[:4] == b'AFS\0':
        count = struct.unpack_from('<I', h, 4)[0]
        end = 8 + count * 8
        if end > size:
            raise ValueError('AFS table outside file')
        table = read_at(stream, base, end)
        for i in range(count):
            offset, length = struct.unpack_from('<II', table, 8 + i * 8)
            entries.append(member(f'{i:05d}.bin', offset, length, 8 + i * 8, 12 + i * 8))
        # Attribute/name tables remain opaque and in their original positions.
        kind, align = 'AFS', 2048
    elif len(h) == 16 and h[4:16] in (bytes.fromhex('010100000000000010000000'),
                                                bytes.fromhex('000100000000000010000000')):
        count = struct.unpack_from('<I', h)[0]
        end = 16 + count * 32
        if end > size:
            raise ValueError('PAC table outside file')
        table = read_at(stream, base, end)
        for i in range(count):
            p = 16 + i * 32
            length, offset, unknown = struct.unpack_from('<III', table, p + 20)
            if unknown:
                raise ValueError('PAC unknown member flags')
            name = name_string(table[p:p + 16]) + '.' + name_string(table[p + 16:p + 20])
            entries.append(member(name, offset, length, p + 24, p + 20))
        kind, align = 'PAC', 16
    else:
        return None
    cursor = end
    for e in sorted(entries, key=lambda e: e['offset']):
        if e['offset'] < cursor or e['offset'] + e['size'] > size:
            raise ValueError(f'{kind} overlapping/out-of-range member {e["name"]}')
        cursor = e['offset'] + e['size']
    return kind, align, entries


def copy_extent(stream, offset, size, target):
    """Scan every byte; store zero spans sparsely without assuming padding."""
    stream.seek(offset)
    digest = hashlib.sha256()
    zero = True
    with target.open('xb') as out:
        left = size
        while left:
            b = stream.read(min(CHUNK, left))
            if not b:
                raise ValueError('truncated source')
            digest.update(b)
            if b.count(0) == len(b):
                out.seek(len(b), 1)
            else:
                zero = False
                out.write(b)
            left -= len(b)
        out.truncate(size)
    return digest.hexdigest(), zero


def export_node(stream, base, size, dest, kind, alignment, entries, census, depth=0):
    if depth > 32:
        raise ValueError('archive nesting exceeds 32')
    dest.mkdir()
    pieces = []
    cursor = 0
    # Stable numeric identity avoids unsafe names, duplicate names and host case folding.
    for i, e in enumerate(sorted(entries, key=lambda e: e['offset'])):
        if e['offset'] < cursor or e['offset'] + e['size'] > size:
            raise ValueError('overlapping or out-of-range extent')
        if e['offset'] > cursor:
            pieces.append(export_piece(stream, base, cursor, e['offset'] - cursor,
                                       dest, f'gap-{i:05d}.bin'))
        e = dict(e)
        filename = f'{i:05d}.bin'
        nested = None
        try:
            nested = archive(stream, base + e['offset'], e['size'])
        except (ValueError, UnicodeError) as exc:
            census['unparsed'].append(dict(name=e['name'], reason=str(exc)))
        if nested:
            filename = f'{i:05d}.asset'
            export_node(stream, base + e['offset'], e['size'], dest / filename,
                        *nested, census, depth + 1)
            e['source'] = filename
            e['container'] = True
        else:
            e.update(export_piece(stream, base, e['offset'], e['size'], dest, filename))
            census['leaves'] += 1
            ext = e['name'].rsplit('.', 1)[-1].lower()
            census['extensions'][ext] = census['extensions'].get(ext, 0) + 1
        pieces.append(e)
        cursor = e['offset'] + e['size']
    if cursor < size:
        pieces.append(export_piece(stream, base, cursor, size - cursor, dest, 'tail.bin'))
    census['containers'][kind] = census['containers'].get(kind, 0) + 1
    save_json(dest / 'layout.json', dict(version=1, kind=kind, alignment=alignment,
                                       size=size, pieces=pieces))


def export_piece(stream, base, offset, size, dest, filename):
    digest, zero = copy_extent(stream, base + offset, size, dest / filename)
    result = dict(offset=offset, size=size, sha256=digest)
    if zero:
        (dest / filename).unlink()
        result['zero'] = True
    else:
        result['source'] = filename
    return result


def disc_entries(stream, size):
    info = inventory(stream, size)
    # Locate actual directory records so mod builds can update both-endian fields.
    directories = [(16 * SECTOR + 156, None)]
    root = read_at(stream, directories[0][0], 34)
    lba, count, _, _ = record(root)
    dirs = [(lba, count, '')]
    result = []
    while dirs:
        lba, count, parent = dirs.pop()
        data = read_at(stream, lba * SECTOR, count)
        pos = 0
        while pos < count:
            n = data[pos]
            if not n:
                pos = (pos // SECTOR + 1) * SECTOR
                continue
            off = lba * SECTOR + pos
            block, length, flags, name = record(data[pos:pos + n])
            pos += n
            if name in (b'\0', b'\1'):
                continue
            path = parent + name.decode('ascii')
            if flags & 2:
                dirs.append((block, length, path + '/'))
            else:
                e = member(path, block * SECTOR, length, off + 2, off + 10, SECTOR)
                e['dual'] = True
                result.append(e)
    return info, result


def export(image, dest, hash_file):
    if dest.exists():
        raise ValueError('destination exists; use a fresh workspace')
    with image.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        if digest != hash_file.read_text().split()[0]:
            raise ValueError('reference SHA-256 mismatch')
        info, entries = disc_entries(stream, image.stat().st_size)
        census = dict(reference_sha256=digest, containers={}, leaves=0, extensions={}, unparsed=[])
        export_node(stream, 0, image.stat().st_size, dest, 'ISO', SECTOR, entries, census)
    save_json(dest / 'census.json', census)
    print(json.dumps(census, ensure_ascii=False, indent=2))


def build_node(root, output, relocate=False, translations=None, text_translations=None,
               logical='disc', graphics_overrides=None, workspace_root=None,
               graphics_state=None, movie_state=None):
    if workspace_root is None:
        workspace_root = Path(root).resolve()
    m = json.loads((root / 'layout.json').read_text())
    if m['version'] != 1 or m['kind'] not in ('ISO', 'YFS', 'PAC', 'AFS'):
        raise ValueError('unsupported workspace')
    cursor = 0
    patches = []
    with output.open('w+b') as out, tempfile.TemporaryDirectory(prefix='mar-assets-') as temp:
        out.truncate(m['size'])
        tail = m['size']
        for i, p in enumerate(m['pieces']):
            if p['offset'] != cursor or p['size'] < 0:
                raise ValueError('layout must cover every byte exactly once')
            cursor += p['size']
            if p.get('zero') and not p.get('source'):
                continue
            source = safe(root, p['source'])
            logical_path = logical + '!/' + p['name'] if p.get('name') else logical
            if p.get('container'):
                nested = Path(temp) / str(i)
                build_node(source, nested, relocate, translations, text_translations,
                           logical_path, graphics_overrides, workspace_root,
                           graphics_state, movie_state)
                source = nested
            if (not p.get('container') and graphics_state is not None and
                    p.get('name', '').lower().endswith('.txc')):
                workspace_relative = root.resolve().relative_to(workspace_root.resolve())
                target = (workspace_relative / p['source']).as_posix()
                entry = graphics_state['entries'].get(target)
                if entry is not None:
                    original = source.read_bytes()
                    if hashlib.sha256(original).hexdigest() != entry['source_sha256']:
                        raise ValueError(f'standalone TXC source differs from graphics manifest: {target}')
                    override = safe(graphics_state['root'], Path('standalone') / target)
                    if not override.is_file():
                        raise ValueError(f'missing standalone TXC graphics override: {target}')
                    if (override.stat().st_size != entry['bytes'] or
                            entry['bytes'] != len(original) or
                            hashlib.sha256(override.read_bytes()).hexdigest() !=
                            entry['override_sha256']):
                        raise ValueError(f'standalone TXC graphics override hash/size mismatch: {target}')
                    source = override
                    graphics_state['applied'].add(target)
            if movie_state is not None and logical_path in movie_state['entries']:
                entry = movie_state['entries'][logical_path]
                workspace_relative = root.resolve().relative_to(workspace_root.resolve())
                target = (workspace_relative / p['source']).as_posix()
                if target != entry['source_path']:
                    raise ValueError(f'movie index source path disagrees with layout: {logical_path}')
                original = source.read_bytes()
                if (len(original) != entry['source_bytes'] or
                        hashlib.sha256(original).hexdigest() != entry['source_sha256']):
                    raise ValueError(f'movie source differs from indexed Japanese baseline: {logical_path}')
                english_video = safe(movie_state['root'], entry['english_video_file'])
                video_bytes = english_video.read_bytes()
                if hashlib.sha256(video_bytes).hexdigest() != entry['english_video_sha256']:
                    raise ValueError(f'English movie override changed during build: {logical_path}')
                patched = Path(temp) / f'movie-{i}'
                patched.write_bytes(sofdec.rebuild(original, video_bytes))
                source = patched
                movie_state['applied'].add(logical_path)
            if p.get('bpe_source'):
                original = source.read_bytes()
                if hashlib.sha256(original).hexdigest() != p.get('bpe_original_sha256'):
                    raise ValueError(f'BPE source differs from prepared original: {logical_path}')
                decoded_source = safe(root, p['bpe_source'])
                decoded = decoded_source.read_bytes()
                decoded_edited = hashlib.sha256(decoded).hexdigest() != p.get('bpe_decoded_sha256')
                if p.get('ui_bundle_source'):
                    bundle_manifest_path = safe(root, p['ui_bundle_source'])
                    bundle_dir = safe(root, p['ui_bundle_dir'])
                    manifest = json.loads(bundle_manifest_path.read_text(encoding='utf-8'))
                    override_dir = None
                    if graphics_overrides is not None:
                        workspace_relative = root.resolve().relative_to(workspace_root.resolve())
                        override_dir = safe(
                            graphics_overrides,
                            str(workspace_relative / p['ui_bundle_dir']))
                    members_edited = ui_bundle.has_edits(manifest, bundle_dir, override_dir)
                    if decoded_edited and members_edited:
                        raise ValueError(f'both decoded BPE payload and UI bundle members edited: {logical_path}')
                    if members_edited:
                        decoded = ui_bundle.rebuild(decoded, manifest, bundle_dir, override_dir)
                        decoded_edited = True
                if decoded_edited:
                    patched = Path(temp) / f'bpe-{i}'
                    patched.write_bytes(bpe.encode(decoded))
                    source = patched
            if text_translations is not None and logical_path in text_translations['catalogs']:
                patched = Path(temp) / f'tsv-{i}'
                patched.write_bytes(text_catalog.apply(
                    source.read_bytes(), text_translations['catalogs'][logical_path]))
                text_translations['applied'].add(logical_path)
                source = patched
            elif p.get('text_source'):
                text_path = safe(root, p['text_source'])
                source = Path(temp) / f'text-{i}'
                source.write_bytes(text_path.read_bytes().decode('utf-8').encode('cp932'))
            elif p.get('message_source'):
                source = Path(temp) / f'messages-{i}'
                document = json.loads(safe(root, p['message_source']).read_text(encoding='utf-8'))
                if translations is not None:
                    document = message_catalog.apply(document, translations['catalog'])
                    translations['applied'] += 1
                source.write_bytes(messages.build(document))
            length = source.stat().st_size
            location = p['offset']
            moved = relocate and p.get('name') is not None
            if length != p['size'] and not moved:
                raise ValueError('size changed; use --relocate for a mod build')
            if moved and length > p['size']:
                location = (tail + m['alignment'] - 1) // m['alignment'] * m['alignment']
                tail = location + length
            if length != p['size']:
                if p.get('size_field') is None or p.get('offset_field') is None:
                    raise ValueError('no evidenced relocation fields')
                patches.append((p, location, length))
            out.seek(location)
            with source.open('rb') as inp:
                while True:
                    block = inp.read(CHUNK)
                    if not block:
                        break
                    if block.count(0) == len(block):
                        out.seek(len(block), 1)
                    else:
                        out.write(block)
            if p.get('container'):
                source.unlink()
        if cursor != m['size']:
            raise ValueError('incomplete layout')
        for p, location, length in patches:
            for field, value in ((p['offset_field'], location // p['unit']), (p['size_field'], length)):
                if not 0 <= field <= m['size'] - (8 if p.get('dual') else 4):
                    raise ValueError('patch outside original container')
                out.seek(field)
                out.write(struct.pack('<I', value))
                if p.get('dual'):
                    out.write(struct.pack('>I', value))
        if tail > m['size']:
            tail = (tail + m['alignment'] - 1) // m['alignment'] * m['alignment']
            out.truncate(tail)
            if m['kind'] == 'ISO':
                out.seek(16 * SECTOR + 80)
                out.write(struct.pack('<I', tail // SECTOR) + struct.pack('>I', tail // SECTOR))


def build(root, output, relocate=False, translations_path=None,
          text_translations_paths=None, graphics_overrides=None,
          replace_existing=False, movie_overrides=None):
    output = Path(output)
    if output.is_symlink() or output.resolve().is_relative_to(root.resolve()):
        raise ValueError('output must be outside the source workspace and not a symlink')
    if output.exists() and (not replace_existing or not output.is_file()):
        raise ValueError('output must be new unless --replace-existing targets a regular file')
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=output.parent, prefix='.assets-')
    os.close(fd)
    try:
        translations = ({'catalog': json.loads(translations_path.read_text(encoding='utf-8')),
                         'applied': 0} if translations_path is not None else None)
        text_translations = None
        if text_translations_paths:
            catalogs = {}
            for path in text_translations_paths:
                catalog = json.loads(path.read_text(encoding='utf-8'))
                text_catalog.validate(catalog)
                if catalog['resource'] in catalogs:
                    raise ValueError(f'duplicate text catalogue resource {catalog["resource"]}')
                catalogs[catalog['resource']] = catalog
            text_translations = {'catalogs': catalogs, 'applied': set()}
        graphics_state = graphics_override_state(graphics_overrides)
        movie_state = (movie_tools.override_state(movie_overrides)
                       if movie_overrides is not None else None)
        build_node(root, Path(tmp), relocate, translations, text_translations,
                   graphics_overrides=graphics_overrides,
                   workspace_root=Path(root).resolve(),
                   graphics_state=graphics_state, movie_state=movie_state)
        if translations is not None and translations['applied'] != 1:
            raise ValueError('translation catalogue was not applied to exactly one message table')
        if text_translations is not None and text_translations['applied'] != set(text_translations['catalogs']):
            missing = sorted(set(text_translations['catalogs']) - text_translations['applied'])
            raise ValueError(f'text catalogues were not applied to all resources: {missing}')
        if (graphics_state is not None and
                graphics_state['applied'] != set(graphics_state['entries'])):
            missing = sorted(set(graphics_state['entries']) - graphics_state['applied'])
            raise ValueError(f'standalone TXC graphics overrides were not applied: {missing[:3]}')
        if (movie_state is not None and
                movie_state['applied'] != set(movie_state['entries'])):
            missing = sorted(set(movie_state['entries']) - movie_state['applied'])
            raise ValueError(f'English movie overrides were not applied: {missing[:3]}')
        os.replace(tmp, output)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def prepare(root, report=Path('reports/assets_census.json')):
    """Expand newly recognized archives and create reversible UTF-8 text sources."""
    root = root.resolve()
    rows = []
    census = dict(containers={}, leaves=0, extensions={}, unparsed=[])

    def walk(folder, logical):
        path = folder / 'layout.json'
        m = json.loads(path.read_text())
        census['containers'][m['kind']] = census['containers'].get(m['kind'], 0) + 1
        for i, e in enumerate(m['pieces']):
            if 'name' not in e:
                continue
            name = logical + '!/' + e['name']
            source = safe(folder, e['source']) if e.get('source') else None
            if source and not e.get('container') and e['name'].lower().endswith('.pac'):
                with source.open('rb') as stream:
                    try:
                        nested = archive(stream, 0, e['size'])
                    except (ValueError, UnicodeError) as exc:
                        nested = None
                        census['unparsed'].append(dict(name=name, reason=str(exc)))
                    if nested:
                        dest = folder / (source.stem + '.asset')
                        if not (dest / 'layout.json').exists():
                            export_node(stream, 0, e['size'], dest, *nested,
                                        dict(containers={}, leaves=0, extensions={}, unparsed=[]))
                        e['source'] = dest.name
                        e['container'] = True
                        source = dest
            if e.get('container'):
                walk(source, name)
                continue
            if e.get('text_source') and e.get('message_source'):
                raise ValueError('leaf cannot have both plain-text and message-table sources')
            extension = e['name'].rsplit('.', 1)[-1].lower()
            is_text = (extension in ('txt', 'cpp', 'h', 'cnf;1')
                       or e['name'].lower().endswith('.dir;1'))
            if source and is_text and not e.get('text_source'):
                raw = source.read_bytes()
                text = raw.decode('cp932')
                if text.encode('cp932') != raw:
                    raise ValueError('text encoding is not reversible')
                editable = source.with_suffix('.utf8.txt')
                if not editable.exists():
                    editable.write_bytes(text.encode('utf-8'))
                e['text_source'] = editable.name
            if source and e['name'].lower().endswith('_msg.dat') and not e.get('message_source'):
                document = messages.parse(source.read_bytes())
                editable = source.with_suffix('.messages.json')
                if not editable.exists():
                    editable.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n',
                                        encoding='utf-8')
                e['message_source'] = editable.name
            if source and e['name'].lower().endswith('.b'):
                raw = source.read_bytes()
                if e.get('bpe_source'):
                    if hashlib.sha256(raw).hexdigest() != e.get('bpe_original_sha256'):
                        raise ValueError(f'BPE source differs from prepared original: {name}')
                    decoded_raw = bpe.decode(raw)
                    if (hashlib.sha256(decoded_raw).hexdigest() != e.get('bpe_decoded_sha256')
                            or len(decoded_raw) != e.get('bpe_decoded_size')):
                        raise ValueError(f'BPE decode differs from prepared metadata: {name}')
                else:
                    decoded_raw = bpe.decode(raw)
                    editable = source.with_name(source.stem + '.decoded.bin')
                    if not editable.exists():
                        editable.write_bytes(decoded_raw)
                    e['bpe_source'] = editable.name
                    e['bpe_original_sha256'] = hashlib.sha256(raw).hexdigest()
                    e['bpe_decoded_sha256'] = hashlib.sha256(decoded_raw).hexdigest()
                    e['bpe_decoded_size'] = len(decoded_raw)
                try:
                    ui_bundle.parse(decoded_raw)
                except ValueError as exc:
                    census.setdefault('ui_bundle_unparsed', []).append(
                        dict(name=name, reason=str(exc)))
                else:
                    bundle_manifest = source.with_name(source.stem + '.bundle.json')
                    bundle_dir = source.with_name(source.stem + '.resources')
                    ui_bundle.extract(decoded_raw, bundle_dir, bundle_manifest)
                    e['ui_bundle_source'] = bundle_manifest.name
                    e['ui_bundle_dir'] = bundle_dir.name
            rows.append(dict(name=name, size=e['size'],
                             source=str(source.relative_to(root)) if source else None,
                             text_source=str((folder / e['text_source']).relative_to(root)) if e.get('text_source') else None,
                             message_source=str((folder / e['message_source']).relative_to(root)) if e.get('message_source') else None,
                             bpe_source=str((folder / e['bpe_source']).relative_to(root)) if e.get('bpe_source') else None,
                             ui_bundle_source=str((folder / e['ui_bundle_source']).relative_to(root)) if e.get('ui_bundle_source') else None,
                             ui_bundle_dir=str((folder / e['ui_bundle_dir']).relative_to(root)) if e.get('ui_bundle_dir') else None,
                             zero=e.get('zero', False)))
            census['leaves'] += 1
            census['extensions'][extension] = census['extensions'].get(extension, 0) + 1
        save_json(path, m)

    walk(root, 'disc')
    save_json(root / 'catalog.json', rows)
    save_json(root / 'prepared-census.json', census)
    if report:
        save_json(report, census)
    print(json.dumps(census, indent=2))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    e = sub.add_parser('export')
    e.add_argument('image', type=Path)
    e.add_argument('workspace', type=Path)
    e.add_argument('--hash-file', type=Path, default=Path('config/reference.sha256'))
    prep = sub.add_parser('prepare')
    prep.add_argument('workspace', type=Path)
    prep.add_argument('--report', type=Path, default=Path('reports/assets_census.json'))
    b = sub.add_parser('build')
    b.add_argument('workspace', type=Path)
    b.add_argument('output', type=Path)
    b.add_argument('--relocate', action='store_true', help='allow growth by appending members; runtime unverified')
    b.add_argument('--translations', type=Path,
                   help='apply a validated original/translation message catalogue')
    b.add_argument('--text-translations', type=Path, action='append', default=[],
                   help='apply a validated CP932 TSV catalogue; may be repeated')
    b.add_argument('--graphics-overrides', type=Path,
                   help='apply generated RTX3 replacements without editing extracted sidecars')
    b.add_argument('--movie-overrides', type=Path,
                   help='apply indexed *_eng.m2v overrides while preserving original movie audio and CRI metadata')
    b.add_argument('--replace-existing', action='store_true',
                   help='atomically replace an existing regular output after a successful build')
    args = p.parse_args()
    if args.command == 'export':
        export(args.image, args.workspace, args.hash_file)
    elif args.command == 'prepare':
        prepare(args.workspace, args.report)
    else:
        build(args.workspace, args.output, args.relocate, args.translations,
              args.text_translations, args.graphics_overrides, args.replace_existing,
              args.movie_overrides)


if __name__ == '__main__':
    main()
