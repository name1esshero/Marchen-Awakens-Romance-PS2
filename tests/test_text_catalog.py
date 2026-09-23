import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import text_catalog


class TextCatalogTests(unittest.TestCase):
    def test_roundtrip_and_edit_preserve_tabs_blank_cells_and_crlf(self):
        raw = 'ID\tギンタ\t\r\n02\tスノウ\tquote\r\n'.encode('cp932')
        catalog = text_catalog.create(raw, 'disc!/CardList.txt', [1, 2], id_column=0)
        self.assertEqual(text_catalog.apply(raw, catalog), raw)
        catalog['rows'][0]['translations']['1'] = 'Ginta'
        catalog['rows'][1]['translations']['1'] = 'Snow'
        rebuilt = text_catalog.apply(raw, catalog)
        self.assertEqual(rebuilt, b'ID\tGinta\t\r\n02\tSnow\tquote\r\n')

    def test_reject_stale_rows_duplicate_ids_and_unencodable_text(self):
        raw = 'ID\tギンタ\r\n'.encode('cp932')
        catalog = text_catalog.create(raw, 'disc!/CardList.txt', [1], id_column=0)
        with self.assertRaisesRegex(ValueError, 'source hash'):
            text_catalog.apply(raw + b'\r\n', catalog)
        invalid = dict(catalog)
        invalid['rows'] = [dict(catalog['rows'][0])]
        invalid['rows'][0]['translations'] = {'1': 'Ginta ☃'}
        with self.assertRaisesRegex(ValueError, 'not CP932-encodable'):
            text_catalog.validate(invalid)
        with self.assertRaisesRegex(ValueError, 'duplicate stable row ID'):
            text_catalog.create('ID\tA\r\nID\tB\r\n'.encode(),
                                'disc!/CardList.txt', [1], id_column=0)


if __name__ == '__main__':
    unittest.main()
