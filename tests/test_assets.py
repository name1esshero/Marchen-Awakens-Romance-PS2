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
import ui_bundle
import graphics
import rtx3
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
    def test_graphics_categories_are_human_readable_and_flat(self):
        cases = (
            ('icon_armset', '', 'icon'),
            ('btnhlptxt', 'disc!/data/menu/option_tex.b', 'user_interface'),
            ('eff_001', '', 'effects'),
            ('chr_s001', '', 'characters'),
            ('card_001', '', 'cards'),
            ('bg_001', '', 'backgrounds'),
        )
        for name, asset_path, expected in cases:
            with self.subTest(name=name):
                self.assertEqual(graphics._category(name, asset_path), expected)

    def test_graphics_index_marks_short_rtx3_as_not_fully_parsed(self):
        width = height = 8
        expected_pixels = width * height * 4
        raw = bytearray(rtx3.HEADER_SIZE + expected_pixels - 8)
        raw[:4] = b'RTX3'
        struct.pack_into('<I', raw, 4, len(raw) - 8)
        struct.pack_into('<Q', raw, 8,
                         (rtx3.PSMCT32 << 20) | (3 << 26) | (3 << 30))
        struct.pack_into('<HHI', raw, 0x20, width, height, expected_pixels)

        with tempfile.TemporaryDirectory() as d:
            workspace = Path(d) / 'source'
            workspace.mkdir()
            (workspace / 'short.txc').write_bytes(raw)
            (workspace / 'catalog.json').write_text(json.dumps([
                {"name": "disc!/short.txc", "source": "short.txc",
                 "size": len(raw), "zero": False}
            ]))
            with redirect_stdout(io.StringIO()):
                index = graphics.export(workspace, Path(d) / 'graphics')

        row = index['entries'][0]
        self.assertFalse(row['rtx3_parse_valid'])
        self.assertIsNone(row['image'])
        self.assertIn('length does not match', row['unsupported_reason'])

    def test_graphics_staging_refuses_user_owned_or_source_paths(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            workspace = root / 'source'
            graphics_root = root / 'graphics'
            output = root / 'existing-output'
            workspace.mkdir()
            graphics_root.mkdir()
            output.mkdir()
            sentinel = output / 'keep.txt'
            sentinel.write_text('user data')
            with self.assertRaisesRegex(ValueError, 'unrecognized output directory'):
                graphics._reset_overrides(workspace, graphics_root, output)
            self.assertEqual(sentinel.read_text(), 'user data')
            with self.assertRaisesRegex(ValueError, 'unsafe graphics override'):
                graphics._reset_overrides(workspace, graphics_root, workspace)

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

    def test_ui_bundle_member_edit_grows_and_relocates_through_bpe_and_pac(self):
        decoded = bytearray(0x36)
        struct.pack_into('<I', decoded, 0, 1)
        decoded[4:8] = b'\x01\x01\0\0'
        decoded[16:22] = b'window'
        decoded[32:36] = b'txc\0'
        struct.pack_into('<III', decoded, 36, 6, 0x30, 0)
        decoded[0x30:] = b'pixels'
        original = bytearray(pac([bpe.encode(bytes(decoded))]))
        original[16 + 16:16 + 20] = b'b\0\0\0'
        original = bytes(original)

        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'source'
            self.export(original, root)
            with redirect_stdout(io.StringIO()):
                assets.prepare(root, report=None)
            audit = ui_bundle.audit(root)
            self.assertEqual(audit['bundle_count'], 1)
            self.assertEqual(audit['untouched_exact_rebuilds'], 1)
            self.assertEqual(audit['type_counts'], {'txc': 1})
            layout = json.loads((root / 'layout.json').read_text())
            leaf = next(piece for piece in layout['pieces'] if piece.get('name') == 'test.b')
            manifest = json.loads((root / leaf['ui_bundle_source']).read_text())
            member_path = root / leaf['ui_bundle_dir'] / manifest['entries'][0]['source']
            member_path.write_bytes(b'English image replacement')

            output = Path(d) / 'mod.pac'
            assets.build(root, output, relocate=True)
            with output.open('rb') as stream:
                pac_entry = assets.archive(stream, 0, output.stat().st_size)[2][0]
                stream.seek(pac_entry['offset'])
                packed_bundle = stream.read(pac_entry['size'])
            rebuilt_bundle = bpe.decode(packed_bundle)
            rebuilt_manifest = ui_bundle.parse(rebuilt_bundle)
            entry = rebuilt_manifest['entries'][0]
            self.assertEqual(rebuilt_bundle[entry['offset']:entry['offset'] + entry['size']],
                             b'English image replacement')
            self.assertGreater(entry['offset'], 0x30)

    def test_graphics_override_reinserts_through_ui_bundle_bpe_and_pac(self):
        width, height = 128, 64
        tex0 = (rtx3.PSMT8 << 20) | (7 << 26) | (6 << 30)
        pixel_size = width * height
        header = bytearray(rtx3.HEADER_SIZE)
        header[:4] = b'RTX3'
        struct.pack_into('<I', header, 4, 0x40 + pixel_size + 1024 - 8)
        struct.pack_into('<Q', header, 8, tex0)
        struct.pack_into('<HHI', header, 0x20, width, height, pixel_size)
        texture = (bytes(header) + bytes((i * 17) & 0xFF for i in range(pixel_size)) +
                   b''.join(bytes((i, i, i, 0x80)) for i in range(256)))

        decoded = bytearray(0x30)
        struct.pack_into('<I', decoded, 0, 1)
        decoded[4:8] = b'\x01\x01\0\0'
        decoded[16:29] = b'title_marh_jp'
        decoded[32:36] = b'txc\0'
        struct.pack_into('<III', decoded, 36, len(texture), 0x30, 0)
        decoded.extend(texture)
        original = bytearray(pac([bpe.encode(bytes(decoded))]))
        original[16 + 16:16 + 20] = b'b\0\0\0'
        original = bytes(original)

        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'source'
            self.export(original, root)
            with redirect_stdout(io.StringIO()):
                assets.prepare(root, report=None)
            graphics_root = Path(d) / 'graphics'
            with redirect_stdout(io.StringIO()):
                index = graphics.export(root, graphics_root)
            row = next(item for item in index['entries']
                       if item['name'] == 'title_marh_jp')
            self.assertTrue(row['rtx3_parse_valid'])
            self.assertEqual(row['category'], 'title')
            self.assertEqual(Path(row['image']).parent, Path('title'))
            self.assertTrue(Path(row['image']).stem.endswith('_jp'))
            self.assertEqual(row['asset_path'], 'disc!/test.b')
            image_path = graphics_root / row['image']
            original_image = image_path.read_bytes()
            w, h, rgba = rtx3.read_tga(original_image)
            changed = bytearray(rgba)
            palette_offset = rtx3.parse(texture)['palette_offset']
            stored_index = rtx3._clut_index(100, rtx3.PSMT8)
            target = texture[palette_offset + stored_index * 4:
                             palette_offset + (stored_index + 1) * 4]
            changed[:4] = target[:3] + bytes((min(255, target[3] * 2),))
            english_path = graphics.english_variant_path(image_path)
            self.assertTrue(english_path.stem.endswith('_eng'))
            english_path.write_bytes(rtx3.write_tga(w, h, changed))
            english_image = english_path.read_bytes()
            with redirect_stdout(io.StringIO()):
                graphics.export(root, graphics_root)
                audit = graphics.audit(root, graphics_root)
            self.assertEqual(image_path.read_bytes(), original_image)
            self.assertEqual(english_path.read_bytes(), english_image)
            self.assertEqual(audit['edited_images'], 0)
            self.assertEqual(audit['english_overrides'], 1)
            overrides_root = Path(d) / 'graphics-overrides'
            with redirect_stdout(io.StringIO()):
                report = graphics.build(root, graphics_root, overrides_root)
            self.assertEqual(len(report['changed']), 1)
            self.assertEqual(report['changed'][0]['language'], 'eng')
            self.assertEqual(report['changed'][0]['image'],
                             english_path.relative_to(graphics_root).as_posix())
            self.assertEqual(image_path.read_bytes(), original_image)
            source_member = root / row['bundle_dir'] / row['source']
            self.assertEqual(source_member.read_bytes(), texture)

            output = Path(d) / 'mod.pac'
            assets.build(root, output, relocate=True,
                          graphics_overrides=overrides_root)
            with output.open('rb') as stream:
                pac_entry = assets.archive(stream, 0, output.stat().st_size)[2][0]
                stream.seek(pac_entry['offset'])
                packed_bundle = stream.read(pac_entry['size'])
            rebuilt_bundle = bpe.decode(packed_bundle)
            bundle_entry = ui_bundle.parse(rebuilt_bundle)['entries'][0]
            rebuilt_texture = rebuilt_bundle[
                bundle_entry['offset']:bundle_entry['offset'] + bundle_entry['size']]
            override = (overrides_root / row['bundle_dir'] /
                        row['source']).read_bytes()
            self.assertEqual(rebuilt_texture, override)
            self.assertNotEqual(rebuilt_texture, texture)

    def test_standalone_txc_english_override_reinserts_through_pac(self):
        width = height = 16
        pixel_size = width * height
        header = bytearray(rtx3.HEADER_SIZE)
        header[:4] = b'RTX3'
        struct.pack_into('<I', header, 4, 0x40 + pixel_size + 1024 - 8)
        struct.pack_into('<Q', header, 8,
                         (rtx3.PSMT8 << 20) | (4 << 26) | (4 << 30))
        struct.pack_into('<HHI', header, 0x20, width, height, pixel_size)
        texture = (bytes(header) + bytes(range(256)) +
                   b''.join(bytes((i, i, i, 0x80)) for i in range(256)))
        packed = bytearray(pac([pac([texture])]))
        inner_base = 16 + 32
        packed[inner_base + 16 + 16:inner_base + 16 + 20] = b'txc\0'

        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'source'
            self.export(bytes(packed), root)
            with redirect_stdout(io.StringIO()):
                assets.prepare(root, report=None)
            graphics_root = Path(d) / 'graphics'
            with redirect_stdout(io.StringIO()):
                index = graphics.export(root, graphics_root)
            row = next(item for item in index['entries']
                       if item['source_kind'] == 'standalone')
            self.assertEqual(row['logical_path'], 'disc!/test.bin!/test.txc')
            self.assertEqual(row['category'], 'user_interface')
            baseline = graphics_root / row['image']
            width, height, rgba = rtx3.read_tga(baseline.read_bytes())
            edited = bytearray(rgba)
            edited[:4] = bytes((255, 0, 0, 255))
            english = graphics.english_variant_path(baseline)
            english.write_bytes(rtx3.write_tga(width, height, edited))

            overrides = Path(d) / 'overrides'
            with redirect_stdout(io.StringIO()):
                report = graphics.build(root, graphics_root, overrides)
            self.assertEqual(len(report['changed']), 1)
            manifest = json.loads((overrides / graphics.STANDALONE_MANIFEST).read_text())
            self.assertEqual(len(manifest['entries']), 1)
            staged = (overrides / 'standalone' /
                      manifest['entries'][0]['target']).read_bytes()

            output = Path(d) / 'mod.pac'
            assets.build(root, output, relocate=True, graphics_overrides=overrides)
            rebuilt_bytes = output.read_bytes()
            outer = assets.archive(io.BytesIO(rebuilt_bytes), 0,
                                   len(rebuilt_bytes))[2][0]
            inner_base = outer['offset']
            inner = assets.archive(io.BytesIO(rebuilt_bytes), inner_base,
                                   outer['size'])[2][0]
            start = inner_base + inner['offset']
            rebuilt = rebuilt_bytes[start:start + inner['size']]
            self.assertEqual(rebuilt, staged)
            self.assertNotEqual(rebuilt, texture)


if __name__ == '__main__':
    unittest.main()
