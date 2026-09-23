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
