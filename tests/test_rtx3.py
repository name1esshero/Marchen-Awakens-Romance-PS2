import struct
import unittest

from tools import rtx3


def fixture(psm, width, height):
    tw, th = width.bit_length() - 1, height.bit_length() - 1
    tex0 = (psm << 20) | (tw << 26) | (th << 30)
    bpp = {0: 32, 19: 8, 20: 4, 27: 8, 36: 4, 44: 4}[psm]
    pixels = width * height * bpp // 8
    palette = (bytes((i, i, i, 0x80)) for i in range(256 if psm in (19, 27) else 16))
    palette = b''.join(palette) if psm != 0 else b''
    header = bytearray(0x40)
    header[:4] = b'RTX3'
    struct.pack_into('<I', header, 4, 0x40 + pixels + len(palette) - 8)
    struct.pack_into('<Q', header, 8, tex0)
    struct.pack_into('<HHI', header, 0x20, width, height, pixels)
    raw_pixels = bytes((i * 17) & 0xff for i in range(pixels))
    return bytes(header) + raw_pixels + palette


class RTX3Tests(unittest.TestCase):
    def test_indexed_modes_export_tga_and_noop_import_exactly(self):
        for psm, width, height in ((19, 128, 64), (20, 128, 64)):
            with self.subTest(psm=psm):
                raw = fixture(psm, width, height)
                decoded = rtx3.decode_rgba(raw)
                tga = rtx3.write_tga(*decoded)
                self.assertEqual(rtx3.read_tga(tga), decoded)
                self.assertEqual(rtx3.encode_tga(raw, tga), raw)

    def test_stored_order_preview_skips_pixel_and_palette_mapping(self):
        raw = bytearray(fixture(19, 128, 64))
        info = rtx3.parse(raw)
        raw[info['pixels_offset']:info['pixels_offset'] + info['pixel_size']] = bytes([8]) * info['pixel_size']
        palette = info['palette_offset']
        raw[palette + 8 * 4:palette + 9 * 4] = bytes((11, 22, 33, 64))
        raw[palette + 16 * 4:palette + 17 * 4] = bytes((44, 55, 66, 64))
        stored = rtx3.decode_stored_order_rgba(raw)
        decoded = rtx3.decode_rgba(raw)
        self.assertEqual(stored[2][:4], bytes((11, 22, 33, 64)))
        self.assertEqual(decoded[2][:4], bytes((44, 55, 66, 128)))

    def test_high_bit_modes_are_parsed_but_not_guessed(self):
        for psm in (27, 36, 44):
            with self.subTest(psm=psm):
                raw = fixture(psm, 128, 64)
                self.assertEqual(rtx3.parse(raw)['psm'], psm)
                with self.assertRaisesRegex(ValueError, 'storage order is unresolved'):
                    rtx3.decode_rgba(raw)

    def test_psmct32_swizzle_and_noop_import_exactly(self):
        raw = fixture(0, 64, 32)
        decoded = rtx3.decode_rgba(raw)
        self.assertEqual(rtx3.read_tga(rtx3.write_tga(*decoded)), decoded)
        self.assertEqual(rtx3.encode_tga(raw, rtx3.write_tga(*decoded)), raw)

    def test_changed_same_size_tga_reinserts_and_decodes(self):
        raw = fixture(19, 128, 64)
        width, height, rgba = rtx3.decode_rgba(raw)
        changed = bytearray(rgba)
        changed[:4] = bytes((255, 255, 255, 255))
        rebuilt = rtx3.encode_tga(raw, rtx3.write_tga(width, height, changed))
        self.assertEqual(len(rebuilt), len(raw))
        self.assertEqual(rtx3.parse(rebuilt)['width'], width)
        self.assertEqual(rtx3.decode_rgba(rebuilt), (width, height, bytes(changed)))

    def test_dimensions_and_malformed_header_are_rejected(self):
        raw = fixture(19, 128, 64)
        bad = bytearray(rtx3.write_tga(*rtx3.decode_rgba(raw)))
        struct.pack_into('<H', bad, 12, 64)
        del bad[-128 * 64 // 2 * 4:]
        with self.assertRaisesRegex(ValueError, 'dimensions must match'):
            rtx3.encode_tga(raw, bad)
        with self.assertRaisesRegex(ValueError, 'not an RTX3'):
            rtx3.parse(b'not an image')


if __name__ == '__main__':
    unittest.main()
