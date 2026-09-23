#!/usr/bin/env python3
"""Inspect the filename TOCs in the observed AFS archives.

The parser recognizes the little-endian AFS header/member table and the
48-byte filename records found in this game's MOVIE.AFS and BGM.AFS. The
16-byte record suffix is preserved as opaque data; this tool does not edit or
interpret it.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

SECTOR_SIZE = 2048
AFS_MAGIC = b'AFS\0'
TOC_RECORD_SIZE = 48
NAME_SIZE = 32
OPAQUE_METADATA_SIZE = 16
HASH_CHUNK = 1024 * 1024


def _read_exact(stream, offset, size, limit):
    if offset < 0 or size < 0 or offset + size > limit:
        raise ValueError('read outside AFS extent')
    stream.seek(offset)
    data = stream.read(size)
    if len(data) != size:
        raise ValueError('truncated AFS extent')
    return data


def _overlap(left, right):
    return left[0] < right[1] and right[0] < left[1]


def parse(stream, size):
    """Parse one AFS extent from a seekable binary stream at offset zero.

    ``size`` is the authenticated parent extent, not necessarily the stream's
    total length. Member payloads and the trailing filename TOC must be fully
    contained in that extent and must not overlap the AFS header/table or one
    another. The TOC pointer is the observed pair of little-endian u32 values
    immediately after the member table.
    """
    if size < 16:
        raise ValueError('AFS extent is too small for header and TOC pointer')
    header = _read_exact(stream, 0, 8, size)
    if header[:4] != AFS_MAGIC:
        raise ValueError('invalid AFS signature')
    count = struct.unpack_from('<I', header, 4)[0]
    table_end = 8 + count * 8
    pointer_end = table_end + 8
    if pointer_end > size:
        raise ValueError('AFS member table or TOC pointer outside file')
    table = _read_exact(stream, 8, count * 8, size)
    pointer = _read_exact(stream, table_end, 8, size)
    toc_offset, toc_size = struct.unpack('<II', pointer)
    if toc_offset == 0 and toc_size == 0:
        raise ValueError('AFS has no filename TOC pointer')
    if toc_offset == 0 or toc_size == 0:
        raise ValueError('incomplete AFS TOC pointer')
    if toc_size != count * TOC_RECORD_SIZE:
        raise ValueError('AFS TOC size does not match 48-byte records')
    if toc_offset < pointer_end or toc_offset + toc_size > size:
        raise ValueError('AFS TOC outside file or overlaps its header tables')

    members = []
    member_ranges = []
    structural = (0, pointer_end)
    toc_range = (toc_offset, toc_offset + toc_size)
    for index in range(count):
        offset, length = struct.unpack_from('<II', table, index * 8)
        end = offset + length
        if end > size:
            raise ValueError(f'AFS member {index} outside file')
        extent = (offset, end)
        if length and (_overlap(extent, structural) or _overlap(extent, toc_range)):
            raise ValueError(f'AFS member {index} overlaps archive metadata')
        members.append({'index': index, 'offset': offset, 'size': length})
        if length:
            member_ranges.append(extent)
    member_ranges.sort()
    for previous, current in zip(member_ranges, member_ranges[1:]):
        if _overlap(previous, current):
            raise ValueError('overlapping AFS member extents')

    raw_toc = _read_exact(stream, toc_offset, toc_size, size)
    toc = []
    for index in range(count):
        start = index * TOC_RECORD_SIZE
        record = raw_toc[start:start + TOC_RECORD_SIZE]
        name_slot = record[:NAME_SIZE]
        name_bytes = name_slot.split(b'\0', 1)[0]
        if not name_bytes:
            raise ValueError(f'AFS TOC record {index} has an empty name')
        if b'\0' in name_slot and any(name_slot[name_slot.index(0) + 1:]):
            raise ValueError(f'AFS TOC record {index} has nonzero name padding')
        try:
            name = name_bytes.decode('cp932')
        except UnicodeDecodeError as exc:
            raise ValueError(f'AFS TOC record {index} name is not CP932') from exc
        metadata = record[NAME_SIZE:]
        toc.append({
            'index': index,
            'name': name,
            'name_slot_hex': name_slot.hex(),
            'opaque_metadata_hex': metadata.hex(),
            'opaque_metadata_sha256': hashlib.sha256(metadata).hexdigest(),
        })

    return {
        'format': 'observed-afs-v1-filename-toc',
        'archive_size': size,
        'member_count': count,
        'member_table_offset': 8,
        'member_table_size': count * 8,
        'toc_pointer_offset': table_end,
        'toc_offset': toc_offset,
        'toc_size': toc_size,
        'toc_record_size': TOC_RECORD_SIZE,
        'members': members,
        'toc': toc,
    }


def _measure(stream, absolute_offset, size):
    """Return a streaming SHA-256 and zero-byte observation for a region."""
    digest = hashlib.sha256()
    all_zero = True
    stream.seek(absolute_offset)
    left = size
    while left:
        block = stream.read(min(HASH_CHUNK, left))
        if not block:
            raise ValueError('source image ended while hashing AFS region')
        digest.update(block)
        if any(block):
            all_zero = False
        left -= len(block)
    return digest.hexdigest(), all_zero


def _regions(parsed):
    """Partition archive bytes into metadata, members, and unclassified gaps."""
    extents = [
        (0, parsed['toc_pointer_offset'] + 8, 'header_member_table_and_toc_pointer'),
    ]
    extents.extend((member['offset'], member['offset'] + member['size'],
                    f"member:{member['index']}")
                   for member in parsed['members'] if member['size'])
    extents.append((parsed['toc_offset'], parsed['toc_offset'] + parsed['toc_size'],
                    'filename_toc'))
    extents.sort()
    regions = []
    cursor = 0
    gap_index = 0
    for start, end, label in extents:
        if start > cursor:
            regions.append((cursor, start - cursor, f'unclassified_gap:{gap_index}'))
            gap_index += 1
        if start < cursor:
            raise ValueError('AFS region partition overlaps')
        regions.append((start, end - start, label))
        cursor = end
    if cursor < parsed['archive_size']:
        regions.append((cursor, parsed['archive_size'] - cursor,
                        f'unclassified_gap:{gap_index}'))
    if sum(length for _, length, _ in regions) != parsed['archive_size']:
        raise ValueError('AFS region partition does not cover archive')
    return regions


def inventory_iso(iso_path, manifest_path):
    """Hash and inventory AFS extents listed by the pinned ISO manifest."""
    manifest = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    iso_path = Path(iso_path)
    iso_size = iso_path.stat().st_size
    if iso_size != manifest.get('image_bytes'):
        raise ValueError('ISO length does not match source manifest')
    afs_entries = [entry for entry in manifest['entries']
                   if entry['path'].upper().endswith('.AFS;1')]
    if not afs_entries:
        raise ValueError('source manifest contains no AFS files')

    archives = []
    with iso_path.open('rb') as iso:
        for entry in afs_entries:
            base = entry['lba'] * SECTOR_SIZE
            size = entry['size']
            if base + size > iso_size:
                raise ValueError(f"{entry['path']} extent outside ISO")
            iso.seek(base)
            observed_prefix = iso.read(16)
            expected_prefix = entry.get('prefix_hex')
            if expected_prefix and observed_prefix.hex() != expected_prefix:
                raise ValueError(f"{entry['path']} prefix differs from ISO manifest")
            bounded = _ExtentStream(iso, base, size)
            parsed = parse(bounded, size)
            archive_sha, _ = _measure(iso, base, size)
            toc_sha, toc_zero = _measure(iso, base + parsed['toc_offset'],
                                         parsed['toc_size'])
            rows = []
            names = {record['index']: record for record in parsed['toc']}
            for member in parsed['members']:
                sha, is_zero = _measure(iso, base + member['offset'], member['size'])
                iso.seek(base + member['offset'])
                prefix = iso.read(min(16, member['size']))
                row = dict(member)
                row.update(name=names[member['index']]['name'], sha256=sha,
                           prefix_hex=prefix.hex(), all_zero=is_zero)
                rows.append(row)
            region_rows = []
            for offset, length, label in _regions(parsed):
                sha, is_zero = _measure(iso, base + offset, length)
                region_rows.append(dict(label=label, offset=offset, size=length,
                                        sha256=sha, all_zero=is_zero))
            member_bytes = sum(member['size'] for member in parsed['members'])
            gap_rows = [region for region in region_rows
                        if region['label'].startswith('unclassified_gap:')]
            accounting = {
                'archive_bytes': size,
                'header_member_table_and_toc_pointer_bytes': parsed['toc_pointer_offset'] + 8,
                'member_payload_bytes': member_bytes,
                'filename_toc_bytes': parsed['toc_size'],
                'unclassified_gap_bytes': sum(region['size'] for region in gap_rows),
                'all_zero_unclassified_gap_bytes': sum(
                    region['size'] for region in gap_rows if region['all_zero']),
            }
            if (accounting['header_member_table_and_toc_pointer_bytes']
                    + accounting['member_payload_bytes']
                    + accounting['filename_toc_bytes']
                    + accounting['unclassified_gap_bytes'] != size):
                raise ValueError(f"{entry['path']} byte accounting does not close")
            archives.append({
                'path': entry['path'],
                'lba': entry['lba'],
                'iso_byte_offset': base,
                'size': size,
                'manifest_prefix_hex': entry.get('prefix_hex'),
                'sha256': archive_sha,
                'parsed': parsed,
                'toc_sha256': toc_sha,
                'toc_all_zero': toc_zero,
                'members': rows,
                'byte_regions': region_rows,
                'byte_accounting': accounting,
            })
    return {
        'schema': 'observed-afs-inventory-v1',
        'source_iso_filename': iso_path.name,
        'source_iso_size': iso_size,
        'source_iso_sha256_from_manifest': manifest.get('sha256'),
        'source_manifest_filename': Path(manifest_path).name,
        'archive_count': len(archives),
        'archives': archives,
        'limits': [
            'This census covers AFS archives named by the supplied ISO manifest only.',
            'The 16-byte suffix in each 48-byte filename record remains opaque.',
            'Names and member extents are structural inventory, not proof of runtime use.',
            'Archive relocation, edited-member reinsertion, and runtime loading are not validated here.',
        ],
    }


class _ExtentStream:
    """Read-only view of a bounded ISO extent, with offsets relative to it."""
    def __init__(self, stream, base, size):
        self.stream = stream
        self.base = base
        self.size = size

    def seek(self, offset, whence=0):
        if whence == 0:
            absolute = self.base + offset
        elif whence == 1:
            raise ValueError('relative seeks are not supported')
        elif whence == 2:
            absolute = self.base + self.size + offset
        else:
            raise ValueError('invalid seek mode')
        if absolute < self.base or absolute > self.base + self.size:
            raise ValueError('seek outside ISO archive extent')
        self.stream.seek(absolute)
        return absolute - self.base

    def read(self, size=-1):
        position = self.stream.tell() - self.base
        if position < 0 or position > self.size:
            raise ValueError('read outside ISO archive extent')
        if size < 0:
            size = self.size - position
        return self.stream.read(min(size, self.size - position))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--iso', type=Path, required=True,
                        help='source ISO image')
    parser.add_argument('--manifest', type=Path, default=Path('reports/disc.json'),
                        help='ISO inventory manifest containing file extents')
    parser.add_argument('--output', type=Path, required=True,
                        help='write machine-readable JSON inventory here')
    args = parser.parse_args(argv)
    report = inventory_iso(args.iso, args.manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n',
                           encoding='utf-8')
    print(f"inventoried {report['archive_count']} AFS archives -> {args.output}")
    for archive in report['archives']:
        print(f"{archive['path']}: {archive['parsed']['member_count']} members, "
              f"TOC {archive['parsed']['toc_size']} bytes, sha256 {archive['sha256']}")


if __name__ == '__main__':
    main()
