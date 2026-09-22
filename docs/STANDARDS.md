# Decompilation Standards & Best Practices Guide

## Core Philosophy: The Golden Rule

There is one absolute, unbreakable rule that supersedes all others:

> **The reconstructed program must match the authenticated original
> binary byte-for-byte under the project's authoritative comparison
> gate.**

Human readability and natural source recovery are the second priority. A
byte match is necessary, but it is not sufficient evidence that
recovered source is authentic.

If a function cannot be reproduced from natural source without compiler
steering, implementation tricks, or unsupported assumptions, preserve
the verified lower-level implementation and document the blocker. Do not
manufacture a source-level match.

**Strictly forbidden as matching shortcuts:**

-   forced register assignments or register pinning;
-   naked functions used to manufacture code shape;
-   compiler-option changes made only to force a match;
-   fake matches that rely on deliberately misleading source or
    accidental compiler behavior;
-   hand-written instruction bytes presented as recovered high-level
    source;
-   weakening, bypassing, or changing verification gates to accept a
    mismatch;
-   silently copying bytes from the reference binary into generated
    output.

Platform-, compiler-, ABI-, and toolchain-specific behavior must be
discovered from evidence and documented in project methodology or
institutional memory. It must not be assumed from another system.

------------------------------------------------------------------------

## 1. Naming Conventions

Naming is part of the recovered understanding. Do not assign semantic
names until evidence supports them.

-   **Global variables:** prefix with `g` and use camelCase where
    compatible with the project.
-   **Static/file-local variables:** prefix with `s` and use camelCase.
-   **Functions:** use PascalCase/UpperCamelCase and prefer verb-noun
    names when semantics are known.
-   **Macros and enums:** use `ALL_CAPS_WITH_UNDERSCORES`.
-   **Structs and unions:** use PascalCase and meaningful subsystem
    names once known.
-   **Constants:** use named constants rather than unexplained magic
    numbers.
-   **Unknown symbols:** use stable address-, offset-, or tool-derived
    placeholder names until semantics are established.
-   **Tables:** replace raw addresses with symbols only after the target
    and interpretation are evidenced.

A placeholder is preferable to a confident but unsupported name.

------------------------------------------------------------------------

## 2. Types and Variables

### Exact-width types

Use exact-width integer types for recovered binary interfaces and data
layouts. Prefer the project's established aliases when available (`u8`,
`u16`, `u32`, `u64`, `s8`, `s16`, `s32`, `s64`) or the equivalent
standard fixed-width types.

Do not assume pointer width, register width, endianness, alignment, or
ABI rules. Establish them from the target system and toolchain.

### Pointers

Use the project's established pointer formatting consistently.

Pointer arithmetic should model the recovered operation:

-   use a pointer to the real element type when evidence establishes an
    array or structure;
-   use a byte pointer when the operation is genuinely byte-oriented or
    the layout remains unknown;
-   prefer named structure members once offsets and meanings are proven.

### Pointer/integer authenticity

Do not cast pointers through integers, unions, or other representations
merely to influence register allocation, instruction scheduling, alias
analysis, or compiler output.

Pointer/integer conversion is acceptable when the recovered program
genuinely performs an address-as-data operation, including verified
examples such as:

-   masking or alignment;
-   tagging or mode bits;
-   serialization;
-   ABI-defined integer address fields;
-   signed/unsigned address comparisons;
-   platform-specific encoded pointers.

Document the evidence beside unusual conversions.

A clean audit for one steering pattern proves only that pattern has been
reviewed. Declaration order, extra locals, type width, expression
grouping, aliasing, control-flow spelling, and other source choices can
also influence code generation. Never describe a narrow audit as proof
that all compiler steering is absent.

### Volatile

Use `volatile` only when required by recovered semantics, such as
memory-mapped I/O, shared hardware state, interrupt-visible state, or
another demonstrated external mutation source.

### Const correctness

Use `const` for data proven not to be modified.

------------------------------------------------------------------------

## 3. Functions and Headers

-   Put externally visible declarations in appropriate headers.
-   Keep file-local functions `static` when evidence and project
    structure support it.
-   Use recovered calling conventions and types; do not choose argument
    or return types merely because they make codegen match.
-   Include what a translation unit uses and avoid unnecessary
    dependency cycles.
-   Use include guards or `#pragma once` consistently with project
    conventions.
-   Do not assume the original source language was C where evidence does
    not establish that. The project's recovered-source strategy may
    evolve as the original toolchain is identified.

Function boundaries, calling conventions, and prototypes are claims
about the original program and require evidence.

------------------------------------------------------------------------

## 4. Constants, Addresses, and Magic Numbers

Unexplained numbers should not remain embedded in recovered logic once
their meanings are understood.

-   Use named masks and flags.
-   Use named sentinel values.
-   Use array-size helpers rather than duplicated counts where
    appropriate.
-   Prefer hexadecimal for addresses, bit patterns, encoded fields, and
    hardware values.
-   Prefer decimal for ordinary counts and arithmetic where it improves
    readability.
-   Replace software-object addresses with symbols as those objects are
    recovered.
-   Keep true platform physical addresses represented through named
    constants or typed platform interfaces.

A named macro that merely hides an unexplained software address is
transitional, not full recovery.

------------------------------------------------------------------------

## 5. Data Tables and Structures

Raw binary representation is acceptable during bootstrap and while
classification is genuinely unknown. It is **technical debt**, not final
recovered source.

As evidence accumulates:

-   replace function addresses with verified symbols;
-   replace string addresses with verified string symbols;
-   recover arrays, structures, enums, flags, and tables;
-   use designated initializers where they improve correctness and
    readability;
-   mark file-local lookup data `static const` where appropriate;
-   preserve ordering, packing, alignment, and relocation behavior
    required by the original binary.

### Encoded and indirect pointers

Do not assume a pointer encoding from value shape alone.

Architectures and ABIs may use:

-   instruction-set/mode bits;
-   tagged pointers;
-   relative pointers;
-   segmented addresses;
-   relocation records;
-   overlays;
-   pointer-to-pointer tables;
-   packed flags;
-   runtime rebasing.

Before interpreting an encoded value, require corroborating evidence
such as a known target region, matching symbol, caller behavior,
relocation semantics, loader behavior, or runtime use.

Double indirection and runtime relocation should be considered before
declaring a table entry unidentified.

### Shiftability

The long-term recovered source should prefer symbolic software
references over fixed original addresses.

Matching link scripts may intentionally preserve original placement.
That is separate from whether source code contains hardcoded
software-object addresses.

Physical platform addresses are not shiftability violations when they
genuinely represent hardware or fixed ABI regions and are expressed
through named, correctly typed interfaces.

------------------------------------------------------------------------

## 6. Compiler, ABI, and Toolchain Near-Misses

Compiler-specific behavior can make semantically equivalent source
produce different bytes. Treat these as research problems, not
invitations to force the compiler.

Potential causes include:

-   register allocation;
-   instruction scheduling;
-   calling convention details;
-   stack-frame/prologue choices;
-   literal/constant pool placement;
-   alignment and padding;
-   delay-slot behavior;
-   instruction selection;
-   signedness and width;
-   alias analysis;
-   structure layout;
-   linker relaxation;
-   relocation form;
-   assembler syntax aliases;
-   optimization passes;
-   language dialect and compiler version.

When a near-match occurs:

1.  establish the exact mismatch;
2.  determine whether natural source variation can explain it;
3.  test hypotheses with the smallest useful compile/assemble
    experiment;
4.  document successful and failed mechanisms;
5.  never change compiler flags solely to force one function to match;
6.  preserve the lower-level implementation if natural source cannot
    currently reproduce the original.

### The fakematch trap

A fakematch is source that byte-matches by exploiting fragile or
misleading compiler behavior rather than authentically expressing the
recovered program.

A passing binary comparison does not excuse a fakematch. Rewrite it
naturally or restore the verified lower-level implementation.

### Toolchain discovery

Do not import compiler folklore from another architecture or project as
fact.

Record target-specific discoveries in `SUCCESSES.md`, `FAILURES.md`, and
the relevant `TASK_XXX_METHODOLOGY.md`, including:

-   compiler/linker/assembler versions;
-   flags;
-   ABI;
-   architecture and instruction set;
-   observed mechanism;
-   minimal reproducer where practical;
-   verification;
-   known counterexamples and limits.

------------------------------------------------------------------------

## 7. Formatting and Style

Unless the recovered project establishes a stronger historical
convention:

-   use 4-space indentation;
-   use consistent brace style;
-   keep lines reasonably readable;
-   use consistent spacing;
-   follow the project's pointer-declaration convention;
-   prefer readable source over unnecessarily clever expressions.

Formatting may be adapted if the original source style becomes known,
but style changes must never be used as a disguised matching shortcut.

------------------------------------------------------------------------

## 8. Comments and Documentation

Comments should explain **why**, evidence, recovered meaning, or
unresolved uncertainty---not narrate obvious syntax.

Document:

-   unusual ABI behavior;
-   hardware interactions;
-   encoded pointers;
-   hardcoded physical addresses;
-   uncertain structure fields;
-   compiler/toolchain quirks;
-   intentional low-level constructs;
-   unresolved semantic questions.

Use Doxygen-style comments for public functions and structures when
appropriate to the project.

Do not present guesses as recovered facts. Label uncertainty explicitly.

------------------------------------------------------------------------

## 9. Matching, Non-Matching, and Lower-Level Workflow

The repository should maintain a clear distinction between:

### Matching recovered source

High-level source that passes the authoritative byte comparison and
meets authenticity standards belongs in the normal recovered-source
tree.

### Non-matching candidates

Plausible high-level source that expresses recovered semantics but does
not reproduce the original bytes belongs in the project's designated
non-matching/candidate area.

Record the exact mismatch and why the candidate remains useful.

### Lower-level preserved implementation

Code that has not yet been naturally recovered remains in assembly or
another verified low-level representation.

Do not delete the known-good implementation until its replacement passes
all required gates.

### Documentation requirement

Whenever work is deferred or moved to non-matching status, record:

-   what was attempted;
-   the exact mismatch/blocker;
-   hypotheses tested;
-   relevant toolchain behavior;
-   evidence;
-   and the preserved known-good state.

Correct deferral is successful work.

------------------------------------------------------------------------

## 10. Fast Iteration Without Weakening Final Verification

The full authoritative build and binary comparison remain mandatory
before integration, but they may be too slow for every micro-iteration.

Use the smallest faithful experiment that preserves the relevant
toolchain behavior.

For function-level matching, this commonly means:

1.  compile the candidate independently using the **same compiler,
    preprocessing environment, flags, ABI, and assembler** as the real
    project;
2.  disassemble or inspect the resulting object;
3.  compare it instruction-by-instruction against bytes from the
    authenticated original binary;
4.  iterate only natural source shapes;
5.  integrate the candidate only after the local experiment matches;
6.  run the complete project build, binary comparison, tests, audits,
    and other required gates.

Do not assume a single-object workflow is valid until the project's
methodology confirms that it preserves the relevant behavior. Link-time
optimization, whole-program optimization, linker relaxation, overlays,
section placement, or other system-specific behavior may require a
different fast loop.

Local iteration accelerates investigation. It never replaces final
verification.

------------------------------------------------------------------------

## 11. Bootstrap and Binary Reconstruction

A new decompilation may begin before code, data, assets, compiler, or
function boundaries are fully known.

During bootstrap:

-   authenticate the reference binary;
-   identify container/executable formats from evidence;
-   identify architecture, endianness, ABI, load addresses, sections,
    overlays, and executable regions from evidence;
-   establish a source-only reconstruction path;
-   preserve unknown bytes explicitly rather than guessing their
    meaning;
-   build an independent comparison tool;
-   inventory classified and unclassified regions;
-   create regression fixtures for newly recognized binary/control-flow
    patterns;
-   distinguish byte reconstruction from semantic recovery.

> **A byte-identical reconstruction is a baseline, not proof of complete
> decompilation.**

The normal build should not secretly copy from the reference binary.
Reference input may be used for explicit regeneration, research, and
comparison, but a reconstructed build must consume project source
artifacts.

When the target uses containers, filesystems, multiple executables,
overlays, modules, compressed segments, or runtime-loaded code, define
the authoritative comparison boundary for each artifact and for the
final reconstructed image.

------------------------------------------------------------------------

## 12. Assets and Non-Code Data

Assets and data are part of the decompilation.

Do not assume unexplained bytes are executable code or ordinary data.

Classify regions using evidence and recover editable source forms where
practical:

-   graphics;
-   audio;
-   text;
-   scripts;
-   maps;
-   models;
-   animation;
-   archives;
-   compressed resources;
-   filesystem/container metadata;
-   tables;
-   padding/alignment.

Before replacing raw binary regions with extracted assets, define an
extraction/rebuild contract and add round-trip verification.

Generated binary blobs are transitional unless the project's final
standards explicitly accept them.

------------------------------------------------------------------------

## 13. Verification and Evidence

Every integrated change must satisfy the gates relevant to its scope.

Typical gates include:

-   authoritative byte comparison;
-   source-only/independent rebuild;
-   unit/regression tests;
-   extraction/repacking round trips;
-   provenance checks;
-   compiler-steering audits;
-   shiftability audits;
-   syntax/toolchain checks;
-   host-side behavioral tests where meaningful.

Do not claim a gate passed unless it was actually run.

Do not weaken expected hashes, baselines, tolerances, tests, or audit
rules to make work pass.

A clean narrow audit does not prove broader correctness.

------------------------------------------------------------------------

## 14. Institutional Learning Requirements

Apply `AGENT_ENVIRONMENT.md`.

Every meaningful task must evaluate whether its findings should update:

-   `SUCCESSES.md`;
-   `FAILURES.md`;
-   a `TASK_XXX_METHODOLOGY.md`;
-   tests;
-   audits;
-   tools;
-   project status;
-   or the work queue.

### Success documentation

Record generalized mechanisms, discriminating conditions, verification,
scope, limits, and references---not merely "task X succeeded."

### Failure documentation

Record plausible hypotheses, observed failure, mechanism, evidence,
reconsideration conditions, and what the failure does not prove.

### Methodology

Methodology is a living algorithm. When the actual verified procedure
improves, update the methodology so later workers inherit the better
process.

### Tool creation

When the same deterministic analysis is performed manually three times,
evaluate whether it should become a tested tool.

### Test creation

Every discovered invariant must be evaluated for mechanical enforcement.

------------------------------------------------------------------------

## 15. Platform-Specific Knowledge Belongs in Project Memory

This standards file is deliberately system-agnostic.

Do **not** add platform-specific compiler quirks, instruction encodings,
hardware addresses, pointer-tagging rules, linker tricks, filesystem
details, or tool commands here unless they express a genuinely universal
rule.

Put target-specific discoveries in:

-   `SUCCESSES.md`;
-   `FAILURES.md`;
-   the relevant methodology document;
-   target/platform documentation;
-   tested tools.

Examples of knowledge that belongs outside this file include ARM/Thumb
mode-bit behavior, MIPS-specific ABI behavior, console memory maps, a
particular compiler's register allocator, specific linker flags,
executable-container layouts, and game-specific addresses.

The constitution governs **how such knowledge is established and used**,
not what the target must look like.

------------------------------------------------------------------------

## 16. AI Worker Directive

When an AI worker enters the repository:

> Read `STANDARDS.md` and `AGENT_ENVIRONMENT.md` first. Inspect the
> current project state, status, work queue, relevant methodology,
> successes, failures, and verification tooling before editing. Treat
> the authenticated original binary as the authority for matching.
> Recover natural, readable source without compiler steering or fake
> matches. Preserve uncertainty rather than inventing semantics. Use the
> smallest faithful experiment during iteration and run all required
> final gates before integration. Document reusable successes and
> failures, update methodology when the verified process improves,
> evaluate repeated reasoning for tooling, evaluate invariants for
> tests, and leave a reviewable handoff. Never weaken standards or
> verification to make work pass.

------------------------------------------------------------------------

## 17. Definition of Done

The project is complete only when the repository's documented final
completion gates are satisfied.

At minimum, those gates should account for:

-   reproducible source builds;
-   authoritative binary equality;
-   recovered code under authenticity standards;
-   recovered assets/data to the required editable-source standard;
-   provenance;
-   unresolved regions;
-   tests and audits;
-   project-specific shiftability or relocatability goals;
-   documentation and methodology;
-   and explicitly accepted exceptions, if any.

Do not invent a completion percentage from total binary size when
executable-code extent, asset extent, or classification remains unknown.

**"Builds identically" and "fully decompiled" are different claims.**
