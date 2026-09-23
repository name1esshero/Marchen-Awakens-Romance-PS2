#!/usr/bin/env python3
"""Export and patch validated YOBJ vertex positions and normals."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

try:
    from tools.yobj import parse as parse_yobj
except ModuleNotFoundError:  # Direct execution places tools/ on sys.path.
    from yobj import parse as parse_yobj


MESH_DESCRIPTOR_SIZE = 0x40
VIF_UNPACK_V4_32 = 0x6C


def _u32(raw: bytes, offset: int) -> int:
    return int.from_bytes(raw[offset:offset + 4], "little")


def _geometry_layout(raw: bytes) -> tuple[dict, list[dict]]:
    envelope = parse_yobj(raw)
    base = envelope["header_base"]
    end = envelope["pof0_offset"]
    slots = set(envelope["pof0_reference_slots"])
    mesh_count = _u32(raw, base + 0x10)
    mesh_table_offset = _u32(raw, base + 0x1C)
    if mesh_count == 0:
        return envelope, []
    if mesh_table_offset == 0:
        raise ValueError("YOBJ mesh count is nonzero but its descriptor table is absent")
    mesh_table = base + mesh_table_offset
    if mesh_table + mesh_count * MESH_DESCRIPTOR_SIZE > end:
        raise ValueError("YOBJ mesh descriptor table crosses the POF0 boundary")

    meshes = []
    for index in range(mesh_count):
        descriptor = mesh_table + index * MESH_DESCRIPTOR_SIZE
        vertex_count = _u32(raw, descriptor + 0x28)
        vertex_data_relative = _u32(raw, descriptor + 0x18)
        if vertex_count == 0 or vertex_data_relative == 0:
            raise ValueError(f"YOBJ mesh {index} has no supported vertex buffer")
        if descriptor + 0x18 not in slots:
            raise ValueError(f"YOBJ mesh {index} vertex pointer is absent from POF0")

        vertex_data = base + vertex_data_relative
        if vertex_data + 4 > end or vertex_data not in slots:
            raise ValueError(f"YOBJ mesh {index} VIF-buffer pointer is unbounded or unlisted")
        vif_relative = _u32(raw, vertex_data)
        vif_header = base + vif_relative
        if vif_header < base + 0x40 or vif_header + 16 > end:
            raise ValueError(f"YOBJ mesh {index} position VIF header is outside the model body")
        if raw[vif_header + 14] != vertex_count:
            raise ValueError(f"YOBJ mesh {index} position VIF count disagrees with its descriptor")
        if raw[vif_header + 15] != VIF_UNPACK_V4_32:
            raise ValueError(f"YOBJ mesh {index} position VIF command is unsupported")
        positions_offset = vif_header + 16
        positions_end = positions_offset + vertex_count * 16
        if positions_end + 16 > end:
            raise ValueError(f"YOBJ mesh {index} position array crosses the POF0 boundary")

        normal_header = positions_end
        if raw[normal_header + 14] != vertex_count:
            raise ValueError(f"YOBJ mesh {index} normal VIF count disagrees with its descriptor")
        if raw[normal_header + 15] != VIF_UNPACK_V4_32:
            raise ValueError(f"YOBJ mesh {index} normal VIF command is unsupported")
        normals_offset = normal_header + 16
        normals_end = normals_offset + vertex_count * 16
        if normals_end > end:
            raise ValueError(f"YOBJ mesh {index} normal array crosses the POF0 boundary")

        positions = []
        normals = []
        for vector_index in range(vertex_count):
            pos = struct.unpack_from("<4f", raw, positions_offset + vector_index * 16)
            normal = struct.unpack_from("<4f", raw, normals_offset + vector_index * 16)
            if not all(math.isfinite(value) for value in (*pos, *normal)):
                raise ValueError(f"YOBJ mesh {index} has a non-finite position or normal")
            if pos[3] != 1.0 or normal[3] != 0.0:
                raise ValueError(f"YOBJ mesh {index} has an unsupported position/normal W value")
            positions.append([pos[0], pos[1], pos[2]])
            normals.append([normal[0], normal[1], normal[2]])

        meshes.append({
            "index": index,
            "vertex_count": vertex_count,
            "positions_xyz": positions,
            "normals_xyz": normals,
            "_positions_offset": positions_offset,
            "_normals_offset": normals_offset,
        })
    return envelope, meshes


def export_geometry(raw: bytes) -> dict:
    """Return source-bound editable XYZ arrays for validated mesh buffers."""
    envelope, meshes = _geometry_layout(raw)
    public_meshes = [
        {key: mesh[key] for key in ("index", "vertex_count", "positions_xyz", "normals_xyz")}
        for mesh in meshes
    ]
    return {
        "schema_version": 1,
        "format": "YOBJ vertex positions and normals",
        "variant": envelope["variant"],
        "source_size": len(raw),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "mesh_count": len(public_meshes),
        "editable_xyz_source_bytes": sum(mesh["vertex_count"] * 24 for mesh in public_meshes),
        "meshes": public_meshes,
        "limits": [
            "Only XYZ position and normal floats are editable; VIF W components are preserved as 1.0 and 0.0.",
            "Mesh counts and array lengths are fixed. This writer does not add/remove vertices, decode faces, UVs, materials or skinning, or regenerate POF0 after growth.",
            "The format mapping is accepted only when the descriptor count, VIF Vector4f command, POF0 pointer slots, finite floats and W values match the observed corpus contract.",
        ],
    }


def _edited_vector(value, mesh_index: int, field: str, vertex_index: int) -> tuple[float, float, float]:
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"YOBJ mesh {mesh_index} {field}[{vertex_index}] must have three floats")
    result = []
    for component in value:
        if isinstance(component, bool) or not isinstance(component, (int, float)):
            raise ValueError(f"YOBJ mesh {mesh_index} {field}[{vertex_index}] has a non-numeric component")
        component = float(component)
        if not math.isfinite(component):
            raise ValueError(f"YOBJ mesh {mesh_index} {field}[{vertex_index}] is not finite")
        result.append(component)
    return tuple(result)


def rebuild_geometry(raw: bytes, edited: dict) -> bytes:
    """Patch same-count XYZ arrays while preserving every other source byte."""
    expected_hash = hashlib.sha256(raw).hexdigest()
    if not isinstance(edited, dict) or edited.get("schema_version") != 1:
        raise ValueError("unsupported YOBJ geometry representation")
    if edited.get("source_size") != len(raw) or edited.get("source_sha256") != expected_hash:
        raise ValueError("YOBJ geometry representation belongs to a different source")
    envelope, layout = _geometry_layout(raw)
    if edited.get("variant") != envelope["variant"]:
        raise ValueError("YOBJ geometry variant changed")
    meshes = edited.get("meshes")
    if not isinstance(meshes, list) or len(meshes) != len(layout):
        raise ValueError("YOBJ geometry mesh count changed")
    if edited.get("mesh_count") != len(layout):
        raise ValueError("YOBJ geometry mesh count metadata is inconsistent")

    output = bytearray(raw)
    editable_bytes = 0
    for index, (candidate, original) in enumerate(zip(meshes, layout)):
        if not isinstance(candidate, dict) or candidate.get("index") != index:
            raise ValueError(f"YOBJ geometry mesh ordering changed at index {index}")
        count = original["vertex_count"]
        if candidate.get("vertex_count") != count:
            raise ValueError(f"YOBJ mesh {index} vertex count changed")
        for field, offset in (("positions_xyz", original["_positions_offset"]),
                              ("normals_xyz", original["_normals_offset"])):
            vectors = candidate.get(field)
            if not isinstance(vectors, list) or len(vectors) != count:
                raise ValueError(f"YOBJ mesh {index} {field} count changed")
            for vertex_index, vector in enumerate(vectors):
                xyz = _edited_vector(vector, index, field, vertex_index)
                try:
                    struct.pack_into("<3f", output, offset + vertex_index * 16, *xyz)
                except (OverflowError, struct.error) as exc:
                    raise ValueError(f"YOBJ mesh {index} {field}[{vertex_index}] is out of float32 range") from exc
            editable_bytes += count * 12
    if editable_bytes != edited.get("editable_xyz_source_bytes"):
        raise ValueError("YOBJ editable-byte metadata is inconsistent")

    rebuilt = bytes(output)
    # Reparse to verify the edited vectors, unchanged record counts, and preserved
    # VIF/POF0 structure before exposing the candidate binary.
    verified = export_geometry(rebuilt)
    if verified["mesh_count"] != len(layout):
        raise ValueError("YOBJ geometry mesh count changed during rebuild")
    return rebuilt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output-json", type=Path,
                        help="export the source-bound editable XYZ arrays")
    parser.add_argument("--build-json", type=Path,
                        help="patch XYZ arrays from this representation")
    parser.add_argument("--output", type=Path,
                        help="binary output path used with --build-json")
    args = parser.parse_args()
    if bool(args.output_json) == bool(args.build_json):
        parser.error("choose exactly one of --output-json or --build-json")
    if args.build_json and not args.output:
        parser.error("--build-json requires --output")
    if args.output_json and args.output:
        parser.error("--output is only valid with --build-json")
    try:
        raw = args.source.read_bytes()
        if args.output_json:
            representation = export_geometry(raw)
            args.output_json.parent.mkdir(parents=True, exist_ok=True)
            args.output_json.write_text(json.dumps(representation, indent=2) + "\n",
                                        encoding="utf-8")
            print(f"Exported {representation['mesh_count']} meshes / "
                  f"{representation['editable_xyz_source_bytes']:,} editable source bytes")
        else:
            edited = json.loads(args.build_json.read_text(encoding="utf-8"))
            rebuilt = rebuild_geometry(raw, edited)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_bytes(rebuilt)
            print(f"Wrote {len(rebuilt):,} bytes to {args.output}")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
