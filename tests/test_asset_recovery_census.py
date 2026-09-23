import unittest

from tools.asset_recovery_census import build_census, format_census_summary


class AssetRecoveryCensusTests(unittest.TestCase):
    def fixture(self):
        leaves = [
            {"name": "disc!/tex/editable.txc", "source": "00001.bin", "size": 10, "zero": False},
            {"name": "disc!/tex/unresolved.txc", "source": "00002.bin", "size": 5, "zero": False},
            {"name": "disc!/menu/screen.b", "source": "00003.bin", "size": 20, "zero": False,
             "bpe_source": "screen.decoded", "ui_bundle_source": "00003.bundle.json"},
            {"name": "disc!/menu/alternate.b", "source": "00004.bin", "size": 4, "zero": False,
             "bpe_source": "alternate.decoded", "bpe_decoded_size": 8,
             "ui_bundle_source": None},
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
                 "image": "editable.tga", "psm_name": "psmt4", "rtx3_parse_valid": True},
                {"key": "direct-opaque", "source_kind": "standalone", "source_path": "00002.bin",
                 "image": None, "psm_name": "psmct32", "rtx3_parse_valid": False},
                {"key": "nested-edit", "source_kind": "bundle", "bundle_manifest": "00003.bundle.json",
                 "source": "a.txc.bin", "source_sha256": "a", "image": "nested-a.tga",
                 "rtx3_parse_valid": True,
                 "psm_name": "psmt8"},
                {"key": "nested-opaque", "source_kind": "bundle", "bundle_manifest": "00003.bundle.json",
                 "source": "b.txc.bin", "source_sha256": "b", "image": None,
                 "rtx3_parse_valid": False,
                 "psm_name": "psmct32"},
            ],
            "_manifest_entries": {
                "00003.bundle.json": {"entries": [
                    {"source": "a.txc.bin", "size": 6, "source_sha256": "a",
                     "kind_hex": "74786300"},
                    {"source": "b.txc.bin", "size": 4, "source_sha256": "b",
                     "kind_hex": "74786300"},
                    {"source": "other.at3", "size": 3, "source_sha256": "c",
                     "kind_hex": "61743300"},
                ]},
            },
        }
        disc = {
            "image_bytes": 1200,
            "sha256": "reference",
            "_layout_partition": {
                "named_member_count": 9,
                "all_zero_named_member_count": 1,
                "all_zero_named_member_bytes": 1000,
                "information_bearing_named_member_count": 8,
                "information_bearing_named_member_bytes": 71,
                "all_zero_gap_span_count": 1,
                "all_zero_gap_bytes": 29,
                "nonzero_gap_span_count": 1,
                "nonzero_gap_bytes": 100,
            },
        }
        roundtrip = {"reference_sha256": "reference", "reference_size": 1200,
                     "authenticated": True, "match": True, "differing_bytes": 0,
                     "rebuilt_size": 1200, "rebuilt_sha256": "reference"}
        return leaves, index, disc, roundtrip

    def test_expanded_payload_and_recovery_levels_use_nonoverlapping_bytes(self):
        census = build_census(*self.fixture())

        physical = census["physical_disc_accounting"]
        self.assertEqual(physical["partition_bytes"], 1200)
        self.assertTrue(physical["partition_matches_image"])
        self.assertEqual(physical["information_bearing_terminal_member_bytes"], 71)
        self.assertEqual(physical["measured_all_zero_bytes"], 1029)
        self.assertIsNone(physical["intentional_zero_padding_bytes"])
        self.assertFalse(physical["zero_byte_purpose_established"])

        logical = census["expanded_logical_payload"]
        self.assertEqual(logical["information_bearing_payload_bytes_Y"], 68)
        levels = logical["recovery_levels"]
        self.assertEqual(levels["structurally_classified"]["bytes_Z"], 34)
        self.assertAlmostEqual(levels["structurally_classified"]["percent_Z_of_Y"], 50.0)
        self.assertEqual(levels["losslessly_rebuildable"]["bytes_A"], 68)
        self.assertEqual(levels["semantically_editable"]["bytes_B"], 31)
        self.assertAlmostEqual(levels["semantically_editable"]["percent_B_of_Y"], 45.5882)
        self.assertAlmostEqual(
            levels["semantically_editable"]["component_percentages_of_Y"][
                "supported_editable_TGA_texture_source_bytes"
            ],
            23.5294,
        )
        self.assertEqual(levels["runtime_validated_editable"]["bytes_C"], 0)

        logical = census["expanded_logical_payload"]
        structured_only = logical["classified_but_not_semantically_editable"]
        self.assertEqual(structured_only["bytes"], 3)
        opaque = logical["opaque_after_structural_classification"]
        self.assertEqual(opaque["bytes"], 34)
        self.assertEqual(sum(item["source_bytes"] for item in
                             opaque["exclusive_byte_weighted_categories"]), 34)

        texture = census["texture_corpus"]
        self.assertEqual(texture["expanded_txc_payload_bytes"], 25)
        self.assertEqual(texture["editable_txc_payload_bytes"], 16)
        self.assertEqual(texture["unresolved_txc_payload_bytes"], 9)
        self.assertEqual(texture["editable_txc_byte_percent"], 64.0)
        categories = logical["remaining_after_semantic_editability"][
            "exclusive_byte_weighted_categories"
        ]
        self.assertEqual(sum(item["source_bytes"] for item in categories), 37)

    def test_summary_keeps_recovery_levels_and_remainder_bases_separate(self):
        leaves, index, disc, roundtrip = self.fixture()
        movie = next(leaf for leaf in leaves if leaf["source"] == "00007.bin")
        movie["name"] = "disc!/MOVIE.AFS;1!/00000.bin"
        movie["_mpeg_program_stream"] = True
        movie["_mpeg_ps_structural_bytes"] = movie["size"]
        summary = format_census_summary(build_census(leaves, index, disc, roundtrip))

        self.assertIn("padding intent unverified", summary)
        self.assertIn("Intentional zero/padding: not established from byte contents alone", summary)
        self.assertIn("Structurally classified Z/Y: 50/68 bytes (73.5294%)", summary)
        self.assertIn("Losslessly rebuildable from unchanged inputs A/Y: 68/68 bytes (100.0000%)",
                      summary)
        self.assertIn("Semantically editable B/Y: 31/68 bytes (45.5882%)", summary)
        self.assertIn("Semantically editable source components (% of Y; rounded independently):",
                      summary)
        self.assertIn("Runtime-validated editable C/Y: 0/68 bytes (0.0000%)", summary)
        self.assertIn("Y-B byte breakdown (% of Y-B):", summary)
        self.assertIn("Y-Z structurally unclassified inventory (% of Y-Z; not all semantic opacity):",
                      summary)
        self.assertIn("video cinematics: 16 bytes (43.2432%)", summary)
        opaque_breakdown = summary.split("Y-Z structurally unclassified inventory", 1)[1]
        self.assertNotIn("video cinematics", opaque_breakdown)

    def test_requires_explicit_rtx3_parse_evidence(self):
        leaves, index, disc, roundtrip = self.fixture()
        del index["entries"][0]["rtx3_parse_valid"]

        with self.assertRaisesRegex(ValueError, "lacks strict RTX3 parse status"):
            build_census(leaves, index, disc, roundtrip)

    def test_rejects_roundtrip_evidence_for_another_reference(self):
        leaves, index, disc, roundtrip = self.fixture()
        roundtrip["reference_sha256"] = "another image"

        with self.assertRaisesRegex(ValueError, "different reference"):
            build_census(leaves, index, disc, roundtrip)

    def test_validated_direct_at3_envelopes_extend_structural_coverage(self):
        leaves, index, disc, roundtrip = self.fixture()
        at3_leaf = next(leaf for leaf in leaves if leaf["source"] == "00007.bin")
        at3_leaf["name"] = "disc!/motion/test.at3"
        at3_leaf["_at3_reference_table_bytes"] = 4
        at3_leaf["_at3_preamble_bytes"] = 4
        at3_leaf["_at3_node_record_bytes"] = 8

        census = build_census(leaves, index, disc, roundtrip)
        level = census["expanded_logical_payload"]["recovery_levels"]["structurally_classified"]
        self.assertEqual(level["bytes_Z"], 50)
        self.assertEqual(level["components"]["direct_AT3_reference_table_bytes"], 4)
        self.assertEqual(level["components"]["direct_AT3_bounded_preamble_bytes"], 4)
        self.assertEqual(level["components"]["direct_AT3_validated_node_record_bytes"], 8)
        self.assertEqual(
            census["expanded_logical_payload"]["recovery_levels"]["semantically_editable"]["bytes_B"],
            31,
        )

    def test_validated_direct_yobj_envelope_extends_structure_not_editability(self):
        leaves, index, disc, roundtrip = self.fixture()
        ymp_leaf = next(leaf for leaf in leaves if leaf["source"] == "00007.bin")
        ymp_leaf["name"] = "disc!/model/test.ymp"
        ymp_leaf["_yobj_structural_bytes"] = ymp_leaf["size"]

        census = build_census(leaves, index, disc, roundtrip)
        levels = census["expanded_logical_payload"]["recovery_levels"]
        self.assertEqual(levels["structurally_classified"]["bytes_Z"], 50)
        self.assertEqual(
            levels["structurally_classified"]["components"][
                "direct_YOBJ_YMP_validated_envelope_bytes"
            ],
            16,
        )
        self.assertEqual(levels["semantically_editable"]["bytes_B"], 31)

    def test_direct_yobj_geometry_is_counted_only_for_editable_coordinate_bytes(self):
        leaves, index, disc, roundtrip = self.fixture()
        ymp_leaf = next(leaf for leaf in leaves if leaf["source"] == "00007.bin")
        ymp_leaf["name"] = "disc!/model/test.ymp"
        ymp_leaf["_yobj_structural_bytes"] = ymp_leaf["size"]
        ymp_leaf["_yobj_editable_geometry_bytes"] = 8
        index["_yobj_resource_corpus"] = {
            "direct_resources": {"editable_xyz_source_bytes": 8},
            "nested_ui_bundle_resources": {"editable_xyz_source_bytes": 0},
        }

        census = build_census(leaves, index, disc, roundtrip)
        levels = census["expanded_logical_payload"]["recovery_levels"]
        editable = levels["semantically_editable"]
        self.assertEqual(editable["bytes_B"], 39)
        self.assertEqual(
            editable["components"]["editable_YOBJ_position_and_normal_source_bytes"], 8
        )
        self.assertEqual(
            census["expanded_logical_payload"]["remaining_after_semantic_editability"]["bytes"],
            29,
        )

    def test_nested_yobj_geometry_is_counted_without_counting_entire_member(self):
        leaves, index, disc, roundtrip = self.fixture()
        nested_model = index["_manifest_entries"]["00003.bundle.json"]["entries"][2]
        nested_model["source"] = "other.ymp"
        nested_model["kind_hex"] = "796d7000"
        nested_model["_yobj_editable_geometry_bytes"] = 2
        index["_yobj_resource_corpus"] = {
            "direct_resources": {"editable_xyz_source_bytes": 0},
            "nested_ui_bundle_resources": {"editable_xyz_source_bytes": 2},
        }

        census = build_census(leaves, index, disc, roundtrip)
        editable = census["expanded_logical_payload"]["recovery_levels"]["semantically_editable"]
        self.assertEqual(editable["bytes_B"], 33)
        self.assertEqual(
            editable["components"]["editable_YOBJ_position_and_normal_source_bytes"], 2
        )

    def test_validated_movie_packet_extents_extend_structure_not_editability(self):
        leaves, index, disc, roundtrip = self.fixture()
        movie_leaf = next(leaf for leaf in leaves if leaf["source"] == "00007.bin")
        movie_leaf["name"] = "disc!/MOVIE.AFS;1!/00000.bin"
        movie_leaf["_mpeg_program_stream"] = True
        movie_leaf["_mpeg_ps_structural_bytes"] = movie_leaf["size"]
        index["_mpeg_ps_resource_corpus"] = {
            "file_count": 1,
            "source_bytes": movie_leaf["size"],
            "parse_successful_count": 1,
            "exact_noop_roundtrip_count": 1,
        }

        census = build_census(leaves, index, disc, roundtrip)
        logical = census["expanded_logical_payload"]
        levels = logical["recovery_levels"]
        self.assertEqual(levels["structurally_classified"]["bytes_Z"], 50)
        self.assertEqual(
            levels["structurally_classified"]["components"][
                "direct_MPEG_PS_validated_packet_and_sector_bytes"
            ],
            16,
        )
        self.assertEqual(levels["semantically_editable"]["bytes_B"], 31)
        self.assertEqual(logical["opaque_after_structural_classification"]["bytes"], 18)
        opaque_classes = {
            item["name"]
            for item in logical["opaque_after_structural_classification"][
                "exclusive_byte_weighted_categories"
            ]
        }
        self.assertNotIn("video_cinematics", opaque_classes)
        self.assertEqual(census["video_resource_corpus"]["parse_successful_count"], 1)


if __name__ == "__main__":
    unittest.main()
