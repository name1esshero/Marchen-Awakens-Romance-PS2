#!/usr/bin/env python3
"""Build a byte-weighted census with physical and expanded payload bases.

The physical view partitions every disc byte into named leaf spans and gaps.
The expanded logical view replaces compressed BPE/UI bundle wrappers with
their decoded member payloads, counting each member once. The recovery levels
are kept distinct: structural classification, unchanged-source rebuild,
semantic editability, and runtime validation are independent evidence.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

try:
    from tools import movies as movies_tool
    from tools.at3 import parse as parse_at3, rebuild as rebuild_at3
    from tools.mpeg_ps import parse as parse_mpeg_ps, rebuild as rebuild_mpeg_ps
    from tools.yobj import parse as parse_yobj, rebuild as rebuild_yobj
    from tools.yobj_geometry import export_geometry as export_yobj_geometry
    from tools.yobj_geometry import rebuild_geometry as rebuild_yobj_geometry
except ModuleNotFoundError:  # Direct execution places tools/ on sys.path.
    import movies as movies_tool
    from at3 import parse as parse_at3, rebuild as rebuild_at3
    from mpeg_ps import parse as parse_mpeg_ps, rebuild as rebuild_mpeg_ps
    from yobj import parse as parse_yobj, rebuild as rebuild_yobj
    from yobj_geometry import export_geometry as export_yobj_geometry
    from yobj_geometry import rebuild_geometry as rebuild_yobj_geometry


def _read_json(path: Path):
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def _percent(numerator: int, denominator: int) -> float:
    return round(100.0 * numerator / denominator, 4) if denominator else 0.0


def _logical_basename(name: str) -> str:
    return name.rsplit("!/", 1)[-1]


def _source_extension(name: str) -> str:
    # ISO version suffixes (for example, .IRX;1) are not part of the extension.
    basename = _logical_basename(name).split(";", 1)[0]
    return Path(basename).suffix.lower() or "[none]"


def _member_extension(member: dict) -> str:
    kind_hex = member.get("kind_hex")
    if not isinstance(kind_hex, str):
        return _source_extension(member.get("source", ""))
    try:
        kind = bytes.fromhex(kind_hex).rstrip(b"\0").decode("ascii").lower()
    except (ValueError, UnicodeDecodeError):
        return "[unknown]"
    return f".{kind}" if kind else "[none]"


def _load_layout_partition(layout_path: Path, expected_image_bytes: int) -> dict:
    """Walk nested layouts and account for physical member and gap extents."""
    counts = Counter()

    def walk(path: Path) -> int:
        layout = _read_json(path)
        size = layout.get("size")
        pieces = layout.get("pieces")
        if not isinstance(size, int) or size < 0 or not isinstance(pieces, list):
            raise ValueError(f"invalid physical layout: {path}")

        cursor = 0
        for piece in sorted(pieces, key=lambda row: row.get("offset", -1)):
            offset, piece_size = piece.get("offset"), piece.get("size")
            if not isinstance(offset, int) or not isinstance(piece_size, int) or piece_size < 0:
                raise ValueError(f"invalid extent in physical layout: {path}")
            if offset != cursor:
                raise ValueError(f"layout extents do not partition {path}: expected {cursor}, got {offset}")
            cursor = offset + piece_size

            if piece.get("container"):
                child_path = path.parent / piece["source"] / "layout.json"
                child_size = walk(child_path)
                if child_size != piece_size:
                    raise ValueError(f"nested layout size disagrees with parent extent: {child_path}")
                continue

            if piece.get("name") is not None:
                counts["named_member_count"] += 1
                if piece.get("zero"):
                    counts["all_zero_named_member_count"] += 1
                    counts["all_zero_named_member_bytes"] += piece_size
                else:
                    counts["information_bearing_named_member_count"] += 1
                    counts["information_bearing_named_member_bytes"] += piece_size
            else:
                counts["gap_span_count"] += 1
                if piece.get("zero"):
                    counts["all_zero_gap_span_count"] += 1
                    counts["all_zero_gap_bytes"] += piece_size
                else:
                    counts["nonzero_gap_span_count"] += 1
                    counts["nonzero_gap_bytes"] += piece_size

        if cursor != size:
            raise ValueError(f"layout extents cover {cursor} bytes, expected {size}: {path}")
        return size

    walked_bytes = walk(layout_path)
    accounted = sum(counts[key] for key in (
        "all_zero_named_member_bytes", "information_bearing_named_member_bytes",
        "all_zero_gap_bytes", "nonzero_gap_bytes"))
    if walked_bytes != expected_image_bytes or accounted != expected_image_bytes:
        raise ValueError("physical layout partition does not equal the pinned disc image size")
    return dict(counts)


def _load_inputs(workspace: Path, catalog_path: Path, graphics_path: Path,
                 disc_path: Path, roundtrip_path: Path,
                 movies_path: Path = Path("movies")):
    catalog = _read_json(catalog_path)
    graphics = _read_json(graphics_path)
    disc = _read_json(disc_path)
    roundtrip = _read_json(roundtrip_path)
    root_layout = workspace / "layout.json"
    disc["_layout_partition"] = _load_layout_partition(root_layout, disc["image_bytes"])

    # The editable video numerator is tied to immutable Japanese elementary
    # stream exports and a profile-checked override audit, not to whole movie
    # containers or to filenames alone.
    movie_audit = movies_tool.audit(workspace, movies_path)
    movie_entries = {
        entry["logical_path"]: entry for entry in movie_audit["_audited_entries"]
    }
    catalog_movie_paths = {
        leaf["name"] for leaf in catalog
        if leaf.get("source") and "MOVIE.AFS;1!/" in leaf["name"]
    }
    if catalog_movie_paths != set(movie_entries):
        raise ValueError("movie export index does not cover the direct MOVIE.AFS catalog")

    # Prepared metadata records exact BPE hashes for the three unparsed YMA
    # payloads, but older catalogs omitted their decoded lengths.
    mpeg_stats = {
        "file_count": 0,
        "source_bytes": 0,
        "parse_successful_count": 0,
        "parse_failure_count": 0,
        "exact_noop_roundtrip_count": 0,
        "pack_header_count": 0,
        "packet_count": 0,
        "packet_counts_by_stream_id": {},
        "terminal_ff_bytes": 0,
        "profile_checked_video_reinsertion_path_count": 0,
        "editable_MPEG2_video_ES_source_bytes": 0,
        "preserved_noneditable_ADX_ES_source_bytes": 0,
        "container_and_packetization_source_bytes": 0,
        "english_override_count": movie_audit["english_override_count"],
        "english_overrides": movie_audit["english_overrides"],
        "failures": [],
    }
    for leaf in catalog:
        if leaf.get("bpe_source"):
            decoded_path = workspace / leaf["bpe_source"]
            if not decoded_path.is_file():
                raise ValueError(f"missing decoded BPE source: {decoded_path}")
            leaf["_decoded_payload_size"] = decoded_path.stat().st_size
        if leaf.get("source") and _source_extension(leaf["name"]) == ".at3":
            raw = (workspace / leaf["source"]).read_bytes()
            try:
                parsed_at3 = parse_at3(raw)
                leaf["_at3_reference_table_bytes"] = parsed_at3["reference_table_end"]
                leaf["_at3_node_record_count"] = (
                    parsed_at3["node_envelope"]["record_count"]
                    if parsed_at3["node_envelope"] is not None else 0
                )
                envelope = parsed_at3["node_envelope"]
                leaf["_at3_preamble_bytes"] = (
                    len(bytes.fromhex(envelope["preamble_hex"])) if envelope is not None else 0
                )
                leaf["_at3_node_record_bytes"] = (
                    sum(node["size"] for node in envelope["nodes"])
                    if envelope is not None else 0
                )
            except ValueError:
                leaf["_at3_reference_table_bytes"] = 0
                leaf["_at3_node_record_count"] = 0
                leaf["_at3_preamble_bytes"] = 0
                leaf["_at3_node_record_bytes"] = 0
        if leaf.get("source") and _source_extension(leaf["name"]) == ".ymp":
            raw = (workspace / leaf["source"]).read_bytes()
            try:
                leaf["_yobj_structural_bytes"] = parse_yobj(raw)["file_size"]
            except ValueError:
                leaf["_yobj_structural_bytes"] = 0
        if leaf.get("source") and "MOVIE.AFS;1!/" in leaf["name"]:
            raw = (workspace / leaf["source"]).read_bytes()
            movie_entry = movie_entries.get(leaf["name"])
            if movie_entry is None:
                raise ValueError(f"movie has no audited editable stream entry: {leaf['name']}")
            if (len(raw) != movie_entry["source_bytes"] or
                    hashlib.sha256(raw).hexdigest() != movie_entry["source_sha256"]):
                raise ValueError(f"movie sidecar differs from movie export index: {leaf['name']}")
            mpeg_stats["file_count"] += 1
            mpeg_stats["source_bytes"] += len(raw)
            leaf["_mpeg_program_stream"] = raw.startswith(b"\0\0\1\xba")
            try:
                parsed_mpeg = parse_mpeg_ps(raw)
                if rebuild_mpeg_ps(parsed_mpeg, raw) != raw:
                    raise ValueError("MPEG packet reassembly differs from its source")
            except ValueError as exc:
                leaf["_mpeg_ps_structural_bytes"] = 0
                mpeg_stats["parse_failure_count"] += 1
                mpeg_stats["failures"].append({"name": leaf["name"], "reason": str(exc)})
            else:
                if parsed_mpeg["sha256"] != movie_entry["source_sha256"]:
                    raise ValueError(f"parsed movie hash differs from audited source: {leaf['name']}")
                video_bytes = movie_entry["video_bytes"]
                audio_bytes = movie_entry["audio_bytes"]
                if video_bytes + audio_bytes > len(raw):
                    raise ValueError(f"extracted movie streams exceed source extent: {leaf['name']}")
                leaf["_editable_movie_video_bytes"] = video_bytes
                leaf["_movie_audio_source_bytes"] = audio_bytes
                mpeg_stats["profile_checked_video_reinsertion_path_count"] += 1
                mpeg_stats["editable_MPEG2_video_ES_source_bytes"] += video_bytes
                mpeg_stats["preserved_noneditable_ADX_ES_source_bytes"] += audio_bytes
                mpeg_stats["container_and_packetization_source_bytes"] += (
                    len(raw) - video_bytes - audio_bytes
                )
                leaf["_mpeg_program_stream"] = True
                leaf["_mpeg_ps_structural_bytes"] = parsed_mpeg["structural_bytes"]
                leaf["_mpeg_ps_packet_count"] = parsed_mpeg["packet_count"]
                mpeg_stats["parse_successful_count"] += 1
                mpeg_stats["exact_noop_roundtrip_count"] += 1
                mpeg_stats["pack_header_count"] += parsed_mpeg["pack_header_count"]
                mpeg_stats["packet_count"] += parsed_mpeg["packet_count"]
                mpeg_stats["terminal_ff_bytes"] += parsed_mpeg["terminal_ff_bytes"]
                packet_counts = mpeg_stats["packet_counts_by_stream_id"]
                for stream_id, count in parsed_mpeg["packet_counts_by_stream_id"].items():
                    packet_counts[stream_id] = packet_counts.get(stream_id, 0) + count
    if mpeg_stats["parse_successful_count"] != mpeg_stats["exact_noop_roundtrip_count"]:
        raise ValueError("MPEG program-stream no-op round-trip audit failed")
    mpeg_stats["note"] = (
        "Direct MOVIE.AFS resources use the observed sectorized CRI SofDec "
        "MPEG-2 video plus CRI ADX audio profile. Pack/PES extents and original "
        "metadata sectors rebuild with exact elementary streams. Only extracted "
        "MPEG-2 video source bytes count as semantically editable; ADX audio and "
        "container/packetization bytes remain preserved but not editable."
    )
    if mpeg_stats["file_count"] != movie_audit["movie_count"]:
        raise ValueError("movie export index count disagrees with direct stream corpus")
    if mpeg_stats["source_bytes"] != movie_audit["source_bytes"]:
        raise ValueError("movie export index byte total disagrees with direct stream corpus")
    if mpeg_stats["editable_MPEG2_video_ES_source_bytes"] != movie_audit[
            "video_elementary_stream_bytes"]:
        raise ValueError("movie video source spans disagree with the audited movie exports")
    if mpeg_stats["preserved_noneditable_ADX_ES_source_bytes"] != movie_audit[
            "audio_elementary_stream_bytes"]:
        raise ValueError("movie ADX source spans disagree with the audited movie exports")
    graphics["_mpeg_ps_resource_corpus"] = mpeg_stats

    manifest_paths = {entry["bundle_manifest"] for entry in graphics.get("entries", [])
                      if entry.get("source_kind") == "bundle"}
    manifest_paths.update(leaf["ui_bundle_source"] for leaf in catalog
                          if leaf.get("ui_bundle_source"))
    graphics["_manifest_entries"] = {
        path: _read_json(workspace / path) for path in sorted(manifest_paths)
    }

    # Audit the same structural envelope and exact no-op rebuild for direct
    # AT3 leaves and AT3 members nested in parsed UI bundles. Nested members
    # already count as bounded UI-bundle members in Z and must not be added a
    # second time to the structural numerator.
    at3_stats = {
        "direct_resources": {"file_count": 0, "source_bytes": 0,
                             "parse_successful_count": 0,
                             "parse_failure_count": 0,
                             "parsed_node_envelope_count": 0,
                             "node_preamble_bytes": 0,
                             "node_record_bytes": 0,
                             "node_record_count": 0,
                             "exact_noop_roundtrip_count": 0},
        "nested_ui_bundle_resources": {"file_count": 0, "source_bytes": 0,
                                        "parse_successful_count": 0,
                                        "parse_failure_count": 0,
                                        "parsed_node_envelope_count": 0,
                                        "node_preamble_bytes": 0,
                                        "node_record_bytes": 0,
                                        "node_record_count": 0,
                                        "exact_noop_roundtrip_count": 0},
    }

    def audit_at3(raw: bytes, stats: dict):
        stats["file_count"] += 1
        stats["source_bytes"] += len(raw)
        try:
            parsed = parse_at3(raw)
        except ValueError:
            stats["parse_failure_count"] += 1
            return
        stats["parse_successful_count"] += 1
        envelope = parsed["node_envelope"]
        if envelope is not None:
            stats["parsed_node_envelope_count"] += 1
            stats["node_preamble_bytes"] += len(bytes.fromhex(envelope["preamble_hex"]))
            stats["node_record_bytes"] += sum(node["size"] for node in envelope["nodes"])
            stats["node_record_count"] += envelope["record_count"]
        if rebuild_at3(parsed) == raw:
            stats["exact_noop_roundtrip_count"] += 1

    direct_sources = {leaf.get("source") for leaf in catalog
                      if leaf.get("source") and _source_extension(leaf["name"]) == ".at3"}
    for source in direct_sources:
        raw = (workspace / source).read_bytes()
        audit_at3(raw, at3_stats["direct_resources"])

    for manifest_path, manifest in graphics["_manifest_entries"].items():
        rel = Path(manifest_path)
        resources_dir = workspace / rel.parent / (rel.name.removesuffix(".bundle.json") + ".resources")
        for member in manifest.get("entries", []):
            if _member_extension(member) != ".at3":
                continue
            member_path = resources_dir / member["source"]
            raw = member_path.read_bytes()
            if len(raw) != member.get("size"):
                raise ValueError(f"nested AT3 size disagrees with bundle manifest: {member_path}")
            expected_hash = member.get("source_sha256")
            if expected_hash and hashlib.sha256(raw).hexdigest() != expected_hash:
                raise ValueError(f"nested AT3 hash disagrees with bundle manifest: {member_path}")
            audit_at3(raw, at3_stats["nested_ui_bundle_resources"])

    for kind, stats in at3_stats.items():
        if stats["exact_noop_roundtrip_count"] != stats["parse_successful_count"]:
            raise ValueError(f"AT3 no-op round-trip audit failed for {kind}")
    at3_stats["note"] = (
        "Validated node-envelope counts are structural only; 192-byte fixed regions and "
        "112-byte repeated regions remain opaque. Direct resources may contribute their "
        "bounded preambles and validated node records to Z, alongside the parsed "
        "reference tables. Nested UI-bundle resources are already counted as bounded "
        "child extents and are not double-counted."
    )
    graphics["_at3_resource_corpus"] = at3_stats

    # YMP resources directly listed in the archive catalog can contribute
    # their complete bounded YOBJ/POF0 envelope to Z. YMP members nested in
    # parsed UI bundles are audited too, but those bytes already count once as
    # bounded bundle children and must not be added again.
    def new_yobj_stats():
        return {"file_count": 0, "source_bytes": 0,
                "parse_successful_count": 0, "parse_failure_count": 0,
                "pof0_reference_slot_count": 0, "exact_noop_roundtrip_count": 0,
                "pof0_zero_tail_bytes": 0, "format_variants": {},
                "geometry_parse_successful_count": 0,
                "geometry_parse_failure_count": 0,
                "geometry_mesh_count": 0, "geometry_vertex_count": 0,
                "editable_xyz_source_bytes": 0,
                "exact_geometry_noop_roundtrip_count": 0,
                "geometry_failures": []}

    yobj_stats = {
        "direct_resources": new_yobj_stats(),
        "nested_ui_bundle_resources": new_yobj_stats(),
    }

    def audit_yobj(raw: bytes, stats: dict, owner: dict | None = None):
        stats["file_count"] += 1
        stats["source_bytes"] += len(raw)
        try:
            parsed = parse_yobj(raw)
        except ValueError:
            stats["parse_failure_count"] += 1
            if owner is not None:
                owner["_yobj_editable_geometry_bytes"] = 0
            return
        stats["parse_successful_count"] += 1
        stats["pof0_reference_slot_count"] += parsed["pof0_reference_count"]
        stats["pof0_zero_tail_bytes"] += parsed["pof0_zero_tail_bytes"]
        variant = parsed["variant"]
        stats["format_variants"][variant] = stats["format_variants"].get(variant, 0) + 1
        if rebuild_yobj(parsed) == raw:
            stats["exact_noop_roundtrip_count"] += 1
        try:
            geometry = export_yobj_geometry(raw)
            rebuilt_geometry = rebuild_yobj_geometry(raw, geometry)
            if rebuilt_geometry != raw:
                raise ValueError("YOBJ geometry no-op rebuild differs from its source")
        except ValueError as exc:
            stats["geometry_parse_failure_count"] += 1
            stats["geometry_failures"].append({"source": (owner or {}).get("name"),
                                               "reason": str(exc)})
            if owner is not None:
                owner["_yobj_editable_geometry_bytes"] = 0
            return
        stats["geometry_parse_successful_count"] += 1
        stats["geometry_mesh_count"] += geometry["mesh_count"]
        stats["geometry_vertex_count"] += sum(
            mesh["vertex_count"] for mesh in geometry["meshes"]
        )
        stats["editable_xyz_source_bytes"] += geometry["editable_xyz_source_bytes"]
        stats["exact_geometry_noop_roundtrip_count"] += 1
        if owner is not None:
            owner["_yobj_editable_geometry_bytes"] = geometry["editable_xyz_source_bytes"]

    for leaf in catalog:
        if leaf.get("source") and _source_extension(leaf["name"]) == ".ymp":
            audit_yobj((workspace / leaf["source"]).read_bytes(),
                       yobj_stats["direct_resources"], leaf)

    for manifest_path, manifest in graphics["_manifest_entries"].items():
        rel = Path(manifest_path)
        resources_dir = workspace / rel.parent / (
            rel.name.removesuffix(".bundle.json") + ".resources"
        )
        for member in manifest.get("entries", []):
            if _member_extension(member) != ".ymp":
                continue
            member_path = resources_dir / member["source"]
            raw = member_path.read_bytes()
            if len(raw) != member.get("size"):
                raise ValueError(f"nested YMP size disagrees with bundle manifest: {member_path}")
            expected_hash = member.get("source_sha256")
            if expected_hash and hashlib.sha256(raw).hexdigest() != expected_hash:
                raise ValueError(f"nested YMP hash disagrees with bundle manifest: {member_path}")
            audit_yobj(raw, yobj_stats["nested_ui_bundle_resources"], member)

    for kind, stats in yobj_stats.items():
        if stats["exact_noop_roundtrip_count"] != stats["parse_successful_count"]:
            raise ValueError(f"YOBJ no-op round-trip audit failed for {kind}")
        if (stats["exact_geometry_noop_roundtrip_count"] !=
                stats["geometry_parse_successful_count"] or
                stats["geometry_parse_successful_count"] +
                stats["geometry_parse_failure_count"] != stats["parse_successful_count"]):
            raise ValueError(f"YOBJ geometry audit did not account for every parsed source in {kind}")
    yobj_stats["note"] = (
        "The parser validates the 0x40-byte header envelope, four bounded "
        "numeric count/offset pairs, the exact POF0-to-EOF extent, and the "
        "delta-coded pointer-slot list. A corpus-validated same-count editor "
        "covers XYZ position and normal floats in Vector4f mesh buffers; W, "
        "vertex counts, pointers, face/UV topology, object data, skinning, and "
        "material semantics remain unchanged or opaque. Direct YMP envelopes "
        "may contribute to Z. Nested UI-bundle YMP files are already counted as "
        "bounded child extents and are not double-counted."
    )
    graphics["_yobj_resource_corpus"] = yobj_stats
    return catalog, graphics, disc, roundtrip


def _residual_category(row: dict) -> tuple[str, str]:
    """Assign a conservative inventory class; opaque bodies remain opaque."""
    name = row["name"].lower()
    extension = row["extension"]
    leaf = row.get("leaf", {})

    if row.get("editable_kind"):
        return row["editable_kind"], "indexed editable source representation"
    if row.get("is_txc"):
        return "unresolved_graphics", "TXC indexed, current pixel decoder has no editable export"
    if "movie.afs;1" in name:
        if leaf.get("_mpeg_program_stream"):
            return "video_cinematics", "MOVIE.AFS path and MPEG pack-start signature; packet parse is reported separately"
        return "video_cinematics", "MOVIE.AFS path; video format remains a candidate"
    if "bgm.afs;1" in name or "/data/sound/" in name:
        return "audio_sound_candidates", "BGM archive or sound-directory path; payload audio is not decoded"
    if extension in (".ymp", ".ypc"):
        return "model_geometry_candidates", (
            "YMP/YPC resource naming; corpus-validated YMP coordinate vectors are editable, "
            "but the remaining model fields and YPC bodies are not decoded"
        )
    if extension in (".at3", ".yap", ".mpc", ".yma"):
        return "animation_motion_candidates", "AT3/YAP/MPC/YMA name or member type; bodies are not fully decoded"
    if "/data/font/" in name:
        return "font_assets", "font resource directory path; internal font records remain unparsed"
    if extension in (".pms", ".scd", ".dat", ".txt"):
        return "scripts_event_and_data_candidates", "data/script/event extension or member type; semantics are partial"
    if (name.endswith("/slpm_661.56;1") or name.endswith(".irx;1") or
            name.endswith("ioprp300.img;1")):
        return "executables_and_modules", "boot executable/module filename; full semantics are outside this census"
    return "other_unclassified", "fallback for payload without a stronger evidence-backed inventory class"


def build_census(catalog, graphics_index, disc, roundtrip):
    """Return physical, logical, and recovery-level byte coverage data."""
    leaves = catalog
    if not isinstance(leaves, list) or not isinstance(graphics_index, dict):
        raise ValueError("catalog must be a list and graphics index an object")
    entries = graphics_index.get("entries")
    if not isinstance(entries, list):
        raise ValueError("graphics index has no entries list")

    by_source = {}
    for leaf in leaves:
        size = leaf.get("size")
        source = leaf.get("source")
        if not isinstance(size, int) or size < 0:
            raise ValueError(f"invalid source size for {leaf.get('name')!r}")
        if source:
            if source in by_source:
                raise ValueError(f"duplicate catalog source path: {source}")
            by_source[source] = leaf

    def leaf_id(leaf):
        return leaf.get("source") or f"zero:{leaf['name']}:{id(leaf)}"

    leaf_bytes = sum(leaf["size"] for leaf in leaves)
    zero_leaves = [leaf for leaf in leaves if leaf.get("zero")]
    zero_bytes = sum(leaf["size"] for leaf in zero_leaves)
    nonzero_bytes = leaf_bytes - zero_bytes
    image_bytes = disc.get("image_bytes")
    reference_hash = disc.get("sha256")
    layout = disc.get("_layout_partition")
    if not isinstance(image_bytes, int) or image_bytes < leaf_bytes:
        raise ValueError("disc image size is missing or smaller than logical leaf bytes")
    if not isinstance(layout, dict):
        raise ValueError("census requires the recursively validated physical layout partition")
    if layout.get("information_bearing_named_member_bytes") != nonzero_bytes:
        raise ValueError("physical layout nonzero named extents disagree with the asset catalog")
    if layout.get("all_zero_named_member_bytes") != zero_bytes:
        raise ValueError("physical layout zero named extents disagree with the asset catalog")
    if layout.get("named_member_count") != len(leaves):
        raise ValueError("physical layout member count disagrees with the asset catalog")
    if roundtrip.get("reference_sha256") != reference_hash:
        raise ValueError("round-trip evidence is for a different reference image")
    if roundtrip.get("reference_size") != image_bytes:
        raise ValueError("round-trip evidence has a different reference size")
    if not roundtrip.get("authenticated") or not roundtrip.get("match"):
        raise ValueError("prepared baseline round-trip is not authenticated and byte-identical")

    manifest_entries = graphics_index.get("_manifest_entries", {})
    manifest_cache = {}
    txc_rows = []
    txc_sizes = {}
    txc_status = {}
    txc_parse_status = {}
    psm_stats = defaultdict(lambda: {"count": 0, "bytes": 0, "editable_count": 0,
                                     "editable_bytes": 0, "unresolved_count": 0,
                                     "unresolved_bytes": 0})
    txc_sources = Counter()

    for entry in entries:
        source_kind = entry.get("source_kind")
        if source_kind == "standalone":
            source = entry.get("source_path")
            leaf = by_source.get(source)
            if leaf is None or _source_extension(leaf["name"]) != ".txc":
                raise ValueError(f"standalone TXC has no matching catalog leaf: {source!r}")
            size = leaf["size"]
            txc_key = ("standalone", source)
        elif source_kind == "bundle":
            manifest_path = entry.get("bundle_manifest")
            member_name = entry.get("source")
            if not manifest_path or not member_name:
                raise ValueError("bundle TXC is missing its manifest/member reference")
            if manifest_path not in manifest_cache:
                manifest = manifest_entries.get(manifest_path)
                if manifest is None:
                    raise ValueError(f"missing embedded member manifest: {manifest_path}")
                manifest_cache[manifest_path] = {
                    item["source"]: item for item in manifest.get("entries", [])
                }
            member = manifest_cache[manifest_path].get(member_name)
            if member is None:
                raise ValueError(f"manifest lacks embedded TXC member: {manifest_path}/{member_name}")
            size = member.get("size")
            if not isinstance(size, int) or size < 0:
                raise ValueError(f"invalid embedded TXC size: {manifest_path}/{member_name}")
            if member.get("source_sha256") != entry.get("source_sha256"):
                raise ValueError(f"embedded TXC hash disagrees with manifest: {manifest_path}/{member_name}")
            txc_key = ("bundle", manifest_path, member_name)
        else:
            raise ValueError(f"unknown TXC source kind: {source_kind!r}")

        key = entry.get("key")
        if not key or key in txc_sizes:
            raise ValueError(f"missing or duplicate TXC key: {key!r}")
        if txc_key in txc_status:
            raise ValueError(f"duplicate TXC source occurrence: {txc_key!r}")
        editable = bool(entry.get("image"))
        parsed = entry.get("rtx3_parse_valid")
        if not isinstance(parsed, bool):
            raise ValueError(f"TXC index lacks strict RTX3 parse status: {key!r}")
        if editable and not parsed:
            raise ValueError(f"TXC has an editable image without a valid RTX3 parse: {key!r}")
        txc_sizes[key] = size
        txc_status[txc_key] = editable
        txc_parse_status[txc_key] = parsed
        txc_rows.append((entry, size, txc_key))
        txc_sources[source_kind] += 1
        psm = entry.get("psm_name") or f"unparsed:{entry.get('unsupported_reason') or 'unknown'}"
        stats = psm_stats[psm]
        stats["count"] += 1
        stats["bytes"] += size
        if editable:
            stats["editable_count"] += 1
            stats["editable_bytes"] += size
        else:
            stats["unresolved_count"] += 1
            stats["unresolved_bytes"] += size

    txc_source_bytes = sum(size for _, size, _ in txc_rows)
    txc_editable_bytes = sum(size for entry, size, _ in txc_rows if entry.get("image"))
    txc_unresolved_bytes = txc_source_bytes - txc_editable_bytes
    txc_editable_count = sum(bool(entry.get("image")) for entry, _, _ in txc_rows)
    catalog_txc = {leaf_id(leaf) for leaf in leaves
                   if _source_extension(leaf["name"]) == ".txc"}
    indexed_standalone = {leaf_id(by_source[key[1]]) for key in txc_status
                          if key[0] == "standalone"}
    if catalog_txc != indexed_standalone:
        missing = sorted(catalog_txc - indexed_standalone)[:3]
        extra = sorted(indexed_standalone - catalog_txc)[:3]
        raise ValueError(f"standalone TXC index/catalog mismatch (missing={missing}, extra={extra})")

    bpe = [leaf for leaf in leaves if leaf.get("bpe_source")]
    parsed_bpe = [leaf for leaf in bpe if leaf.get("ui_bundle_source")]
    unparsed_bpe = [leaf for leaf in bpe if not leaf.get("ui_bundle_source")]
    text = [leaf for leaf in leaves if leaf.get("text_source")]
    messages = [leaf for leaf in leaves if leaf.get("message_source")]
    text_bytes = sum(leaf["size"] for leaf in text)
    message_bytes = sum(leaf["size"] for leaf in messages)

    # Create a de-duplicated expanded content inventory. A compressed .b leaf
    # is replaced by decoded member payloads; table/gap bytes are not content.
    expanded_rows = []
    parsed_bundle_member_bytes = 0
    nested_txc_bytes = 0
    for leaf in leaves:
        if leaf.get("zero") or leaf["size"] == 0:
            continue
        if leaf.get("bpe_source"):
            if leaf.get("ui_bundle_source"):
                manifest_path = leaf["ui_bundle_source"]
                manifest = manifest_entries.get(manifest_path)
                if manifest is None:
                    raise ValueError(f"missing UI bundle manifest: {manifest_path}")
                for member in manifest.get("entries", []):
                    size = member.get("size")
                    if not isinstance(size, int) or size < 0:
                        raise ValueError(f"invalid UI bundle member size: {manifest_path}/{member.get('source')}")
                    name = f"{leaf['name']}!/{member['source']}"
                    extension = _member_extension(member)
                    row = {"name": name, "size": size, "extension": extension,
                           "origin": "parsed_ui_bundle_member", "leaf": leaf,
                           "member": member, "manifest_path": manifest_path,
                           "editable_kind": None, "is_txc": extension == ".txc",
                           "structural_bytes": size if extension != ".txc" else 0,
                           "semantic_editable_bytes": 0}
                    if extension == ".ymp":
                        row["semantic_editable_bytes"] = member.get(
                            "_yobj_editable_geometry_bytes", 0
                        )
                    if row["is_txc"]:
                        key = ("bundle", manifest_path, member["source"])
                        if key not in txc_status:
                            raise ValueError(f"bundle TXC is absent from graphics index: {manifest_path}/{member['source']}")
                        row["structural_bytes"] = size if txc_parse_status[key] else 0
                        row["editable_kind"] = "editable_graphics" if txc_status[key] else None
                        row["semantic_editable_bytes"] = size if txc_status[key] else 0
                        row["unresolved_txc"] = not txc_status[key]
                        nested_txc_bytes += size
                    parsed_bundle_member_bytes += size
                    expanded_rows.append(row)
            else:
                size = leaf.get("_decoded_payload_size", leaf.get("bpe_decoded_size"))
                if not isinstance(size, int) or size < 0:
                    raise ValueError(f"decoded BPE length missing for {leaf['name']}")
                expanded_rows.append({
                    "name": leaf["name"].removesuffix(".b") + "[decoded]",
                    "size": size,
                    "extension": ".yma" if "_yma.b" in leaf["name"].lower() else "[unknown]",
                    "origin": "decoded_but_bundle_unparsed", "leaf": leaf,
                    "editable_kind": None, "is_txc": False,
                    "structural_bytes": 0, "semantic_editable_bytes": 0,
                })
            continue

        extension = _source_extension(leaf["name"])
        row = {"name": leaf["name"], "size": leaf["size"], "extension": extension,
               "origin": "terminal_leaf", "leaf": leaf,
               "editable_kind": None, "is_txc": extension == ".txc",
               "structural_bytes": 0, "semantic_editable_bytes": 0}
        if row["is_txc"]:
            key = ("standalone", leaf["source"])
            if key not in txc_status:
                raise ValueError(f"standalone TXC is absent from graphics index: {leaf['name']}")
            row["structural_bytes"] = leaf["size"] if txc_parse_status[key] else 0
            if txc_status[key]:
                row["editable_kind"] = "editable_graphics"
                row["semantic_editable_bytes"] = leaf["size"]
            else:
                row["unresolved_txc"] = True
        elif leaf.get("text_source") or leaf.get("message_source"):
            row["editable_kind"] = "editable_text_and_catalogs"
            row["structural_bytes"] = leaf["size"]
            row["semantic_editable_bytes"] = leaf["size"]
        elif extension == ".at3":
            row["structural_bytes"] = (leaf.get("_at3_reference_table_bytes", 0) +
                                        leaf.get("_at3_preamble_bytes", 0) +
                                        leaf.get("_at3_node_record_bytes", 0))
        elif extension == ".ymp":
            row["structural_bytes"] = leaf.get("_yobj_structural_bytes", 0)
            row["semantic_editable_bytes"] = leaf.get(
                "_yobj_editable_geometry_bytes", 0
            )
        elif leaf.get("_mpeg_ps_structural_bytes"):
            row["structural_bytes"] = leaf["_mpeg_ps_structural_bytes"]
            row["semantic_editable_bytes"] = leaf.get(
                "_editable_movie_video_bytes", 0
            )
        expanded_rows.append(row)

    expanded_payload_bytes = sum(row["size"] for row in expanded_rows)
    compressed_bpe_bytes = sum(leaf["size"] for leaf in bpe if not leaf.get("zero"))
    if expanded_payload_bytes != nonzero_bytes - compressed_bpe_bytes + parsed_bundle_member_bytes + sum(
            leaf.get("_decoded_payload_size", leaf.get("bpe_decoded_size", 0)) or 0
            for leaf in unparsed_bpe):
        raise ValueError("expanded logical payload does not balance against physical source leaves")
    if nested_txc_bytes != sum(size for entry, size, key in txc_rows if key[0] == "bundle"):
        raise ValueError("nested TXC member total disagrees with the graphics index")

    editable_graphics = txc_editable_bytes
    semantically_editable_bytes = sum(row["semantic_editable_bytes"] for row in expanded_rows)
    row_model_geometry_bytes = sum(
        row["semantic_editable_bytes"] for row in expanded_rows
        if row["extension"] == ".ymp"
    )
    yobj_corpus = graphics_index.get("_yobj_resource_corpus", {})
    editable_model_geometry_bytes = sum(
        stats.get("editable_xyz_source_bytes", 0)
        for stats in yobj_corpus.values() if isinstance(stats, dict)
    )
    if row_model_geometry_bytes != editable_model_geometry_bytes:
        raise ValueError("editable YOBJ geometry spans disagree with the audited model corpus")
    editable_movie_video_bytes = sum(
        leaf.get("_editable_movie_video_bytes", 0) for leaf in leaves
    )
    row_movie_video_bytes = sum(
        row["semantic_editable_bytes"] for row in expanded_rows
        if row.get("leaf", {}).get("_editable_movie_video_bytes")
    )
    if row_movie_video_bytes != editable_movie_video_bytes:
        raise ValueError("editable movie video spans disagree with the audited movie corpus")
    expected_editable_bytes = (editable_graphics + text_bytes + message_bytes +
                               editable_model_geometry_bytes + editable_movie_video_bytes)
    if semantically_editable_bytes != expected_editable_bytes:
        raise ValueError("editable source spans do not match indexed texture/text sources")
    remaining_bytes = expanded_payload_bytes - semantically_editable_bytes
    if remaining_bytes < 0:
        raise ValueError("semantic editable byte count exceeds the logical content denominator")

    # Z counts complete RTX3 parses, validated child-member extents,
    # reversible text/catalog sources, and directly parsed AT3 regions. The
    # known-short RTX3 files have visible headers but failed their complete
    # extent contract, so their bodies stay outside Z until the format is proven.
    bundle_nontexture_member_bytes = parsed_bundle_member_bytes - nested_txc_bytes
    direct_at3_table_bytes = sum(leaf.get("_at3_reference_table_bytes", 0) for leaf in leaves
                                 if _source_extension(leaf["name"]) == ".at3")
    direct_at3_preamble_bytes = sum(
        leaf.get("_at3_preamble_bytes", 0) for leaf in leaves
        if _source_extension(leaf["name"]) == ".at3"
    )
    direct_at3_node_record_bytes = sum(
        leaf.get("_at3_node_record_bytes", 0) for leaf in leaves
        if _source_extension(leaf["name"]) == ".at3"
    )
    direct_yobj_file_bytes = sum(
        leaf.get("_yobj_structural_bytes", 0) for leaf in leaves
        if _source_extension(leaf["name"]) == ".ymp"
    )
    direct_mpeg_ps_file_bytes = sum(
        leaf.get("_mpeg_ps_structural_bytes", 0) for leaf in leaves
        if "MOVIE.AFS;1!/" in leaf["name"]
    )
    txc_structural_bytes = sum(size for entry, size, key in txc_rows
                               if txc_parse_status[key])
    structurally_classified_bytes = (txc_structural_bytes + bundle_nontexture_member_bytes +
                                     text_bytes + message_bytes + direct_at3_table_bytes +
                                     direct_at3_preamble_bytes + direct_at3_node_record_bytes +
                                     direct_yobj_file_bytes + direct_mpeg_ps_file_bytes)
    row_structural_bytes = sum(row["structural_bytes"] for row in expanded_rows)
    if row_structural_bytes != structurally_classified_bytes:
        raise ValueError("parser-backed structural spans overlap or disagree with their components")
    if structurally_classified_bytes > expanded_payload_bytes:
        raise ValueError("structural byte ranges overlap or exceed the logical payload")
    if semantically_editable_bytes > structurally_classified_bytes:
        raise ValueError("semantic editability exceeds structurally validated coverage")

    structurally_classified_not_editable = structurally_classified_bytes - semantically_editable_bytes
    opaque_bytes = expanded_payload_bytes - structurally_classified_bytes

    remainder_totals = Counter()
    remainder_counts = Counter()
    remainder_basis = {}
    def add_remainder(name: str, basis: str, byte_count: int):
        if byte_count <= 0:
            return
        remainder_totals[name] += byte_count
        remainder_counts[name] += 1
        remainder_basis[name] = basis

    for row in expanded_rows:
        remaining_row_bytes = row["size"] - row["semantic_editable_bytes"]
        if remaining_row_bytes == 0:
            continue
        leaf = row.get("leaf", {})
        if leaf.get("_movie_audio_source_bytes"):
            audio_bytes = leaf["_movie_audio_source_bytes"]
            if audio_bytes > remaining_row_bytes:
                raise ValueError(f"ADX remainder exceeds movie noneditable bytes: {row['name']}")
            add_remainder(
                "audio_sound_candidates",
                "Verified CRI ADX elementary stream; source is preserved but has no authored audio override path.",
                audio_bytes,
            )
            add_remainder(
                "video_container_and_packetization",
                "Remaining MOVIE.AFS SofDec sectors, CRI metadata, PES framing, and padding after editable MPEG-2 video and preserved ADX stream extraction.",
                remaining_row_bytes - audio_bytes,
            )
            continue
        category_name, basis = _residual_category(row)
        add_remainder(category_name, basis, remaining_row_bytes)
    if sum(remainder_totals.values()) != remaining_bytes:
        raise ValueError("exclusive remaining-payload categories do not sum to Y minus B")
    remaining_categories = [
        {"name": name, "file_count": remainder_counts[name], "source_bytes": size,
         "percent_of_remaining_payload": _percent(size, remaining_bytes),
         "percent_of_expanded_payload": _percent(size, expanded_payload_bytes),
         "classification_basis": remainder_basis[name]}
        for name, size in sorted(remainder_totals.items(), key=lambda item: (-item[1], item[0]))
    ]

    opaque_totals = Counter()
    opaque_counts = Counter()
    opaque_basis = {}
    for row in expanded_rows:
        row_opaque_bytes = row["size"] - row["structural_bytes"]
        if row_opaque_bytes == 0:
            continue
        category_name, basis = _residual_category(row)
        opaque_totals[category_name] += row_opaque_bytes
        opaque_counts[category_name] += 1
        opaque_basis[category_name] = basis
    if sum(opaque_totals.values()) != opaque_bytes:
        raise ValueError("exclusive opaque-byte categories do not sum to Y minus Z")
    opaque_categories = [
        {"name": name, "file_count": opaque_counts[name], "source_bytes": size,
         "percent_of_opaque_payload": _percent(size, opaque_bytes),
         "percent_of_expanded_payload": _percent(size, expanded_payload_bytes),
         "classification_basis": opaque_basis[name]}
        for name, size in sorted(opaque_totals.items(), key=lambda item: (-item[1], item[0]))
    ]

    psm_report = {
        key: {**stats,
              "editable_percent_of_psm_bytes": _percent(stats["editable_bytes"], stats["bytes"])}
        for key, stats in sorted(psm_stats.items())
    }
    bundle_manifests = manifest_entries
    bundle_txc_rows = [row for row in expanded_rows if row["origin"] == "parsed_ui_bundle_member"
                       and row["is_txc"]]
    source_categories = {
        "standalone": {
            "entry_count": txc_sources["standalone"],
            "source_bytes": sum(size for _, size, key in txc_rows if key[0] == "standalone"),
        },
        "embedded_in_menu_bpe_bundles": {
            "entry_count": txc_sources["bundle"],
            "expanded_txc_payload_bytes": nested_txc_bytes,
            "editable_txc_payload_bytes": sum(row["size"] for row in bundle_txc_rows
                                               if row["editable_kind"] == "editable_graphics"),
            "parsed_menu_bpe_leaf_count": len(parsed_bpe),
            "bundle_manifest_count_with_indexed_txc": len({
                entry["bundle_manifest"] for entry, _, key in txc_rows if key[0] == "bundle"
            }),
            "bundle_member_count": sum(len(manifest.get("entries", []))
                                        for manifest in bundle_manifests.values()),
        },
    }
    texture_corpus = {
        "entry_count": len(txc_rows),
        "expanded_txc_payload_bytes": txc_source_bytes,
        "editable_entry_count": txc_editable_count,
        "editable_entry_percent": _percent(txc_editable_count, len(txc_rows)),
        "editable_txc_payload_bytes": txc_editable_bytes,
        "editable_txc_byte_percent": _percent(txc_editable_bytes, txc_source_bytes),
        "unresolved_entry_count": len(txc_rows) - txc_editable_count,
        "unresolved_txc_payload_bytes": txc_unresolved_bytes,
        "unresolved_txc_byte_percent": _percent(txc_unresolved_bytes, txc_source_bytes),
        "source_kinds": source_categories,
        "psm_byte_breakdown": psm_report,
        "accounting_note": "Expanded TXC payload includes standalone and nested members once. Nested textures are not added a second time on top of their expanded UI-bundle members.",
    }

    extensions = defaultdict(lambda: {"file_count": 0, "source_bytes": 0})
    for leaf in leaves:
        item = extensions[_source_extension(leaf["name"])]
        item["file_count"] += 1
        item["source_bytes"] += leaf["size"]
    extensions = dict(sorted(extensions.items(), key=lambda item: (-item[1]["source_bytes"], item[0])))

    zero_span_bytes = layout["all_zero_named_member_bytes"] + layout["all_zero_gap_bytes"]
    return {
        "schema_version": 8,
        "evidence_date": dt.date.today().isoformat(),
        "reference_sha256": reference_hash,
        "scope": "Pinned physical image partition plus a de-duplicated expanded logical content inventory; recovery levels have separate definitions and evidence.",
        "physical_disc_accounting": {
            "image_bytes": image_bytes,
            "named_member_count": layout["named_member_count"],
            "all_zero_named_member_count": layout["all_zero_named_member_count"],
            "all_zero_named_member_bytes": layout["all_zero_named_member_bytes"],
            "all_zero_named_member_percent_of_image": _percent(layout["all_zero_named_member_bytes"], image_bytes),
            "all_zero_gap_bytes": layout["all_zero_gap_bytes"],
            "all_zero_gap_percent_of_image": _percent(layout["all_zero_gap_bytes"], image_bytes),
            "measured_all_zero_bytes": zero_span_bytes,
            "measured_all_zero_percent_of_image": _percent(zero_span_bytes, image_bytes),
            "intentional_zero_padding_bytes": None,
            "zero_byte_purpose_established": False,
            "zero_byte_interpretation": "Measured by byte value only; intentional padding or placeholder use is not established.",
            "information_bearing_terminal_member_bytes": layout["information_bearing_named_member_bytes"],
            "information_bearing_terminal_member_count": layout["information_bearing_named_member_count"],
            "information_bearing_terminal_member_percent_of_image": _percent(nonzero_bytes, image_bytes),
            "nonzero_unassigned_gap_or_structure_bytes": layout["nonzero_gap_bytes"],
            "all_zero_gap_span_count": layout["all_zero_gap_span_count"],
            "nonzero_unassigned_gap_or_structure_percent_of_image": _percent(layout["nonzero_gap_bytes"], image_bytes),
            "nonzero_gap_span_count": layout["nonzero_gap_span_count"],
            "partition_bytes": zero_span_bytes + nonzero_bytes + layout["nonzero_gap_bytes"],
            "partition_matches_image": zero_span_bytes + nonzero_bytes + layout["nonzero_gap_bytes"] == image_bytes,
            "terminal_leaf_count": len(leaves),
            "zero_length_terminal_leaf_count": sum(leaf["size"] == 0 for leaf in leaves),
            "terminal_leaf_source_bytes_including_all_zero_members": leaf_bytes,
            "layout_evidence": "Recursively validated ISO/AFS/YFS/PAC layout pieces; parent container extents are replaced by child pieces to avoid double counting.",
            "round_trip": {
                "authenticated": roundtrip["authenticated"],
                "byte_identical": roundtrip["match"],
                "differing_bytes": roundtrip.get("differing_bytes"),
                "rebuilt_bytes": roundtrip.get("rebuilt_size"),
                "rebuilt_sha256": roundtrip.get("rebuilt_sha256"),
                "evidence_file": "reports/assets-roundtrip-prepared.json",
            },
        },
        "expanded_logical_payload": {
            "information_bearing_payload_bytes_Y": expanded_payload_bytes,
            "expanded_payload_percent_of_physical_image": _percent(expanded_payload_bytes, image_bytes),
            "definition": "Sum of nonzero terminal member payloads, replacing each compressed BPE .b source leaf with its decoded UI-bundle member extents or raw decoded payload. Bundle table/gap bytes and compressed wrappers are excluded; nested members are counted once.",
            "physical_nonzero_terminal_member_bytes_before_expansion": nonzero_bytes,
            "compressed_bpe_wrapper_bytes_replaced": compressed_bpe_bytes,
            "parsed_ui_bundle_member_payload_bytes_added": parsed_bundle_member_bytes,
            "raw_unparsed_bpe_payload_bytes_added": sum(
                leaf.get("_decoded_payload_size", leaf.get("bpe_decoded_size", 0)) or 0
                for leaf in unparsed_bpe),
            "expansion_delta_vs_physical_terminal_members": expanded_payload_bytes - nonzero_bytes,
            "recovery_levels": {
                "container_hierarchy_addressed": {
                    "bytes": nonzero_bytes,
                    "denominator_bytes": nonzero_bytes,
                    "percent": 100.0,
                    "meaning": "Every nonzero physical terminal member has a named catalog path and a validated parent extent. This says nothing about the member's internal format or semantics.",
                },
                "structurally_classified": {
                    "bytes_Z": structurally_classified_bytes,
                    "denominator_bytes_Y": expanded_payload_bytes,
                    "percent_Z_of_Y": _percent(structurally_classified_bytes, expanded_payload_bytes),
                    "components": {
                        "complete_RTX3_parser_validated_extents": txc_structural_bytes,
                        "parsed_UI_bundle_nontexture_member_extents": bundle_nontexture_member_bytes,
                        "reversible_CP932_text_and_message_source_bytes": text_bytes + message_bytes,
                        "direct_AT3_reference_table_bytes": direct_at3_table_bytes,
                        "direct_AT3_bounded_preamble_bytes": direct_at3_preamble_bytes,
                        "direct_AT3_validated_node_record_bytes": direct_at3_node_record_bytes,
                        "direct_YOBJ_YMP_validated_envelope_bytes": direct_yobj_file_bytes,
                        "direct_MPEG_PS_validated_packet_and_sector_bytes": direct_mpeg_ps_file_bytes,
                    },
                    "meaning": "Bytes assigned to complete parser-validated records or bounded child extents, de-duplicated across nested TXCs. The 43 RTX3 records that fail the complete length contract are excluded. Direct AT3 preambles and node envelopes, YOBJ/YMP envelopes, and sectorized CRI SofDec MPEG pack/PES framing are structurally validated; media payload semantics are reported separately.",
                },
                "losslessly_rebuildable": {
                    "bytes_A": expanded_payload_bytes,
                    "denominator_bytes_Y": expanded_payload_bytes,
                    "percent_A_of_Y": _percent(expanded_payload_bytes, expanded_payload_bytes),
                    "evidence": "The authenticated prepared workspace rebuild is byte-identical to the pinned full disc; parsed UI bundles also have exact no-op reassembly evidence.",
                    "meaning": "All payload bytes are preserved by an authenticated unchanged-input no-op rebuild. This does not claim that arbitrary edits, growth, relocation, or runtime behavior are lossless or correct.",
                },
                "semantically_editable": {
                    "bytes_B": semantically_editable_bytes,
                    "denominator_bytes_Y": expanded_payload_bytes,
                    "percent_B_of_Y": _percent(semantically_editable_bytes, expanded_payload_bytes),
                    "components": {
                        "supported_editable_TGA_texture_source_bytes": editable_graphics,
                        "reversible_text_companion_source_bytes": text_bytes,
                        "structured_message_catalog_source_bytes": message_bytes,
                        "editable_YOBJ_position_and_normal_source_bytes": editable_model_geometry_bytes,
                        "editable_MPEG2_video_elementary_stream_source_bytes": editable_movie_video_bytes,
                    },
                    "component_percentages_of_Y": {
                        "supported_editable_TGA_texture_source_bytes": _percent(
                            editable_graphics, expanded_payload_bytes
                        ),
                        "reversible_text_companion_source_bytes": _percent(
                            text_bytes, expanded_payload_bytes
                        ),
                        "structured_message_catalog_source_bytes": _percent(
                            message_bytes, expanded_payload_bytes
                        ),
                        "editable_YOBJ_position_and_normal_source_bytes": _percent(
                            editable_model_geometry_bytes, expanded_payload_bytes
                        ),
                        "editable_MPEG2_video_elementary_stream_source_bytes": _percent(
                            editable_movie_video_bytes, expanded_payload_bytes
                        ),
                    },
                    "meaning": "A source representation has an evidence-backed editable representation and insertion path. For partially editable resources only validated source fields count: YOBJ XYZ spans and extracted MPEG-2 video elementary-stream bytes. Movie audio and container bytes remain outside B. This measures editability, not the fraction already translated.",
                },
                "runtime_validated_editable": {
                    "bytes_C": 0,
                    "denominator_bytes_Y": expanded_payload_bytes,
                    "percent_C_of_Y": 0.0,
                    "meaning": "No edited payload in this census has passed in-game runtime validation.",
                },
            },
            "remaining_after_semantic_editability": {
                "bytes": remaining_bytes,
                "denominator_bytes_Y": expanded_payload_bytes,
                "percent_of_Y": _percent(remaining_bytes, expanded_payload_bytes),
                "exclusive_byte_weighted_categories": remaining_categories,
                "accounting_note": "Categories partition Y minus B. This is the complete non-editable work queue, including spans whose container bounds or record structure are known; it is not synonymous with fully opaque bytes.",
            },
            "classified_but_not_semantically_editable": {
                "bytes": structurally_classified_not_editable,
                "denominator_bytes_Y": expanded_payload_bytes,
                "percent_of_Y": _percent(structurally_classified_not_editable, expanded_payload_bytes),
                "definition": "Z minus B: parser-classified spans without an evidence-backed semantic editing representation.",
            },
            "opaque_after_structural_classification": {
                "bytes": opaque_bytes,
                "denominator_bytes_Y": expanded_payload_bytes,
                "percent_of_Y": _percent(opaque_bytes, expanded_payload_bytes),
                "exclusive_byte_weighted_categories": opaque_categories,
                "accounting_note": "Categories partition Y minus Z: bytes without one of the explicit parser-backed structural classifications used by Z. This is not a census of every semantically opaque field inside structurally bounded records; filenames and paths provide only candidate inventory labels.",
            },
        },
        "texture_corpus": texture_corpus,
        "animation_resource_corpus": graphics_index.get("_at3_resource_corpus", {}),
        "model_resource_corpus": yobj_corpus,
        "video_resource_corpus": graphics_index.get("_mpeg_ps_resource_corpus", {}),
        "logical_leaf_extensions": extensions,
        "limits": [
            "All-zero members and gaps are measured by byte value only. Their zero contents do not prove intentional padding, placeholder use, or historical purpose.",
            "Information-bearing means a named terminal member extent that is not wholly zero. Zero-valued bytes inside a nonzero member are retained in its full extent.",
            "Expanded logical payload is a normalized content inventory, not a second physical disc size; it replaces compressed BPE wrappers with decoded child payloads and excludes bundle control/gap bytes.",
            "The structural numerator counts only the explicit parser-backed extents listed. Records counted in Z can still contain semantically opaque fields or payloads. Container hierarchy addressing is reported separately and must not be mistaken for semantic understanding.",
            "The video B numerator counts only extracted MPEG-2 video elementary-stream bytes covered by an audited profile-compatible override and source-preserving remux path. ADX audio and SofDec container/packetization bytes remain noneditable.",
            "A byte-identical unchanged rebuild proves source preservation. It does not prove relocation correctness for every edit or runtime correctness.",
            "Candidate remainder classes rely on signatures, member types, extensions, or directory names as documented; unparsed member bodies are not claimed to be semantically recovered.",
            "Generated TGAs and YOBJ geometry JSON are editable representations; their output sizes are not counted as original source bytes. YOBJ contributes only validated XYZ position/normal float spans, not opaque model bytes.",
        ],
    }


def format_census_summary(report: dict) -> str:
    """Format the independent physical, recovery, and remaining-byte measures."""
    physical = report["physical_disc_accounting"]
    logical = report["expanded_logical_payload"]
    recovery = logical["recovery_levels"]
    image_bytes = physical["image_bytes"]
    lines = [
        f"Disc image: {image_bytes / 1_000_000_000:.3f} GB ({image_bytes:,} bytes)",
        "Measured all-zero members/gaps (padding intent unverified): "
        f"{physical['measured_all_zero_bytes'] / 1_000_000_000:.3f} GB "
        f"({physical['measured_all_zero_percent_of_image']:.4f}% of disc)",
        "Intentional zero/padding: not established from byte contents alone",
        "Information-bearing physical terminal members: "
        f"{physical['information_bearing_terminal_member_bytes'] / 1_000_000_000:.3f} GB "
        f"({physical['information_bearing_terminal_member_percent_of_image']:.4f}% of disc)",
        "Nonzero unassigned gap/structure bytes: "
        f"{physical['nonzero_unassigned_gap_or_structure_bytes'] / 1_000_000_000:.3f} GB "
        f"({physical['nonzero_unassigned_gap_or_structure_percent_of_image']:.4f}% of disc)",
        "Expanded information-bearing logical payload Y: "
        f"{logical['information_bearing_payload_bytes_Y'] / 1_000_000_000:.3f} GB "
        f"({logical['expanded_payload_percent_of_physical_image']:.4f}% of physical image)",
    ]
    hierarchy = recovery["container_hierarchy_addressed"]
    lines.append(
        "Container hierarchy addressed (physical named members): "
        f"{hierarchy['bytes']:,}/{hierarchy['denominator_bytes']:,} bytes "
        f"({hierarchy['percent']:.4f}%; separate from Y)"
    )

    for name, bytes_key, percent_key, label in (
        ("structurally_classified", "bytes_Z", "percent_Z_of_Y", "Structurally classified Z/Y"),
        ("losslessly_rebuildable", "bytes_A", "percent_A_of_Y",
         "Losslessly rebuildable from unchanged inputs A/Y"),
        ("semantically_editable", "bytes_B", "percent_B_of_Y", "Semantically editable B/Y"),
        ("runtime_validated_editable", "bytes_C", "percent_C_of_Y",
         "Runtime-validated editable C/Y"),
    ):
        row = recovery[name]
        lines.append(
            f"{label}: {row[bytes_key]:,}/{row['denominator_bytes_Y']:,} bytes "
            f"({row[percent_key]:.4f}%)"
        )
    lines.append(
        "Z is parser-backed structure, not necessarily semantic understanding; "
        "A is unchanged-input preservation; B is editable source plus an insertion path."
    )
    editable = recovery["semantically_editable"]
    lines.append("Semantically editable source components (% of Y; rounded independently):")
    for name, source_bytes in editable["components"].items():
        label = name.removesuffix("_source_bytes").replace("_", " ")
        percent = editable["component_percentages_of_Y"][name]
        lines.append(f"  {label}: {source_bytes:,} bytes ({percent:.4f}%)")

    video = report.get("video_resource_corpus", {})
    if video.get("file_count"):
        lines.append(
            "Movie source split: "
            f"{video.get('editable_MPEG2_video_ES_source_bytes', 0):,} editable MPEG-2 video ES bytes; "
            f"{video.get('preserved_noneditable_ADX_ES_source_bytes', 0):,} preserved, noneditable ADX bytes; "
            f"{video.get('container_and_packetization_source_bytes', 0):,} container/packetization bytes"
        )

    classified_only = logical["classified_but_not_semantically_editable"]
    remaining = logical["remaining_after_semantic_editability"]
    opaque = logical["opaque_after_structural_classification"]
    lines.extend((
        f"Classified but not editable Z-B: {classified_only['bytes']:,} bytes "
        f"({classified_only['percent_of_Y']:.4f}% of Y)",
        f"All non-editable payload Y-B: {remaining['bytes']:,} bytes "
        f"({remaining['percent_of_Y']:.4f}% of Y)",
        "Y-B byte breakdown (% of Y-B):",
    ))
    for item in remaining["exclusive_byte_weighted_categories"]:
        label = item["name"].replace("_", " ")
        lines.append(
            f"  {label}: {item['source_bytes']:,} bytes "
            f"({item['percent_of_remaining_payload']:.4f}%)"
        )
    lines.extend((
        f"Strictly unclassified payload Y-Z: {opaque['bytes']:,} bytes "
        f"({opaque['percent_of_Y']:.4f}% of Y)",
        "Y-Z structurally unclassified inventory (% of Y-Z; not all semantic opacity):",
    ))
    for item in opaque["exclusive_byte_weighted_categories"]:
        label = item["name"].replace("_", " ")
        lines.append(
            f"  {label}: {item['source_bytes']:,} bytes "
            f"({item['percent_of_opaque_payload']:.4f}%)"
        )
    return "\n".join(lines)


def format_census_markdown(report: dict) -> str:
    """Render a durable human-readable report without merging evidence levels."""
    physical = report["physical_disc_accounting"]
    logical = report["expanded_logical_payload"]
    recovery = logical["recovery_levels"]
    image_bytes = physical["image_bytes"]
    payload_bytes = logical["information_bearing_payload_bytes_Y"]

    def gb(byte_count: int) -> str:
        return f"{byte_count / 1_000_000_000:.2f} GB"

    def byte_label(byte_count: int) -> str:
        return f"{gb(byte_count)} ({byte_count:,} bytes)"

    def category_label(name: str) -> str:
        labels = {
            "audio_sound_candidates": "Audio/sound candidates",
            "model_geometry_candidates": "Model/geometry candidates",
            "animation_motion_candidates": "Animation/motion candidates",
            "video_container_and_packetization": "Video container/packetization",
            "executables_and_modules": "Executables/modules",
            "other_unclassified": "Other unclassified",
            "font_assets": "Font assets",
            "scripts_event_and_data_candidates": "Scripts/event/data candidates",
            "unresolved_graphics": "Unresolved graphics",
        }
        return labels.get(name, name.replace("_", " ").capitalize())

    lines = [
        "# Byte-weighted asset recovery census",
        "",
        f"Evidence date: {report['evidence_date']}",
        "",
        f"Pinned reference SHA-256: `{report['reference_sha256']}`",
        "",
        "## Physical disc accounting",
        "",
        f"**Disc image:** {byte_label(image_bytes)}.",
        "",
        "These disjoint physical spans sum to the image size:",
        "",
        "| Physical span | Bytes | Share of image |",
        "| --- | ---: | ---: |",
        (f"| All-zero named members | {physical['all_zero_named_member_bytes']:,} | "
         f"{physical['all_zero_named_member_percent_of_image']:.4f}% |"),
        (f"| All-zero gaps | {physical['all_zero_gap_bytes']:,} | "
         f"{physical['all_zero_gap_percent_of_image']:.4f}% |"),
        (f"| Information-bearing terminal members | "
         f"{physical['information_bearing_terminal_member_bytes']:,} | "
         f"{physical['information_bearing_terminal_member_percent_of_image']:.4f}% |"),
        (f"| Nonzero unassigned gaps/structure | "
         f"{physical['nonzero_unassigned_gap_or_structure_bytes']:,} | "
         f"{physical['nonzero_unassigned_gap_or_structure_percent_of_image']:.4f}% |"),
        "",
        (f"Measured all-zero bytes total {byte_label(physical['measured_all_zero_bytes'])} "
         f"({physical['measured_all_zero_percent_of_image']:.4f}% of the image). "
         "**Intentional zero/padding: not established.** Zero contents alone do not "
         "prove the spans were padding or placeholders."),
        "",
        "## Recovery levels",
        "",
        (f"**Expanded information-bearing payload Y:** {byte_label(payload_bytes)} "
         f"({logical['expanded_payload_percent_of_physical_image']:.4f}% of the physical image). "
         "Compressed BPE wrappers are replaced by their decoded member payloads once; "
         "bundle control and gap bytes are excluded."),
        "",
        "| Measure | Covered bytes / denominator | Coverage | Evidence represented |",
        "| --- | ---: | ---: | --- |",
        (f"| Container hierarchy addressed | "
         f"{recovery['container_hierarchy_addressed']['bytes']:,} / "
         f"{recovery['container_hierarchy_addressed']['denominator_bytes']:,} physical member bytes | "
         f"{recovery['container_hierarchy_addressed']['percent']:.4f}% | "
         "Named path and validated parent extent; separate from Y |"),
        (f"| Structurally classified Z/Y | {recovery['structurally_classified']['bytes_Z']:,} / "
         f"{payload_bytes:,} | {recovery['structurally_classified']['percent_Z_of_Y']:.4f}% | "
         "Parser-backed records or bounded extents |"),
        (f"| Losslessly rebuildable A/Y | {recovery['losslessly_rebuildable']['bytes_A']:,} / "
         f"{payload_bytes:,} | {recovery['losslessly_rebuildable']['percent_A_of_Y']:.4f}% | "
         "Authenticated unchanged-input rebuild |"),
        (f"| Semantically editable B/Y | {recovery['semantically_editable']['bytes_B']:,} / "
         f"{payload_bytes:,} | {recovery['semantically_editable']['percent_B_of_Y']:.4f}% | "
         "Editable source representation and insertion path |"),
        (f"| Runtime-validated editable C/Y | {recovery['runtime_validated_editable']['bytes_C']:,} / "
         f"{payload_bytes:,} | {recovery['runtime_validated_editable']['percent_C_of_Y']:.4f}% | "
         "Edited payload passed in-game runtime validation |"),
        "",
        "These are independent evidence levels, not a combined decompilation or translation percentage. "
        "In particular, B measures available editable representations, not how much content has been translated.",
        "",
        "### Editable source bytes counted in B",
        "",
        "| Editable source surface | Source bytes | Share of Y |",
        "| --- | ---: | ---: |",
    ]
    editable = recovery["semantically_editable"]
    component_labels = {
        "supported_editable_TGA_texture_source_bytes": "Editable texture source bytes",
        "reversible_text_companion_source_bytes": "Reversible text companions",
        "structured_message_catalog_source_bytes": "Structured message catalog",
        "editable_YOBJ_position_and_normal_source_bytes": "YOBJ position/normal XYZ fields",
        "editable_MPEG2_video_elementary_stream_source_bytes": "MPEG-2 video elementary streams",
    }
    for name, source_bytes in editable["components"].items():
        lines.append(
            f"| {component_labels.get(name, name.replace('_source_bytes', '').replace('_', ' '))} | "
            f"{source_bytes:,} | {editable['component_percentages_of_Y'][name]:.4f}% |"
        )

    remaining = logical["remaining_after_semantic_editability"]
    classified_only = logical["classified_but_not_semantically_editable"]
    opaque = logical["opaque_after_structural_classification"]
    lines.extend((
        "",
        "## Remaining payload, with denominators kept separate",
        "",
        (f"**Full non-editable queue Y-B:** {byte_label(remaining['bytes'])} "
         f"({remaining['percent_of_Y']:.4f}% of Y). It includes both structurally "
         "classified but non-editable bytes and structurally unclassified bytes."),
        "",
        (f"Structurally classified but not semantically editable Z-B: "
         f"{classified_only['bytes']:,} bytes ({classified_only['percent_of_Y']:.4f}% of Y)."),
        "",
        "| Y-B inventory class | Bytes | Share of Y-B | Share of Y | Catalog records |",
        "| --- | ---: | ---: | ---: | ---: |",
    ))
    for item in remaining["exclusive_byte_weighted_categories"]:
        lines.append(
            f"| {category_label(item['name'])} | {item['source_bytes']:,} | "
            f"{item['percent_of_remaining_payload']:.4f}% | "
            f"{item['percent_of_expanded_payload']:.4f}% | {item['file_count']:,} |"
        )
    lines.extend((
        "",
        (f"**Strictly structurally unclassified queue Y-Z:** {byte_label(opaque['bytes'])} "
         f"({opaque['percent_of_Y']:.4f}% of Y). This is not a measure of every "
         "opaque field: a structurally bounded record may still contain uninterpreted data."),
        "",
        "| Y-Z inventory class | Bytes | Share of Y-Z | Share of Y | Catalog records |",
        "| --- | ---: | ---: | ---: | ---: |",
    ))
    for item in opaque["exclusive_byte_weighted_categories"]:
        lines.append(
            f"| {category_label(item['name'])} | {item['source_bytes']:,} | "
            f"{item['percent_of_opaque_payload']:.4f}% | "
            f"{item['percent_of_expanded_payload']:.4f}% | {item['file_count']:,} |"
        )
    lines.extend((
        "",
        "Category names are evidence-led inventory labels based on parsed signatures, member types, "
        "extensions, or paths. They do not claim semantic decoding of every listed payload.",
        "",
    ))
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path("extracted/assets"))
    parser.add_argument("--catalog", type=Path, default=Path("extracted/assets/catalog.json"))
    parser.add_argument("--graphics-index", type=Path, default=Path("graphics/index.json"))
    parser.add_argument("--disc-report", type=Path, default=Path("reports/disc.json"))
    parser.add_argument("--roundtrip", type=Path, default=Path("reports/assets-roundtrip-prepared.json"))
    parser.add_argument("--movies", type=Path, default=Path("movies"),
                        help="movie workspace containing index.json and immutable *_jp streams")
    parser.add_argument("--output", type=Path, default=Path("reports/asset_recovery_census.json"))
    parser.add_argument("--summary-output", type=Path,
                        help="Markdown report path (defaults to --output with .md suffix)")
    args = parser.parse_args()
    inputs = _load_inputs(args.workspace, args.catalog, args.graphics_index,
                          args.disc_report, args.roundtrip, args.movies)
    report = build_census(*inputs)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    summary_output = args.summary_output or args.output.with_suffix(".md")
    summary_output.parent.mkdir(parents=True, exist_ok=True)
    summary_output.write_text(format_census_markdown(report), encoding="utf-8")
    print(format_census_summary(report))
    print(f"JSON report: {args.output}")
    print(f"Markdown report: {summary_output}")


if __name__ == "__main__":
    main()
