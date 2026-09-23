# Negative knowledge

Authority: [STANDARDS.md](STANDARDS.md).

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
texture layout or missing composition metadata. Keep the verified PSMT4/PSMT8
pixel import/export separate from claims about final UI appearance. Decode the
associated AT/UV metadata and compare rendered output before changing the
swizzler. PSMT8H/PSMT4HL/PSMT4HH stay parse-only pending their own storage-order
evidence. Evidence: RTX3 census and sample previews in
`reports/rtx3_format_survey.json`; final in-game rendering has not been tested.

Follow-up hypothesis: the repeated title-logo preview came from a bad outer
BPE decode or corrupted bundle member. The exact `title_marh_jp` span in the
decoded bundle matches its manifest SHA-256, and a new stored-order preview
shows coherent Japanese logo shapes in two stacked variants. This rules out
corruption in the recorded outer decode/member extraction for this texture,
but does not prove its game-side pixel layout. Applying a generic GS page/block
address map directly to RTX3 bytes made the title image more striped and
garbled. That map is not established for this file format and was discarded;
the legacy image swizzler remains unchanged. Reconsider the GS map only if TXC
serialization evidence or runtime comparison demonstrates that the file stores
raw GS VRAM order. See `tasks/TITLE_TEXTURE_RENDERING.md`.

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
