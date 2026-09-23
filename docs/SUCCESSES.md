# Verified mechanisms

Authority: [STANDARDS.md](STANDARDS.md).

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
