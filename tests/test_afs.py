import hashlib
import io
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tests'))
import afs
import assets


def make_afs():
    """Build a small archive matching the observed 48-byte TOC-record shape."""
    count = 2
    toc_offset = 0xA00
    toc_size = count * afs.TOC_RECORD_SIZE
    data = bytearray(0xB00)
    data[:8] = b'AFS\0' + struct.pack('<I', count)
    struct.pack_into('<II', data, 8, 0x800, 5)
    struct.pack_into('<II', data, 16, 0x900, 7)
    struct.pack_into('<II', data, 24, toc_offset, toc_size)
    data[0x800:0x805] = b'first'
    data[0x900:0x907] = b'second!'
    for index, name in enumerate((b'first.adx', b'voice.sfd')):
        start = toc_offset + index * afs.TOC_RECORD_SIZE
        data[start:start + len(name)] = name
        data[start + afs.NAME_SIZE:start + afs.TOC_RECORD_SIZE] = bytes([index + 1]) * 16
    return bytes(data)


class AfsTests(unittest.TestCase):
    def test_parses_members_names_and_opaque_metadata(self):
        parsed = afs.parse(io.BytesIO(make_afs()), len(make_afs()))
        self.assertEqual(parsed['format'], 'observed-afs-v1-filename-toc')
        self.assertEqual(parsed['member_count'], 2)
        self.assertEqual(parsed['toc_offset'], 0xA00)
        self.assertEqual([member['size'] for member in parsed['members']], [5, 7])
        self.assertEqual([record['name'] for record in parsed['toc']],
                         ['first.adx', 'voice.sfd'])
        self.assertEqual(parsed['toc'][0]['opaque_metadata_hex'], '01' * 16)
        self.assertEqual(parsed['toc'][1]['opaque_metadata_sha256'],
                         hashlib.sha256(bytes([2]) * 16).hexdigest())

    def test_rejects_bad_signature_and_truncated_table(self):
        with self.assertRaisesRegex(ValueError, 'signature'):
            afs.parse(io.BytesIO(b'NOPE' + bytes(32)), 36)
        broken = b'AFS\0' + struct.pack('<I', 20) + bytes(8)
        with self.assertRaisesRegex(ValueError, 'table or TOC pointer'):
            afs.parse(io.BytesIO(broken), len(broken))

    def test_rejects_incomplete_or_wrong_size_toc_pointer(self):
        data = bytearray(make_afs())
        struct.pack_into('<II', data, 24, 0xA00, 0)
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            afs.parse(io.BytesIO(data), len(data))
        data = bytearray(make_afs())
        struct.pack_into('<II', data, 24, 0xA00, 48)
        with self.assertRaisesRegex(ValueError, 'does not match'):
            afs.parse(io.BytesIO(data), len(data))

    def test_rejects_out_of_range_and_overlapping_extents(self):
        data = bytearray(make_afs())
        struct.pack_into('<II', data, 24, len(data) - 8, 96)
        with self.assertRaisesRegex(ValueError, 'outside file'):
            afs.parse(io.BytesIO(data), len(data))
        data = bytearray(make_afs())
        struct.pack_into('<II', data, 16, 0x802, 7)
        with self.assertRaisesRegex(ValueError, 'overlapping AFS member'):
            afs.parse(io.BytesIO(data), len(data))
        data = bytearray(make_afs())
        struct.pack_into('<II', data, 8, 0xA10, 5)
        with self.assertRaisesRegex(ValueError, 'overlaps archive metadata'):
            afs.parse(io.BytesIO(data), len(data))

    def test_rejects_malformed_filename_slot(self):
        data = bytearray(make_afs())
        data[0xA00] = 0
        with self.assertRaisesRegex(ValueError, 'empty name'):
            afs.parse(io.BytesIO(data), len(data))
        data = bytearray(make_afs())
        data[0xA00 + len(b'first.adx') + 1] = 0x7F
        with self.assertRaisesRegex(ValueError, 'nonzero name padding'):
            afs.parse(io.BytesIO(data), len(data))

    def test_existing_asset_builder_preserves_synthetic_afs_byte_exactly(self):
        original = make_afs()
        parsed = assets.archive(io.BytesIO(original), 0, len(original))
        self.assertEqual(parsed[0], 'AFS')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'source'
            census = dict(containers={}, leaves=0, extensions={}, unparsed=[])
            assets.export_node(io.BytesIO(original), 0, len(original), root,
                               *parsed, census)
            rebuilt = Path(directory) / 'rebuilt.afs'
            assets.build(root, rebuilt)
            self.assertEqual(rebuilt.read_bytes(), original)
            with rebuilt.open('rb') as stream:
                afs.parse(stream, len(original))

    def test_iso_inventory_hashes_and_accounts_for_every_archive_byte(self):
        archive = make_afs()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            image = root / 'source.iso'
            image.write_bytes(bytes(afs.SECTOR_SIZE) + archive)
            manifest = root / 'disc.json'
            manifest.write_text(json.dumps({
                'image_bytes': afs.SECTOR_SIZE + len(archive),
                'sha256': 'pinned-manifest-value',
                'entries': [{'path': 'TEST.AFS;1', 'lba': 1,
                             'size': len(archive), 'prefix_hex': archive[:16].hex()}],
            }))
            report = afs.inventory_iso(image, manifest)
        item = report['archives'][0]
        self.assertEqual(item['sha256'], hashlib.sha256(archive).hexdigest())
        self.assertEqual(sum(region['size'] for region in item['byte_regions']),
                         len(archive))
        self.assertEqual([member['name'] for member in item['members']],
                         ['first.adx', 'voice.sfd'])


if __name__ == '__main__':
    unittest.main()
