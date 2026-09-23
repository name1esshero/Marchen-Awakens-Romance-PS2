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

## Common menu bundles expose typed resources with lossless extraction and relocation

Symptom: the decoded BPE bytes still combine animation metadata, textures, and
other resources, so editing a whole opaque bundle would leave inner extents stale.
Mechanism: in 721 of 724 menu `.b` payloads, `u32le@0` is an entry count followed by
a `01 01 00 00` marker and 32-byte records. Each record carries a 16-byte name,
4-byte type, size at +20, offset at +24, and an unknown +28 field. The parser checks
the table extent, 16-byte member alignment and non-overlap, while retaining the
original decoded container bytes and all gaps. Extracted members use stable index
names and source-hash manifests. Same-size edits patch the old range; grown members
append at a 16-byte boundary and update size/offset. BPE and outer archive builders
then propagate growth.
Pathway: `make prepare-assets` creates `.bundle.json` manifests and `.resources/`
member sidecars beside decoded `.b` payloads. Edit one member and run the existing
`tools/assets.py build ... --relocate` workflow. Do not edit both a decoded bundle
and its member sidecars in the same build.
Verification: `python3 tools/ui_bundle.py audit extracted/assets` reports 721/721
untouched bundle rebuilds byte-identically across 3,084 resources (1,605 `at3`,
1,457 `txc`, 14 `ymp`, seven `pac`, one `txt`); no table ranges overlap and all
offsets are 16-byte aligned. A synthetic `txc` growth test reparses after BPE and
PAC relocation. `python3 -m unittest tests.test_ui_bundle tests.test_assets -v`
passed 13 tests.
Limits: three `.yma` BPE payloads use an unresolved layout. TXC pixel conversion is
covered in the later RTX3 entry below; runtime asset acceptance and runtime
relocation remain unverified.
References: `tools/ui_bundle.py`, `tools/assets.py`, `tests/test_ui_bundle.py`,
`tests/test_assets.py`, `reports/ui_bundle_survey.json`,
[asset methodology](TASK_ASSET_WORKSPACE_METHODOLOGY.md).

## Indexed RTX3 textures export as editable TGAs and reinsert through archive paths

Symptom: menu texture payloads begin with `RTX3` and are not directly editable
as ordinary raster files. An early TGA pass also copied the PS2's 0..128 alpha
range unchanged, making opaque colors display at half opacity.
Mechanism: indexed PSMT4/PSMT8/PSMT8H/PSMT4HL/PSMT4HH export currently reads
the compact declared pixel extent in linear order, applies the PSMT8 CLUT index
permutation (identity for the PSMT4-family layout), and expands alpha from the
GS 0..128 range to TGA's 0..255 range. Sony's GS manual describes the high-bit
lanes in PSMCT32 GS memory; the RTX3 compact-pixel interpretation is separately
supported by source extents and coherent previews, not proven runtime sampling.
Import preserves original indexed pixels when unchanged and maps edited colors
to the existing palette; canvas and palette growth are unsupported. The root
`graphics/` workspace exports directly into flat, human-readable category
folders and indexes image/source hashes plus the original logical path. English
siblings ending `_eng.tga` are selected over Japanese baselines for the mod ISO.
Menu members stage under their bundle path; standalone TXC leaves stage under a
hash-anchored manifest and are applied only to the matching raw leaf during
recursive archive rebuilding. Both paths leave source sidecars intact.
Pathway: `make graphics-export`; edit same-size files under `graphics/`; name an
English sibling `*_eng.tga` (replace a trailing `_jp` with `_eng`); run
`make graphics-audit` and `make graphics-stage`; then run
`make build-mod-disc` to produce `mar_eng.iso` in the workspace root.
Verification: controlled visual comparison covered 10 PSMT8 and 10 PSMT4
resources; the owner selected the mapped-linear `title_marh_jp` preview matching
the supplied reference. The corrected title image has 141,269 fully transparent
pixels, 54,738 alpha-128 source pixels mapped to fully opaque TGA alpha, and
66,137 intermediate-alpha pixels. The workspace indexes 30,397 TXCs (28,940
standalone leaves and 1,457 menu members) and exports 30,354 images: 27,316
PSMT4, 1,654 PSMT8, 677 PSMT8H, 690 PSMT4HL, and 17 PSMT4HH. This direct
full-index count corrected the swapped PSM labels in the earlier format report.
The complete source-hash/dimension audit passes with Japanese baselines unchanged.
Synthetic end-to-end tests confirm
English siblings reach both nested UI-table/BPE/PAC and standalone TXC/PAC while source
sidecars stay intact. The full audit uses `rtx3.tga_dimensions` to validate TGA
headers and extents without decoding every pixel. Separate PNG previews of five
standalone character, environment, sky, effect, and font textures looked coherent
without visible tile artifacts; their source hashes and raster paths are recorded
in `reports/rtx3_layout_diagnostics.json`. The follow-up high-bit extension's
source-hash/dimension audit also passed.
Previews for `hp_face_00` (PSMT8H), `hp_mar` (PSMT4HL), and `txts` (PSMT4HH)
show coherent character, icon and text-atlas content; paths and source/TGA hashes
are in the format survey.
Scope: all catalogued TXCs plus nested menu-bundle TXCs; an unparsed PAC leaf
could contain undiscovered members. The 43 PSMCT32 payloads remain raw because
each is eight bytes short of its declared pixel extent. The controlled 20-image
layout matrix covers PSMT4/PSMT8; the three high-bit previews are separate
candidate evidence, not a corpus-wide decoder or runtime proof. AT/UV composition
and runtime rendering remain unresolved. The first English title-parts sibling
now passes audit and exact ISO/YFS/BPE/UI-table reparse, but no English graphic
has yet been runtime-validated. The literal-identity BPE writer expands edited
`title_tex.b` from 301,071 to 922,091 bytes, so reinsertion works with a material
space cost until a verified compressing encoder exists.
References: `tools/rtx3.py`, `tools/graphics.py`, `graphics_rules.mk`,
`tests/test_rtx3.py`, `tests/test_assets.py`, `reports/rtx3_format_survey.json`,
`reports/rtx3_layout_diagnostics.json`, `reports/translation_surfaces.json`,
[asset methodology](TASK_ASSET_WORKSPACE_METHODOLOGY.md),
[`TITLE_TEXTURE_RENDERING.md`](../tasks/TITLE_TEXTURE_RENDERING.md).

## Mod-disc rebuilds can replace an existing ISO atomically

Symptom: a second `make build-mod-disc` previously stopped because its root
`mar_eng.iso` output already existed, leaving the user to move or delete an ISO
manually before iterating on localization.
Mechanism: `assets.build` already writes a complete candidate to a sibling temp
file and installs it with `os.replace` only after all requested translations and
overrides were applied. The output guard now has an explicit
`--replace-existing` option for replacing an existing regular file; the default
remains fail-closed, and symlinks or outputs inside the source workspace remain
rejected.
Pathway: use the project `make build-mod-disc` target, which opts into atomic
replacement of the root `mar_eng.iso`. Other build callers retain the new-output
requirement unless they explicitly pass the flag.
Verification: `test_existing_build_output_replacement_is_opt_in_and_atomic`
proves default refusal, preservation of the previous output after a failed
relocation, and successful replacement after a valid build. The real mod target
also replaced a prior ISO only after the new full image completed; its nested
resources and pinned-reference comparison were then checked.
Limits: atomic installation says nothing about game/runtime correctness; the
previous output is replaced after success and is not retained as a backup.
References: `tools/assets.py`, `tests/test_assets.py`, `Makefile`,
[asset methodology](TASK_ASSET_WORKSPACE_METHODOLOGY.md),
[`TITLE_TEXTURE_RENDERING.md`](../tasks/TITLE_TEXTURE_RENDERING.md).

## AT header inspection links animation texture names to TXC members

Symptom: `.at3` files refer to `.tga` names, but the texture payloads are stored
as TXC resources and the relationship needs verification before composing a
menu screen.
Mechanism: observed AT files begin with `AT  `, a 16-byte header, then the
declared number of 64-byte CP932 name slots, each followed by a four-byte field.
The trailing field values are retained as raw integers because their purpose is
not established.
Pathway: run `python3 tools/at3.py SOURCE.at3`; compare each decoded name stem
with sibling TXC member names. The corpus-wide follow-up now recognizes bounded
node envelopes; keep their internal fields opaque until their semantics are
evidenced.
Verification: the title file yields four references, all matching names in the
sibling TXC bundle manifest; the bounded parser passes valid and malformed
synthetic cases in `tests.test_at3`.
Scope: observed title AT resource and matching bundle. Node records are described
in the following success; actual draw order and UV interpretation remain
unresolved.
References: `tools/at3.py`, `tests/test_at3.py`,
[`TITLE_TEXTURE_RENDERING.md`](../tasks/TITLE_TEXTURE_RENDERING.md).

## AT3 animation node envelopes can be split and rebuilt without guessing field meanings

Symptom: AT3 resources contain animation data after their texture-reference
table, and treating the entire tail as one opaque byte range hides stable record
boundaries needed for later decoding.
Mechanism: across the observed corpus, each node begins with a `u32` value 64
and a zero-padded 64-byte CP932 name slot. Consecutive name slots and EOF bound
records whose remaining extent is always 192 bytes plus zero or more 112-byte
blocks. The invariant establishes envelope boundaries; it does not name fields
inside those regions.
Pathway: use `python3 tools/at3.py INPUT.at3 --output-json EDITABLE.json` to expose
references, fixed-slot node names, the preserved preamble, and opaque regions.
After a same-size byte/name edit, rebuild with
`python3 tools/at3.py --build-json EDITABLE.json --output OUTPUT.at3`. The writer
preserves unknown bytes and refuses reference-count or node-size changes.
Verification: `make asset-census` audits 723 direct archive leaves and 1,605
nested UI-bundle resources: all 2,328 parse, all 2,328 rebuild byte-identically,
and all 26,798 node envelopes satisfy the size invariant. Synthetic tests cover
name-slot editing, exact round trips, unsupported extents, and rejected growth.
Scope: the pinned image's current prepared asset tree. Direct AT3 reference
tables (68,144 bytes), bounded preambles (3,328 bytes), and node records
(1,769,236 bytes) add 1,772,564 bytes to structural coverage Z; nested AT3
members were already counted once as bounded UI-bundle extents.
Limits: the 192-byte regions and 112-byte blocks remain raw, fixed-size hex
editing is not semantic recovery, texture UVs and layer order are unproven, and
no edited AT3 has been runtime-tested. Do not grow records until reference and
relocation semantics are recovered.
References: `tools/at3.py`, `tools/asset_recovery_census.py`,
`tests/test_at3.py`, `tests/test_asset_recovery_census.py`,
[`asset census`](../reports/asset_recovery_census.json),
[`title evidence`](../tasks/TITLE_TEXTURE_RENDERING.md).

## YOBJ/YMP header and POF0 extents can be audited and rebuilt losslessly

Symptom: nearly 200 MB of `.ymp` model candidates were counted only by filename;
their model bodies were opaque and could not be separated from malformed or
misidentified files by the asset census.
Mechanism: 898 direct files begin with `YOBJ`; one `basebone.ymp` begins with an
8-byte `DUMY` preamble and then `YOBJ`. Both variants carry a fixed 0x40-byte
header whose duplicated POF0 offset resolves to a `POF0` block ending exactly
at EOF. Its length-bounded payload decodes into monotonically increasing,
four-byte-aligned pointer-slot offsets. The parser validates all listed slots
and their nonzero targets against the complete model envelope. It keeps all
header numbers and body bytes opaque. The basebone file's additional zero tail
inside POF0 is retained.
Pathway: use `python3 tools/yobj.py SOURCE.ymp --output-json EDITABLE.json`, then
`python3 tools/yobj.py --build-json EDITABLE.json --output REBUILT.ymp` for an
unchanged or same-size body edit. The bounded writer rejects growth.
Verification: `make asset-census` parses and rebuilds all 899 direct YMP files
(197,085,308 bytes) and 14 nested UI-bundle YMP members exactly. It validates
803,754 direct and 3,685 nested POF0 pointer slots. The 899 direct envelopes
add 197,085,308 bytes to structural coverage Z; nested members were already
counted in their bundle extents. Tests cover both header variants, POF0 decoding,
same-size body edits, malformed pointer streams and no-growth rejection.
Scope: every YMP in the current prepared archive catalog and parsed UI bundles.
Limits: this establishes envelope structure, not geometry/material semantics,
safe internal relocation, YPC structure, edited-model runtime behavior or
semantic editability. The external
[YOBJ POF0 generator](https://github.com/rumblerosesxx/yobj_pof0_generator/blob/main/pof0gen.c)
was a cross-format lead; the tool's claims are not treated as game provenance.
References: `tools/yobj.py`, `tools/asset_recovery_census.py`,
`tests/test_yobj.py`, `tests/test_asset_recovery_census.py`,
[`YOBJ evidence`](../tasks/YOBJ_MODEL_RECOVERY.md),
[`asset census`](../reports/asset_recovery_census.json).

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

## An untyped or wrongly-passed parameter silently mismangles a linkonce section name

Symptom: `compare_sections.py` raises a `KeyError` (missing section), not a
byte mismatch, after adding a natural-looking candidate method with a
class-typed parameter.
Mechanism: GNU v2/cfront mangling encodes a class-typed parameter's exact type
*and* how it is passed in the section name, and EE GCC happily compiles and
emits a section under whatever name that produces — just not the target name,
if any of these differ from the evidence. Three confirmed letter codes:
`P<len><Name>` (pointer, e.g. `P9objMatrix`), `R<len><Name>` (a genuine C++
reference, `Type &`), and `G<len><Name>` (a class passed **by value**,
distinct from a real `&` reference in the source).
**Correction (superseding the original wording of this entry):** `G` was
first believed to require a non-trivial constructor/destructor specifically
(reasoning backward from one case where adding an empty constructor "fixed"
a mismatch). Two later standalone probes disproved this: a completely empty
`class SArmTypeD {};` and a class with a plain data member both mangle their
by-value parameter as `G<len><Name>` with no constructor at all, and
retesting the original `MotionNo` case with the constructor removed produced
the identical `G8MotionNoif`. The constructor was never necessary — `G`
simply marks *any* class type passed by value, trivial or not.
Declaring the parameter as `void *` instead of the named class mangles to
`Pv`; guessing `R` for a `G` case (or vice versa) also produces a different
name. A related shape is a bare `T<n>` suffix (e.g.
`OnMotionJumpPre__8CPAppearP9AprMotionT1`): this is a back-reference
compressing a parameter whose type exactly repeats an earlier parameter's
type in the same list, so `(AprMotion *, AprMotion *)` mangles with the
second occurrence as `T1` rather than repeating `P9AprMotion` — simply
declaring the repeated parameter with the identical type reproduces it,
confirmed on a standalone probe before use in the real candidate.
The comparison tool correctly reports the target section as absent
rather than mismatched, which can look like "the method wasn't emitted" when
the real cause is a wrong parameter type or passing convention.
Pathway: when a raw parameter-encoding suffix from
`tools/linkonce_inventory.py`'s census (or the mangled name directly) shows
`P<len><Name>`, `R<len><Name>`, or `G<len><Name>`, define a class `<Name>`
(a bare `class <Name> {};` suffices — no constructor needed for any of the
three) and match the encoded pointer/reference/by-value shape exactly —
never substitute `void *` or guess between `R`/`G`. Before committing a guess,
verify it on a small standalone probe (compile, inspect the emitted section
name) rather than assuming a letter's meaning. This has now been needed four
times independently: `C3dObject::SetLinkBoneMat(objMatrix *)` (`P`),
`CCharaBase::SetCurrentStatus(int, int, TypeArmParam *, int)` (`P`),
`CWeapon::SetSubMotion(MotionNo, int, float)` (`G`, after an initial `R` guess
compiled cleanly but produced `R8MotionNoif` instead of the target
`G8MotionNoif`), and `CCharaDataSts::CheckGatyaStsArm(SArmTypeD)` (`G` again,
this time confirmed directly with an empty class on the first try). The same
length-prefixed-name shape also applies to enum
parameters (no `P`/`R`/`G` letter — an enum is a value type, so it just needs
a matching-named definition, e.g. `enum InterpType { ... };` for
`SetInterpolateType__7CMotion10InterpType`); unlike the class/`G` case, no
non-trivial-constructor trick is needed since the enum already mangles by its
own name.
Verification: all cases compile with the unchanged EE GCC `2.96-ee-001003-1`
`-O2` probe and reproduce the exact target section after the fix, confirmed
by `make verify-ee`.
Scope: GNU v2/cfront-style mangling on this EE GCC target; likely generalizes
to any compiler using the same mangling scheme.
Limits: this only fixes the *name*; it says nothing about the pointee class's
real layout, size or members, which remain unrecovered placeholders.
References: [linkonce cluster task](tasks/LINKONCE_CLUSTER.md).

## The `move` pseudo-op and EE GCC disagree on which register-move encoding to use

Symptom: a hand-written `.s` accessor using `move $rd, $rs` for an
already-evidenced `daddu`-based register move fails `compare_sections.py`
with a same-size byte mismatch.
Mechanism: on this MIPS/R5900 target, Clang's assembler lowers the `move`
pseudo-instruction to `or $rd, $rs, $0` (opcode 0x25), but the reference
binary (and independently, EE GCC 2.96 compiling equivalent C++ such as
`return value;` or `return 0;`) uses `daddu $rd, $rs, $0` (opcode 0x2d) for
the same logical operation. Both encode the same result register-to-register
copy; only the raw bytes differ.
Pathway: in hand-preserved `.s` files for this target, never rely on the
`move` pseudo-op to reproduce an evidenced register-copy — write
`daddu $rd, $rs, $0` explicitly. This does not apply at the C++ layer: EE GCC
chose `daddu` on its own with no steering needed.
Verification: `llvm-objdump-21` on both a `move`-assembled test object and a
`daddu`-assembled one, compared against the original bytes at
`CChara::GetNowGmPadCheck` (`daddu $2, $5, $0`) and several
`CCharaBase`/`CChara` zero-returning stubs (`daddu $2, $0, $0`).
Scope: Clang 21.1.8 assembling `-target mipsel-none-elf -march=mips3 -mabi=32`
for this project's boot ELF; likely generalizes to other MIPS/R5900 pseudo-op
lowering choices worth double-checking against evidence rather than assuming.
Limits: does not establish that `or`-based moves never appear in the real
binary elsewhere, only that this specific evidenced pattern uses `daddu`.
References: [linkonce cluster task](tasks/LINKONCE_CLUSTER.md).

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
bytes. All 142 CardList caption cells now have CP932-encodable English drafts;
with names/titles/categories, the applied file grows from 13,451 to 14,152 bytes
and reparses exactly from the rebuilt ISO. The same full-image build reparses all
three catalog-applied text resources. DataBase headings/display labels/password
markers are drafted; 39 condition metadata cells remain unchanged.
Scope: the two observed tab-separated resources in `MenuBinary.pac`.
Limits: caption quality, runtime use, display constraints, condition-field
semantics and runtime relocation remain unverified.
References: `tools/text_catalog.py`, `localization/card_list.json`,
`localization/database.json`, `tests/test_text_catalog.py`,
`tests/test_assets.py`, [asset methodology](TASK_ASSET_WORKSPACE_METHODOLOGY.md).

## Separate physical and expanded byte bases in asset recovery censuses

Symptom: a file-count percentage hides byte scale, while a single leaf-byte
percentage either lets measured all-zero spans dominate or misses editable
members nested inside compressed `.b` bundles. Calling unchanged round-trip
coverage “decompilation” would overstate semantic recovery.

Mechanism: the physical layout tree partitions every image byte into named
members and gap spans; BPE/UI manifests describe a second, expanded logical
member layer. The layers overlap physically, so they require separate
denominators and explicit replacement accounting. Structure, unchanged-source
rebuildability, semantic editability and runtime validation are independent
evidence levels.

Successful pathway: first partition physical all-zero members/gaps,
information-bearing leaf extents and nonzero structure/gaps. Then replace
compressed wrappers with decoded member extents once, excluding bundle control
bytes. Carry strict parser-success evidence into the asset index: a recognized
header alone does not qualify a truncated RTX3 member for structural coverage.
Define parser-backed structural coverage and semantic-editable sources
explicitly; keep unchanged round-trip and runtime evidence separate. Report both
the full non-editable queue `Y-B` and the strictly structurally unclassified
remainder `Y-Z`, with the `Z-B` bridge for structurally classified but
non-editable bytes. Give every
remaining byte exactly one evidence-labeled inventory class and assert all
physical, logical, and category totals balance. Report all-zero spans as byte
measurements only; do not infer intentional padding from zero contents.

Verification: `make test` and `python3 tools/asset_recovery_census.py` pass; the
census audits all 13 video streams, partitions the 4,587,749,376-byte image
exactly, and reports expanded logical payload Y=1,303,947,016. The schema-v6
snapshot at this milestone reported Z/Y=86.8157%, A/Y=100%, B/Y=18.3698%, and
C/Y=0%. Its human-readable
summary prints the zero-byte measurement with intent caveat, physical and
expanded byte bases, independent recovery levels, and both remaining queues.
The snapshot's levels were Z/Y=86.8157% parser-backed structure, A/Y=100%
unchanged-input no-op rebuild, B/Y=18.3698% semantic editability, and C/Y=0%
runtime-validated editability. The increase in Z includes complete packet/sector
coverage for all 13 direct movie streams (685,111,296 bytes); packet framing
does not establish video/audio codec semantics or editability. The 43 short
PSMCT32 records (140,648 bytes) remain excluded from Z because strict RTX3
parsing rejects their full-length contract. TXC-only editability is
239,444,320/239,584,968 bytes (99.9413%). The AT3 audit covers 2,328
direct/nested resources and validates 26,798 node envelopes with exact no-op
rebuilds. The YOBJ audit covers 899 direct and 14 nested resources, validating
807,439 POF0 pointer slots with exact no-op rebuilds. `Y-B` is 1,064,414,202
bytes; `Z-B` is 892,498,008 bytes; the strictly unclassified `Y-Z` remainder is
171,916,194 bytes. The report gives separate byte-weighted category totals for
both denominators. Tests verify physical partitioning, nested accounting,
parser-validity gating, distinct level numerators, both remainder totals,
summary denominators, and reference binding.

Scope: this pinned image, current prepared catalog, validated layout tree,
strictly indexed TXCs and parsed bundle manifests. Limits: broad remainder
classes may be signature-, extension- or path-led; they are not complete
semantic recovery. Structurally bounded resource bodies can still be opaque.
No edited payload has passed runtime validation; one nested `tex.pac` remains
raw.

References: `tools/asset_recovery_census.py`,
`tests/test_asset_recovery_census.py`,
[`reports/asset_recovery_census.json`](../reports/asset_recovery_census.json),
[asset methodology](TASK_ASSET_WORKSPACE_METHODOLOGY.md).

## Reuse native English lettering when localizing a Japanese logo atlas

Symptom: a Japanese title wordmark needs an English graphic, while recreating
the game's custom lettering with a generic font would lose the original brand
style. A neighboring title texture already contains the same title in English,
but also embeds a Japanese subtitle along its lower edge.
Mechanism: the native English wordmark can be reused as source artwork; masking
the subtitle region before scaling preserves the actual letter shapes and avoids
copying Japanese fragments into the localized atlas.
Successful pathway: keep the `_jp.tga` source immutable. Crop the English
lettering from the sibling texture, remove the Japanese-only subtitle, map it
into the corresponding English atlas slots, preserve other marks, and retain
the original canvas and indexed palette. Insert it only as a same-size `_eng.tga`
override.
Verification: the complete graphics audit recognized six English overrides and
reported zero changed Japanese baselines. `make verify-graphics-image` reparsed
all six TXCs through ISO/YFS/BPE/UI-table layers and matched 709,120 bytes to
their staged overrides. The new root ISO is 5,020,790,784 bytes with SHA-256
`6619394dc8343641d5c2acb9a33e7cfe6e3c40abf4687c92d9b53ff8b579e901`; its
authenticated pinned-reference comparison is recorded in
`reports/mar_eng_compare.json`.
Scope: the `title`, `title_marh`, and `title_parts` marks, plus the `shop`, mode
name and field-name UI textures.
Limits: reusing the wordmark does not establish the correct on-screen crop,
scale, animation state or draw order. Other title variants and Japanese text in
`windisp` remain queued; the failed `sbttl` image-generation attempt is
documented in [`GRAPHIC_TEXT_LOCALIZATION.md`](../tasks/GRAPHIC_TEXT_LOCALIZATION.md).
The sibling texture still displays English branding elsewhere, so duplicate
marks are possible until AT/UV layout and runtime rendering are checked.
References: `graphics/title/00039_01566_0002_title_marh_eng.tga`,
`graphics/title/00039_01566_0003_title_parts_eng.tga`,
[`TITLE_TEXTURE_RENDERING.md`](../tasks/TITLE_TEXTURE_RENDERING.md),
`tools/graphics.py`, `tools/verify_graphics_in_iso.py`, `tools/rtx3.py`.

## Reuse localized title lettering in the ttlprts atlas

Symptom: `title_new_tex.b`'s 512x512 `ttlprts` atlas contains three Japanese
wordmark treatments and a vertical Japanese creator/publisher credit alongside
English title prompts. Replacing the full image would also discard existing
English lettering and layout.
Mechanism: leave the `_jp.tga` baseline immutable; reuse the reviewed native
English `MÄR HEAVEN` gray/color marks for the three matching slots and the
localized creator/publisher credit from the sibling title-parts texture. Keep
the source canvas and import through its existing PSMT8 palette.
Verification: the 512x512 English TGA changes pixels only in the three logo
regions and credit strip. `tools/rtx3.py` import retained the source TXC's
263,232-byte size, dimensions, header, and palette; exporting it returned a
512x512 TGA. The source and re-export previews were inspected at native texture
scale. The baseline TGA SHA-256 remains
`a528447c14929d7d16fc62254d6fdca90ff6d3f336c8b3a27b53f303d646542c`.
Scope and limits: this is one atlas's local palette round-trip evidence. It
does not validate ISO reinsertion, runtime UVs, draw order, or whether the
three marks are separate display layers. No ISO build/reparse or emulator
runtime validation was run.
References: `graphics/title/00039_01565_0000_ttlprts_jp.tga`,
`graphics/title/00039_01565_0000_ttlprts_eng.tga`,
[`GRAPHIC_TEXT_TTLPRTS.md`](../tasks/GRAPHIC_TEXT_TTLPRTS.md),
`tools/rtx3.py`.

## Preserve source line positions when replacing small UI text

Symptom: generated English labels fit the words onto the texture but collapse
the wider vertical spacing used by the Japanese source.
Mechanism: inspect the decoded source texture's alpha bounds and center each
English row within its original label band before importing through the source
PSMT4 palette. Keep the transparent 128x128 canvas and `_jp.tga` baseline
unchanged.
Successful pathway: localize the three `shop_tex.b` actions as `BUY ITEM`,
`SELL ITEM`, and `ARM REPAIR`; align their text rows with the source label
centers; encode the sibling TGA through the existing RTX3 importer; stage it as
an `_eng.tga` override.
Verification: the Japanese TGA retains its indexed SHA-256. The rebuilt ISO
reparses the resulting 8,320-byte TXC exactly (SHA-256
`ca376525ca57c5612b291c5d2e64b95766dc89c408bffe4f0e416d6a2a667ea6`). All seven
English graphics overrides pass `make verify-graphics-image`; `make test`
passes 107 tests.
Scope: this 128x128 PSMT4 shop-action texture and the current UI graphics build.
Limits: “BUY ITEM” and “SELL ITEM” are contextual English action labels rather
than literal repetitions of ARM; runtime readability and UV placement remain
unvalidated. Image-generation layout and safety-filter failures are recorded in
[`FAILURES.md`](FAILURES.md).
References: `graphics/text/00039_01556_0014_subtitle_eng.tga`,
[`GRAPHIC_TEXT_LOCALIZATION.md`](../tasks/GRAPHIC_TEXT_LOCALIZATION.md),
`tools/rtx3.py`, `tools/verify_graphics_in_iso.py`.

## Preserve UI atlas layout by reusing only reviewed English lettering

Symptom: an image-generation edit of `00039_01631_0025_windisp` returned a
1774x887 composition for the 512x256 source and redrew its team labels, logo,
and arrows. Importing the whole image would have changed the original screen
layout.
Mechanism: discard the generated composition, retain only the reviewed English
lettering crops, clear Japanese text inside measured label bands on the original
mapped texture, position the new labels within those bands, and import through
the source PSMT4 palette. The source logo, arrows, existing English player labels,
canvas, palette and unrelated alpha remain from the recovered artwork.
Successful pathway: map `メルチーム`, `チェスチーム`, `リマッチ`, `終了`,
`ネクストバトル`, and `ウォーゲーム` to `MÄR TEAM`, `CHESS TEAM`, `REMATCH`,
`EXIT`, `NEXT BATTLE`, and glossary-backed `WAR GAMES`. Preserve the `_jp.tga`
baseline and write only the same-size `_eng.tga` sibling.
Verification: the complete graphics audit recognized eight English overrides,
30,354 editable images and 43 unresolved records, with zero edited Japanese
baselines. The 524,306-byte English TGA has SHA-256
`52a8a4cc7e08aaf4e97d36db1ad64a4b8b950ff372e349576e7f26fcf5e985dd`; its imported
65,664-byte TXC has SHA-256
`a727d554971d876a5fe7c0690add70042fdcd16714c95a43720f4acf6473f2d1`. The built
ISO reparses all eight English textures exactly (783,104 combined TXC bytes), and
`make test` passes 107 tests.
Scope: this winner-screen atlas and the existing same-size graphics override
pipeline.
Limits: source bounds are observed from the mapped texture, not recovered runtime
UV rectangles. There is no emulator confirmation of final screen placement,
translation readability, or gameplay behavior. The rejected full generated image
does not prove other UI atlases can be edited the same way.
References: `graphics/user_interface/00039_01631_0025_windisp_eng.tga`,
[`GRAPHIC_TEXT_LOCALIZATION.md`](../tasks/GRAPHIC_TEXT_LOCALIZATION.md),
[`FAILURES.md`](FAILURES.md), `tools/graphics.py`, `tools/rtx3.py`,
`tools/verify_graphics_in_iso.py`.

## Byte-weight recovery levels after editable YOBJ coordinate surfaces

Symptom: one "decompiled percentage" conflates file preservation, parser
structure, semantic editability and runtime acceptance, while file counts hide
large opaque resources.
Mechanism: use one de-duplicated expanded information-bearing payload `Y` and
report hierarchy addressing separately from `Z` (parser-validated spans), `A`
(unchanged-input lossless rebuild), `B` (source bytes with semantic editing
representation and insertion path), and `C` (runtime-validated edited bytes).
For partially editable resources, count only source fields exposed through the
verified editable representation; leave remaining bytes in the weighted queue.
Successful pathway: preserve a disjoint physical ISO partition; replace BPE
wrappers with parsed child payloads once; audit source hashes and exact no-op
rebuilds; then count TXC/text/message spans and only the validated XYZ float
components from YOBJ geometry. Partition `Y-B` and `Y-Z` independently because
the former includes structurally known but opaque bytes.
Verification at this pre-movie milestone: `make asset-census` reported `Z/Y=86.8157%`, `A/Y=100%`,
`B/Y=20.9454%`, and `C/Y=0%` for this pinned image. B is 273,116,350 of
1,303,947,016 bytes, including 33,583,536 editable YOBJ coordinate bytes.
The B components contribute 18.3630% of Y from textures, 0.0052% from
reversible text, 0.0016% from message catalogs, and 2.5755% from YOBJ
coordinates (rounded independently). `make test` passes all 101 tests. A fresh
unchanged build followed by `make compare-disc` matches the 4,587,749,376-byte
pinned image with zero differing bytes.
Synthetic tests verify that direct and nested YOBJ edit spans are counted
without counting the entire model, and a synthetic nested edit survives bundle,
BPE and PAC reinsertion. Census invariants check denominator balance and both
remaining-payload partitions.
Scope: this image, its expanded bundle catalog, and the current validated asset
editors. Limits: source-span coverage is not translation completion or runtime
acceptance; coordinate semantics remain unconfirmed by the game, and all-zero
byte spans do not prove intentional padding. Remainder labels are inventory
candidates rather than complete semantic classification.
References: `tools/asset_recovery_census.py`, `tools/yobj_geometry.py`,
`tests/test_asset_recovery_census.py`, `tests/test_assets.py`,
[`YOBJ evidence`](../tasks/YOBJ_MODEL_RECOVERY.md),
[`asset census report`](../reports/asset_recovery_census.json),
[asset methodology](TASK_ASSET_WORKSPACE_METHODOLOGY.md).

## Recovered editable video streams and separated them in the byte census

Symptom: all 13 movie streams were structurally parsed, but their 685,111,296
bytes were counted as noneditable because generic MPEG muxers rejected the
game's ADX audio.
Mechanism: extract the MPEG-2 and ADX elementary streams from the observed
sectorized CRI SofDec profile; use a game-specific mux adapter that retains both
CRI metadata packets, original ADX bytes and sector-safe picture headers. Export
Japanese video/audio baselines into flat `movies/` files and accept only
profile-compatible `_eng.m2v` siblings. Reinsert with the existing relocated
archive builder.
Verification: `make movies-audit` checks all 13 immutable source/export hashes
and reports 615,212,537 MPEG-2 video bytes, 59,642,694 ADX bytes and 10,256,065
container/packetization bytes. All 13 no-op remuxes recovered exact elementary
streams; full decoded frame-hash and PCM-byte comparisons matched. An expanded
movie member relocated through synthetic YFS/AFS tables while preserving its
ADX stream and both CRI metadata sectors. The normal `make build-mod-disc`
target also produced a temporary 5,705,777,152-byte mod ISO with an edited test
clip; reparsing `MOVIE.AFS` recovered the exact edited MPEG-2 stream and original
ADX. The smoke-test image was discarded. The full `make test` run passed all
106 tests; the focused census/movie subset covers 14 tests.
The refreshed census now reports `Z/Y=86.8157%`, `A/Y=100%`,
`B/Y=68.1261%` (888,328,887/1,303,947,016 bytes), and `C/Y=0%`. Its noneditable
queue is `Y-B=415,618,129` bytes (31.8739% of Y), led by audio/sound candidates
(51.9940% of Y-B) and model/geometry candidates (40.4335%). Only editable video
elementary-stream bytes enter B; ADX and mux/container bytes remain queued.
Scope: direct movies in this pinned disc image and profile-compatible video
replacement through the observed SofDec container and full ISO relocation path.
Limits: no audio editing, translation-quality review, or emulator runtime
acceptance has been verified.
References: `tools/sofdec.py`, `tools/movies.py`,
`tests/test_sofdec_movies.py`, `tools/asset_recovery_census.py`,
[`movie evidence`](tasks/VIDEO_STREAM_RECOVERY.md),
[`asset census report`](../reports/asset_recovery_census.json),
[`asset methodology`](TASK_ASSET_WORKSPACE_METHODOLOGY.md).

## Human-readable census preserves recovery levels and remainder denominators

Symptom: the machine-readable census and terminal summary contain the byte
measurements, but readers need a durable view that distinguishes physical image
space, expanded logical payload, independent recovery levels, and more than one
definition of "what remains."
Mechanism: render the Markdown report from the same in-memory census object as
the JSON file. Its physical partition does not infer zero-padding purpose, its
Z/A/B/C rows retain separate definitions, and it reports `Y-B` and `Y-Z` as
different disjoint work queues with byte-weighted categories.
Pathway: run `make asset-census`; it writes
`reports/asset_recovery_census.json` and
`reports/asset_recovery_census.md`. A custom `--output` path gets a matching
`.md` companion unless `--summary-output` is supplied.
Verification: `make asset-census` completed on 2026-09-23. It measured a
4,587,749,376-byte physical image, Y=1,303,947,016 bytes, Z/Y=86.8157%,
A/Y=100%, B/Y=68.1261%, and C/Y=0%. The complete `Y-B` remainder is
415,618,129 bytes, led by audio/sound (51.9940%) and model/geometry candidates
(40.4335%); `Y-Z` is 171,916,194 bytes, 91.0058% of which is audio/sound
candidates. The 3,327,295,881 all-zero bytes remain measurements; intentional
padding is not established. Focused formatter tests and the full test suite are
recorded with this change.
Scope: human-readable presentation of the current pinned-image census; JSON
remains the source data for tooling.
Limits: category labels use signatures, member types, extensions, or paths and
do not prove semantic understanding of those payloads. B is editable source
coverage, not translation completion; C remains zero until in-game validation.
References: `tools/asset_recovery_census.py`,
`tests/test_asset_recovery_census.py`,
[`readable report`](../reports/asset_recovery_census.md),
[`machine-readable report`](../reports/asset_recovery_census.json),
[`asset methodology`](TASK_ASSET_WORKSPACE_METHODOLOGY.md).

## Native game glyphs produce a stable English subtitle texture

Symptom: generated title-lettering edits changed the full composition, and
lettering-only outputs showed horizontal artifacts at native resolution.
Mechanism: the game already contains a 128x128 atlas with 8x16 Latin glyphs.
For the short `ARM FIGHT DREAM` subtitle in `00039_01565_0003_sbttl`, compose
those native glyph shapes inside the measured subtitle band, preserve the
512x128 source canvas and surrounding logo, then map the edited colors through
the source TXC palette.
Verification: the English TGA imports as a 66,624-byte TXC, and
`make verify-graphics-image` reparses that exact TXC from the rebuilt ISO. The
full graphics audit finds ten English overrides and zero modified Japanese
baselines. Source atlas and output hashes, band bounds, and TXC bytes are in
[`graphic localization evidence`](../tasks/GRAPHIC_TEXT_LOCALIZATION.md).
Scope: this single uppercase title subtitle and the current atlas/palette.
Limits: the atlas glyph-cell interpretation is visually observed rather than
recovered from the renderer; static layout and ISO reinsertion do not establish
runtime UV placement or screen readability. This does not establish that every
Japanese UI surface can be translated with the same glyph set.
References: `graphics/text/00039_00825_font_jp.tga`,
`graphics/title/00039_01565_0003_sbttl_eng.tga`, `tools/rtx3.py`,
`tools/graphics.py`, `tools/verify_graphics_in_iso.py`,
[`graphic localization evidence`](../tasks/GRAPHIC_TEXT_LOCALIZATION.md),
[`negative result`](FAILURES.md).
