import struct
import unittest

from tools import at3


def fixture(name='title_marh_jp.tga', body=b'opaque'):
    header = b'AT  ' + struct.pack('<III', 3, 1, at3.TEXTURE_NAME_RECORD_SIZE)
    record = name.encode('ascii') + b'\0'
    record += bytes(at3.TEXTURE_NAME_RECORD_SIZE - len(record))
    return header + record + struct.pack('<I', 0) + body


def node(name, opaque_data):
    encoded = name.encode('cp932')
    slot = encoded + b'\0' + bytes(at3.NODE_NAME_SLOT_SIZE - len(encoded) - 1)
    return struct.pack('<I', at3.NODE_NAME_SLOT_SIZE) + slot + opaque_data


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
        self.assertIsNone(parsed['node_envelope'])
        self.assertEqual(at3.rebuild(parsed), fixture())

    def test_node_envelope_roundtrips_and_supports_fixed_slot_name_edit(self):
        opaque_data = bytes(range(at3.NODE_FIXED_REGION_SIZE)) + bytes(
            2 * at3.NODE_REPEAT_BLOCK_SIZE)
        preamble = b'NODE' + struct.pack('<I', 1)
        raw = fixture(body=preamble + node('Scene00', opaque_data))
        parsed = at3.parse(raw)
        envelope = parsed['node_envelope']
        self.assertEqual(envelope['state'], 'validated_envelope')
        self.assertEqual(envelope['preamble_hex'], preamble.hex())
        self.assertEqual(envelope['record_count'], 1)
        self.assertEqual(envelope['nodes'][0]['name'], 'Scene00')
        self.assertEqual(envelope['nodes'][0]['opaque_repeat_block_count'], 2)
        self.assertEqual(at3.rebuild(parsed), raw)

        parsed['node_envelope']['nodes'][0]['name'] = 'Scene01'
        rebuilt = at3.rebuild(parsed)
        self.assertEqual(len(rebuilt), len(raw))
        self.assertEqual(at3.parse(rebuilt)['node_envelope']['nodes'][0]['name'], 'Scene01')
        name_start = len(raw) - at3.NODE_NAME_PREFIX_SIZE - at3.NODE_NAME_SLOT_SIZE - len(opaque_data)
        self.assertEqual(rebuilt[:name_start], raw[:name_start])
        self.assertEqual(rebuilt[name_start + 4 + at3.NODE_NAME_SLOT_SIZE:], raw[name_start + 4 + at3.NODE_NAME_SLOT_SIZE:])

    def test_unsupported_node_extent_stays_opaque_and_roundtrips(self):
        preamble = b'\0' * 4
        bad_node = node('Layer00', b'not a validated node extent')
        raw = fixture(body=preamble + bad_node)
        parsed = at3.parse(raw)
        self.assertIsNone(parsed['node_envelope'])
        self.assertEqual(parsed['opaque_post_table_hex'], raw[0x54:].hex())
        self.assertEqual(at3.rebuild(parsed), raw)

    def test_fixed_slot_builder_rejects_growth_and_reference_count_changes(self):
        opaque_data = bytes(at3.NODE_FIXED_REGION_SIZE)
        raw = fixture(body=b'\0' * 4 + node('Scene00', opaque_data))
        parsed = at3.parse(raw)
        parsed['node_envelope']['nodes'][0]['name'] = 'x' * 64
        with self.assertRaisesRegex(ValueError, 'must encode'):
            at3.rebuild(parsed)
        parsed = at3.parse(raw)
        parsed['node_envelope']['nodes'][0]['opaque_data_hex'] += bytes(
            at3.NODE_REPEAT_BLOCK_SIZE).hex()
        with self.assertRaisesRegex(ValueError, 'record growth or shrinkage'):
            at3.rebuild(parsed)
        parsed = at3.parse(raw)
        parsed['references'].clear()
        with self.assertRaisesRegex(ValueError, 'reference count changes'):
            at3.rebuild(parsed)

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
