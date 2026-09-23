# Verified mechanisms

Authority: [STANDARDS.md](STANDARDS.md).

## Recursive container layouts make a full disc round-trip without source-byte fallback

Symptom: ISO extraction alone cannot support editing or prove reconstruction when
large data archives and unknown padding are present.
Mechanism: represent each recognized container as an exact ordered partition of
members and intervening gaps/tails. Preserve unrecognized leaves as raw files;
record observed parent offset/size fields for members. A source-only builder can
then recreate untouched containers without reading the reference image.
Pathway: authenticate the ISO before export; recursively parse only evidenced
ISO9660, YFS, AFS and PAC signatures; use stable numeric filenames plus a logical
catalog; compare complete reconstructed image using a streaming comparator that
also authenticates the reference hash.
Verification: both the initial and fully prepared workspace rebuilds of the supplied
4,587,749,376-byte image compare exactly; output and input SHA-256
both equal `cc059a3acf818dfbd0a782a9d20ee67e020d167866cd1c4dca77e6eb9224e3ec`,
and comparison reports zero differing bytes. Synthetic tests cover nested archive
round-trip and relocation-table updates.
Scope: one single-volume ISO, its observed YFS, AFS and two PAC table variants.
Limits: byte equality does not recover internal model/texture/audio/font/script
semantics. Appending grown members and changing archive/ISO references has not been
tested by game runtime. Reference provenance remains limited to the pinned file.
References: [asset methodology](TASK_ASSET_WORKSPACE_METHODOLOGY.md),
`tools/assets.py`, `tools/compare_disc.py`, `tests/test_assets.py`,
`tests/test_compare_disc.py`.

## BPE-wrapped menu bundles can be edited and reinserted as decoded payloads

Symptom: 724 menu `.b` leaves expose no useful image/string structure while
sharing a `BPE\0` header whose +0x0c field appears to be a decoded byte count.
Mechanism: the 16-byte wrapper has a 256-entry translation-table size, packed
payload length at +8 and decoded length at +12. Its recursive pair table can be
decoded with bounded expansion checks. A valid literal identity table can wrap
edited payloads in blocks up to 65535 bytes. The asset workspace saves each
decoded payload beside its compressed source and compares source/decoded hashes:
untouched assets retain original compressed bytes; edits are wrapped and fed into
the existing archive/ISO relocation path.
Pathway: run `make prepare-assets`, edit a `.decoded.bin`, then build through
`tools/assets.py build ... --relocate`; use the regular untouched `make verify-disc`
gate when proving no-op source-byte preservation.
Verification: all 724 prepared menu `.b` leaves decode to exactly their declared
output size. Tests cover malformed wrappers, cyclic expansion, block boundaries,
edited-payload reinsertion and growth relocation; `make test` passed all 51 tests.
The no-op full-disc build and `make verify-disc` compare match exactly at
4,587,749,376 bytes, SHA-256
`cc059a3acf818dfbd0a782a9d20ee67e020d167866cd1c4dca77e6eb9224e3ec`, with zero
differing bytes.
Scope: the sampled menu BPE wrapper and generic asset builder integration.
Limits: identity-table packing does not reproduce original compressed bytes after
an edit and is larger than source; nested resource records are only sampled, TGA
references are not images, `RTX3` pixels are not decoded, and no runtime test has
been performed.
References: [asset methodology](TASK_ASSET_WORKSPACE_METHODOLOGY.md),
`tools/bpe.py`, `tools/assets.py`, `tests/test_bpe.py`, `tests/test_assets.py`,
`reports/ui_b_format_survey.json`.

## UTF-8 translation edits can grow through CP932 and ISO relocation

Symptom: translated text may encode to more bytes than the original Japanese
member and invalidate fixed-size container assumptions.
Mechanism: the workspace stores a UTF-8 companion while retaining the raw leaf
and layout size. During build, the edited UTF-8 is encoded back to CP932; the
explicit relocation mode appends the grown member, patches its evidenced parent
extent, and updates the ISO directory record and volume length.
Pathway: edit UTF-8, use `make build-mod-disc` for the growth-enabled output,
inventory the resulting ISO, and compare it against the pinned image to inspect
the expected changed ranges.
Verification: `test_utf8_translation_grows_cp932_leaf_and_relocates_iso` confirms
encoded payload bytes, updated file size/LBA and ISO volume length on a synthetic
ISO. `python3 -m unittest tests.test_assets -v` passed all seven focused tests.
Limits: this proves packaging mechanics only; it does not validate game-specific
text layout, glyph coverage, or runtime acceptance. See the separate
[`_msg.dat` task evidence](../tasks/MESSAGE_TABLE.md) for the structured Japanese
dialogue-table pathway.
References: [asset methodology](TASK_ASSET_WORKSPACE_METHODOLOGY.md),
`tests/test_assets.py`, `Makefile`.

## Strict structured export keeps a message table editable while recalculating offsets

Symptom: a binary message table contains readable text but fixed byte offsets make
direct replacement unsafe when translations change length.
Mechanism: one observed `_msg.dat` has an 8-byte header, 229 fixed-size records,
and an ordered CP932 NUL-terminated string area. Record offsets are relative to
byte 8; string extents end at the next record's offset.
Pathway: validate the complete table before producing JSON with stable record
`kind`/`key` fields, then encode CP932 and recalculate the offset table on build.
The workspace builder can then relocate the grown archive member.
Verification: the original 20,452-byte table rebuilds exactly; all 30 recorded
member/gap hashes in the containing PAC match on untouched rebuild; a temporary
translation grew and relocated the real member and survived reparsing. Unit tests
cover exact roundtrip, invalid records, encoding failure, growth, and PAC relocation.
Scope: only `disc!/_DATA.YFS;1!/data/common.pac!/_msg.dat` in the pinned image.
Limits: record field semantics, other `.dat` variants, game line layout and runtime
acceptance are unresolved.
References: [task evidence](../tasks/MESSAGE_TABLE.md), `tools/messages.py`,
`tools/assets.py`, `tests/test_messages.py`, `tests/test_assets.py`.

## Stable translation IDs keep catalogue edits attached to the authenticated source

Symptom: editable extraction JSON is useful for experiments but is ignored
workspace state, so translation edits are not reviewable or reproducible in Git.
Mechanism: preserve the source table hash and each exact original string in a
tracked catalogue. Identify records by observed `kind`, `key`, and their
occurrence among duplicate pairs; use the table index as corroborating evidence.
Pathway: generate the catalogue once from the prepared source, edit only the
nullable translation/status/context fields, and let `build-mod-disc` validate
the pinned table identity before applying overrides. Blank translations retain
the original bytes; stale or unmatched catalogues fail closed.
Verification: the all-original tracked catalogue built a full image matching the
pinned reference exactly. One 15-byte translated growth rebuilt through the full
ISO/YFS/PAC path; inventory passed and the streaming comparator authenticated
the baseline while reporting the expected changed-image mismatch. The current
227-entry draft also rebuilt and reparsed all 229 messages exactly; the translated
table grows by 250 bytes in aggregate and the comparator reports the expected
authenticated mismatch. Unit tests cover duplicate IDs, source drift and
catalogue-driven PAC relocation.
Scope: the one observed `disc!/_DATA.YFS;1!/data/common.pac!/_msg.dat` resource.
Limits: the 229 English strings are draft translations; review, runtime layout,
script call sites, and remaining text-bearing formats are still unresolved.
References: [message-table evidence](../tasks/MESSAGE_TABLE.md),
`localization/messages.json`, `tools/message_catalog.py`, `tests/test_message_catalog.py`,
`Makefile`.

## Section names survive removal of the symbol table

Symptom: ELF has no SHT_SYMTAB but thousands of named sections.
Mechanism: GNU linkonce section names can preserve method/type spellings separately
from symbol tables. Inspect the section-string table before treating all code as anonymous.
Evidence: this boot ELF has 2,251 sections, including named CCamera accessors.
Verification: Python inventory, GNU readelf and LLVM disassembly agree on the selected
sections; eight accessor sections reassemble to the same 64 bytes.
Scope: this single ELF and these eight standard MIPS sequences with Clang 21.1.8.
Limits: section names do not prove original signatures, class layout, compiler version,
or boundaries inside the main `.text`; do not generalize assembler support to R5900.
References: [bootstrap evidence](tasks/BOOTSTRAP.md), `make verify-camera`.

## Require inline definitions through an explicit experiment harness

Symptom: a historical compiler emits no section for an unused inline member.
Mechanism: the experiment has not required an out-of-line definition. Taking a
member-function address makes that requirement explicit without changing the
method body or adding code-generation attributes.
Pathway: keep address-taking in a separate harness and compare only the evidenced
method sections; never present harness objects as recovered game data.
Verification: EE GCC `2.96-ee-001003-1` with the same `-O2` for 62 accessors
across seven partial classes reproduces all 496 bytes; the full probe ELF also
compares identically.
Limits: trivial methods do not identify the original compiler or complete class.
References: [compiler experiment](tasks/COMPILER_PROBE.md),
[linkonce cluster](tasks/LINKONCE_CLUSTER.md), `make verify-ee`.

## Linkonce sections cluster contiguously outside main .text, and their address range predicts a census

Symptom: only a handful of named sections were known, all within one class;
the possibility of many more went unnoticed because nothing pointed a worker
at them.
Mechanism: a linker that folds GNU linkonce/COMDAT-style sections (one per
inline/template instantiation) tends to place them together, after the
"normal" compiled `.text`. Here `.text` ends at exactly the address where the
first `.gnu.linkonce.t.*` section begins (`0x33af18`), and 1,694 more named
sections (71,932 bytes, 497 classes by mangled-name heuristic) follow
contiguously. 733 of them are exactly 8 bytes — the same trivial
`jr $ra` + one delay-slot instruction shape already proven recoverable.
Pathway: when one named section is found, check whether `.text`'s
declared `address + size` equals that section's address; if so, inventory the
whole contiguous run instead of treating the one finding as isolated. A small
mangled-name shape classifier (`tools/linkonce_inventory.py`) turns this into
a reusable census: kind (member/const member/constructor/destructor/type-info),
class name where the shape supports it, and a size histogram to prioritize
which sections are cheap to recover next.
Verification: `reports/linkonce_text_inventory.json`; classifier tested in
`tests/test_linkonce_inventory.py` against real observed mangled names,
including cases deliberately left `unparsed` (template instantiations) rather
than guessed.
Scope: this single ELF's linkonce region and GNU v2/cfront-style mangling.
Limits: the classifier is a naming-shape heuristic, not a demangler; it does
not decode parameter/return types and must not be trusted for semantics.
A section's small size does not guarantee its recovery is risk-free — always
disassemble before writing a natural-source candidate.
References: [linkonce cluster task](tasks/LINKONCE_CLUSTER.md), `make verify-ee`.

## Exclude replaced bytes from bootstrap source intervals

Symptom: a bootstrap can appear to match while silently retaining original bytes
instead of consuming changed compiled code.
Mechanism: a layout with exhaustive, non-overlapping intervals and mandatory
object-sourced regions eliminates that fallback path.
Pathway: explicitly export unknown bytes as labeled debt, omit selected methods,
require relocation-free objects for those holes, and compare the complete file
with an independent byte comparator. Test that changed object bytes propagate.
Verification: full boot equality, negative reconstruction tests and a temporary
build tree without reference files all pass.
Scope: fixed-placement boot ELF, eight position-independent accessor sections.
Limits: this is not a linker, a full-disc rebuild or semantic recovery of raw regions.
Reference: [reconstruction procedure](TASK_BOOT_RECONSTRUCTION_METHODOLOGY.md).


## Source-hash-anchored TSV localization catalogues

Symptom: CP932 menu catalogues carry player-facing labels and captions in
fixed tab-separated records, but plain UTF-8 companions alone do not provide
stable translation identities or guard against stale source data.
Mechanism: retain each original cell, a row ID (observed key where available,
otherwise row index), original line ending, resource path and source SHA-256 in
an editable UTF-8 JSON catalogue. Apply only selected columns, preserving tabs,
blank trailing cells and line endings; reject source drift and non-CP932 output.
Pathway: use `tools/text_catalog.py` catalogs and pass their paths through
`--text-translations`; the nested asset builder applies by exact logical resource
path and fails if any requested catalogue is unused.
Verification: tests cover round trip, CRLF, blank fields, source mismatch, duplicate
IDs, encoding errors and archive reinsertion. The mod ISO inventory and nested
ISO/YFS/PAC reparse recovered exact catalog-applied `CardList.txt` and `DataBase.txt`
bytes. The current drafts translate CardList names/titles/categories (captions still
Japanese) and DataBase headings/display labels/password markers (condition metadata
still unresolved).
Scope: the two observed tab-separated resources in `MenuBinary.pac`.
Limits: runtime use, display constraints, captions, condition-field semantics and
runtime relocation remain unverified.
References: `tools/text_catalog.py`, `localization/card_list.json`,
`localization/database.json`, `tests/test_text_catalog.py`,
`tests/test_assets.py`, [asset methodology](TASK_ASSET_WORKSPACE_METHODOLOGY.md).
