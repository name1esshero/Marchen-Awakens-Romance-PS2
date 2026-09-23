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
format. Evidence-supported PSMT4/PSMT8/PSMT8H/PSMT4HL/PSMT4HH TXCs have indexed
TGA companions; the 43 short PSMCT32 TXCs, YPC models, audio, script bytecode and
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
texture data. `tools/rtx3.py` exports indexed PSMT4, PSMT8, PSMT8H, PSMT4HL and
PSMT4HH records to uncompressed 32-bit TGA, and imports uncompressed 24/32-bit
TGA back into the original RTX3 dimensions and palette. The current candidate
reads the compact declared pixel extent in linear order, applies the PSMT8 CLUT
index map (the PSMT4-family map is identity), and expands GS alpha values from
0..128 to TGA's 0..255 range. The Sony GS manual describes high-bit mode lanes in
the GS PSMCT32 memory representation; it does not prove how RTX3 stores or
samples these compact payloads. Three exported high-bit samples render coherent
previews, while actual GS sampling, UV composition and runtime remain unverified.
PSMCT32 still uses the legacy decoder and 43 short corpus records remain raw.
See [the GS manual, §8.3](https://github.com/ninjadynamics/PS2Docs/blob/main/GS_Users_Manual.pdf).
For example:

```sh
python3 tools/rtx3.py export SOURCE.txc /tmp/texture.tga
# Raw palette-order diagnostic: leave pixel bytes and CLUT entries in stored order:
python3 tools/rtx3.py export SOURCE.txc /tmp/texture-stored-order.tga --stored-order
# Edit /tmp/texture.tga in an image editor, preserving dimensions.
python3 tools/rtx3.py import SOURCE.txc /tmp/texture-edited.txc /tmp/texture.tga
```

Run `python3 tools/at3.py SOURCE.at3 --output-json EDITABLE.json` to inspect the
AT header, texture-name table, and observed node envelopes. The builder command
`python3 tools/at3.py --build-json EDITABLE.json --output REBUILT.at3` preserves
unknown bytes and rejects reference-count or node-size changes. Observed files
have a 16-byte header, a 64-byte CP932 NUL-terminated name slot followed by a
4-byte field for each declared texture reference. Preserve the trailing fields
as uninterpreted values: the title sample uses `64` for its first three and `0`
for its last, but their semantics are not proven.

Across 2,328 observed AT3 resources, node records begin with a `u32` 64-byte
name slot. Consecutive names and EOF bound records with a 192-byte opaque fixed
region and zero or more 112-byte opaque blocks. The parser exposes these raw
regions but does not decode their fields, establish UV meaning, or support safe
growth. Compare reference name stems with sibling TXC member names to identify
which textures an AT file references.

`--stored-order` is a diagnostic that reads indexed pixels linearly and uses
palette entries as stored, without the PSMT8 CLUT index permutation or GS alpha
expansion. The normal export applies that CLUT map, expands GS alpha, and leaves
pixel indices linear. In a controlled matrix of 10 PSMT8 and 10 PSMT4 resources,
this linear-pixel candidate avoided the tile artifacts in the old pixel-unswizzle
path. The owner selected the mapped-linear `title_marh_jp` preview: it shows the
Japanese logo in gray and color variants stacked vertically, matching the
supplied reference image. The TXC bytes match the enclosing bundle member
SHA-256. This supports an editable texture-surface representation for these
sampled indexed resources; it does not establish AT animation, UVs, or runtime
appearance. Sample paths and source hashes are in
`reports/rtx3_layout_diagnostics.json`.

The full prepared asset catalog plus parsed menu resource bundles contains
30,397 TXC records: 28,940 standalone archive leaves and 1,457 nested menu
bundle members. `make graphics-export` indexes every record and writes editable
images for 30,354 textures: 27,316 PSMT4, 1,654 PSMT8, 677 PSMT8H, 690 PSMT4HL
and 17 PSMT4HH. The full source-hash and TGA-dimension audit passes with
Japanese baselines unchanged; the latest pass found one English sibling for
`title_parts`. The 43 PSMCT32 records remain raw because their declared pixel
extents exceed their file bodies by eight bytes. See
`reports/rtx3_format_survey.json` for the sample preview/source-hash evidence
and [title rendering evidence](../tasks/TITLE_TEXTURE_RENDERING.md) for the first
English graphic reparse.

Images live directly inside flat, human-readable category folders such as
`graphics/title/`,
`graphics/icon/`, `graphics/user_interface/`, `graphics/effects/`,
`graphics/characters/`, `graphics/cards/`, and `graphics/backgrounds/`; there
are no PSM or source-container subfolders inside these art folders. Filenames
include stable archive IDs and resource names to prevent collisions. The
adjacent `graphics/index.json` maps each image to its exact TXC source and
original logical path, whether the TXC came from a menu bundle or a standalone
archive leaf. Category labels use path/resource evidence; generic assets fall
into `user_interface` rather than receiving a guessed subtype.
`make graphics-audit` checks source hashes, TGA dimensions, and local edits
across the entire indexed corpus.

Every exported baseline ends in `_jp.tga`, represents the recovered game artwork,
and must never be edited for localization. Keep it as the comparison and recovery
source. To localize an image, copy it to a sibling ending in `_eng.tga`, then
edit or regenerate only that English file. For example,
`...title_marh_jp.tga` pairs with `...title_marh_eng.tga`. When
`make build-mod-disc` stages the English ISO, the English sibling takes
precedence for that resource while the Japanese baseline stays intact. Generated
`_jp.tga` files and the index are ignored workspace outputs; authored `_eng.tga`
files remain visible to Git so completed localization art can be versioned. This
selects a user-authored variant; the tool does not translate or generate its
contents. Preserve canvas dimensions and use only
colors in the original palette. `make graphics-stage` writes changed TXCs under
`build/graphics-overrides/`, outside both `graphics/` and the extracted source
sidecars. Nested menu TXCs reinsert through the UI table/BPE path; standalone
TXCs are applied only when a generated manifest matches both their original and
replacement hashes, then reinsert through the containing archive. Synthetic
regressions cover both paths, and the unchanged source sidecars remain intact.
The normal mod-disc build consumes those overrides and builds `mar_eng.iso` in
the workspace root. In-game display is not yet validated.

The synthetic regressions exercise UTF-8 editing, CP932 encoding, ISO directory
extent growth, and volume-length update, plus structured message editing with
offset updates through a PAC. The real `_msg.dat` table has also been extracted,
rebuilt byte-identically, and grown using the tracked translation catalogue
through the full ISO build.
These checks do not prove retail text line wrapping, glyph coverage, or runtime
relocation behavior.
The verified mod run exposes two placement costs: a 15-byte single-prompt
growth appends a complete new PAC member at its parent, and the edited title
atlas must be rewrapped by the literal-identity BPE encoder. The build uses all
three tracked catalogues plus the title-parts English sibling. It grows
`_msg.dat` by 248 bytes (20,452 to 20,700), `CardList.txt` to 14,152 bytes
(13,451 to 14,152), and `DataBase.txt` to 3,319 bytes. The title bundle's decoded
size remains 922,000 bytes, while its `.b` wrapper grows from 301,071 to 922,091
bytes. The rebuilt 429,924,352-byte YFS is appended at the ISO end. The final
5,017,673,728-byte image inventories as 42 entries; nested reparsing matches all
four changed resources exactly. Its SHA-256 is
`4853c7a12799f52074a698ae5483a2def15178df741d81081d171e0d59be7c63`; the
authenticated comparator reports 752,229,873 differing bytes. This is an
expected mismatch for translation and append relocation. The current method is
space-heavy and has no runtime acceptance evidence. Exact-baseline comparison
is therefore an expected mismatch for a changed build; verify the authenticated
reference hash and inspect changed ranges rather than requiring equality.

## Byte-weighted recovery census

Use `make asset-census` to regenerate
[`reports/asset_recovery_census.json`](../reports/asset_recovery_census.json).
The generator combines the prepared leaf catalog, recursively validated layout
pieces, TXC index, parsed UI-bundle manifests, reversible text and message
catalogs, AT3 parser evidence, pinned disc inventory, and authenticated
unchanged-round-trip report. It fails if the reference or physical partition
does not balance, a standalone TXC is missing, a nested member hash disagrees,
or exclusive byte categories do not sum to their denominator.

Keep the two byte bases separate. The **physical image** is 4,587,749,376
bytes. It contains 3,324,768,000 bytes in all-zero named members and 2,527,881
bytes in all-zero gaps, totaling 3,327,295,881 measured all-zero bytes (72.5257%).
It also contains 1,237,522,725 bytes in nonzero terminal members (26.9745%) and
22,930,770 bytes in nonzero gap/structure extents (0.4998%). Those four disjoint
spans sum exactly to the image. The zero measurements prove byte values only;
they do not prove intentional padding, placeholder use, or historical purpose.

The **expanded logical information payload Y** is 1,303,947,016 bytes, or
28.4224% of the physical image size. It
starts with nonzero terminal member extents, replaces the 61,240,661 compressed
BPE wrapper bytes with 127,660,056 decoded UI-bundle member bytes plus 4,896
decoded raw bytes, and excludes UI-bundle control/gap bytes. This makes nested
assets visible without counting them twice or treating compressed wrapper
bytes as editable meaning.

Report each recovery level independently. Every nonzero physical member has a
validated hierarchy path and extent. Strict parser-backed structural coverage
is **Z/Y = 249,834,218 / 1,303,947,016 = 19.1598%**: complete RTX3 parses,
non-texture members bounded by parsed UI bundle tables, reversible text/message
sources, and directly parsed AT3 reference tables and validated node envelopes.
The 43 PSMCT32 RTX3 records fail the complete declared-length check and are
excluded from Z even though their headers identify candidate dimensions and
storage mode. The graphics index records strict parse success separately from
image-export support. Full unchanged-source rebuild coverage is **A/Y = 100%**,
backed by a byte-identical full-disc rebuild; it does not mean edited assets have
been runtime validated.

The AT3 envelope audit covers 723 direct archive leaves (1,840,708 bytes) and
1,605 nested UI-bundle resources (6,979,660 bytes). All 2,328 resources parse and
rebuild byte-identically; they contain 26,798 named node envelopes. For each
node, a 64-byte CP932 name slot is followed by a 192-byte opaque region and zero
or more 112-byte opaque blocks. Record boundaries satisfy this layout across the
entire observed corpus. The fixed and repeated regions are preserved raw; their
field meanings, runtime use, and relocation behavior remain unknown. Direct AT3
reference tables (68,144 bytes), bounded preambles (3,328), and node records
(1,769,236) contribute 1,772,564 bytes to Z; nested AT3 resources are already
counted as bounded UI-bundle members and are not added again. See
[`AT3 parser evidence`](../tasks/TITLE_TEXTURE_RENDERING.md) and the
`animation_resource_corpus` section of the census JSON.
Semantic editability is **B/Y = 239,532,814 / 1,303,947,016 = 18.3698%**,
comprising 239,444,320 editable texture bytes and 88,494 reversible text/message
source bytes. This measures available editable representations, not the share
already translated. Runtime-validated editable coverage is **C/Y = 0%**.

Keep two disjoint work-queue views. The complete non-editable remainder **Y-B**
is 1,064,414,202 bytes (81.6302% of Y); it includes structurally bounded members
that do not yet have an editable representation. Of that, **Z-B = 10,301,404**
bytes (0.7900% of Y) are structurally classified but not semantically editable.
The strictly unclassified remainder **Y-Z = 1,054,112,798** bytes (80.8402% of
Y) is the byte base for the opaque-payload breakdown below. These bases answer
different questions and must not be substituted for one another.

The disjoint `Y - B` remainder is 1,064,414,202 bytes. Its byte-weighted
inventory is:

| Remaining class | Bytes | Share of `Y - B` |
| --- | ---: | ---: |
| Video/cinematics | 685,111,296 | 64.3651% |
| Model/geometry candidates | 201,632,448 | 18.9430% |
| Audio/sound candidates | 156,453,642 | 14.6986% |
| Animation/motion candidates | 12,552,248 | 1.1793% |
| Executables/modules | 4,101,870 | 0.3854% |
| Other unclassified | 2,644,996 | 0.2485% |
| Font assets | 896,928 | 0.0843% |
| Script/data candidates | 880,126 | 0.0827% |
| Unresolved graphics (43 short PSMCT32 records) | 140,648 | 0.0132% |

These classes partition `Y - B`. Their names classify inventory by validated
signature, bundle member type, filename or path; they do not claim the opaque
bodies have been semantically decoded.

For the stricter opaque queue, use `Y - Z`, not `Y - B`. Its disjoint byte shares
are: video/cinematics 64.9941% (685,111,296 bytes), model/geometry candidates
19.0326% (200,625,168), audio/sound candidates 14.8422% (156,453,642),
executables/modules 0.3891% (4,101,870), animation/motion candidates 0.3540%
(3,731,880), other unclassified 0.2073% (2,184,740), font assets 0.0851%
(896,928), script/data candidates 0.0822% (866,626), and unresolved graphics
0.0133% (140,648). These are evidence-led inventory labels; candidate models,
audio, animation and script bodies remain opaque. The AT3 node envelopes narrow
the opaque queue without increasing semantic editability.

Texture-specific coverage remains a distinct measure: 30,397 occurrences
contain 239,584,968 TXC bytes, of which 239,444,320 (99.9413%) have editable
TGA exports. The tool tests exact physical partitioning, expanded accounting,
separate Z/A/B/C levels, and remainder balance in
`tests/test_asset_recovery_census.py`. The test suite also rejects absent strict
RTX3 parse evidence, checks malformed textures are excluded from Z, and verifies
that both `Y - B` and `Y - Z` category totals balance.

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
   Without `--relocate`, any member size change fails. By default, the output
   path must be new. `--replace-existing` is an explicit mod-build option for an
   existing regular output file; reconstruction still goes to a sibling
   temporary file, and `os.replace` installs it only after every requested
   catalogue and override was applied. A failed rebuild preserves the prior ISO.
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
`build WORKSPACE OUTPUT [--relocate] [--replace-existing]
[--translations CATALOG.json]` reads only workspace files, verifies complete
non-overlapping byte coverage and updates only table fields already located
during export. Existing-output replacement is opt-in, regular-file-only, and
atomic after successful reconstruction; symlinks and outputs inside the source
workspace are rejected. When given a catalogue, it verifies the original table
SHA-256 and requires exactly one matching message table. Unknown bytes are
preserved. `make build-mod-disc` supplies the tracked catalogues/graphics
overrides and opts into atomic replacement of the root `mar_eng.iso`.
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
