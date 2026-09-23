import struct
import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import ui_bundle


def bundle(name=b'window', kind=b'txc\0', data=b'pixels'):
    raw = bytearray(0x30)
    struct.pack_into('<I', raw, 0, 1)
    raw[4:8] = b'\x01\x01\0\0'
    raw[12:16] = b'\x10\0\0\0'
    raw[16:16 + len(name)] = name
    raw[32:36] = kind
    struct.pack_into('<III', raw, 36, len(data), 0x30, 0)
    raw.extend(data)
    return bytes(raw)


class UiBundleTests(unittest.TestCase):
    def test_extract_untouched_rebuild_and_edit(self):
        original = bundle()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            members = root / 'members'
            manifest_path = root / 'bundle.json'
            manifest = ui_bundle.extract(original, members, manifest_path)
            self.assertEqual(ui_bundle.rebuild(original, manifest, members), original)

            entry_path = members / manifest['entries'][0]['source']
            entry_path.write_bytes(b'PIXELS')
            replaced = ui_bundle.rebuild(original, manifest, members)
            self.assertEqual(replaced[0x30:0x36], b'PIXELS')

            entry_path.write_bytes(b'English graphic data')
            grown = ui_bundle.rebuild(original, manifest, members)
            self.assertEqual(struct.unpack_from('<II', grown, 36),
                             (len(b'English graphic data'), 0x40))
            length, offset = struct.unpack_from('<II', grown, 36)
            self.assertEqual(grown[offset:offset + length], b'English graphic data')
            self.assertEqual(offset % ui_bundle.ALIGNMENT, 0)

    def test_parse_rejects_bad_header_table_and_overlap(self):
        with self.assertRaisesRegex(ValueError, 'header variant'):
            ui_bundle.parse(b'\0' * 64)
        with self.assertRaisesRegex(ValueError, 'truncated UI bundle entry table'):
            ui_bundle.parse(b'\x01\0\0\0\x01\x01\0\0' + b'\0' * 8)
        raw = bytearray(0x56)
        struct.pack_into('<I', raw, 0, 2)
        raw[4:8] = b'\x01\x01\0\0'
        for index, name in enumerate((b'first', b'second')):
            record = 16 + index * 32
            raw[record:record + len(name)] = name
            raw[record + 16:record + 20] = b'txc\0'
            struct.pack_into('<III', raw, record + 20, 3, 0x50, 0)
        with self.assertRaisesRegex(ValueError, 'overlapping'):
            ui_bundle.parse(bytes(raw))


if __name__ == '__main__':
    unittest.main()
