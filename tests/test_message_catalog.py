import copy
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import message_catalog


class MessageCatalogTests(unittest.TestCase):
    def setUp(self):
        self.document = dict(format='observed-msg-v1', header_hex='0200000011223344', entries=[
            dict(kind=2, key=4, text='保存しますか？'),
            dict(kind=2, key=4, text='上書きしますか？'),
            dict(kind=4, key=9, text='いいえ'),
        ])
        self.catalog = message_catalog.create(self.document)

    def test_stable_ids_preserve_duplicate_keys_and_apply_translation(self):
        rows = self.catalog['entries']
        self.assertNotEqual(rows[0]['id'], rows[1]['id'])
        self.assertEqual(rows[0]['id'], 'msg-k00000002-i00000004-o000')
        self.assertEqual(rows[1]['id'], 'msg-k00000002-i00000004-o001')
        rows[0]['translation'] = 'Save data?'
        rows[0]['status'] = 'translated'
        rebuilt = message_catalog.apply(self.document, self.catalog)
        self.assertEqual(rebuilt['entries'][0]['text'], 'Save data?')
        self.assertEqual(rebuilt['entries'][1]['text'], '上書きしますか？')
        self.assertEqual(self.document['entries'][0]['text'], '保存しますか？')

    def test_source_drift_and_inconsistent_catalog_are_rejected(self):
        changed = copy.deepcopy(self.document)
        changed['entries'][0]['text'] = '違う原文'
        with self.assertRaisesRegex(ValueError, 'source hash'):
            message_catalog.apply(changed, self.catalog)
        invalid = copy.deepcopy(self.catalog)
        invalid['entries'][1]['id'] = invalid['entries'][0]['id']
        with self.assertRaisesRegex(ValueError, 'IDs'):
            message_catalog.apply(self.document, invalid)


if __name__ == '__main__':
    unittest.main()
