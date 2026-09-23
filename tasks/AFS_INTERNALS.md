# AFS filename TOC inventory

## Objective and scope

Inventory the internal member tables and trailing filename TOCs of the two
`AFS\0` archives listed in the pinned disc manifest. This is a read-only
structural recovery slice. `IOPRP`/YFS internals, AFS writing, edited-member
reinsertion, metadata interpretation, and game runtime behavior are outside
scope.

## Method and tool contract

Run from the repository root with the pinned image available:

```sh
python3 tools/afs.py --iso baserom.iso --manifest reports/disc.json \
  --output reports/afs_inventory.json
```

The tool reads only ISO extents enumerated in the manifest whose path ends in
`.AFS;1`. It verifies each extent's length and recorded 16-byte prefix, then
checks the `AFS\0` header, little-endian member count, offset/size table, and
the eight-byte pointer immediately after that table. The observed pointer
addresses `count` records of 48 bytes: a 32-byte CP932 name slot and a 16-byte
suffix retained as raw hex and SHA-256. Every member and TOC range must fit in
the enclosing ISO extent, and member ranges may not overlap archive metadata,
the TOC, or one another. Names are paired with member offset/size rows by
their common record index. This row-order association is corroborated by the
member signatures in both archives.

The JSON records archive, TOC, member, and disjoint byte-region hashes. Each
archive's accounting closes as header/member table/pointer + member payloads +
filename TOC + gaps. Gaps are reported as unclassified even when observed to
contain only zero bytes. The tool reads/hashes archive regions in bounded
chunks; it does not hash the entire ISO itself. The `source_iso_sha256_from_manifest`
field records the expected image hash from `reports/disc.json`, not a new full
image hash measurement.

## Findings

`reports/afs_inventory.json` covers `MOVIE.AFS;1` (13 members) and `BGM.AFS;1`
(25 members). Both use a TOC immediately described by the pointer after the
member table: `count * 48` bytes. All member starts are 2048-byte aligned, and
each TOC row is associated with the same-index offset/size row. Every MOVIE
member begins with the MPEG-2 pack prefix `00 00 01 BA`; every BGM member begins
with `80 00`, consistent with its `.adx` name. This supports the observed name
and member association, without interpreting the 16-byte suffix.

| Archive | Archive bytes | Member payload bytes | Table + pointer | Name TOC | Unclassified gaps (all observed zero) |
| --- | ---: | ---: | ---: | ---: | ---: |
| `MOVIE.AFS;1` | 685,115,392 | 685,111,296 | 120 | 624 | 3,352 |
| `BGM.AFS;1` | 123,400,192 | 123,389,590 | 216 | 1,200 | 9,186 |

For both archives the categories sum exactly to the archive extent. The only
unclassified bytes in these two archives are the zero-filled gaps recorded in
the JSON; their zero content does not by itself prove intended padding.

The source image used to generate the report had size 4,587,749,376 bytes, and
its measured SHA-256 matched the manifest's pinned value
`cc059a3acf818dfbd0a782a9d20ee67e020d167866cd1c4dca77e6eb9224e3ec`.
Archive SHA-256 values are recorded per archive and member in the report.

## Verification and limits

`tests/test_afs.py` exercises the observed header/table/TOC shape, bad
signatures, truncated tables, invalid and out-of-range TOC pointers, malformed
names, overlapping member/metadata ranges, whole-archive byte accounting, and
an exact no-op rebuild of a synthetic AFS through the existing asset workspace
export/build path. The real archives are read-only evidence; this work does
not claim that edits to AFS members can be reinserted safely or accepted by the
game. The 16-byte per-name suffix remains uninterpreted. The parser handles the
specific 48-byte filename-TOC form observed here, not every CRI AFS variant.
