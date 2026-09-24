# Negative knowledge — code/compiler frontier

Authority: [STANDARDS.md](STANDARDS.md). Scope: this file is the dedicated
negative-knowledge log for the "Claude / code" queue lead (boot ELF
reconstruction, linkonce accessor recovery, EE GCC compiler identification),
kept separate from the shared [`FAILURES.md`](FAILURES.md) so concurrent
asset/localization work never needs to touch the same file. Earlier
code-frontier failures recorded before this file existed remain in
`FAILURES.md` and are not duplicated here; new ones go here going forward.

Entry format matches `FAILURES.md`: hypothesis/pathway, why it was
plausible, observed result, mechanism of failure, supporting evidence,
reconsideration conditions, and what the evidence does not justify.

## Hand-written struct field lists silently drift from evidenced offsets

Hypothesis: for a small class (2-3 fields), writing the `unsigned char
unknownXXX[N]` gap-filler struct by hand is faster than invoking the
offset-sorting generator script, and just as reliable once the offsets are
copied from the disassembly.
Observed result: happened twice in the linkonce cluster recovery
(`CCol` in the ActionObject/CCol/CMotionC/ArmEffectBase batch;
`CMotionPMS` in the CFade/CBgCtrl/CGameCntrlGm/CMotionPMS/CPDataGef batch).
Both times an extra or misplaced `unsigned char unknownXXX[N]` gap was
inserted between two real fields, silently shifting every field after it to
the wrong offset -- which would have produced wrong `lw`/`sw`/`addiu`
offsets in the compiled candidate.
Mechanism: manually re-deriving "gap size = next offset − previous end" by
eye is exactly the kind of small arithmetic that is easy to get right most
of the time and silently wrong occasionally, especially once there are more
than two fields. Nothing catches the mistake until either a spot check
against the generator or an actual failing `compare_sections.py`/`make
verify-ee` run.
Both caught this session before reaching the EE GCC compile step, by
re-deriving the same struct with the small Python offset-sorting generator
used throughout this task (sort `(offset, name, kind)` tuples, emit a gap
whenever `offset > cursor`) and diffing it against the hand-written version.
Reconsider hand-writing only for genuinely single-field classes, where there
is no ordering to get wrong.
References: [linkonce cluster task](tasks/LINKONCE_CLUSTER.md).

## Matching size does not mean the register allocator is reproducible, and this repo's disassembler cannot even name R5900 quadword ops

Hypothesis: once an aggregate-returning accessor's candidate compiles to the
exact target byte *count* under the pinned, unmodified EE GCC 2.96 `-O2`
probe, the remaining register-allocation difference is a shallow, fixable
mismatch (e.g. a different but equally valid instruction ordering the
compiler could be nudged into via a legitimate source-level rephrasing).
Observed result: for `CCamera::GetViewMatrix`/`GetProjectionMatrix`
(`objMatrix`, 64 bytes, `aligned(8)`), the reference consistently reuses
`$2`/`$3` (`move $2,$4` once, then `ld $3,off($5)` / `sd $3,off($2)`
repeated), while the pinned compiler's candidate — same source shape, same
flags, same field offsets — alternates `$6`/`$3` for loads and stores
directly through `$4`. Multiple source-level rephrasings were not attempted
further once the pattern was understood to be scheduler/allocator behavior,
not a source-shape difference (see mechanism).
For the paired setters (`SetViewMatrix`/`SetProjectionMatrix`), the gap is
categorically worse: the reference uses instructions in the `0x7b`/`0x7c`
major-opcode space (R5900-specific 128-bit quadword `LQ`/`SQ`, outside MIPS
III) that `llvm-objdump-21`'s generic `mips` target renders as `<unknown>`
or misdecodes as an unrelated MIPS32R2 `ext`. The candidate never emits
these — it stays in plain 64-bit GPRs the whole time — so there is no
"different register choice" to reconcile; the two codegen strategies are not
comparable instruction-for-instruction at all.
Mechanism: GCC 2.96's instruction scheduler/register allocator is not
guaranteed deterministic relative to whatever historical build produced the
original binary (different scheduler heuristics, possibly a different
exact sub-version or build environment); this is a known, already-recorded
limit (see the `$gp`-relative entry in `CODE_SUCCESSES.md`) now confirmed to
also apply to same-size aggregate copies, not just field accessors. The
`LQ`/`SQ` gap is separate and more fundamental: it is a real ISA extension
this repository's tooling (both the disassembler used for evidence-gathering
and the `clang`-based assembler used for the source-only ASM path) does not
support at all, so no source-level change can produce it.
Supporting evidence: `docs/tasks/CAMERA_MATRIX_PROBE.md` (exact disassembly
excerpts for both the getter register mismatch and the setter `<unknown>`
opcodes, with reproduction commands).
Reconsideration conditions: the register-allocation gap could be
reconsidered if a different, still-unmodified EE GCC 2.96 sub-build/patch
level is ever identified as the actual original toolchain (a compiler
identity question, not a source or flag change). The `LQ`/`SQ` gap requires
an R5900-aware disassembler and assembler before setters in this shape are
even attemptable.
What this does not justify: this does not mean `objMatrix`'s recovered size
and 8-byte alignment (see `CODE_SUCCESSES.md`) are wrong, or that EE GCC
2.96 is the wrong compiler family in general — only that this specific
pair of accessor shapes cannot be reproduced byte-exactly with current
tooling and without a forbidden register-pinning or flag change.
References: [camera matrix probe](tasks/CAMERA_MATRIX_PROBE.md).

## Identical-shape original-binary sections still vary in register allocation — this is not just a probe-isolation artifact

Hypothesis: the register-allocation/instruction-count mismatches already
seen when comparing an isolated probe against the original binary (the
`GetViewMatrix` case above, and the `$gp`-relative-static case in
`CODE_SUCCESSES.md`) are specifically caused by the probe's *isolation* —
a real, full translation unit's original source would not show this kind of
variance between two functions of the identical C++ shape.
Observed result: disassembling every `__tf*` RTTI section (498 total, see
`docs/tasks/TYPEINFO_SECTIONS.md`) found the same root construct-on-first-use
shape compiled to five different byte counts (52/64/80/84/88/92) purely from
how many separate `lui` instructions the address computations needed —
itself just a coincidence of which absolute addresses happen to share upper
16 bits. Concretely, `__tf9type_info` (64 bytes) and `__tf6CBgCol` (52
bytes) are the *exact same* shape (guard check, one conditional call to the
shared one-argument helper) but `__tf9type_info` spills an extra
callee-saved register (`$16`) that `__tf6CBgCol` never touches — and both
sections are part of the same original, fully-linked binary, not one probe
vs. one original.
Mechanism: GCC 2.96's register allocator/scheduler decisions are sensitive
to per-translation-unit context (what else is live, what else competes for
registers, what other constants are nearby) even for structurally identical
generated code, independent of whether that code came from an isolated
probe or the original multi-thousand-file build. This means "recompile just
this one class in isolation and expect an exact byte match" is not a
reliably achievable goal for aggregate-shaped or multi-register-address
code in general, not only for the specific `GetViewMatrix`/`$gp`-static
cases already logged.
Supporting evidence: `reports/typeinfo_hierarchy.json` (`size_histogram`);
disassembly excerpts for `__tf6CBgCol`, `__tf9type_info`, `__tf8bad_cast`,
`__tf7CCamera`, `__tf8CCamera2` in `docs/tasks/TYPEINFO_SECTIONS.md`.
Reconsideration conditions: none identified; treat exact-byte reproduction
of any multi-address-computation function recovered via an isolated probe
as inherently best-effort (size/shape/field-offset match, not guaranteed
byte match) unless a smaller, single-address-computation shape (most of the
441 already-recovered accessors) applies instead.
What this does not justify: this does not mean the recovered class/field
evidence from these sections is wrong — the *shape*, *base-class calls*,
and *argument roles* are still fully evidenced; only the exact register
choice within a shape is shown to be non-deterministic across otherwise
identical code in the same binary.
References: [typeinfo sections task](tasks/TYPEINFO_SECTIONS.md).

## Guessing independent-field-store order from source order or field-declaration order both fail; test empirically

Hypothesis: for a `void` setter writing two unrelated, independently-typed
fields with no data dependency between them (`CActBoyake::DispOff`,
`CChara::SetPadChk`, `CActReversal::SetRevMax`), writing the statements in
either natural reading order (matching field declaration order) or in
matching-the-reference-instruction order would predict which store lands
in the branch-delay slot after `jr $ra`.
Observed result: naive source order matching field-declaration order was
wrong for 2 of the first 3 cases tried (`SetPadChk`, `SetRevMax`); only
`DispOff` happened to match on the first guess. There was no consistent
"first-declared-first" or "lower-offset-first" or "byte-store-before-
word-store" rule visible from inspection alone across the 3 examples.
Mechanism: GCC's instruction scheduler reorders independent stores by its
own internal heuristics (likely related to its internal statement/RTL
numbering or a scheduling pass's tie-breaking, not something visible from
the C++ source's textual order). Confirmed by a controlled two-field probe
(`Test1::OrderAB`/`OrderBA`, `Test2::SetXYab`/`SetXYba`, one class with an
int+byte pair mimicking `DispOff`'s shape, one with two ints mimicking
`SetPadChk`'s shape): both orderings were compiled and disassembled side
by side, and the actual match required writing the statement for the
*later-declared* field *first* in source (so it lands in the delay slot
last), which is the opposite of naive reading-order intuition and was
determined only by testing, not by reasoning about the compiler further.
Supporting evidence: `docs/tasks/LINKONCE_CLUSTER.md` (2026-09-23
non-trivial-tier batch entry) records the exact reference and candidate
bytes for all three cases before and after the fix.
Reconsideration conditions: if a future batch finds >2 consecutive
examples where naive source order matches on the first try, the "always
test both orders" default could be relaxed to "try naive order first, but
still verify" — not yet warranted from 3 data points.
What this does not justify: this does not mean the *values* being stored
or the *field identities* were wrong — only the emission order of two
already-correct, independent store instructions. A `verify-ee` failure on
a multi-statement `void` setter with no other error signal is a strong
hint to try the reversed statement order before suspecting the field
offsets or values themselves.
References: [linkonce cluster task](tasks/LINKONCE_CLUSTER.md).

## Two more confirmed instances of the isolated-probe register-allocation limitation, both pointer chases

Hypothesis: `CBgCtrl::GetNowBgColGrp` (`return nowBg->group;`) and
`CPAppear::GetType` (`return nodeData->type;`) — both a two-`lw`
pointer-chase through an already-evidenced pointer field plus a fixed
member offset — would reproduce byte-exactly once the field's pointer
type and the member offset were correctly modeled, following the same
`GetColHitData`-style pattern that worked immediately for other classes
in the same batch.
Observed result: both compiled to the exact target *size* (12 bytes) on
the first attempt, but with `$3` as the intermediate register holding the
loaded pointer where the reference reuses `$2` throughout
(`lw $2,off($4); jr $ra; lw $2,extra($2)` in the reference vs.
`lw $3,off($4); jr $ra; lw $2,extra($3)` in the candidate). Three
rephrasings were tried for `GetNowBgColGrp` alone (direct return
expression, an explicit local pointer variable, and a `const`-qualified
method) — all three produced the identical `$3`/`$2` split.
Mechanism: this is the same isolated-probe register-allocation-context
limitation already logged for `CCamera::GetViewMatrix` and generalized
across the whole `__tf*` RTTI cluster — GCC 2.96's register allocator
makes different choices depending on surrounding register pressure/context
that an isolated probe cannot reproduce, even holding the exact source
shape fixed.
Supporting evidence: `docs/tasks/LINKONCE_CLUSTER.md` (2026-09-23
non-trivial-tier batch entry); the exact reference/candidate disassembly
for both methods and all three `GetNowBgColGrp` rephrasing attempts.
Reconsideration conditions: same as the existing `CAMERA_MATRIX_PROBE.md`
entry — a different, still-unmodified EE GCC 2.96 sub-build/patch level
identified as the actual original toolchain could change this; no source
rephrasing found in this batch changed it.
What this does not justify: the field retyping (`nowBg`/`nodeData` as
typed pointers, not plain `int`/`void*`) that made these two methods
possible to even attempt remains valid, reusable evidence recorded in
`CODE_SUCCESSES.md` — only the specific getter method for each is deferred,
left as a comment in `candidates/ee_camera/CCamera.h` rather than a
compiled, verified section.
References: [linkonce cluster task](tasks/LINKONCE_CLUSTER.md).
