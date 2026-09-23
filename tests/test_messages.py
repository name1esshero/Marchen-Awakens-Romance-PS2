import struct
import sys
import tempfile
from unittest.mock import patch
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import messages


def fixture():
    entries = [(2, 10, '保存しますか？'), (4, 92, 'いいえ')]
    header = bytearray(b'\x02\0\0\0\x12\x34\x56\x78')
    out = bytearray(header + b'\0' * (len(entries) * messages.ENTRY_SIZE))
    for i, (kind, key, text) in enumerate(entries):
        offset = len(out) - messages.HEADER_SIZE
        struct.pack_into('<III', out, messages.HEADER_SIZE + i * messages.ENTRY_SIZE,
                         kind, key, offset)
        out.extend(text.encode('cp932') + b'\0')
    return bytes(out)


class MessageTests(unittest.TestCase):
    def test_extract_build_is_lossless(self):
        original = fixture()
        self.assertEqual(messages.build(messages.parse(original)), original)

    def test_translation_growth_repoints_later_entries(self):
        document = messages.parse(fixture())
        document['entries'][0]['text'] = 'Would you like to save? 保存しますか？'
        rebuilt = messages.build(document)
        parsed = messages.parse(rebuilt)
        self.assertEqual(parsed['entries'][0]['text'], document['entries'][0]['text'])
        self.assertEqual(parsed['entries'][1]['text'], 'いいえ')
        self.assertEqual(parsed['entries'][1]['key'], 92)
        self.assertGreater(len(rebuilt), len(fixture()))

    def test_reject_invalid_extents_nuls_and_unencodable_text(self):
        broken = bytearray(fixture())
        struct.pack_into('<I', broken, 8 + 8, 0xffffffff)
        with self.assertRaises(ValueError):
            messages.parse(bytes(broken))
        document = messages.parse(fixture())
        document['entries'][0]['text'] += '\0hidden'
        with self.assertRaises(ValueError):
            messages.build(document)
        document['entries'][0]['text'] = 'emoji 😀'
        with self.assertRaises(ValueError):
            messages.build(document)
        document['entries'] = [None]
        with self.assertRaises(ValueError):
            messages.build(document)

    def test_cli_extract_and_build(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / 'message.dat'
            editable = Path(d) / 'message.json'
            rebuilt = Path(d) / 'rebuilt.dat'
            source.write_bytes(fixture())
            with patch.object(sys, 'argv', ['messages.py', 'extract', str(source), str(editable)]):
                self.assertEqual(messages.main(), 0)
            with patch.object(sys, 'argv', ['messages.py', 'build', str(editable), str(rebuilt)]):
                self.assertEqual(messages.main(), 0)
            self.assertEqual(rebuilt.read_bytes(), source.read_bytes())


if __name__ == '__main__':
    unittest.main()
