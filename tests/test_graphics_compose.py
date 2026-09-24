import binascii
import struct
import sys
from pathlib import Path
import unittest
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import graphics_compose
import rtx3


def _chunk(kind, data):
    body = kind + data
    return struct.pack('>I', len(data)) + body + struct.pack(
        '>I', binascii.crc32(body) & 0xffffffff)


def _paeth(left, above, upper_left):
    estimate = left + above - upper_left
    distances = (abs(estimate - left), abs(estimate - above),
                 abs(estimate - upper_left))
    return (left, above, upper_left)[distances.index(min(distances))]


def png_rgba(rows, filters=None):
    height, width = len(rows), len(rows[0]) // 4
    filters = filters or [0] * height
    scanlines = bytearray()
    previous = bytes(width * 4)
    for row, filter_type in zip(rows, filters):
        encoded = bytearray(len(row))
        for i, value in enumerate(row):
            left = row[i - 4] if i >= 4 else 0
            above = previous[i]
            upper_left = previous[i - 4] if i >= 4 else 0
            if filter_type == 0:
                predictor = 0
            elif filter_type == 1:
                predictor = left
            elif filter_type == 2:
                predictor = above
            elif filter_type == 3:
                predictor = (left + above) // 2
            else:
                predictor = _paeth(left, above, upper_left)
            encoded[i] = (value - predictor) & 0xff
        scanlines.append(filter_type)
        scanlines.extend(encoded)
        previous = row
    header = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    return (graphics_compose.PNG_SIGNATURE + _chunk(b'IHDR', header)
            + _chunk(b'IDAT', zlib.compress(scanlines))
            + _chunk(b'IEND', b''))


class GraphicsComposeTests(unittest.TestCase):
    def test_png_decoder_reverses_all_standard_filters(self):
        rows = [bytes((value, value + 1, value + 2, 255,
                       value + 3, value + 4, value + 5, 200))
                for value in (10, 30, 50, 70, 90)]
        png = png_rgba(rows, [0, 1, 2, 3, 4])
        expected = b''.join(rows)
        self.assertEqual(graphics_compose.decode_png(png), (2, 5, expected))

    def test_png_decoder_rejects_bad_crc_palette_and_interlacing(self):
        valid = png_rgba([bytes((1, 2, 3, 255))])
        bad_crc = bytearray(valid)
        bad_crc[29] ^= 1
        with self.assertRaisesRegex(ValueError, 'checksum'):
            graphics_compose.decode_png(bytes(bad_crc))

        palette = (graphics_compose.PNG_SIGNATURE
                   + _chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 3, 0, 0, 0))
                   + _chunk(b'IDAT', zlib.compress(b'\x00\x00'))
                   + _chunk(b'IEND', b''))
        with self.assertRaisesRegex(ValueError, 'must be 8-bit non-interlaced'):
            graphics_compose.decode_png(palette)

    def test_alpha_threshold_removes_transparent_noise_before_crop(self):
        rgba = bytearray(5 * 5 * 4)
        rgba[3] = 16
        for y in range(1, 4):
            for x in range(1, 4):
                offset = (y * 5 + x) * 4
                rgba[offset:offset + 4] = bytes((255, 255, 255, 255))
        width, height, fitted, bounds = graphics_compose.fit_overlay(
            5, 5, rgba, 3, 3, alpha_threshold=128)
        self.assertEqual(bounds, (1, 1, 4, 4))
        self.assertEqual((width, height), (3, 3))
        self.assertEqual(fitted, bytes((255, 255, 255, 255)) * 9)

    def test_compose_clears_old_text_region_but_preserves_other_pixels(self):
        width, height = 6, 4
        base_rgba = bytes((20, 30, 40, 255)) * (width * height)
        base = rtx3.write_tga(width, height, base_rgba)
        overlay = png_rgba([
            bytes((240, 10, 20, 255)) * 2,
            bytes((240, 10, 20, 255)) * 2,
        ])
        out_width, out_height, result, report = graphics_compose.compose(
            base, overlay, region=(2, 1, 2, 2), clear_region=(1, 1, 4, 2))
        self.assertEqual((out_width, out_height), (width, height))
        self.assertEqual(rtx3.tga_dimensions(result), (width, height))
        decoded = rtx3.read_tga(result)[2]
        pixel = lambda x, y: decoded[(y * width + x) * 4:(y * width + x + 1) * 4]
        self.assertEqual(pixel(0, 0), bytes((20, 30, 40, 255)))
        self.assertEqual(pixel(1, 1), bytes(4))
        self.assertEqual(pixel(2, 1), bytes((240, 10, 20, 255)))
        self.assertEqual(pixel(5, 3), bytes((20, 30, 40, 255)))
        self.assertEqual(report['clear_region'], [1, 1, 4, 2])


if __name__ == '__main__':
    unittest.main()
