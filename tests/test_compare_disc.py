import hashlib
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from compare_disc import compare


class CompareDiscTests(unittest.TestCase):
    def run_compare(self, original, rebuilt, expected=None):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / 'a', Path(d) / 'b'
            a.write_bytes(original)
            b.write_bytes(rebuilt)
            with patch('compare_disc.CHUNK', 4):
                return compare(a, b, expected or hashlib.sha256(original).hexdigest(), 2)

    def test_equal_and_reference_authentication(self):
        self.assertTrue(self.run_compare(b'abcdefghij', b'abcdefghij')['match'])
        r = self.run_compare(b'abcd', b'abcd', '0' * 64)
        self.assertFalse(r['authenticated'])
        self.assertFalse(r['match'])
        self.assertEqual(r['differing_bytes'], 0)

    def test_chunk_boundaries_and_length(self):
        r = self.run_compare(b'abcdefghij', b'abcXefgYi')
        self.assertEqual(r['differing_bytes'], 3)
        self.assertEqual([e['offset'] for e in r['first_differences']], [3, 7])
        r = self.run_compare(b'abcd', b'abcdef')
        self.assertEqual(r['differing_bytes'], 2)
        self.assertIsNone(r['first_differences'][0]['reference'])
        self.assertFalse(r['match'])

    def test_empty(self):
        self.assertTrue(self.run_compare(b'', b'')['match'])
