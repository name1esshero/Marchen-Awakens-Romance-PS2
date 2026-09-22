import hashlib
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from reconstruct_elf import export_sources, rebuild, selected_sections
from test_bootstrap import elf


class ReconstructionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.sources = Path(self.temp.name) / 'sources'
        self.reference = bytes(elf())
        self.digest = hashlib.sha256(self.reference).hexdigest()
        self.manifest = export_sources(self.reference, ['.text'], self.sources, self.digest)

    def write_manifest(self):
        (self.sources / 'layout.json').write_text(json.dumps(self.manifest))

    def test_round_trip_and_object_changes_propagate(self):
        self.assertEqual(rebuild(self.sources, elf()), self.reference)
        # A changed instruction must reach the output, not be replaced by original bytes.
        changed = rebuild(self.sources, elf(b'87654321'))
        self.assertEqual(changed[64:72], b'87654321')
        self.assertNotEqual(changed, self.reference)

    def test_wrong_reference_hash_and_existing_destination(self):
        with self.assertRaises(ValueError):
            export_sources(self.reference, ['.text'], self.sources, '0' * 64)
        with self.assertRaises(FileExistsError):
            export_sources(self.reference, ['.text'], self.sources, self.digest)

    def test_gap_overlap_and_incomplete_coverage(self):
        original = json.loads(json.dumps(self.manifest))
        for delta in (-1, 1):
            self.manifest = json.loads(json.dumps(original))
            self.manifest['regions'][1]['offset'] += delta
            self.write_manifest()
            with self.assertRaises(ValueError):
                rebuild(self.sources, elf())
        self.manifest = original
        self.manifest['regions'].pop()
        self.write_manifest()
        with self.assertRaises(ValueError):
            rebuild(self.sources, elf())

    def test_wrong_object_size_and_missing_section(self):
        with self.assertRaises(ValueError):
            rebuild(self.sources, elf(b'short'))
        data = elf()
        data[81:86] = b'.none'
        with self.assertRaises(ValueError):
            rebuild(self.sources, data)

    def test_hex_size_and_path_escape(self):
        region = self.manifest['regions'][0]
        (self.sources / region['source']).write_text('00')
        with self.assertRaises(ValueError):
            rebuild(self.sources, elf())
        region['source'] = '../outside.hex'
        self.write_manifest()
        with self.assertRaises(ValueError):
            rebuild(self.sources, elf())

    def test_reject_executable_as_object(self):
        data = elf()
        struct.pack_into('<H', data, 16, 2)
        with self.assertRaises(ValueError):
            rebuild(self.sources, data)

    def test_reject_relocations_to_selected_section(self):
        # Append a fourth section header describing a relocation against .text.
        data = elf()
        data.extend(b'\0' * 32)
        struct.pack_into('<H', data, 48, 4)
        struct.pack_into('<10I', data, 248, 0, 9, 0, 0, 104, 8, 0, 1, 4, 8)
        with self.assertRaisesRegex(ValueError, 'unapplied relocations'):
            rebuild(self.sources, data)

    def test_missing_duplicate_and_ambiguous_selections(self):
        for names in ([], ['.text', '.text'], ['.missing']):
            with self.assertRaises(ValueError):
                selected_sections(elf(), names)
        data = elf()
        data.extend(b'\0' * 32)
        struct.pack_into('<H', data, 48, 4)
        struct.pack_into('<10I', data, 248, 1, 1, 6, 0, 64, 8, 0, 0, 4, 0)
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            selected_sections(data, ['.text'])


if __name__ == '__main__':
    unittest.main()
