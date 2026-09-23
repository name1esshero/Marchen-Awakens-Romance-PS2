# Negative knowledge

Authority: [STANDARDS.md](STANDARDS.md).

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
