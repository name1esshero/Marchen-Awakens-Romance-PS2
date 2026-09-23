import struct
import unittest

from tools import at3


def fixture(name='title_marh_jp.tga', body=b'opaque'):
    header = b'AT  ' + struct.pack('<III', 3, 1, at3.TEXTURE_NAME_RECORD_SIZE)
    record = name.encode('ascii') + b'\0'
    record += bytes(at3.TEXTURE_NAME_RECORD_SIZE - len(record))
    return header + record + struct.pack('<I', 0) + body


class AT3Tests(unittest.TestCase):
    def test_header_and_texture_reference_table(self):
        parsed = at3.parse(fixture())
        self.assertEqual(parsed['field_04'], 3)
        self.assertEqual(parsed['texture_reference_count'], 1)
        self.assertEqual(parsed['reference_record_size'], 64)
        self.assertEqual(parsed['reference_stride'], 68)
        self.assertEqual(parsed['reference_table_end'], 0x54)
        self.assertEqual(parsed['references'][0]['name'], 'title_marh_jp.tga')
        self.assertEqual(parsed['post_table_size'], len(b'opaque'))

    def test_invalid_header_records_and_extents_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'not an AT3'):
            at3.parse(b'wrong header bytes')
        with self.assertRaisesRegex(ValueError, 'record size'):
            at3.parse(b'AT  ' + struct.pack('<III', 3, 1, 32))
        with self.assertRaisesRegex(ValueError, 'exceeds file size'):
            at3.parse(b'AT  ' + struct.pack('<III', 3, 2, 64) + bytes(64))
        malformed = bytearray(fixture())
        malformed[0x10:0x50] = b'X' * 64
        with self.assertRaisesRegex(ValueError, 'no NUL terminator'):
            at3.parse(malformed)


if __name__ == '__main__':
    unittest.main()
