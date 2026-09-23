# Full disc asset workspace

Authority: [STANDARDS.md](STANDARDS.md), [AGENT_ENVIRONMENT.md](AGENT_ENVIRONMENT.md).
Objective: expose container members as editable files, rebuild the ISO from workspace
artifacts, and mechanically compare the complete result with the pinned input.

## Current evidence and scope

`tools/assets.py` reads the pinned ISO and recursively recognizes the observed
PlayStation ISO9660 directory tree, YFS, AFS and two PAC table-header variants.
Stable numeric workspace names preserve original logical paths in `catalog.json`;
every archive layout accounts for each byte exactly once as a member, gap, or tail.
All other members remain binary leaves. The prepare step creates UTF-8 companions
for reversible CP932 text files and converts them back during build.

Both the initial workspace rebuild and the fully prepared rebuild compare equal
to the 4,587,749,376-byte pinned image: all bytes match and both SHA-256 values are
`cc059a3acf818dfbd0a782a9d20ee67e020d167866cd1c4dca77e6eb9224e3ec`.
The completed prepared census contains 3,557 PAC, two AFS and one YFS container,
plus 34,486 leaves. One nested `tex.pac` candidate has an unknown table field and
is kept as a binary leaf. Six text/source files (ISO boot configuration, file list,
two menu tables and script interface source/header) have reversible CP932/UTF-8 companions.
The census is checked in at `reports/assets_census.json` and copied into the
workspace; the logical path catalog is in ignored `extracted/assets/catalog.json`.
The prepared-workspace comparison evidence is recorded in
`reports/assets-roundtrip-prepared.json`.

This is lossless container extraction/reinsertion, not semantic editing for every
format. YPC models, texture encodings, audio, font bitmaps, script bytecode and
other unknown leaves remain raw. `--relocate` appends a grown member and updates
its observed parent-table offset/size fields, recursively; for ISO files it also
updates the directory record and volume length. Whether the game accepts these
relocations, enlarged archives, changed model geometry, or changed text layout is
not established. Relocation is not a recovered runtime pointer/cross-reference
audit.

## Translation-bearing surfaces and mod rebuild loop

The prepared workspace currently exposes six CP932/UTF-8 text companions. The
two `MenuBinary.pac` tables, `CardList.txt` and `DataBase.txt`, contain Japanese
catalog/menu text. `script_func.cpp` and `.h` are source/interface files, and
`SYSTEM.CNF` plus `0FLIST.DIR;1` are system metadata; those four are not established
as player-facing dialogue. This inventory is a starting point, not a claim that
all game text has been found. UI `.b` resources, `_msg.dat`, and other binary
formats remain candidates for separate format work.

For a discovered text leaf, edit its `.utf8.txt` companion and retain control
codes, delimiters, columns, and line structure until the format is understood.
The builder encodes the edited text as CP932. Same-size edits can use
`make verify-disc` and should compare exactly only if the workspace has no edits.
For a growing edit, run `make build-mod-disc`; it enables the observed relocation
path and writes `build/assets-modded.iso`. Then run
`python3 tools/bootstrap.py build/assets-modded.iso --reports /tmp/marps2-mod-check`
to re-parse and inventory the ISO, and
`python3 tools/compare_disc.py build/assets-modded.iso` to authenticate the
pinned baseline, count all differing bytes, and sample the first differing
offsets. Comparator result 1 is expected for a modified image; result 2 is an
authentication or I/O error. Inspect the reported offsets and ISO inventory, and
test the image in a PS2 runtime before claiming the translation works in game.
The comparator's byte count is evidence of a change, not a semantic or gameplay
validator.

The synthetic regression `test_utf8_translation_grows_cp932_leaf_and_relocates_iso`
exercises UTF-8 editing, CP932 encoding, ISO directory extent growth, and volume
length update as one closed-loop packaging case. It does not prove any retail
text format's line wrapping, glyph coverage, or runtime relocation behavior.

## Procedure

1. Preserve `baserom.iso` and verify `config/reference.sha256`.
2. Export into a new ignored destination: `make export-assets`. Export refuses an
   existing destination. The parser fails on unsupported directory features,
   malformed archive tables, overlapping/out-of-range extents, duplicate YFS
   ownership, or unsupported member flags.
3. Run `make prepare-assets` to discover nested PAC tables and write the catalog
   and text companions. Text conversion is accepted only when CP932 encode/decode
   reproduces the exact input bytes.
4. Edit a raw leaf or its UTF-8 companion. Preserve the table-defined names and
   member order in the generated layout. Same-size edits can retain the original
   location. Changed sizes require `python3 tools/assets.py build extracted/assets
   build/mod.iso --relocate`; relocation is an experimental packaging pathway.
5. Build consumes only workspace files and manifests, never `baserom.iso`.
   Without `--relocate`, any member size change fails. Builds go to a new output
   path and are atomically installed after successful reconstruction.
6. Run `python3 tools/compare_disc.py build/assets-rebuilt.iso`. The comparator
   reads both complete files in chunks, authenticates the reference hash, counts
   every unequal/missing byte, and reports initial mismatch offsets. Exit 0 means
   authenticated byte equality; exit 1 means a valid reference but mismatch; exit
   2 means reference or I/O error.
7. For a changed build, inspect the first differing offsets and independently
   parse affected containers. Byte equality proves preservation only; it is not
   semantic asset validation or runtime validation.

## Tool contracts and limits

`assets.py export IMAGE WORKSPACE --hash-file HASH` is read-only on the image and
creates extracted files plus per-container JSON layouts. The image is SHA-256
checked before output. `prepare WORKSPACE [--report PATH]` expands observed nested
PAC containers and generates catalog/text source files in the workspace. By default
it also updates the compact census at `reports/assets_census.json`; use `--report`
to choose another evidence path or `/dev/null` to suppress that copy.
`build WORKSPACE OUTPUT [--relocate]` reads only workspace files, verifies complete
non-overlapping byte coverage and updates only table fields already located during
export. Unknown bytes are preserved. The parser currently assumes little-endian
YFS/PAC/AFS fields, 16-byte PAC and 2048-byte YFS/AFS allocation alignment, and
the observed single-volume ISO directory form. These assumptions need further
cross-entry/runtime evidence before treating arbitrary images as supported.

`compare_disc.py` requires an expected hash file and compares streams without
loading either image into memory. Its hash authenticates the supplied reference
against this repository's pinned input; it does not establish independent retail
provenance. It reports differing byte count, not a semantic diff.

## Verification and remaining work

Focused tests cover nested round trips, malformed tables, unsafe source paths,
UTF-8-to-CP932 translation growth through ISO relocation, nested offset updates,
comparator chunk boundaries, truncation, and pinned-reference rejection. Final
verification for this workflow is
`make test`, unchanged full-disc rebuild plus `compare_disc.py`, and changed-member
round trips through each affected table. Runtime testing on the target/emulator,
format-specific editable conversions, and full understanding of DMY extents are
open tasks.
