#!/usr/bin/env python3
"""Build a byte-weighted census of recovered asset payloads.

The logical-leaf denominator counts each terminal asset once. TXCs nested in
BPE/UI bundles are measured in a separate expanded-texture denominator and are
never added to the leaf-byte total a second time.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from collections import Counter, defaultdict
from pathlib import Path


def _read_json(path: Path):
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def _percent(numerator: int, denominator: int) -> float:
    return round(100.0 * numerator / denominator, 4) if denominator else 0.0


def _logical_basename(name: str) -> str:
    return name.rsplit("!/", 1)[-1]


def _extension(name: str) -> str:
    suffix = Path(_logical_basename(name)).suffix.lower()
    return suffix or "[none]"


def build_census(catalog, graphics_index, disc, roundtrip):
    """Return census data from the prepared leaf catalog and graphics index."""
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

    # Source paths are stable unique catalog identities; logical member names
    # can legitimately repeat in the same archive (for example, duplicate
    # character-frame records).
    def leaf_id(leaf):
        return leaf.get("source") or f"zero:{leaf['name']}:{id(leaf)}"

    leaf_bytes = sum(leaf["size"] for leaf in leaves)
    zero_leaves = [leaf for leaf in leaves if leaf.get("zero")]
    zero_bytes = sum(leaf["size"] for leaf in zero_leaves)
    nonzero_bytes = leaf_bytes - zero_bytes
    image_bytes = disc.get("image_bytes")
    reference_hash = disc.get("sha256")
    if not isinstance(image_bytes, int) or image_bytes < leaf_bytes:
        raise ValueError("disc image size is missing or smaller than logical leaf bytes")
    if roundtrip.get("reference_sha256") != reference_hash:
        raise ValueError("round-trip evidence is for a different reference image")
    if roundtrip.get("reference_size") != image_bytes:
        raise ValueError("round-trip evidence has a different reference size")
    if not roundtrip.get("authenticated") or not roundtrip.get("match"):
        raise ValueError("prepared baseline round-trip is not authenticated and byte-identical")

    # A catalog source leaf may appear in exactly one exclusive source-byte
    # category below. Nested TXCs are deliberately not source leaves here.
    txc_editable_leaves = set()
    txc_unresolved_leaves = set()
    txc_sizes = {}
    txc_rows = []
    bundle_manifest_cache = {}
    psm_stats = defaultdict(lambda: {"count": 0, "bytes": 0, "editable_count": 0,
                                     "editable_bytes": 0, "unresolved_count": 0,
                                     "unresolved_bytes": 0})
    txc_sources = Counter()

    for entry in entries:
        source_kind = entry.get("source_kind")
        if source_kind == "standalone":
            source = entry.get("source_path")
            leaf = by_source.get(source)
            if leaf is None or _extension(leaf["name"]) != ".txc":
                raise ValueError(f"standalone TXC has no matching catalog leaf: {source!r}")
            size = leaf["size"]
            (txc_editable_leaves if entry.get("image") else txc_unresolved_leaves).add(
                leaf_id(leaf)
            )
        elif source_kind == "bundle":
            manifest_path = entry.get("bundle_manifest")
            member_name = entry.get("source")
            if not manifest_path or not member_name:
                raise ValueError("bundle TXC is missing its manifest/member reference")
            if manifest_path not in bundle_manifest_cache:
                # Keep the manifest path here; it is read by the CLI wrapper and
                # supplied below as _manifest_entries when building a report.
                manifest = graphics_index.get("_manifest_entries", {}).get(manifest_path)
                if manifest is None:
                    raise ValueError(f"missing embedded member manifest: {manifest_path}")
                bundle_manifest_cache[manifest_path] = {
                    item["source"]: item for item in manifest.get("entries", [])
                }
            member = bundle_manifest_cache[manifest_path].get(member_name)
            if member is None:
                raise ValueError(f"manifest lacks embedded TXC member: {manifest_path}/{member_name}")
            size = member.get("size")
            if not isinstance(size, int) or size < 0:
                raise ValueError(f"invalid embedded TXC size: {manifest_path}/{member_name}")
            if member.get("source_sha256") != entry.get("source_sha256"):
                raise ValueError(f"embedded TXC hash disagrees with manifest: {manifest_path}/{member_name}")
        else:
            raise ValueError(f"unknown TXC source kind: {source_kind!r}")

        key = entry.get("key")
        if not key or key in txc_sizes:
            raise ValueError(f"missing or duplicate TXC key: {key!r}")
        txc_sizes[key] = size
        txc_rows.append((entry, size))
        txc_sources[source_kind] += 1
        psm = entry.get("psm_name") or f"unparsed:{entry.get('unsupported_reason') or 'unknown'}"
        stats = psm_stats[psm]
        stats["count"] += 1
        stats["bytes"] += size
        if entry.get("image"):
            stats["editable_count"] += 1
            stats["editable_bytes"] += size
        else:
            stats["unresolved_count"] += 1
            stats["unresolved_bytes"] += size

    txc_source_bytes = sum(txc_sizes.values())
    txc_editable_bytes = sum(size for entry, size in txc_rows if entry.get("image"))
    txc_unresolved_bytes = txc_source_bytes - txc_editable_bytes
    txc_editable_count = sum(bool(entry.get("image")) for entry, _ in txc_rows)

    # Confirm every standalone .txc leaf was indexed, not just every index row.
    catalog_txc = {leaf_id(leaf) for leaf in leaves if _extension(leaf["name"]) == ".txc"}
    indexed_standalone = txc_editable_leaves | txc_unresolved_leaves
    if catalog_txc != indexed_standalone:
        missing = sorted(catalog_txc - indexed_standalone)[:3]
        extra = sorted(indexed_standalone - catalog_txc)[:3]
        raise ValueError(f"standalone TXC index/catalog mismatch (missing={missing}, extra={extra})")

    bpe = [leaf for leaf in leaves if leaf.get("bpe_source")]
    parsed_bpe = [leaf for leaf in bpe if leaf.get("ui_bundle_source")]
    unparsed_bpe = [leaf for leaf in bpe if not leaf.get("ui_bundle_source")]
    text = [leaf for leaf in leaves if leaf.get("text_source")]
    messages = [leaf for leaf in leaves if leaf.get("message_source")]
    editable_groups = {
        "standalone_txc_with_editable_image": txc_editable_leaves,
        "parsed_menu_bpe_bundle": {leaf_id(leaf) for leaf in parsed_bpe},
        "reversible_utf8_text_companion": {leaf_id(leaf) for leaf in text},
        "structured_message_catalog": {leaf_id(leaf) for leaf in messages},
    }
    unresolved_groups = {
        "standalone_txc_unresolved": txc_unresolved_leaves,
        "bpe_decoded_but_bundle_unparsed": {leaf_id(leaf) for leaf in unparsed_bpe},
    }
    selected = {}
    for group_name, names in {**editable_groups, **unresolved_groups}.items():
        for key in names:
            if key in selected:
                raise ValueError(f"leaf counted in overlapping categories: {key}")
            selected[key] = group_name
    nonzero_ids = {leaf_id(leaf) for leaf in leaves if not leaf.get("zero") and leaf["size"]}
    if not set(selected).issubset(nonzero_ids):
        raise ValueError("zero-filled or empty leaf classified as recovered content")

    def category(name, names, description):
        rows = [leaf for leaf in leaves if leaf_id(leaf) in names]
        size = sum(leaf["size"] for leaf in rows)
        return {
            "name": name,
            "file_count": len(rows),
            "source_bytes": size,
            "percent_of_nonzero_leaf_bytes": _percent(size, nonzero_bytes),
            "description": description,
        }

    categories = [
        category("standalone_txc_with_editable_image", editable_groups["standalone_txc_with_editable_image"],
                 "Standalone TXC leaf bytes with indexed PSMT4/PSMT8 TGA exports."),
        category("parsed_menu_bpe_bundle", editable_groups["parsed_menu_bpe_bundle"],
                 "Original compressed .b leaf bytes whose decoded UI resource tables and members are extractable/rebuildable."),
        category("reversible_utf8_text_companion", editable_groups["reversible_utf8_text_companion"],
                 "Original text leaf bytes with reversible UTF-8 companions; includes system/source text as well as game tables."),
        category("structured_message_catalog", editable_groups["structured_message_catalog"],
                 "Original _msg.dat leaf bytes with an editable structured JSON catalog."),
        category("standalone_txc_unresolved", unresolved_groups["standalone_txc_unresolved"],
                 "Standalone TXC leaf bytes indexed but without an editable image for the current decoder."),
        category("bpe_decoded_but_bundle_unparsed", unresolved_groups["bpe_decoded_but_bundle_unparsed"],
                 "BPE leaf bytes decode losslessly, but the decoded .yma payloads have no parsed resource table."),
    ]
    classified_ids = set(selected)
    opaque_rows = [leaf for leaf in leaves if leaf_id(leaf) in nonzero_ids - classified_ids]
    opaque_bytes = sum(leaf["size"] for leaf in opaque_rows)
    categories.append({
        "name": "other_nonzero_leaves_not_in_editable_groups",
        "file_count": len(opaque_rows),
        "source_bytes": opaque_bytes,
        "percent_of_nonzero_leaf_bytes": _percent(opaque_bytes, nonzero_bytes),
        "description": "Losslessly extracted terminal payload bytes not included in the listed editable/structured groups; retained raw or still opaque to this census.",
    })
    if sum(item["source_bytes"] for item in categories) != nonzero_bytes:
        raise ValueError("exclusive nonzero-leaf categories do not sum to their denominator")

    extensions = defaultdict(lambda: {"file_count": 0, "source_bytes": 0})
    for leaf in leaves:
        item = extensions[_extension(leaf["name"])]
        item["file_count"] += 1
        item["source_bytes"] += leaf["size"]
    extensions = dict(sorted(extensions.items(), key=lambda item: (-item[1]["source_bytes"], item[0])))

    bundle_manifests = graphics_index.get("_manifest_entries", {})
    bundle_txcs = [entry for entry, _ in txc_rows if entry["source_kind"] == "bundle"]
    nested_bytes = sum(size for entry, size in txc_rows if entry["source_kind"] == "bundle")
    nested_supported_bytes = sum(size for entry, size in txc_rows
                                 if entry["source_kind"] == "bundle" and entry.get("image"))
    psm_report = {
        key: {**stats,
              "editable_percent_of_psm_bytes": _percent(stats["editable_bytes"], stats["bytes"])}
        for key, stats in sorted(psm_stats.items())
    }
    source_categories = {
        "standalone": {
            "entry_count": txc_sources["standalone"],
            "source_bytes": sum(size for entry, size in txc_rows if entry["source_kind"] == "standalone"),
        },
        "embedded_in_menu_bpe_bundles": {
            "entry_count": txc_sources["bundle"],
            "expanded_txc_payload_bytes": nested_bytes,
            "editable_txc_payload_bytes": nested_supported_bytes,
            "parsed_menu_bpe_leaf_count": len(parsed_bpe),
            "bundle_manifest_count_with_indexed_txc": len({
                entry["bundle_manifest"] for entry in bundle_txcs
            }),
            "bundle_member_count": sum(len(manifest.get("entries", []))
                                        for manifest in bundle_manifests.values()),
        },
    }

    editable_leaf_bytes = sum(
        item["source_bytes"] for item in categories if item["name"] in editable_groups
    )
    return {
        "schema_version": 1,
        "evidence_date": dt.date.today().isoformat(),
        "reference_sha256": reference_hash,
        "scope": "Prepared logical leaf payloads plus the indexed TXC corpus. A leaf byte is counted once; embedded TXC member bytes are reported separately because they reside inside counted .b leaf payloads.",
        "disc": {
            "image_bytes": image_bytes,
            "logical_leaf_count": len(leaves),
            "logical_leaf_bytes": leaf_bytes,
            "logical_leaf_percent_of_image": _percent(leaf_bytes, image_bytes),
            "zero_or_empty_leaf_count": len(zero_leaves),
            "zero_filled_leaf_bytes": zero_bytes,
            "zero_filled_percent_of_leaf_bytes": _percent(zero_bytes, leaf_bytes),
            "nonzero_leaf_payload_bytes": nonzero_bytes,
            "nonzero_leaf_percent_of_image": _percent(nonzero_bytes, image_bytes),
            "image_bytes_outside_terminal_leaf_payloads": image_bytes - leaf_bytes,
            "prepared_round_trip": {
                "authenticated": roundtrip["authenticated"],
                "byte_identical": roundtrip["match"],
                "differing_bytes": roundtrip.get("differing_bytes"),
                "rebuilt_bytes": roundtrip.get("rebuilt_size"),
                "rebuilt_sha256": roundtrip.get("rebuilt_sha256"),
                "evidence_file": "reports/assets-roundtrip-prepared.json",
            },
        },
        "exclusive_nonzero_leaf_categories": categories,
        "editable_group_source_bytes": editable_leaf_bytes,
        "editable_group_percent_of_nonzero_leaf_bytes": _percent(editable_leaf_bytes, nonzero_bytes),
        "texture_corpus": {
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
            "accounting_note": "Expanded TXC payload bytes include TXCs extracted from the 721 parsed .b bundles. These nested bytes are a separate texture-corpus denominator and are not added to the logical leaf-byte denominator.",
        },
        "logical_leaf_extensions": extensions,
        "limits": [
            "Percentages describe this pinned image and the prepared/catalogued surfaces, not every possible hidden or runtime-generated asset.",
            "A reversible extraction or supported rebuild path does not prove semantic understanding or in-game visual/runtime correctness.",
            "One nested tex.pac candidate remains unparsed and is included among other nonzero leaf payloads.",
            "Generated TGAs are editable representations; their uncompressed output sizes are not counted as original source bytes.",
        ],
    }


def _load_inputs(workspace: Path, catalog_path: Path, graphics_path: Path,
                 disc_path: Path, roundtrip_path: Path):
    catalog = _read_json(catalog_path)
    graphics = _read_json(graphics_path)
    disc = _read_json(disc_path)
    roundtrip = _read_json(roundtrip_path)
    manifest_paths = {entry["bundle_manifest"] for entry in graphics.get("entries", [])
                      if entry.get("source_kind") == "bundle"}
    manifest_paths.update(leaf["ui_bundle_source"] for leaf in catalog
                          if leaf.get("ui_bundle_source"))
    graphics["_manifest_entries"] = {
        path: _read_json(workspace / path) for path in sorted(manifest_paths)
    }
    return catalog, graphics, disc, roundtrip


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
    texture = report["texture_corpus"]
    print(f"leaf payloads: {report['disc']['logical_leaf_bytes']:,} bytes; "
          f"{report['disc']['zero_filled_leaf_bytes']:,} zero-filled")
    print(f"indexed TXCs: {texture['editable_txc_byte_percent']:.4f}% editable by bytes "
          f"({texture['editable_txc_payload_bytes']:,}/{texture['expanded_txc_payload_bytes']:,})")
    print(f"report: {args.output}")


if __name__ == "__main__":
    main()
