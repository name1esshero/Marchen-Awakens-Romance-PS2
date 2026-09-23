import io
from contextlib import redirect_stdout
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import assets
import messages
import bpe
import message_catalog
import text_catalog
from test_bootstrap import iso as make_iso


def pac(payloads):
    data = bytearray(16 + len(payloads) * 32)
    struct.pack_into('<4I', data, 0, len(payloads), 0x101, 0, 16)
    for i, payload in enumerate(payloads):
        p = 16 + i * 32
        data[p:p + 4] = b'test'
        data[p + 16:p + 20] = b'bin\0'
        struct.pack_into('<3I', data, p + 20, len(payload), len(data), 0)
        data.extend(payload)
    data.extend(b'preserved tail')
    return bytes(data)


class AssetsTests(unittest.TestCase):
    def export(self, data, dest):
        s = io.BytesIO(data)
        census = dict(containers={}, leaves=0, extensions={}, unparsed=[])
        assets.export_node(s, 0, len(data), dest, *assets.archive(s, 0, len(data)), census)
        return census

    def test_nested_roundtrip_without_reference(self):
        data = pac([pac([b'hello']), b'\0' * 12, b'xyz'])
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'source'
            self.export(data, root)
            out = Path(d) / 'rebuilt'
            assets.build(root, out)
            self.assertEqual(out.read_bytes(), data)

    def test_growth_propagates_and_updates_table(self):
        data = pac([pac([b'hello']), b'other'])
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'source'
            self.export(data, root)
            (root / '00000.asset/00000.bin').write_bytes(b'long translation' * 20)
            out = Path(d) / 'rebuilt'
            with self.assertRaises(ValueError):
                assets.build(root, out)
            self.assertFalse(out.exists())
            assets.build(root, out, True)
            s = io.BytesIO(out.read_bytes())
            entries = assets.archive(s, 0, out.stat().st_size)[2]
            first = entries[0]
            self.assertGreater(first['offset'], len(data))
            nested = assets.archive(s, first['offset'], first['size'])[2][0]
            s.seek(first['offset'] + nested['offset'])
            self.assertEqual(s.read(nested['size']), b'long translation' * 20)
            s.seek(entries[1]['offset'])
            self.assertEqual(s.read(entries[1]['size']), b'other')

    def test_malformed_table(self):
        b = bytearray(pac([b'hello']))
        struct.pack_into('<I', b, 16 + 24, 0)
        with self.assertRaises(ValueError):
            assets.archive(io.BytesIO(b), 0, len(b))
        with self.assertRaises(ValueError):
            assets.archive(io.BytesIO(b'AFS\0' + struct.pack('<I', 100)), 0, 8)

    def test_unsafe_source_and_incomplete_layout(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'source'
            self.export(pac([b'hello']), root)
            layout = root / 'layout.json'
            m = json.loads(layout.read_text())
            m['pieces'][0]['source'] = '../outside'
            assets.save_json(layout, m)
            with self.assertRaises(ValueError):
                assets.build(root, Path(d) / 'out')

    def test_yfs_directory_mapping(self):
        b = bytearray(120)
        b[:8] = b'YFS\0' + struct.pack('<HH', 1, 1)
        b[8:13] = b'data/'
        struct.pack_into('<HH', b, 68, 1, 0)
        b[72:76] = b'test'
        struct.pack_into('<III', b, 96, 4, 112, 0)
        b[112:116] = b'TEST'
        parsed = assets.archive(io.BytesIO(b), 0, len(b))
        self.assertEqual(parsed[2][0]['name'], 'data/test')
        struct.pack_into('<H', b, 70, 1)
        with self.assertRaises(ValueError):
            assets.archive(io.BytesIO(b), 0, len(b))

    def test_iso_file_growth_updates_directory_and_volume(self):
        data = bytes(make_iso())
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'source'
            stream = io.BytesIO(data)
            _, entries = assets.disc_entries(stream, len(data))
            assets.export_node(stream, 0, len(data), root, 'ISO', 2048, entries,
                               dict(containers={}, leaves=0, extensions={}, unparsed=[]))
            (root / '00000.bin').write_bytes(b'translated' * 400)
            out = Path(d) / 'rebuilt.iso'
            assets.build(root, out, True)
            with out.open('rb') as rebuilt:
                inventory = assets.inventory(rebuilt, out.stat().st_size)
                item = next(e for e in inventory['entries'] if e['path'] == 'A;1')
                self.assertEqual(item['size'], 4000)
                rebuilt.seek(item['lba'] * 2048)
                self.assertEqual(rebuilt.read(item['size']), b'translated' * 400)
                self.assertEqual(inventory['volume_bytes'], out.stat().st_size)

    def test_utf8_translation_grows_cp932_leaf_and_relocates_iso(self):
        data = bytes(make_iso())
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'source'
            stream = io.BytesIO(data)
            _, entries = assets.disc_entries(stream, len(data))
            assets.export_node(stream, 0, len(data), root, 'ISO', 2048, entries,
                               dict(containers={}, leaves=0, extensions={}, unparsed=[]))

            layout_path = root / 'layout.json'
            layout = json.loads(layout_path.read_text())
            leaf = next(p for p in layout['pieces'] if p.get('name') == 'A;1')
            leaf['text_source'] = 'translation.utf8.txt'
            (root / leaf['text_source']).write_text('日本', encoding='utf-8')
            assets.save_json(layout_path, layout)

            translated = 'A much longer translation: 日本語'.encode('utf-8')
            (root / leaf['text_source']).write_bytes(translated)
            out = Path(d) / 'translated.iso'
            assets.build(root, out, True)

            with out.open('rb') as rebuilt:
                inventory = assets.inventory(rebuilt, out.stat().st_size)
                item = next(e for e in inventory['entries'] if e['path'] == 'A;1')
                self.assertEqual(item['size'], len(translated.decode('utf-8').encode('cp932')))
                rebuilt.seek(item['lba'] * 2048)
                self.assertEqual(rebuilt.read(item['size']), translated.decode('utf-8').encode('cp932'))
                self.assertEqual(inventory['volume_bytes'], out.stat().st_size)

    def test_message_translation_workspace_roundtrip_and_pac_relocation(self):
        document = dict(format='observed-msg-v1', header_hex='0100000078563412',
                        entries=[dict(kind=2, key=7, text='保存しますか？'),
                                 dict(kind=4, key=9, text='いいえ')])
        original = pac([messages.build(document)])
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'source'
            self.export(original, root)
            layout_path = root / 'layout.json'
            layout = json.loads(layout_path.read_text())
            member = next(p for p in layout['pieces'] if p.get('name') == 'test.bin')
            member['name'] = 'menu_msg.dat'
            assets.save_json(layout_path, layout)

            with redirect_stdout(io.StringIO()):
                assets.prepare(root, report=None)
            editable = root / '00000.messages.json'
            self.assertTrue(editable.exists())
            untouched = Path(d) / 'untouched.pac'
            assets.build(root, untouched)
            self.assertEqual(untouched.read_bytes(), original)

            catalog = message_catalog.create(messages.parse(messages.build(document)))
            catalog['entries'][0]['translation'] = 'Would you like to save? 保存しますか？'
            catalog['entries'][0]['status'] = 'translated'
            catalog_path = Path(d) / 'messages.catalog.json'
            assets.save_json(catalog_path, catalog)
            modded = Path(d) / 'translated.pac'
            assets.build(root, modded, relocate=True, translations_path=catalog_path)

            with modded.open('rb') as rebuilt:
                entry = assets.archive(rebuilt, 0, modded.stat().st_size)[2][0]
                self.assertGreater(entry['offset'], 0)
                rebuilt.seek(entry['offset'])
                result = messages.parse(rebuilt.read(entry['size']))
            self.assertEqual(result['entries'][0]['text'], catalog['entries'][0]['translation'])
            self.assertEqual(result['entries'][1]['key'], 9)

    def test_text_catalog_translation_reinserts_through_archive(self):
        raw = 'ID\t名前\t\r\n01\tギンタ\t\r\n'.encode('cp932')
        original = pac([raw])
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'source'
            self.export(original, root)
            layout_path = root / 'layout.json'
            layout = json.loads(layout_path.read_text())
            member = next(piece for piece in layout['pieces'] if piece.get('name') == 'test.bin')
            member['name'] = 'CardList.txt'
            assets.save_json(layout_path, layout)
            with redirect_stdout(io.StringIO()):
                assets.prepare(root, report=None)

            catalog = text_catalog.create(raw, 'disc!/CardList.txt', [1], id_column=0)
            catalog['rows'][1]['translations']['1'] = 'Ginta'
            catalog_path = Path(d) / 'card-list.json'
            assets.save_json(catalog_path, catalog)
            output = Path(d) / 'mod.pac'
            assets.build(root, output, relocate=True, text_translations_paths=[catalog_path])
            with output.open('rb') as stream:
                member = assets.archive(stream, 0, output.stat().st_size)[2][0]
                stream.seek(member['offset'])
                rebuilt = stream.read(member['size'])
            self.assertEqual(rebuilt, 'ID\t名前\t\r\n01\tGinta\t\r\n'.encode('cp932'))

    def test_bpe_prepare_preserves_original_and_reinserts_edited_decoded_asset(self):
        original_payload = b'UI structure\0' + bytes(range(64))
        original = bytearray(pac([bpe.encode(original_payload)]))
        original[16 + 16:16 + 20] = b'b\0\0\0'
        original = bytes(original)
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'source'
            self.export(original, root)
            with redirect_stdout(io.StringIO()):
                assets.prepare(root, report=None)

            layout_path = root / 'layout.json'
            leaf = next(piece for piece in json.loads(layout_path.read_text())['pieces']
                        if piece.get('name') == 'test.b')
            decoded_path = root / leaf['bpe_source']
            self.assertEqual(decoded_path.read_bytes(), original_payload)
            untouched = Path(d) / 'untouched.pac'
            assets.build(root, untouched)
            self.assertEqual(untouched.read_bytes(), original)

            edited = original_payload + b'English UI label'
            decoded_path.write_bytes(edited)
            rebuilt_path = Path(d) / 'edited.pac'
            assets.build(root, rebuilt_path, relocate=True)
            with rebuilt_path.open('rb') as stream:
                member = next(e for e in assets.archive(stream, 0, rebuilt_path.stat().st_size)[2]
                              if e['name'] == 'test.b')
                stream.seek(member['offset'])
                rebuilt_bpe = stream.read(member['size'])
            self.assertEqual(bpe.decode(rebuilt_bpe), edited)
            self.assertGreater(len(rebuilt_bpe), len(bpe.encode(edited)) - 1)


if __name__ == '__main__':
    unittest.main()
