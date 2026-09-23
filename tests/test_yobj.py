import struct
import unittest

from tools import yobj


def fixture(prefix=b''):
    header_base = len(prefix) + 8
    pof0_offset = 192
    pof0_absolute = header_base + pof0_offset
    raw = bytearray(pof0_absolute)
    raw[:len(prefix)] = prefix
    yobj_offset = len(prefix)
    raw[yobj_offset:yobj_offset + 4] = b'YOBJ'
    raw[yobj_offset + 4:yobj_offset + 8] = struct.pack('<I', pof0_offset)
    raw[header_base + 4:header_base + 8] = struct.pack('<I', pof0_offset)
    raw[header_base + 0x1C:header_base + 0x20] = struct.pack('<I', 64)
    raw[header_base + 0x24:header_base + 0x28] = struct.pack('<I', 120)
    pointer_slots = [header_base + 0x1C, header_base + 72, header_base + 96]
    for slot, value in zip(pointer_slots, (64, 128, 144)):
        raw[slot:slot + 4] = struct.pack('<I', value)
    payload = yobj._encode_pof0(pointer_slots, header_base)
    raw.extend(b'POF0' + struct.pack('<I', len(payload)) + payload)
    return bytes(raw)


class YOBJTests(unittest.TestCase):
    def test_standard_yobj_envelope_decodes_and_rebuilds_exactly(self):
        raw = fixture()
        parsed = yobj.parse(raw)
        self.assertEqual(parsed['variant'], 'YOBJ')
        self.assertEqual(parsed['header_base'], 8)
        self.assertEqual(parsed['pof0_reference_slots'], [36, 80, 104])
        self.assertEqual(parsed['pof0_reference_count'], 3)
        self.assertEqual(yobj.rebuild(parsed), raw)

    def test_dumy_prefixed_yobj_envelope_uses_shifted_header_base(self):
        raw = fixture(b'DUMY\0\0\0\0')
        parsed = yobj.parse(raw)
        self.assertEqual(parsed['variant'], 'DUMY_YOBJ')
        self.assertEqual(parsed['header_base'], 16)
        self.assertEqual(parsed['pof0_reference_slots'], [44, 88, 112])
        self.assertEqual(yobj.rebuild(parsed), raw)

    def test_rebuild_accepts_same_size_opaque_body_edit(self):
        raw = fixture()
        parsed = yobj.parse(raw)
        body = bytearray.fromhex(parsed['opaque_body_hex'])
        body[-1] ^= 0x55
        parsed['opaque_body_hex'] = body.hex()
        rebuilt = yobj.rebuild(parsed)
        self.assertEqual(len(rebuilt), len(raw))
        self.assertNotEqual(rebuilt, raw)
        self.assertEqual(yobj.parse(rebuilt)['pof0_reference_slots'], [36, 80, 104])

    def test_rejects_bad_pof0_and_unsupported_body_growth(self):
        raw = fixture()
        malformed = bytearray(raw)
        malformed[-4:] = b'\x00\x00\x00\x01'
        with self.assertRaisesRegex(ValueError, 'nonzero invalid tag'):
            yobj.parse(malformed)

        parsed = yobj.parse(raw)
        parsed['opaque_body_hex'] += '00000000'
        with self.assertRaisesRegex(ValueError, 'POF0 offset does not point to POF0'):
            yobj.rebuild(parsed)

    def test_rejects_pointer_targets_outside_the_model_envelope(self):
        raw = bytearray(fixture())
        raw[80:84] = struct.pack('<I', 0xFFFFFFFF)
        with self.assertRaisesRegex(ValueError, 'POF0-listed value'):
            yobj.parse(raw)


if __name__ == '__main__':
    unittest.main()
