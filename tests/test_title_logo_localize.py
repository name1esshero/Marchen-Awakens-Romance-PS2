import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import rtx3
import title_logo_localize


class TitleLogoLocalizeTests(unittest.TestCase):
    def test_cli_path_guard_keeps_japanese_baselines_read_only(self):
        with self.assertRaisesRegex(ValueError, 'read-only'):
            title_logo_localize._validate_paths(
                Path('source_jp.tga'), Path('localized_eng.tga'))
        with self.assertRaisesRegex(ValueError, 'read-only'):
            title_logo_localize._validate_paths(
                Path('source_eng.tga'), Path('output_jp.tga'))

    def test_build_clears_only_requested_regions_and_places_logo(self):
        base_rgba = bytes((0, 0, 255, 255)) * 16
        base = rtx3.write_tga(4, 4, base_rgba)
        logo = rtx3.write_png(1, 1, bytes((240, 80, 20, 255)))
        layer, output, report = title_logo_localize.build(
            base, logo, [(1, 1, 2, 2)],
            [(1, 1, 2, 2, 'color')])

        self.assertEqual(rtx3.read_tga(base), (4, 4, base_rgba))
        self.assertEqual(rtx3.tga_dimensions(output), (4, 4))
        _, _, actual = rtx3.read_tga(output)
        self.assertEqual(actual[0:4], bytes((0, 0, 255, 255)))
        self.assertEqual(actual[(1 * 4 + 1) * 4:(1 * 4 + 1) * 4 + 4],
                         bytes((240, 80, 20, 255)))
        self.assertEqual(actual[(3 * 4 + 3) * 4:(3 * 4 + 3) * 4 + 4],
                         bytes((0, 0, 255, 255)))
        self.assertEqual(title_logo_localize.graphics_compose.decode_png(layer)[:2],
                         (4, 4))
        self.assertEqual(report['clear_regions'], [[1, 1, 2, 2]])
        self.assertEqual(report['placements'], [[1, 1, 2, 2, 'color']])
        _, rebuilt, _ = title_logo_localize.build(
            output, logo, [(1, 1, 2, 2)], [(1, 1, 2, 2, 'color')])
        self.assertEqual(rebuilt, output)

    def test_gray_placement_preserves_alpha_and_rejects_out_of_bounds(self):
        base = rtx3.write_tga(2, 1, bytes((0, 0, 0, 0)) * 2)
        logo = rtx3.write_png(1, 1, bytes((255, 0, 0, 128)))
        _, output, _ = title_logo_localize.build(
            base, logo, [(0, 0, 1, 1)], [(0, 0, 1, 1, 'gray')])
        _, _, actual = rtx3.read_tga(output)
        self.assertEqual(actual[:4], bytes((76, 76, 76, 128)))
        with self.assertRaisesRegex(ValueError, 'outside'):
            title_logo_localize.build(
                base, logo, [(0, 0, 1, 1)], [(1, 0, 2, 1, 'color')])


if __name__ == '__main__':
    unittest.main()
