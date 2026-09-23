import math
import struct
import unittest

from tools import yobj
from tools.yobj_geometry import export_geometry, rebuild_geometry


def fixture():
    header_base = 8
    pof0_offset = 0x100
    raw = bytearray(header_base + pof0_offset)
    raw[:4] = b"YOBJ"
    raw[4:8] = struct.pack("<I", pof0_offset)
    raw[header_base + 4:header_base + 8] = struct.pack("<I", pof0_offset)
    raw[header_base + 0x10:header_base + 0x14] = struct.pack("<I", 1)
    raw[header_base + 0x1C:header_base + 0x20] = struct.pack("<I", 0x40)

    descriptor = header_base + 0x40
    raw[descriptor + 0x18:descriptor + 0x1C] = struct.pack("<I", 0x80)
    raw[descriptor + 0x28:descriptor + 0x2C] = struct.pack("<I", 2)

    vertex_data = header_base + 0x80
    raw[vertex_data:vertex_data + 4] = struct.pack("<I", 0x90)
    position_header = header_base + 0x90
    raw[position_header + 14:position_header + 16] = bytes((2, 0x6C))
    positions = position_header + 16
    struct.pack_into("<4f", raw, positions, 1.0, 2.0, 3.0, 1.0)
    struct.pack_into("<4f", raw, positions + 16, -4.0, 5.0, 6.0, 1.0)

    normal_header = positions + 32
    raw[normal_header + 14:normal_header + 16] = bytes((2, 0x6C))
    normals = normal_header + 16
    struct.pack_into("<4f", raw, normals, 0.0, 0.0, 1.0, 0.0)
    struct.pack_into("<4f", raw, normals + 16, 0.0, 1.0, 0.0, 0.0)

    slots = [descriptor + 0x18, vertex_data]
    payload = yobj._encode_pof0(slots, header_base)
    raw.extend(b"POF0" + struct.pack("<I", len(payload)) + payload)
    return bytes(raw)


class YOBJGeometryTests(unittest.TestCase):
    def test_xyz_export_and_noop_rebuild_are_byte_exact(self):
        raw = fixture()
        editable = export_geometry(raw)
        self.assertEqual(editable["editable_xyz_source_bytes"], 48)
        self.assertEqual(editable["meshes"][0]["positions_xyz"], [[1.0, 2.0, 3.0], [-4.0, 5.0, 6.0]])
        self.assertEqual(editable["meshes"][0]["normals_xyz"], [[0.0, 0.0, 1.0], [0.0, 1.0, 0.0]])
        self.assertEqual(rebuild_geometry(raw, editable), raw)

    def test_zero_mesh_resource_has_an_empty_geometry_representation(self):
        raw = bytearray(fixture())
        raw[8 + 0x10:8 + 0x14] = struct.pack("<I", 0)
        raw[8 + 0x1C:8 + 0x20] = struct.pack("<I", 0)
        editable = export_geometry(bytes(raw))
        self.assertEqual(editable["mesh_count"], 0)
        self.assertEqual(editable["editable_xyz_source_bytes"], 0)
        self.assertEqual(rebuild_geometry(bytes(raw), editable), bytes(raw))

    def test_xyz_edits_patch_only_vector_components_and_preserve_w(self):
        raw = fixture()
        editable = export_geometry(raw)
        editable["meshes"][0]["positions_xyz"][1] = [-7.5, 8.25, 9.5]
        editable["meshes"][0]["normals_xyz"][0] = [0.25, 0.5, 0.75]
        rebuilt = rebuild_geometry(raw, editable)
        reparsed = export_geometry(rebuilt)
        self.assertEqual(reparsed["meshes"][0]["positions_xyz"][1], [-7.5, 8.25, 9.5])
        self.assertEqual(reparsed["meshes"][0]["normals_xyz"][0], [0.25, 0.5, 0.75])
        self.assertEqual(struct.unpack_from("<f", rebuilt, 8 + 0x90 + 16 + 16 + 12)[0], 1.0)
        self.assertEqual(struct.unpack_from("<f", rebuilt, 8 + 0x90 + 16 + 32 + 16 + 12)[0], 0.0)

        position_start = 8 + 0x90 + 16
        normal_start = position_start + 32 + 16
        allowed = set()
        for start in (position_start, normal_start):
            for vector in range(2):
                allowed.update(range(start + vector * 16, start + vector * 16 + 12))
        changed = {offset for offset, (old, new) in enumerate(zip(raw, rebuilt)) if old != new}
        self.assertTrue(changed)
        self.assertLessEqual(changed, allowed)
        self.assertEqual(len(rebuilt), len(raw))

    def test_rejects_stale_source_growth_and_nonfinite_values(self):
        raw = fixture()
        editable = export_geometry(raw)
        stale = dict(editable)
        stale["source_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "different source"):
            rebuild_geometry(raw, stale)

        grown = export_geometry(raw)
        grown["meshes"][0]["positions_xyz"].append([0.0, 0.0, 0.0])
        with self.assertRaisesRegex(ValueError, "count changed"):
            rebuild_geometry(raw, grown)

        invalid = export_geometry(raw)
        invalid["meshes"][0]["normals_xyz"][0][0] = math.nan
        with self.assertRaisesRegex(ValueError, "not finite"):
            rebuild_geometry(raw, invalid)

    def test_rejects_non_v4_32_or_count_mismatch(self):
        raw = bytearray(fixture())
        raw[8 + 0x90 + 15] = 0x6D
        with self.assertRaisesRegex(ValueError, "VIF command"):
            export_geometry(bytes(raw))

        raw = bytearray(fixture())
        raw[8 + 0x90 + 14] = 1
        with self.assertRaisesRegex(ValueError, "VIF count"):
            export_geometry(bytes(raw))


if __name__ == "__main__":
    unittest.main()
