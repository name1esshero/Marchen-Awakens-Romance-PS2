"""Export immutable movie streams and inspect English video overrides."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

try:
    from . import sofdec
except ImportError:  # Support direct execution of sibling tools.
    import sofdec

INDEX_NAME = "index.json"
MOVIE_PATH = re.compile(r"disc!/MOVIE\.AFS;1!/([0-9]{5})\.bin$")


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _safe(root: Path, relative: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or not rel.parts or ".." in rel.parts:
        raise ValueError(f"unsafe movie workspace path: {relative!r}")
    return root / rel


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".movie-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _write_immutable(path: Path, data: bytes, digest: str) -> None:
    if path.exists():
        if not path.is_file() or _digest(path.read_bytes()) != digest:
            raise ValueError(f"Japanese movie baseline is immutable: {path}")
        return
    _atomic_write(path, data)


def _read_index(movie_root: Path) -> dict:
    path = movie_root / INDEX_NAME
    if not path.is_file():
        raise ValueError(f"movie index is missing: {path}; run make movies-export")
    index = json.loads(path.read_text(encoding="utf-8"))
    if index.get("version") != 1 or not isinstance(index.get("entries"), list):
        raise ValueError("unsupported movie index")
    seen_paths = set()
    seen_sources = set()
    for entry in index["entries"]:
        logical = entry.get("logical_path")
        source = entry.get("source_path")
        if not isinstance(logical, str) or logical in seen_paths:
            raise ValueError(f"missing or duplicate movie logical path: {logical!r}")
        if not isinstance(source, str) or source in seen_sources:
            raise ValueError(f"missing or duplicate movie source path: {source!r}")
        seen_paths.add(logical)
        seen_sources.add(source)
        for field in ("source_sha256", "video_sha256", "audio_sha256"):
            digest = entry.get(field, "")
            if (not isinstance(digest, str) or len(digest) != 64 or
                    any(ch not in "0123456789abcdef" for ch in digest)):
                raise ValueError(f"invalid movie {field} for {logical}")
        for field in ("source_bytes", "video_bytes", "audio_bytes"):
            if not isinstance(entry.get(field), int) or entry[field] <= 0:
                raise ValueError(f"invalid movie {field} for {logical}")
        for field in ("video_file", "audio_file"):
            if not isinstance(entry.get(field), str):
                raise ValueError(f"missing movie {field} for {logical}")
            _safe(movie_root, entry[field])
    return index


def export(workspace: Path, movie_root: Path) -> dict:
    """Extract each direct MOVIE.AFS stream into flat Japanese source files."""
    workspace = Path(workspace).resolve()
    movie_root = Path(movie_root).resolve()
    catalog_path = workspace / "catalog.json"
    if not catalog_path.is_file():
        raise ValueError(f"prepared asset catalog is missing: {catalog_path}")
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    selected = []
    for row in catalog:
        match = MOVIE_PATH.fullmatch(row.get("name", ""))
        if match:
            selected.append((match.group(1), row))
    if not selected:
        raise ValueError("catalog has no direct MOVIE.AFS stream entries")
    selected.sort(key=lambda item: item[0])

    movie_root.mkdir(parents=True, exist_ok=True)
    entries = []
    for stem, row in selected:
        source_path = row.get("source")
        if not isinstance(source_path, str):
            raise ValueError(f"movie source has no workspace sidecar: {row['name']}")
        source_file = _safe(workspace, source_path)
        raw = source_file.read_bytes()
        if len(raw) != row.get("size"):
            raise ValueError(f"movie source size differs from catalog: {row['name']}")
        source_sha256 = _digest(raw)
        if row.get("sha256") and row["sha256"] != source_sha256:
            raise ValueError(f"movie source hash differs from catalog: {row['name']}")
        streams = sofdec.extract(raw)
        video_name = f"{stem}_jp.m2v"
        audio_name = f"{stem}_jp.sfa"
        _write_immutable(movie_root / video_name, streams["video"], streams["video_sha256"])
        _write_immutable(movie_root / audio_name, streams["audio"], streams["audio_sha256"])
        entries.append({
            "logical_path": row["name"],
            "source_path": source_path,
            "source_bytes": len(raw),
            "source_sha256": source_sha256,
            "video_file": video_name,
            "video_bytes": len(streams["video"]),
            "video_sha256": streams["video_sha256"],
            "audio_file": audio_name,
            "audio_bytes": len(streams["audio"]),
            "audio_sha256": streams["audio_sha256"],
            "video_profile": streams["video_profile"],
        })
    index = {
        "version": 1,
        "format": "Observed sectorized CRI SofDec MPEG-2 video plus CRI ADX audio",
        "entries": entries,
    }
    encoded = (json.dumps(index, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    _atomic_write(movie_root / INDEX_NAME, encoded)
    return index


def _catalog_rows(workspace: Path) -> dict:
    catalog_path = workspace / "catalog.json"
    if not catalog_path.is_file():
        raise ValueError(f"prepared asset catalog is missing: {catalog_path}")
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    return {row.get("name"): row for row in catalog}


def audit(workspace: Path, movie_root: Path) -> dict:
    """Verify exported hashes and profile-compatible authored overrides."""
    workspace = Path(workspace).resolve()
    movie_root = Path(movie_root).resolve()
    index = _read_index(movie_root)
    catalog = _catalog_rows(workspace)
    expected_sources = {name for name in catalog if MOVIE_PATH.fullmatch(name or "")}
    indexed_sources = {entry["logical_path"] for entry in index["entries"]}
    if expected_sources != indexed_sources:
        raise ValueError(
            "movie index/catalog coverage differs "
            f"(missing={sorted(expected_sources - indexed_sources)[:3]}, "
            f"extra={sorted(indexed_sources - expected_sources)[:3]})"
        )
    indexed = set()
    total_source_bytes = total_video_bytes = total_audio_bytes = 0
    english = []
    audited_entries = []
    for entry in index["entries"]:
        logical = entry["logical_path"]
        row = catalog.get(logical)
        if row is None or row.get("source") != entry["source_path"]:
            raise ValueError(f"movie index does not match prepared catalog: {logical}")
        source = _safe(workspace, entry["source_path"]).read_bytes()
        if (len(source) != row.get("size") or
                (row.get("sha256") and _digest(source) != row["sha256"])):
            raise ValueError(f"movie source differs from prepared catalog: {logical}")
        if len(source) != entry["source_bytes"] or _digest(source) != entry["source_sha256"]:
            raise ValueError(f"movie source changed since export: {logical}")
        streams = sofdec.extract(source)
        if streams["video_profile"] != entry["video_profile"]:
            raise ValueError(f"movie profile differs from export index: {logical}")
        for kind in ("video", "audio"):
            path = _safe(movie_root, entry[f"{kind}_file"])
            data = path.read_bytes()
            if (len(data) != entry[f"{kind}_bytes"] or
                    _digest(data) != entry[f"{kind}_sha256"] or
                    data != streams[kind]):
                raise ValueError(f"Japanese {kind} baseline changed: {path}")
        total_source_bytes += entry["source_bytes"]
        total_video_bytes += entry["video_bytes"]
        total_audio_bytes += entry["audio_bytes"]
        audited_entries.append({
            "logical_path": logical,
            "source_bytes": entry["source_bytes"],
            "source_sha256": entry["source_sha256"],
            "video_bytes": entry["video_bytes"],
            "video_sha256": entry["video_sha256"],
            "audio_bytes": entry["audio_bytes"],
            "audio_sha256": entry["audio_sha256"],
            "video_profile": entry["video_profile"],
        })
        english_name = entry["video_file"].removesuffix("_jp.m2v") + "_eng.m2v"
        english_path = _safe(movie_root, english_name)
        if english_path.exists():
            if not english_path.is_file():
                raise ValueError(f"English movie override is not a regular file: {english_path}")
            override = english_path.read_bytes()
            baseline_profile = entry["video_profile"]
            edited_profile = sofdec.video_profile(override)
            if any(edited_profile.get(key) != baseline_profile.get(key)
                   for key in sofdec._COMPATIBLE_VIDEO_FIELDS):
                raise ValueError(f"English video profile differs from source: {english_path}")
            english.append({"logical_path": logical, "file": english_name,
                            "bytes": len(override), "sha256": _digest(override)})
        indexed.add(english_name)
    unindexed = sorted(path.name for path in movie_root.glob("*_eng.m2v")
                       if path.name not in indexed)
    if unindexed:
        raise ValueError(f"unindexed English movie override(s): {unindexed[:3]}")
    return {
        "movie_count": len(index["entries"]),
        "source_bytes": total_source_bytes,
        "video_elementary_stream_bytes": total_video_bytes,
        "audio_elementary_stream_bytes": total_audio_bytes,
        "_audited_entries": audited_entries,
        "english_override_count": len(english),
        "english_overrides": english,
    }


def override_state(movie_root: Path) -> dict:
    """Read current English video siblings for the relocated disc builder."""
    movie_root = Path(movie_root).resolve()
    index = _read_index(movie_root)
    entries = {}
    indexed_english = set()
    for entry in index["entries"]:
        english_name = entry["video_file"].removesuffix("_jp.m2v") + "_eng.m2v"
        english_path = _safe(movie_root, english_name)
        indexed_english.add(english_name)
        if not english_path.exists():
            continue
        if not english_path.is_file():
            raise ValueError(f"English movie override is not a regular file: {english_path}")
        baseline = _safe(movie_root, entry["video_file"]).read_bytes()
        if len(baseline) != entry["video_bytes"] or _digest(baseline) != entry["video_sha256"]:
            raise ValueError(f"Japanese movie baseline changed: {entry['video_file']}")
        override = english_path.read_bytes()
        baseline_profile = entry["video_profile"]
        edited_profile = sofdec.video_profile(override)
        if any(edited_profile.get(key) != baseline_profile.get(key)
               for key in sofdec._COMPATIBLE_VIDEO_FIELDS):
            raise ValueError(f"English video profile differs from source: {english_path}")
        entries[entry["logical_path"]] = {
            **entry,
            "english_video_file": english_name,
            "english_video_sha256": _digest(override),
        }
    unindexed = sorted(path.name for path in movie_root.glob("*_eng.m2v")
                       if path.name not in indexed_english)
    if unindexed:
        raise ValueError(f"unindexed English movie override(s): {unindexed[:3]}")
    return {"root": movie_root, "entries": entries, "applied": set()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    export_parser = sub.add_parser("export")
    export_parser.add_argument("workspace", type=Path)
    export_parser.add_argument("movie_root", type=Path)
    audit_parser = sub.add_parser("audit")
    audit_parser.add_argument("workspace", type=Path)
    audit_parser.add_argument("movie_root", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "export":
            result = export(args.workspace, args.movie_root)
            print(json.dumps({"movie_count": len(result["entries"]),
                              "index": str(args.movie_root / INDEX_NAME)}, indent=2))
        else:
            result = audit(args.workspace, args.movie_root)
            print(json.dumps({key: value for key, value in result.items()
                              if not key.startswith("_")}, indent=2))
        return 0
    except (OSError, ValueError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
