import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from linkonce_inventory import classify


class LinkonceInventoryTests(unittest.TestCase):
    def test_member_function(self):
        kind, cls, extra = classify('GetNearClipPlane__7CCamera')
        self.assertEqual((kind, cls), ('member', 'CCamera'))
        self.assertEqual(extra['method'], 'GetNearClipPlane')
        self.assertEqual(extra['raw_params'], '')

    def test_const_member_function_with_encoded_params(self):
        kind, cls, extra = classify('GetViewAngle__C7CCamera')
        self.assertEqual((kind, cls), ('const_member', 'CCamera'))
        kind, cls, extra = classify('SetFogMode__7CCamerai')
        self.assertEqual((kind, cls, extra['raw_params']), ('member', 'CCamera', 'i'))

    def test_typeinfo(self):
        self.assertEqual(classify('__tf8CCamera2'), ('typeinfo', 'CCamera2', {}))

    def test_constructor(self):
        kind, cls, extra = classify('__14FireStorm_Ptcl')
        self.assertEqual((kind, cls), ('constructor', 'FireStorm_Ptcl'))

    def test_destructor(self):
        self.assertEqual(classify('_$_9CColGroup'), ('destructor', 'CColGroup', {}))

    def test_unparsed_when_class_length_does_not_fit(self):
        kind, cls, extra = classify('Weird__99Short')
        self.assertEqual((kind, cls), ('unparsed', None))

    def test_unparsed_template_shape_left_unclassified(self):
        # Template instantiations ("t12CStringStack1i_256_") are not decoded
        # by this heuristic; they must not be silently misattributed.
        kind, cls, extra = classify('GetBuffer__Ct12CStringStack1i_256_')
        self.assertEqual(kind, 'unparsed')


if __name__ == '__main__':
    unittest.main()
