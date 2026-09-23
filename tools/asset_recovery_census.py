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
import json
from collections import Counter, defaultdict
from pathlib import Path

try:
    from tools.at3 import parse as parse_at3
except ModuleNotFoundError:  # Direct execution places tools/ on sys.path.
    from at3 import parse as parse_at3


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
                 disc_path: Path, roundtrip_path: Path):
    catalog = _read_json(catalog_path)
    graphics = _read_json(graphics_path)
    disc = _read_json(disc_path)
    roundtrip = _read_json(roundtrip_path)
    root_layout = workspace / "layout.json"
    disc["_layout_partition"] = _load_layout_partition(root_layout, disc["image_bytes"])

    # Prepared metadata records exact BPE hashes for the three unparsed YMA
    # payloads, but older catalogs omitted their decoded lengths.
    for leaf in catalog:
        if leaf.get("bpe_source"):
            decoded_path = workspace / leaf["bpe_source"]
            if not decoded_path.is_file():
                raise ValueError(f"missing decoded BPE source: {decoded_path}")
            leaf["_decoded_payload_size"] = decoded_path.stat().st_size
        if leaf.get("source") and _source_extension(leaf["name"]) == ".at3":
            raw = (workspace / leaf["source"]).read_bytes()
            try:
                leaf["_at3_reference_table_bytes"] = parse_at3(raw)["reference_table_end"]
            except ValueError:
                leaf["_at3_reference_table_bytes"] = 0
        if leaf.get("source") and "MOVIE.AFS;1" in leaf["name"]:
            with (workspace / leaf["source"]).open("rb") as stream:
                leaf["_mpeg_program_stream"] = stream.read(4) == b"\0\0\1\xba"

    manifest_paths = {entry["bundle_manifest"] for entry in graphics.get("entries", [])
                      if entry.get("source_kind") == "bundle"}
    manifest_paths.update(leaf["ui_bundle_source"] for leaf in catalog
                          if leaf.get("ui_bundle_source"))
    graphics["_manifest_entries"] = {
        path: _read_json(workspace / path) for path in sorted(manifest_paths)
    }
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
    if "movie.afs;1" in name and leaf.get("_mpeg_program_stream"):
        return "video_cinematics", "MOVIE.AFS path and MPEG program-stream pack-start magic"
    if "bgm.afs;1" in name or "/data/sound/" in name:
        return "audio_sound_candidates", "BGM archive or sound-directory path; payload audio is not decoded"
    if extension in (".ymp", ".ypc"):
        return "model_geometry_candidates", "YMP/YPC resource naming; model bodies are not decoded here"
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
        txc_sizes[key] = size
        txc_status[txc_key] = editable
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
                           "editable_kind": None, "is_txc": extension == ".txc"}
                    if row["is_txc"]:
                        key = ("bundle", manifest_path, member["source"])
                        if key not in txc_status:
                            raise ValueError(f"bundle TXC is absent from graphics index: {manifest_path}/{member['source']}")
                        row["editable_kind"] = "editable_graphics" if txc_status[key] else None
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
                })
            continue

        extension = _source_extension(leaf["name"])
        row = {"name": leaf["name"], "size": leaf["size"], "extension": extension,
               "origin": "terminal_leaf", "leaf": leaf,
               "editable_kind": None, "is_txc": extension == ".txc"}
        if row["is_txc"]:
            key = ("standalone", leaf["source"])
            if key not in txc_status:
                raise ValueError(f"standalone TXC is absent from graphics index: {leaf['name']}")
            if txc_status[key]:
                row["editable_kind"] = "editable_graphics"
            else:
                row["unresolved_txc"] = True
        elif leaf.get("text_source") or leaf.get("message_source"):
            row["editable_kind"] = "editable_text_and_catalogs"
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
    semantically_editable_bytes = editable_graphics + text_bytes + message_bytes
    remaining_bytes = expanded_payload_bytes - semantically_editable_bytes
    if remaining_bytes < 0:
        raise ValueError("semantic editable byte count exceeds the logical content denominator")

    # Z is strict and explicitly composed: all indexed RTX3 extents, all
    # non-TXC child extents in validated UI bundles, reversible text/catalog
    # sources, and directly parsed AT3 header/reference tables. Payload bodies
    # outside those extents remain opaque even if their filename is suggestive.
    bundle_nontexture_member_bytes = parsed_bundle_member_bytes - nested_txc_bytes
    direct_at3_table_bytes = sum(leaf.get("_at3_reference_table_bytes", 0) for leaf in leaves
                                 if _source_extension(leaf["name"]) == ".at3")
    structurally_classified_bytes = (txc_source_bytes + bundle_nontexture_member_bytes +
                                     text_bytes + message_bytes + direct_at3_table_bytes)
    if structurally_classified_bytes > expanded_payload_bytes:
        raise ValueError("structural byte ranges overlap or exceed the logical payload")

    remainder_totals = Counter()
    remainder_counts = Counter()
    remainder_basis = {}
    editable_groups = {"editable_graphics", "editable_text_and_catalogs"}
    for row in expanded_rows:
        if row["editable_kind"] in editable_groups:
            continue
        category_name, basis = _residual_category(row)
        remainder_totals[category_name] += row["size"]
        remainder_counts[category_name] += 1
        remainder_basis[category_name] = basis
    if sum(remainder_totals.values()) != remaining_bytes:
        raise ValueError("exclusive remaining-payload categories do not sum to Y minus B")
    remaining_categories = [
        {"name": name, "file_count": remainder_counts[name], "source_bytes": size,
         "percent_of_remaining_payload": _percent(size, remaining_bytes),
         "percent_of_expanded_payload": _percent(size, expanded_payload_bytes),
         "classification_basis": remainder_basis[name]}
        for name, size in sorted(remainder_totals.items(), key=lambda item: (-item[1], item[0]))
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
        "schema_version": 2,
        "evidence_date": dt.date.today().isoformat(),
        "reference_sha256": reference_hash,
        "scope": "Pinned physical image partition plus a de-duplicated expanded logical content inventory; recovery levels have separate definitions and evidence.",
        "physical_disc_accounting": {
            "image_bytes": image_bytes,
            "named_member_count": layout["named_member_count"],
            "all_zero_named_member_count": layout["all_zero_named_member_count"],
            "all_zero_named_placeholder_bytes": layout["all_zero_named_member_bytes"],
            "all_zero_named_placeholder_percent_of_image": _percent(layout["all_zero_named_member_bytes"], image_bytes),
            "all_zero_gap_or_padding_bytes": layout["all_zero_gap_bytes"],
            "all_zero_gap_or_padding_percent_of_image": _percent(layout["all_zero_gap_bytes"], image_bytes),
            "known_all_zero_placeholder_or_gap_bytes": zero_span_bytes,
            "known_all_zero_placeholder_or_gap_percent_of_image": _percent(zero_span_bytes, image_bytes),
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
            "terminal_leaf_source_bytes_including_zero_placeholders": leaf_bytes,
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
                        "indexed_RTX3_record_and_pixel_extents": txc_source_bytes,
                        "parsed_UI_bundle_nontexture_member_extents": bundle_nontexture_member_bytes,
                        "reversible_CP932_text_and_message_source_bytes": text_bytes + message_bytes,
                        "direct_AT3_header_and_reference_table_bytes": direct_at3_table_bytes,
                    },
                    "meaning": "Validated internal extents or records, de-duplicated across nested TXCs. An AT3 body after its parsed reference table is not counted.",
                },
                "losslessly_rebuildable": {
                    "bytes_A": expanded_payload_bytes,
                    "denominator_bytes_Y": expanded_payload_bytes,
                    "percent_A_of_Y": _percent(expanded_payload_bytes, expanded_payload_bytes),
                    "evidence": "The authenticated prepared workspace rebuild is byte-identical to the pinned full disc; parsed UI bundles also have exact no-op reassembly evidence.",
                    "meaning": "Unchanged source preservation/rebuild only; not evidence that edited output is correct or runtime-safe.",
                },
                "semantically_editable": {
                    "bytes_B": semantically_editable_bytes,
                    "denominator_bytes_Y": expanded_payload_bytes,
                    "percent_B_of_Y": _percent(semantically_editable_bytes, expanded_payload_bytes),
                    "components": {
                        "supported_editable_TGA_texture_source_bytes": editable_graphics,
                        "reversible_text_companion_source_bytes": text_bytes,
                        "structured_message_catalog_source_bytes": message_bytes,
                    },
                    "meaning": "A source representation has an evidence-backed editable representation and insertion path. This measures editability, not the fraction already translated.",
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
                "accounting_note": "Categories partition Y minus B. Names indicate evidence-backed inventory classes, not complete reverse engineering; filename/path-led candidates and opaque bodies are explicitly labeled.",
            },
        },
        "texture_corpus": texture_corpus,
        "logical_leaf_extensions": extensions,
        "limits": [
            "Zero placeholders and zero-filled gaps are reported as measured spans; the gap label does not prove historical intent.",
            "Information-bearing means a named terminal member extent that is not wholly zero. Zero-valued bytes inside a nonzero member are retained in its full extent.",
            "Expanded logical payload is a normalized content inventory, not a second physical disc size; it replaces compressed BPE wrappers with decoded child payloads and excludes bundle control/gap bytes.",
            "The structural numerator counts only the explicit parser-backed extents listed. Container hierarchy addressing is reported separately and must not be mistaken for semantic understanding.",
            "A byte-identical unchanged rebuild proves source preservation. It does not prove relocation correctness for every edit or runtime correctness.",
            "Candidate remainder classes rely on signatures, member types, extensions, or directory names as documented; unparsed member bodies are not claimed to be semantically recovered.",
            "Generated TGAs are editable representations; their uncompressed output sizes are not counted as original source bytes.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path("extracted/assets"))
    parser.add_argument("--catalog", type=Path, default=Path("extracted/assets/catalog.json"))
    parser.add_argument("--graphics-index", type=Path, default=Path("graphics/index.json"))
    parser.add_argument("--disc-report", type=Path, default=Path("reports/disc.json"))
    parser.add_argument("--roundtrip", type=Path, default=Path("reports/assets-roundtrip-prepared.json"))
    parser.add_argument("--output", type=Path, default=Path("reports/asset_recovery_census.json"))
    args = parser.parse_args()
    inputs = _load_inputs(args.workspace, args.catalog, args.graphics_index,
                          args.disc_report, args.roundtrip)
    report = build_census(*inputs)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    physical = report["physical_disc_accounting"]
    recovery = report["expanded_logical_payload"]["recovery_levels"]
    print(f"disc: {physical['image_bytes']:,} bytes; known all-zero spans: "
          f"{physical['known_all_zero_placeholder_or_gap_bytes']:,}")
    print(f"logical payload Y: "
          f"{report['expanded_logical_payload']['information_bearing_payload_bytes_Y']:,} bytes")
    for name in ("structurally_classified", "losslessly_rebuildable",
                 "semantically_editable", "runtime_validated_editable"):
        row = recovery[name]
        percent_key = next(key for key in row if key.startswith("percent_") and key.endswith("_of_Y"))
        bytes_key = next(key for key in row if key in ("bytes_Z", "bytes_A", "bytes_B", "bytes_C"))
        print(f"{name}: {row[percent_key]:.4f}% ({row[bytes_key]:,}/{row['denominator_bytes_Y']:,})")
    print(f"report: {args.output}")


if __name__ == "__main__":
    main()
