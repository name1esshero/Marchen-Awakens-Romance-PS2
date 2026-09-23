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

The prepared workspace exposes six CP932/UTF-8 text companions. The two
`MenuBinary.pac` tables, `CardList.txt` and `DataBase.txt`, contain Japanese
catalog/menu text. `script_func.cpp` and `.h` are source/interface files, and
`SYSTEM.CNF` plus `0FLIST.DIR;1` are system metadata; those four are not established
as player-facing dialogue. One `_msg.dat` file contains 229 CP932 UI/message
strings and is exposed as an editable JSON document by `prepare`. Its observed
layout is an 8-byte header followed by a count of 12-byte little-endian records
(`kind`, `key`, offset relative to byte 8), then CP932 NUL-terminated strings.
The strict parser and builder are `tools/messages.py`. The untouched
20,452-byte source rebuilds exactly, and its real containing PAC rebuilds with
all 30 original member/gap hashes intact. See [the message-table evidence](tasks/MESSAGE_TABLE.md).

This inventory is a starting point, not a claim that all game text has been
found. The 724 menu `.b` resources share a 16-byte `BPE\0` wrapper: table-size
field 256, payload length at +8, and decoded length at +12. `tools/bpe.py` now
decodes every prepared menu `.b` to its declared output length. The asset workspace
keeps the original compressed bytes for untouched files; edited decoded files are
wrapped with a literal identity table, and normal container relocation can carry
their growth. This is a decoded binary editing layer, not yet image editing.

The common decoded bundle begins with a little-endian resource count and 32-byte
records containing a 16-byte name, 4-byte type, size at record +20, offset at +24,
and an unknown field at +28. `tools/ui_bundle.py` validates extents and extracts
stable-index member sidecars; its manifest anchors the source hash and preserves
unknown record fields. `make prepare-assets` extracted 3,084 records from 721 of
the 724 `.b` payloads. Types observed were `at3` (1,605), `txc` (1,457), `ymp`
(14), `pac` (7), and `txt` (1). All observed member offsets are 16-byte aligned;
no table entry extents overlap. `python3 tools/ui_bundle.py audit extracted/assets`
rebuilds every untouched extracted bundle and verifies exact decoded-byte identity:
all 721 passed. Editing an extracted member and running the normal relocated asset
build updates its size/offset in the inner table, wraps the changed bundle in BPE,
and allows growth through the enclosing archive. Do not edit the decoded `.bin`
and its extracted members in the same build; the builder rejects that conflict.

Three `.yma` files (`top_yma.b`, `war_common_yma.b`, `war_stage_yma.b`) do not
match this bundle header and remain decoded raw files. Treat that as a known format
boundary, not malformed input. `at3` payloads begin `AT  ` and contain
animation/resource metadata with references such as `window.tga` and `icon.tga`;
sampled `txc` payloads begin `RTX3`. The `.tga` names identify raster-image
authoring references; the `.b` and `.txc` members contain animation and RTX3
texture data. `tools/rtx3.py` exports PSMT4, PSMT8 and PSMCT32 to uncompressed
32-bit TGA, and imports uncompressed 24/32-bit TGA back into the original RTX3
dimensions and palette. For example:

```sh
python3 tools/rtx3.py export SOURCE.txc /tmp/texture.tga
# For an indexed-color diagnostic, leave pixel bytes and CLUT entries in stored order:
python3 tools/rtx3.py export SOURCE.txc /tmp/texture-stored-order.tga --stored-order
# Edit /tmp/texture.tga in an image editor, preserving dimensions.
python3 tools/rtx3.py import SOURCE.txc /tmp/texture-edited.txc /tmp/texture.tga
```

`--stored-order` reads indexed pixels linearly and uses palette entries as
stored, without PSM swizzling, the GS CLUT index permutation, or alpha
expansion. It is a raw layout diagnostic, not an editable spatial representation; the normal export
remains the starting point for edits. For `title_marh_jp.txc`, the stored-order
preview draws recognizable Japanese logo shapes in two vertically stacked
variants. Its extracted TXC bytes match the enclosing bundle member's recorded
SHA-256 exactly. This separates a bad outer BPE/member extraction from the still
unresolved game texture layout, but does not establish UVs or runtime appearance.

Copy the rebuilt TXC over its corresponding `.resources/` member sidecar, then
use the normal relocated asset build. A no-op import returns the exact source
bytes. Indexed imports choose the nearest color in the existing palette; they do
not create colors or enlarge a texture. PSMT8H/PSMT4HL/PSMT4HH are recognized by
the header parser but deliberately rejected by the image decoder until their
storage order is established. Treat standalone previews as texture surfaces:
transparency, atlas regions, UVs, and repeated texture coordinates can make them
look incomplete or tiled. Decode associated `AT  ` metadata and render the
composition before translating artwork. Runtime support remains unverified.

For a discovered plain-text leaf, edit its `.utf8.txt` companion. For `_msg.dat`, use `localization/messages.json`; for the two tab-separated menu
tables, use `localization/card_list.json` and `localization/database.json`. These
source-hash-anchored UTF-8 catalogues preserve original cells, stable row IDs,
blank fields, tabs and line endings. `tools/text_catalog.py` rejects stale sources
and non-CP932 translations. Their resource paths are applied during
`make build-mod-disc`; do not change unclassified fields such as database unlock
metadata until their semantics are established.
`python3 tools/message_catalog.py create SOURCE.json OUTPUT.json` creates a new
message catalogue from prepared original JSON. For a plain TSV,
`python3 tools/text_catalog.py create SOURCE.tsv translations.json --resource RESOURCE --columns 1,2 --id-column 0` creates a hash-anchored catalogue; use
`python3 tools/text_catalog.py apply SOURCE.tsv translations.json OUTPUT.tsv` to
produce CP932 bytes. Ordinary translations belong in the tracked catalogues. Retain control codes, delimiters, columns and line
structure until the format is understood. Same-size edits can use
`make verify-disc` and should compare exactly only if the workspace has no edits.
For growing text edits, update the source-hash-anchored catalogue for the exact
resource path. `CardList.txt` currently has draft English for all 142 nonempty names, all 51
character titles and all 141 categories, while all 142 captions remain untranslated.
`DataBase.txt` has 87 translated fields of 126; its 39 unresolved condition
metadata values remain source text. For a growing edit, run `make build-mod-disc`; it enables the observed relocation
path and writes `mar_eng.iso` in the workspace root for emulator testing. Then run
`python3 tools/bootstrap.py mar_eng.iso --reports /tmp/marps2-mod-check`
to re-parse and inventory the ISO, and
`python3 tools/compare_disc.py mar_eng.iso` to authenticate the
pinned baseline, count all differing bytes, and sample the first differing
offsets. Comparator result 1 is expected for a modified image; result 2 is an
authentication or I/O error. Inspect the reported offsets and ISO inventory, and
test the image in a PS2 runtime before claiming the translation works in game.
The comparator's byte count is evidence of a change, not a semantic or gameplay
validator.

The synthetic regressions exercise UTF-8 editing, CP932 encoding, ISO directory
extent growth, and volume-length update, plus structured message editing with
offset updates through a PAC. The real `_msg.dat` table has also been extracted,
rebuilt byte-identically, and grown using the tracked translation catalogue
through the full ISO build.
These checks do not prove retail text line wrapping, glyph coverage, or runtime
relocation behavior.
The verified mod run also exposes a placement cost: a 15-byte single-prompt
growth appends a complete new PAC member at its parent, then appends the complete
428,967,936-byte YFS at the ISO end. The current build uses all three tracked catalogues. It grows `_msg.dat` by 248
bytes (20,452 to 20,700), `CardList.txt` to 13,567 bytes, and `DataBase.txt` to
3,319 bytes. The ISO inventory reports 42 entries and nested reparsing matches each
catalog-applied resource exactly. Current image SHA-256 is
`15fcacc2ebf2c2fe82fc6153348ca013f9c372202dff1b2c94b7e35eba33bee5`; the
authenticated comparator reports 751,304,175 differing bytes. This is an
expected mismatch for translation and append relocation. The current method is
space-heavy and has no runtime acceptance evidence. Exact-baseline comparison
is therefore an expected mismatch for a changed build; verify the authenticated
reference hash and inspect changed ranges rather than requiring equality.

## Procedure

1. Preserve `baserom.iso` and verify `config/reference.sha256`.
2. Export into a new ignored destination: `make export-assets`. Export refuses an
   existing destination. The parser fails on unsupported directory features,
   malformed archive tables, overlapping/out-of-range extents, duplicate YFS
   ownership, or unsupported member flags.
3. Run `make prepare-assets` to discover nested PAC tables, write the asset index and
   text companions, and expose the observed `_msg.dat` as UTF-8 JSON. Existing
   editable companions are retained on repeated prepare runs. Plain-text
   conversion is accepted only when CP932 encode/decode reproduces the exact
   input bytes.
4. Edit a raw leaf, UTF-8 companion, or the `translation` field in
   `localization/messages.json`. Preserve table-defined names, record keys and member order. Same-size edits
   can retain the original
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
PAC containers, generates catalog/plain-text source files, and parses a leaf named
`_msg.dat` into an adjacent `.messages.json` document when it meets the evidenced
contract. By default
it also updates the compact census at `reports/assets_census.json`; use `--report`
to choose another evidence path or `/dev/null` to suppress that copy.
`build WORKSPACE OUTPUT [--relocate] [--translations CATALOG.json]` reads only
workspace files, verifies complete non-overlapping byte coverage and updates only
table fields already located during export. When given a catalogue, it verifies
the original table SHA-256 and requires exactly one matching message table.
Unknown bytes are preserved. `make build-mod-disc` supplies the tracked catalogue.
`messages.py extract INPUT OUTPUT.json` and `messages.py build INPUT.json OUTPUT`
operate on the observed 8-byte-header/12-byte-record message-table shape. They
reject invalid ranges, embedded NULs, invalid CP932 and unencodable translations;
they do not claim support for other `.dat` variants.
The asset workspace calls this parser only for `_msg.dat` leaves.
The container parser assumes little-endian YFS/PAC/AFS fields, 16-byte PAC and
2048-byte YFS/AFS allocation alignment, and
the observed single-volume ISO directory form. These assumptions need further
cross-entry/runtime evidence before treating arbitrary images as supported.

`compare_disc.py` requires an expected hash file and compares streams without
loading either image into memory. Its hash authenticates the supplied reference
against this repository's pinned input; it does not establish independent retail
provenance. It reports differing byte count, not a semantic diff.

## Verification and remaining work

Focused tests cover nested round trips, malformed tables, unsafe source paths,
plain UTF-8-to-CP932 translation growth through ISO relocation, structured message
growth and PAC relocation, stable catalogue IDs and stale-source rejection,
catalogue-driven repacking, comparator chunk boundaries, truncation, and
pinned-reference rejection. Final verification for the workspace is `make test`
and unchanged full-disc `make verify-disc`. The changed real `_msg.dat` member has
also been built through the full ISO, authenticated against the pinned baseline,
and reparsed through ISO/YFS/PAC; see [message-table evidence](../tasks/MESSAGE_TABLE.md).
Runtime testing on target/emulator, the remaining format-specific conversions,
and full understanding of DMY extents are open.
