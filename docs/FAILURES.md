# Negative knowledge

Authority: [STANDARDS.md](STANDARDS.md).

## A leaf-only editable percentage does not measure the expanded game payload

Hypothesis: editable/structured terminal-leaf bytes divided by nonzero terminal
leaf bytes give a census-wide semantic-editability percentage. That ratio is
not valid when compressed `.b` leaves contain individually indexed resources.
The prior 13.5887% figure treated whole parsed BPE wrapper leaves as editable
while excluding their decoded child members from both the numerator and
denominator. It therefore mixed rebuildable containers with semantic source
surfaces and omitted the nested editable texture payloads.

Use a normalized logical denominator: remove each compressed BPE wrapper once,
add its decoded child member extents once, and exclude bundle table/gap bytes.
Count only editable texture and text/catalog source representations in B. Keep
parser-backed structure Z, unchanged-source rebuildability A, and runtime
validation C separate. Preserve physical disc accounting as its own partition;
do not call either ratio a generic decompilation percentage. The revised tool
fails if physical spans or exclusive remainder categories do not balance.

Evidence: v4 `reports/asset_recovery_census.json` reports Y=1,303,947,016,
Z/Y=19.1598%, A/Y=100%, B/Y=18.3698%, and C/Y=0%, alongside the exact physical
partition. It reports both `Y-B` and `Y-Z` work queues and the `Z-B` bridge.
The high-bit indexed TGA recovery raised B while retaining the same Y
denominator. The AT3 node-envelope parser raises Z while leaving B unchanged
because its property fields remain opaque. The revision supersedes the former
13.5887% leaf-only headline.
See `tools/asset_recovery_census.py`,
`tests/test_asset_recovery_census.py`, and
[`TASK_ASSET_WORKSPACE_METHODOLOGY.md`](TASK_ASSET_WORKSPACE_METHODOLOGY.md).

## An indexed RTX3 entry is not proof that its full extent parsed

Hypothesis: every row in the graphics index is structurally validated, so its
entire source span belongs in Z. The index intentionally retains unresolved TXC
records for inventory; 43 PSMCT32 records expose parseable-looking headers but
fail the strict parser's complete file-length contract by eight bytes each.
Counting all TXC index spans therefore overstated parser-backed coverage by
140,648 bytes while leaving B/Y unchanged.

The exporter now records `rtx3_parse_valid` independently from image-export
support. The census requires that evidence and counts a TXC in Z only when the
strict parser accepted its complete header, dimensions, declared pixel extent,
palette extent, and actual file length. Preserve malformed/unsupported records
in the unresolved graphics inventory and the opaque queue. This does not prove
the 43 records are corrupt or unimportant; only their complete RTX3 structure is
not established by the current parser.

Verification: the regenerated v4 graphics index records 43 parse failures with
`RTX3 length does not match header, palette and pixel extents`; v3 census Z is
248,061,654 bytes. Tests reject missing parse-status evidence, exclude invalid
TXC spans from Z, and check that opaque and non-editable category totals balance.
See `tools/graphics.py`, `tools/asset_recovery_census.py`,
`tests/test_asset_recovery_census.py`, and
[`reports/asset_recovery_census.json`](../reports/asset_recovery_census.json).

## One nested `.pac` file does not meet the observed PAC table contract

Hypothesis: every file named `.pac` in the recognized asset tree uses the same
little-endian PAC member table and can be recursively unpacked. The prepared
census found `disc!/_DATA.YFS;1!/data/bg/00.pac!/tex.pac` with a PAC-like header,
but its table contains a nonzero member field rejected by the current observed
format contract (`PAC unknown member flags`). Keep this file as an opaque leaf;
do not clear or reinterpret the field to force extraction.
Revisit when an independent parser/runtime trace or multiple structurally
consistent examples establish that field's meaning. This does not prove the file
is not a PAC container or that the field is necessarily a flag. Evidence:
`reports/assets_census.json`, generated from the pinned image;
[asset methodology](TASK_ASSET_WORKSPACE_METHODOLOGY.md).

## Three `.yma.b` menu payloads do not use the common UI resource table

Hypothesis: every BPE-decoded menu `.b` starts with a `u32le` entry count,
`01 01 00 00` marker, and `16 + count * 32` table. `top_yma.b`,
`war_common_yma.b`, and `war_stage_yma.b` contradict this: their decoded payloads
are 4,576, 64, and 256 bytes, and the candidate table marker is absent or shifted.
The generic parser rejects these rather than interpreting their bytes as member
records. Keep their decoded payloads available as raw sidecars until another
independent layout is established. This does not show that they are not YMA files,
that their content is uneditable, or that other `.yma` resources share one format.
Evidence: `reports/ui_bundle_survey.json`; the other 721 menu bundles pass the
common table parser and exact no-op rebuild audit.

## A decoded texture preview is not necessarily a complete UI image

Hypothesis: a rendered RTX3 image should appear as one complete screen graphic,
so repeated or incomplete content indicates failed decoding. Actual menu TXCs
include transparent texture surfaces and large PSMT8 images with repeated-looking
regions; the paired `AT  ` members contain animation/authoring references, and
the texture may be addressed through atlas regions or repeat-wrapped UVs. Preview
appearance alone therefore does not distinguish bad swizzling from intended
texture layout or missing composition metadata. Keep verified indexed pixel
import/export separate from claims about final UI appearance. Decode the
associated AT/UV metadata and compare rendered output before changing the
swizzler. Follow-up work added PSMT8H/PSMT4HL/PSMT4HH candidate exports after
coherent previews of three representative samples; this evidence supports
editable raster candidates but does not resolve hardware sampling, composition,
or runtime behavior. The 43 PSMCT32 payloads remain raw because their pixel
extents are short by eight bytes. Evidence: RTX3 census and sample previews in
`reports/rtx3_format_survey.json`; final in-game rendering has not been tested.

Follow-up hypothesis: the title-logo view was only meaningful with pixels and
palette both left in stored order, and the legacy decoder should remain the
standard image path. Controlled four-way comparisons across ten PSMT8 and ten
PSMT4 resources showed the legacy pixel-unswizzle produced tiled/striped results;
linear pixel indices were the coherent candidate. For PSMT8, the owner selected
the linear-pixel plus mapped-CLUT title preview, which shows gray and colorful
Japanese logo variants matching the supplied reference. The title TXC member
span still hashes exactly to its bundle manifest, ruling out outer extraction
corruption for this sample. The early output also copied GS alpha values (0..128)
into TGA unchanged; that made the logo's opaque pixels half-transparent. The
current indexed decoder expands alpha by two while retaining transparency and
antialiased edges. Evidence: `reports/rtx3_layout_diagnostics.json`,
`tasks/TITLE_TEXTURE_RENDERING.md`, and `tests/test_rtx3.py`.

Limits: this selection is a human visual reference and a 20-resource PSMT4/PSMT8
sample, not proof of the complete RTX3 corpus or in-game rendering. The graphics
workspace exports 30,354 supported TXCs; three additional high-bit previews are
coherent but do not establish the same controlled layout comparison. The 43
short PSMCT32 TXCs remain unresolved; AT/UV composition remains unknown. Keep the
old pixel-unswizzle path as a diagnostic until a runtime capture validates
sampling and alpha behavior.

## AT texture-reference rows are not a flat array of 64-byte names

Hypothesis: the AT header's `0x40` field is the complete stride, so the declared
count can be parsed as consecutive 64-byte strings. On `title_00.at3`, that
interpretation returned `@` and empty names after the first reference. The raw
bytes instead show each 64-byte CP932 name slot followed by a four-byte field;
the next name begins 68 bytes after the prior one. This yields names at offsets
`0x10`, `0x54`, `0x98`, and `0xdc`, with trailing values `64`, `64`, `64`, and
`0`. The field's semantics remain unknown and are preserved without
interpretation. Do not reuse a 64-byte flat-stride parser. `tools/at3.py` checks
the file extent and NUL-terminated names; tests cover malformed headers and
truncated tables. Evidence and the four matching TXC resource names are in
`tasks/TITLE_TEXTURE_RENDERING.md`.

## A 16-byte copy does not establish a four-float aggregate

Hypothesis: `CCamera::GetViewRect` returns a four-float rectangle by value.
The name and 16-byte transfer made this plausible. EE GCC `2.96-ee-001003-1`
with the existing `-O2` produces the same hidden-destination register roles,
but 40 bytes of unaligned load/store pairs versus 24 original bytes using
aligned `ld`/`sd`. Aggregate alignment is a mechanism hypothesis, not a recovered
declaration. Do not force alignment or choose wider fields to obtain a match.
Revisit after callers/member writes establish type or alignment, or independent
compiler evidence changes. This does not disprove aggregate return or the
compiler family. Original bytes remain preserved; the reproducible candidate
is excluded from reconstruction. See [exact evidence](tasks/VIEW_RECT_PROBE.md).

## Host GNU objdump is not a target disassembler

Hypothesis: the installed `objdump` could inspect the MIPS code because `readelf`
could read its ELF headers. `objdump -i` instead lists only x86/iamcu architectures.
ELF metadata inspection and instruction decoding have different target requirements.
Use the installed `llvm-objdump-21` for the evidenced accessor instructions.
This does not establish complete R5900 decoding support in LLVM, nor prevent use
of a separately installed R5900-aware GNU toolchain later.

At initial bootstrap no historical compiler experiment had been run. The follow-up
EE GCC probe now matches eight accessor sections; exact original compiler identity
remains unresolved. This is not evidence that natural source cannot match.

## Historical i386 tools fail on the Windows-mounted workspace

Hypothesis: installing the archive in `.tools/` and calling its driver directly
would suffice. Observed failures: `cannot exec cc1plus`; absolute paths and `-B`
backend search paths did not resolve it. Moving only the tools to `/tmp` exposed
`Value too large for defined data type` when the compiler read workspace source.
The workspace files have very large inode values; the temporary copies do not.
Strong mechanism hypothesis: legacy 32-bit file-metadata limits. No syscall trace
was obtained, so do not claim the exact failing syscall was established.
Successful recovery: stage both tools and source on native temporary storage.
The target flags and source text are unchanged; all eight methods and full ELF match.
Scope: this WSL Windows mount and the pinned i386 EE GCC distribution.
Reconsider direct invocation on a native filesystem or a compatible rebuilt host tool.
This failure says nothing about whether the target C++ can match.
Reference: [compiler task](tasks/COMPILER_PROBE.md), `tools/run_ee_probe.py`.

## Unreferenced inline functions do not provide a comparison artifact

Hypothesis: `-fkeep-inline-functions` would emit all unreferenced inline members.
Observed: this EE GCC experiment produced no selected member sections, so the
comparison failed for a missing name. Do not interpret a missing artifact as
an instruction mismatch or a rejection of the compiler hypothesis.
Taking addresses in the separate harness produced definitions using only `-O2`.
Limits: one class/probe on this compiler; no general claim about other GCC releases.
Reference: [compiler task](tasks/COMPILER_PROBE.md).

## The full-disc verification target preserves an existing output

`make verify-disc` stops before rebuilding if `build/assets-rebuilt.iso` already
exists. The builder requires a new output path to avoid silently replacing a
prior artifact. In this checkpoint the standard target exited with that
fail-closed error; the existing ISO remained untouched. Rebuilding to a new
temporary path and running `tools/compare_disc.py` against the pinned reference
passed with zero differing bytes. Preserve or inspect stale build outputs before
choosing another path.

This applies to the unchanged `build-disc`/`verify-disc` output path. The separate
`make build-mod-disc` target now opts into `--replace-existing`, which builds to
a temp file and atomically installs only after success.

## The isolated source-only target omitted an included Makefile fragment

Hypothesis: copying the top-level `Makefile` and boot inputs is sufficient for
`verify-source-only`. After the Makefile began including `graphics_rules.mk`,
the temporary tree failed before compilation with `No rule to make target
'graphics_rules.mk'`. This was an isolation-harness input omission, not a source
or compiler mismatch.

The harness now copies the included fragment along with the Makefile. Verification:
`make verify-source-only` passes and the isolated boot output retains the pinned
SHA-256. When a source-only target includes additional Make fragments, add each
required fragment to the declared minimal input set; do not copy the whole
repository, which would weaken the isolation check.

## Forty-three PSMCT32 TXCs are eight bytes short of their declared pixel extent

Hypothesis: every catalogued PSMCT32 RTX3 payload has the standard 0x40-byte
header followed by the declared `width * height * 4` pixel bytes. The 43 PSM=0
records parse far enough to identify dimensions and pixel size, but every body
ends eight bytes before `0x40 + pixel_size`, while the RTX3 size field still
correctly equals `file_size - 8`. The set has 28 8x8 files, 14 32x64 files, and
one 64x64 file. No TGA is emitted for them.

Keep all 43 records raw. Do not trim the declared size, pad pixels, or shift the
pixel-data start based on this repeated discrepancy alone; each would invent
pixel values or a header variant without evidence. Revisit after a second
independent parser, format sample, or runtime/tool trace establishes the PSMCT32
variant. This does not imply the payloads are corrupt; it establishes only that
they fail the current bounded RTX3 contract. Evidence: `graphics/index.json`,
`reports/rtx3_format_survey.json`, and the full source-hash/TGA-dimension audit.
