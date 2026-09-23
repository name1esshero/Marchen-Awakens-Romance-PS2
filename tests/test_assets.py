import io
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import assets
from test_bootstrap import iso as make_iso


def pac(payloads):
    data = bytearray(16 + len(payloads) * 32)
    struct.pack_into('<4I', data, 0, len(payloads), 0x101, 0, 16)
    for i, payload in enumerate(payloads):
        p = 16 + i * 32
        data[p:p + 4] = b'test'
        data[p + 16:p + 20] = b'bin\0'
        struct.pack_into('<3I', data, p + 20, len(payload), len(data), 0)
        data.extend(payload)
    data.extend(b'preserved tail')
    return bytes(data)


class AssetsTests(unittest.TestCase):
    def export(self, data, dest):
        s = io.BytesIO(data)
        census = dict(containers={}, leaves=0, extensions={}, unparsed=[])
        assets.export_node(s, 0, len(data), dest, *assets.archive(s, 0, len(data)), census)
        return census

    def test_nested_roundtrip_without_reference(self):
        data = pac([pac([b'hello']), b'\0' * 12, b'xyz'])
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'source'
            self.export(data, root)
            out = Path(d) / 'rebuilt'
            assets.build(root, out)
            self.assertEqual(out.read_bytes(), data)

    def test_growth_propagates_and_updates_table(self):
        data = pac([pac([b'hello']), b'other'])
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'source'
            self.export(data, root)
            (root / '00000.asset/00000.bin').write_bytes(b'long translation' * 20)
            out = Path(d) / 'rebuilt'
            with self.assertRaises(ValueError):
                assets.build(root, out)
            self.assertFalse(out.exists())
            assets.build(root, out, True)
            s = io.BytesIO(out.read_bytes())
            entries = assets.archive(s, 0, out.stat().st_size)[2]
            first = entries[0]
            self.assertGreater(first['offset'], len(data))
            nested = assets.archive(s, first['offset'], first['size'])[2][0]
            s.seek(first['offset'] + nested['offset'])
            self.assertEqual(s.read(nested['size']), b'long translation' * 20)
            s.seek(entries[1]['offset'])
            self.assertEqual(s.read(entries[1]['size']), b'other')

    def test_malformed_table(self):
        b = bytearray(pac([b'hello']))
        struct.pack_into('<I', b, 16 + 24, 0)
        with self.assertRaises(ValueError):
            assets.archive(io.BytesIO(b), 0, len(b))
        with self.assertRaises(ValueError):
            assets.archive(io.BytesIO(b'AFS\0' + struct.pack('<I', 100)), 0, 8)

    def test_unsafe_source_and_incomplete_layout(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'source'
            self.export(pac([b'hello']), root)
            layout = root / 'layout.json'
            m = json.loads(layout.read_text())
            m['pieces'][0]['source'] = '../outside'
            assets.save_json(layout, m)
            with self.assertRaises(ValueError):
                assets.build(root, Path(d) / 'out')

    def test_yfs_directory_mapping(self):
        b = bytearray(120)
        b[:8] = b'YFS\0' + struct.pack('<HH', 1, 1)
        b[8:13] = b'data/'
        struct.pack_into('<HH', b, 68, 1, 0)
        b[72:76] = b'test'
        struct.pack_into('<III', b, 96, 4, 112, 0)
        b[112:116] = b'TEST'
        parsed = assets.archive(io.BytesIO(b), 0, len(b))
        self.assertEqual(parsed[2][0]['name'], 'data/test')
        struct.pack_into('<H', b, 70, 1)
        with self.assertRaises(ValueError):
            assets.archive(io.BytesIO(b), 0, len(b))

    def test_iso_file_growth_updates_directory_and_volume(self):
        data = bytes(make_iso())
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'source'
            stream = io.BytesIO(data)
            _, entries = assets.disc_entries(stream, len(data))
            assets.export_node(stream, 0, len(data), root, 'ISO', 2048, entries,
                               dict(containers={}, leaves=0, extensions={}, unparsed=[]))
            (root / '00000.bin').write_bytes(b'translated' * 400)
            out = Path(d) / 'rebuilt.iso'
            assets.build(root, out, True)
            with out.open('rb') as rebuilt:
                inventory = assets.inventory(rebuilt, out.stat().st_size)
                item = next(e for e in inventory['entries'] if e['path'] == 'A;1')
                self.assertEqual(item['size'], 4000)
                rebuilt.seek(item['lba'] * 2048)
                self.assertEqual(rebuilt.read(item['size']), b'translated' * 400)
                self.assertEqual(inventory['volume_bytes'], out.stat().st_size)


if __name__ == '__main__':
    unittest.main()
