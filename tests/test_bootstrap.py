import io
import struct
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from bootstrap import dual, elf_sections, inventory, read_at, record
from compare_sections import compare


def both(value, width):
    return value.to_bytes(width, 'little') + value.to_bytes(width, 'big')


def directory_record(name, lba=20, size=2048, flags=2):
    data = bytearray(33 + len(name) + (len(name) % 2 == 0))
    data[0] = len(data)
    data[2:10] = both(lba, 4)
    data[10:18] = both(size, 4)
    data[25] = flags
    data[28:32] = both(1, 2)
    data[32] = len(name)
    data[33:33 + len(name)] = name
    return data


def iso(name=b'A;1', lba=21, flags=0):
    data = bytearray(22 * 2048)
    pvd = memoryview(data)[16 * 2048:17 * 2048]
    pvd[:7] = b'\x01CD001\x01'
    pvd[80:88] = both(22, 4)
    pvd[120:124] = both(1, 2)
    pvd[124:128] = both(1, 2)
    pvd[128:132] = both(2048, 2)
    pvd[156:190] = directory_record(b'\0')
    data[17 * 2048:17 * 2048 + 7] = b'\xffCD001\x01'
    root = directory_record(b'\0') + directory_record(b'\1')
    root += directory_record(name, lba, 4, flags)
    data[20 * 2048:20 * 2048 + len(root)] = root
    data[21 * 2048:21 * 2048 + 4] = b'TEST'
    return data


def elf(payload=b'12345678'):
    names = b'\0.text\0.shstrtab\0'
    data = bytearray(256)
    data[:7] = b'\x7fELF\x01\x01\x01'
    struct.pack_into('<HHIIIIIHHHHHH', data, 16,
                     1, 8, 1, 0, 0, 128, 0, 52, 0, 0, 40, 3, 2)
    data[64:64 + len(payload)] = payload
    data[80:80 + len(names)] = names
    struct.pack_into('<10I', data, 168, 1, 1, 6, 0, 64, len(payload), 0, 0, 4, 0)
    struct.pack_into('<10I', data, 208, 7, 3, 0, 0, 80, len(names), 0, 0, 1, 0)
    return data


class BootstrapTests(unittest.TestCase):
    def test_iso_inventory(self):
        data = iso()
        result = inventory(io.BytesIO(data), len(data))
        self.assertEqual(result['entries'][0]['path'], 'A;1')
        self.assertEqual(result['entries'][0]['prefix_hex'], b'TEST'.hex())

    def test_bad_iso_extents_names_and_cycles(self):
        for data in (iso(lba=99), iso(name=b'..'), iso(name=b'A/B'),
                     iso(lba=20, flags=2), iso(flags=128)):
            with self.subTest(), self.assertRaises(ValueError):
                inventory(io.BytesIO(data), len(data))

    def test_truncation(self):
        with self.assertRaises(ValueError):
            read_at(io.BytesIO(b'a'), 0, 2)
        with self.assertRaises(ValueError):
            elf_sections(elf()[:200])

    def test_dual_endian_mismatch(self):
        with self.assertRaises(ValueError):
            dual(b'\x01\x00\x00\x02', 0, 2)

    def test_record_length(self):
        with self.assertRaises(ValueError):
            record(b'\x22' * 12)

    def test_elf_inventory(self):
        result = elf_sections(elf())
        self.assertEqual(result['machine'], 8)
        self.assertEqual(result['sections'][1]['name'], '.text')

    def test_compare_equal_and_changed(self):
        self.assertEqual(compare(elf(), elf(), ['.text']), 8)
        with self.assertRaises(ValueError):
            compare(elf(), elf(b'12345679'), ['.text'])
        with self.assertRaises(KeyError):
            compare(elf(), elf(), ['.missing'])
        with self.assertRaises(ValueError):
            compare(elf(), elf(), [])


if __name__ == '__main__':
    unittest.main()
