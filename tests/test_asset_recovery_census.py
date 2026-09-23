import unittest

from tools.asset_recovery_census import build_census


class AssetRecoveryCensusTests(unittest.TestCase):
    def fixture(self):
        leaves = [
            {"name": "disc!/tex/editable.txc", "source": "00001.bin", "size": 10, "zero": False},
            {"name": "disc!/tex/unresolved.txc", "source": "00002.bin", "size": 5, "zero": False},
            {"name": "disc!/menu/screen.b", "source": "00003.bin", "size": 20, "zero": False,
             "bpe_source": "screen.decoded", "ui_bundle_source": "screen.bundle.json"},
            {"name": "disc!/menu/alternate.b", "source": "00004.bin", "size": 4, "zero": False,
             "bpe_source": "alternate.decoded", "ui_bundle_source": None},
            {"name": "disc!/texts/menu.txt", "source": "00005.bin", "size": 7, "zero": False,
             "text_source": "menu.utf8.txt"},
            {"name": "disc!/texts/_msg.dat", "source": "00006.bin", "size": 8, "zero": False,
             "message_source": "messages.json"},
            {"name": "disc!/opaque.bin", "source": "00007.bin", "size": 16, "zero": False},
            {"name": "disc!/opaque.bin", "source": "00008.bin", "size": 1, "zero": False},
            {"name": "disc!/DMY00.;1", "source": None, "size": 1000, "zero": True},
        ]
        index = {
            "entries": [
                {"key": "direct-edit", "source_kind": "standalone", "source_path": "00001.bin",
                 "image": "editable.tga", "psm_name": "psmt4"},
                {"key": "direct-opaque", "source_kind": "standalone", "source_path": "00002.bin",
                 "image": None, "psm_name": "psmct32"},
                {"key": "nested-edit", "source_kind": "bundle", "bundle_manifest": "00003.bundle.json",
                 "source": "a.txc.bin", "source_sha256": "a", "image": "nested-a.tga",
                 "psm_name": "psmt8"},
                {"key": "nested-opaque", "source_kind": "bundle", "bundle_manifest": "00003.bundle.json",
                 "source": "b.txc.bin", "source_sha256": "b", "image": None,
                 "psm_name": "psmct32"},
            ],
            "_manifest_entries": {
                "00003.bundle.json": {"entries": [
                    {"source": "a.txc.bin", "size": 6, "source_sha256": "a"},
                    {"source": "b.txc.bin", "size": 4, "source_sha256": "b"},
                    {"source": "other.at3", "size": 3, "source_sha256": "c"},
                ]},
            },
        }
        disc = {"image_bytes": 1200, "sha256": "reference"}
        roundtrip = {"reference_sha256": "reference", "reference_size": 1200,
                     "authenticated": True, "match": True, "differing_bytes": 0,
                     "rebuilt_size": 1200, "rebuilt_sha256": "reference"}
        return leaves, index, disc, roundtrip

    def test_nested_texture_bytes_use_a_separate_denominator(self):
        census = build_census(*self.fixture())

        self.assertEqual(census["disc"]["logical_leaf_bytes"], 1071)
        self.assertEqual(census["disc"]["nonzero_leaf_payload_bytes"], 71)
        self.assertEqual(census["disc"]["zero_filled_leaf_bytes"], 1000)
        texture = census["texture_corpus"]
        self.assertEqual(texture["expanded_txc_payload_bytes"], 25)
        self.assertEqual(texture["editable_txc_payload_bytes"], 16)
        self.assertEqual(texture["unresolved_txc_payload_bytes"], 9)
        self.assertEqual(texture["editable_txc_byte_percent"], 64.0)
        categories = census["exclusive_nonzero_leaf_categories"]
        self.assertEqual(sum(item["source_bytes"] for item in categories), 71)
        self.assertEqual(census["editable_group_source_bytes"], 45)

    def test_rejects_roundtrip_evidence_for_another_reference(self):
        leaves, index, disc, roundtrip = self.fixture()
        roundtrip["reference_sha256"] = "another image"

        with self.assertRaisesRegex(ValueError, "different reference"):
            build_census(leaves, index, disc, roundtrip)


if __name__ == "__main__":
    unittest.main()
