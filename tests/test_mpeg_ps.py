import unittest

from tools import mpeg_ps


def packet(stream_id, payload):
    return (b'\x00\x00\x01' + bytes((stream_id,)) +
            len(payload).to_bytes(2, 'big') + payload)


def fixture():
    # Corpus-observed MPEG-1 pack header with all marker bits set.
    raw = bytearray(b'\x00\x00\x01\xba\x21\x00\x01\x00\x03\x80\x6b\xeb')
    raw.extend(packet(0xBB, b'\x80\x6b\xeb\x06\x20\xff\xc0\xc0\x04'))
    raw.extend(packet(0xC0, b'\x40\x04\x21\0\1\0\1\x80\0'))
    raw.extend(packet(0xE0, b'\x60\x2e\x31\0\1\0\1\x11\0\1\0\1\0\0\1\xb3'))
    fill_size = 2048 - len(raw) - 6
    if fill_size < 0:
        raise AssertionError('fixture packets exceed one sector')
    raw.extend(packet(0xBE, b'\xff' * fill_size))
    if len(raw) != 2048:
        raise AssertionError('fixture first sector is not exactly full')
    raw.extend(mpeg_ps.PROGRAM_END)
    raw.extend(b'\xff' * (mpeg_ps.SECTOR_SIZE - 4))
    return bytes(raw)


class MpegProgramStreamTests(unittest.TestCase):
    def test_sectorized_program_stream_parses_and_rebuilds_exactly(self):
        raw = fixture()
        parsed = mpeg_ps.parse(raw)
        self.assertEqual(parsed['format'], 'MPEG-1 program stream (observed sectorized variant)')
        self.assertEqual(parsed['sector_count'], 2)
        self.assertEqual(parsed['pack_header_count'], 1)
        self.assertEqual(parsed['packet_count'], 4)
        self.assertEqual(parsed['packet_counts_by_stream_id'], {
            '0xbb': 1, '0xbe': 1, '0xc0': 1, '0xe0': 1,
        })
        self.assertEqual(parsed['program_end_offset'], 2048)
        self.assertEqual(parsed['terminal_ff_bytes'], 2044)
        self.assertEqual(parsed['structural_bytes'], len(raw))
        self.assertEqual(mpeg_ps.rebuild(parsed, raw), raw)

    def test_rejects_truncated_or_zero_length_pes_packet(self):
        raw = bytearray(fixture())
        raw[12 + 4:12 + 6] = b'\0\0'
        with self.assertRaisesRegex(ValueError, 'zero-length MPEG packet'):
            mpeg_ps.parse(bytes(raw))

    def test_rejects_invalid_pack_marker_and_sector_alignment(self):
        raw = bytearray(fixture())
        raw[4] &= 0xFE
        with self.assertRaisesRegex(ValueError, 'marker bits'):
            mpeg_ps.parse(bytes(raw))

        raw = bytearray(fixture())
        raw[0] = 0x01
        with self.assertRaisesRegex(ValueError, 'expected MPEG pack/packet start'):
            mpeg_ps.parse(bytes(raw))

    def test_rejects_non_ff_terminal_sector(self):
        raw = bytearray(fixture())
        raw[-1] = 0
        with self.assertRaisesRegex(ValueError, '0xff trailer'):
            mpeg_ps.parse(bytes(raw))

    def test_rejects_packet_that_crosses_sector_boundary(self):
        raw = bytearray(fixture())
        # Extend the final padding PES's declared body
        # beyond the first sector while leaving the program end code in place.
        # Locate it from the packet sequence instead of depending on fill math.
        cursor = 12
        while raw[cursor:cursor + 4] != b'\x00\x00\x01\xbe':
            cursor += 6 + int.from_bytes(raw[cursor + 4:cursor + 6], 'big')
        length = int.from_bytes(raw[cursor + 4:cursor + 6], 'big')
        raw[cursor + 4:cursor + 6] = (length + 1).to_bytes(2, 'big')
        with self.assertRaisesRegex(ValueError, 'crosses its sector boundary'):
            mpeg_ps.parse(bytes(raw))


if __name__ == '__main__':
    unittest.main()
