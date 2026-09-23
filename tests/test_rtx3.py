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
                self.assertEqual(rtx3.tga_dimensions(tga), (width, height))
                self.assertEqual(rtx3.encode_tga(raw, tga), raw)

    def test_tga_dimensions_validates_extent_without_pixel_decode(self):
        tga = rtx3.write_tga(2, 1, bytes((255, 0, 0, 255, 0, 255, 0, 255)))
        self.assertEqual(rtx3.tga_dimensions(tga), (2, 1))
        with self.assertRaisesRegex(ValueError, 'pixel extent'):
            rtx3.tga_dimensions(tga[:-1])

    def test_stored_order_preview_skips_pixel_and_palette_mapping(self):
        raw = bytearray(fixture(19, 128, 64))
        info = rtx3.parse(raw)
        raw[info['pixels_offset']:info['pixels_offset'] + info['pixel_size']] = bytes([8]) * info['pixel_size']
        palette = info['palette_offset']
        raw[palette + 8 * 4:palette + 9 * 4] = bytes((11, 22, 33, 64))
        raw[palette + 16 * 4:palette + 17 * 4] = bytes((44, 55, 66, 64))
        stored = rtx3.decode_stored_order_rgba(raw)
        mapped_linear = rtx3.decode_rgba(raw)
        legacy = rtx3.decode_legacy_rgba(raw)
        self.assertEqual(stored[2][:4], bytes((11, 22, 33, 64)))
        self.assertEqual(mapped_linear[2][:4], bytes((44, 55, 66, 128)))
        self.assertEqual(legacy[2][:4], bytes((44, 55, 66, 128)))

    def test_default_expands_gs_alpha_to_tga_range(self):
        raw = bytearray(fixture(19, 128, 64))
        info = rtx3.parse(raw)
        palette = info['palette_offset']
        raw[palette + 3] = 0
        raw[palette + 4 + 3] = 64
        raw[palette + 8 + 3] = 128
        raw[info['pixels_offset']:info['pixels_offset'] + 3] = bytes((0, 1, 2))
        _, _, decoded = rtx3.decode_rgba(raw)
        self.assertEqual(decoded[3], 0)
        self.assertEqual(decoded[7], 128)
        self.assertEqual(decoded[11], 255)

    def test_stored_order_indexed_import_preserves_raw_layout(self):
        for psm, index in ((19, 100), (20, 7)):
            with self.subTest(psm=psm):
                raw = bytearray(fixture(psm, 128, 64))
                info = rtx3.parse(raw)
                if psm == 19:
                    # A color edit must not collapse untouched pixels that use
                    # duplicate palette entries to the first equal entry.
                    palette = info['palette_offset']
                    raw[palette + 200 * 4:palette + 201 * 4] = raw[palette:palette + 4]
                raw = bytes(raw)
                width, height, rgba = rtx3.decode_stored_order_rgba(raw)
                tga = rtx3.write_tga(width, height, rgba)
                self.assertEqual(rtx3.encode_stored_order_tga(raw, tga), raw)

                changed = bytearray(rgba)
                changed[:4] = bytes((index, index, index, 0x80))
                rebuilt = rtx3.encode_stored_order_tga(
                    raw, rtx3.write_tga(width, height, changed))
                self.assertEqual(rtx3.decode_stored_order_rgba(rebuilt),
                                 (width, height, bytes(changed)))
                expected = bytearray(raw)
                if psm == 19:
                    expected[info['pixels_offset']] = index
                else:
                    expected[info['pixels_offset']] = (
                        expected[info['pixels_offset']] & 0xF0) | index
                self.assertEqual(rebuilt, bytes(expected))

    def test_default_linear_clut_import_keeps_palette_mapping_and_untouched_indices(self):
        raw = bytearray(fixture(19, 128, 64))
        info = rtx3.parse(raw)
        palette = info['palette_offset']
        raw[palette + 200 * 4:palette + 201 * 4] = raw[palette:palette + 4]
        raw = bytes(raw)
        width, height, rgba = rtx3.decode_rgba(raw)
        self.assertEqual(rtx3.encode_tga(raw, rtx3.write_tga(width, height, rgba)), raw)

        mapped_index = 100
        stored_palette_index = rtx3._clut_index(mapped_index, rtx3.PSMT8)
        target_raw = raw[palette + stored_palette_index * 4:
                         palette + (stored_palette_index + 1) * 4]
        target = target_raw[:3] + bytes((min(255, target_raw[3] * 2),))
        changed = bytearray(rgba)
        changed[:4] = target
        rebuilt = rtx3.encode_tga(raw, rtx3.write_tga(width, height, changed))
        expected = bytearray(raw)
        expected[info['pixels_offset']] = mapped_index
        self.assertEqual(rebuilt, bytes(expected))
        self.assertEqual(rtx3.decode_rgba(rebuilt),
                         (width, height, bytes(changed)))

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
