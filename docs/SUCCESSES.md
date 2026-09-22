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
Verification: EE GCC `2.96-ee-001003-1` with the same `-O2` for eight CCamera
accessors reproduces all 64 bytes; the full probe ELF also compares identically.
Limits: trivial methods do not identify the original compiler or complete class.
Reference: [compiler experiment](tasks/COMPILER_PROBE.md), `make verify-ee`.

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
