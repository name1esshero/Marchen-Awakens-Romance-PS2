import struct
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import bpe


class BpeTests(unittest.TestCase):
    def test_identity_encoder_roundtrips_block_boundaries(self):
        for size in (0, 1, 255, 0xFFFF, 0x10000, 0x10002):
            raw = bytes(i & 0xff for i in range(size))
            packed = bpe.encode(raw)
            self.assertEqual(bpe.decode(packed), raw)
            self.assertEqual(struct.unpack_from('<III', packed, 4)[2], size)

    def test_decode_rejects_bad_wrapper_payload_and_expansion(self):
        packed = bytearray(bpe.encode(b'asset'))
        with self.assertRaisesRegex(ValueError, 'not an observed'):
            bpe.decode(b'NOPE' + packed[4:])
        with self.assertRaisesRegex(ValueError, 'payload size'):
            bpe.decode(packed[:-1])
        struct.pack_into('<I', packed, 12, 4)
        with self.assertRaisesRegex(ValueError, 'exceeds declared'):
            bpe.decode(packed)

    def test_decode_rejects_cyclic_expansion_table(self):
        # One block; code 0 maps to pair (1, 0), which recursively refers to 0.
        table = bytes((1, 1, 0, 0, 0, 255, 130, 254))
        payload = table + b'\x00\x01\x00'
        raw = bpe.MAGIC + struct.pack('<III', 256, len(payload), 10000) + payload
        with self.assertRaisesRegex(ValueError, 'stack exceeds'):
            bpe.decode(raw)


if __name__ == '__main__':
    unittest.main()
