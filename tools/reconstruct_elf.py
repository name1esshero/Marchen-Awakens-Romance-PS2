"""Explicitly export bootstrap sources, or rebuild an ELF without its reference.

Unrecovered intervals are hexadecimal text, never claimed as recovered code.
Selected relocation-free sections must come from an independently built object.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

from bootstrap import elf_sections


def selected_sections(data, names, require_object=False):
    if not names or len(names) != len(set(names)):
        raise ValueError('section selection must be nonempty and unique')
    metadata = elf_sections(data)
    if metadata['machine'] != 8:
        raise ValueError('expected a MIPS ELF')
    if require_object and struct.unpack_from('<H', data, 16)[0] != 1:
        raise ValueError('expected a relocatable object')
    sections = metadata['sections']
    result = {}
    for name in names:
        matches = [s for s in sections if s['name'] == name]
        if len(matches) != 1:
            raise ValueError(f'{name}: missing or ambiguous section')
        section = matches[0]
        if section['type'] != 1 or not section['size'] or not section['flags'] & 4:
            raise ValueError(f'{name}: expected nonempty executable PROGBITS')
        result[name] = section
    indices = {s['index'] for s in result.values()}
    table_offset = struct.unpack_from('<I', data, 32)[0]
    for section in sections:
        if section['type'] in (4, 9) and section['size']:
            target = struct.unpack_from('<I', data, table_offset + 40 * section['index'] + 28)[0]
            if target in indices:
                raise ValueError('selected section has unapplied relocations')
    return result


def export_sources(reference, names, destination, expected_sha256):
    digest = hashlib.sha256(reference).hexdigest()
    if digest != expected_sha256:
        raise ValueError('reference hash mismatch; do not regenerate the baseline')
    sections = selected_sections(reference, names)
    regions = []
    raw = {}
    cursor = 0
    for section in sorted(sections.values(), key=lambda s: s['offset']):
        start = section['offset']
        if start < cursor:
            raise ValueError('selected sections overlap')
        if start > cursor:
            filename = f'unrecovered_{cursor:08x}.hex'
            raw[filename] = reference[cursor:start]
            regions.append(dict(offset=cursor, size=start - cursor,
                                kind='unrecovered_hex', source=filename))
        regions.append(dict(offset=start, size=section['size'],
                            kind='object_section', section=section['name']))
        cursor = start + section['size']
    if cursor < len(reference):
        filename = f'unrecovered_{cursor:08x}.hex'
        raw[filename] = reference[cursor:]
        regions.append(dict(offset=cursor, size=len(reference) - cursor,
                            kind='unrecovered_hex', source=filename))
    manifest = dict(schema=1, reference_sha256=digest, file_size=len(reference), regions=regions)
    # Refuse to clobber existing source work. Regenerate in a fresh directory.
    destination.mkdir(parents=True, exist_ok=False)
    for filename, data in raw.items():
        text = '\n'.join(data[i:i + 32].hex() for i in range(0, len(data), 32)) + '\n'
        (destination / filename).write_text(text, encoding='ascii')
    (destination / 'layout.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def rebuild(source_dir, object_data):
    manifest = json.loads((source_dir / 'layout.json').read_text())
    if manifest['schema'] != 1 or manifest['file_size'] <= 0:
        raise ValueError('unsupported manifest schema or size')
    names = [r['section'] for r in manifest['regions'] if r['kind'] == 'object_section']
    sections = selected_sections(object_data, names, require_object=True)
    output = bytearray()
    for region in manifest['regions']:
        if region['offset'] != len(output) or region['size'] <= 0:
            raise ValueError('regions must cover the output exactly once, in order')
        if region['offset'] + region['size'] > manifest['file_size']:
            raise ValueError('region exceeds declared file size')
        if region['kind'] == 'unrecovered_hex':
            path = (source_dir / region['source']).resolve()
            if not path.is_relative_to(source_dir.resolve()):
                raise ValueError('source path escapes source directory')
            payload = bytes.fromhex(path.read_text(encoding='ascii'))
        elif region['kind'] == 'object_section':
            section = sections[region['section']]
            payload = object_data[section['offset']:section['offset'] + section['size']]
        else:
            raise ValueError('unknown region kind')
        if len(payload) != region['size']:
            raise ValueError('source/section size does not match its declared region')
        output.extend(payload)
    if len(output) != manifest['file_size']:
        raise ValueError('incomplete output coverage')
    return bytes(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    export = commands.add_parser('export', help='explicit reference-to-source bootstrap only')
    export.add_argument('reference', type=Path)
    export.add_argument('selection', type=Path)
    export.add_argument('destination', type=Path)
    export.add_argument('--hash-file', type=Path, required=True)
    build = commands.add_parser('build', help='rebuild using only source text and compiled object')
    build.add_argument('sources', type=Path)
    build.add_argument('object', type=Path)
    build.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.command == 'export':
        expected = args.hash_file.read_text().split()[0]
        manifest = export_sources(args.reference.read_bytes(), args.selection.read_text().splitlines(),
                                  args.destination, expected)
        print(f"Exported {len(manifest['regions'])} regions; raw intervals remain technical debt")
    else:
        output = rebuild(args.sources, args.object.read_bytes())
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(output)
        print(f'Rebuilt {len(output)} bytes; SHA256 {hashlib.sha256(output).hexdigest()}')


if __name__ == '__main__':
    main()
