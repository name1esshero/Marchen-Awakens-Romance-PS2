# Verified mechanisms — code/compiler frontier

Authority: [STANDARDS.md](STANDARDS.md). Scope: this file is the dedicated
knowledge log for the "Claude / code" queue lead (boot ELF reconstruction,
linkonce accessor recovery, EE GCC compiler identification), kept separate
from the shared [`SUCCESSES.md`](SUCCESSES.md) so concurrent asset/
localization work never needs to touch the same file. Earlier code-frontier
findings recorded before this file existed remain in `SUCCESSES.md` and are
not duplicated here; new ones go here going forward.

Entry format matches `SUCCESSES.md`: Symptom, Mechanism, Pathway,
Verification, Scope, Limits, References.

## Nested-enum and const-reference parameters mangle predictably from known letters

Symptom: a stub method's mangled name includes a shape not yet seen in this
project (`Q2...`, `RC...`) and it is unclear what C++ declaration reproduces
it.
Mechanism: this GNU v2/cfront-style mangler composes previously-established
letters/shapes rather than introducing arbitrary new ones. `Q<n>` introduces
an `n`-component qualified name, each component a plain `<len><name>` pair
in order (e.g. `Q28CCharCom17ComTrainingStatus` = `CCharCom::
ComTrainingStatus`, a nested enum). `RC<len><name>` is simply `R` (reference)
composed with `C` (const) ahead of the plain class name (`const objMatrix &`).
Pathway: when a raw suffix shows `Q<n>` followed by `n` `<len><name>` pairs,
declare the nested type inside the outer class/scope named by the first
pair(s) and use it as the parameter type. When a suffix combines known
letters (`RC`, `PC`, etc.), compose the corresponding C++ qualifiers/pointer
or reference forms in the same order rather than treating the combination
as an unknown shape. Verify on a standalone probe before touching the real
candidate, as with every other parameter-mangling case in this project.
Verification: both shapes matched their exact target mangled names on the
first attempt once composed this way, confirmed on a standalone probe
(`CCharCom::SetTrainingStatus(CCharCom::ComTrainingStatus)`,
`CArmEffect::GameEffectOn(const objMatrix &)`) before use in the real
candidates, then again via `make verify-ee`.
Scope: GNU v2/cfront-style mangling on this EE GCC target.
Limits: only two-letter (`RC`) and two-component (`Q2`) cases are confirmed;
longer qualified names or other letter combinations are unverified.
References: [linkonce cluster task](tasks/LINKONCE_CLUSTER.md).

## A trivial-looking accessor can still compute, not just pass through a field

Symptom: after assuming every recovered method in a cluster is a field
read/write, constant return, or no-op, a new one-instruction method's
operand register doesn't correspond to any evidenced field offset.
Mechanism: `CWeaponArm::GetSubNo(int a, int b, int c)` is `addu $2, $7, $5`
— for a 3-argument member function under this ABI ($4=this, $5=a, $6=b,
$7=c), that is `c + a`, ignoring `this` and `b` entirely. Nothing about the
one-instruction size guaranteed a passthrough; `addu` combining two
argument registers is just as compact as a single `lw`.
Pathway: don't assume a one-instruction method is a field access just
because every prior one in the cluster was. Decode the actual operands
against the calling convention ($4=this, $5.. = arguments in order) before
guessing the body. For a commutative op like `addu`, operand *order* still
matters for byte-exact reproduction (`addu $2,$7,$5` and `addu $2,$5,$7`
are different instruction words) — verify the exact source expression
(`c + a` vs `a + c`) on a standalone probe rather than assuming either
order is equivalent.
Verification: standalone probe compiling both `return a + c;` and
`return c + a;` — only `c + a` reproduced the exact target bytes
(`addu $2, $7, $5`); `a + c` produced the reversed, non-matching encoding.
Scope: this compiler's register-argument ABI ($4=this, $5/$6/$7 = first
three integer arguments). Likely generalizes to any similarly-shaped
one-instruction "compute from arguments" method in this or similar MIPS o32
targets.
Limits: only addition of two of three arguments confirmed; other arithmetic
operators or argument counts are unverified.
References: [linkonce cluster task](tasks/LINKONCE_CLUSTER.md).

## $gp-relative addressing marks a static/global, not an instance field — don't force a match

Symptom: a method compiled from `this->field` guesses does not match; the
original section's instruction uses a register other than `$4`/`this` as
its base.
Mechanism: `CArmEffect::GetUpdateFlag`/`GetHead` use `lb`/`lw` with `$gp` as
the base register (`-0x60dc($gp)`, `-0x60e0($gp)`), not `$4`. This is MIPS
small-data-section addressing for a `static`/file-scope/global variable,
whose exact `$gp`-relative offset depends on the *entire original binary's*
small-data segment layout — a link-time property of the whole program, not
something an isolated single-class probe can reproduce, since the probe's
own linker places its own (entirely different) set of statics.
Pathway: recognize `$gp`-relative addressing (base register `$28`/`gp`
rather than `$4`/`this`) as a structurally different case from every
instance-field accessor in this cluster. Do not attempt to force a byte
match by padding the probe with synthetic globals to nudge its own
`$gp`-relative offsets into alignment — that would manufacture a match
rather than discover one, which STANDARDS.md prohibits. Leave such sections
as explicit raw-hex debt; recovering them would need a way to establish
the *whole program's* static-data layout, not just this class's.
Verification: N/A (explicit non-attempt, not a failed attempt) — the
decision was made from the disassembly alone (`lb $2, -0x60dc($gp)` /
`lw $2, -0x60e0($gp)`, both distinct from over 380 other recovered
sections that all use `$4` as their base) before writing any candidate.
Scope: this MIPS/eabi64 target's small-data-section convention; likely
generalizes to any MIPS toolchain using `$gp`-relative addressing for
statics.
Limits: does not establish that these two bytes are permanently
unrecoverable, only that the current isolated-probe methodology cannot
reach them without manufacturing a match.
References: [linkonce cluster task](tasks/LINKONCE_CLUSTER.md).

## A one-instruction method can unconditionally zero a field, not just pass a value through

Symptom: a candidate setter modeled as `field = value;` (taking the field's
value from an argument) does not match a target `sw`/`swc1` instruction
that stores a literal zero register (`$zero`), because the real method
takes no such argument at all.
Mechanism: `CCharaPmv::RestartConvertStone` (`sw $zero, 0x63c($4)`) and
`CActTblC::DisableReversal` (`sw $zero, 0x5c($4)`) are zero-argument methods
whose entire evidenced body is "set this field to zero" — not a setter
receiving a caller-supplied value. The parameter list and the field-write
value are independent claims; a one-instruction store doesn't imply the
stored value came from an argument.
Pathway: when a store instruction's source register is `$zero` rather than
an argument register (`$5`/`$6`/`$7`/`$f12`), and the mangled name has no
parameter encoding for that position, model the method as taking no
parameters and assigning the literal constant, e.g.
`void DisableReversal() { reversalFlag = 0; }` — not
`void DisableReversal(int value) { reversalFlag = value; }`.
Verification: `make verify-ee` — the unmodified EE GCC `2.96-ee-001003-1`
`-O2` probe reproduces both exact `sw $zero, ...` byte patterns from these
zero-argument bodies.
Scope: general MIPS codegen convention (any zero-argument "clear/disable"
method); not specific to this compiler.
Limits: only integer-field zeroing confirmed; float-field zeroing via
`swc1 $f0-implicit-zero` or similar has not been observed in this cluster.
References: [linkonce cluster task](tasks/LINKONCE_CLUSTER.md).

## `RC` (const reference) composes with primitive types, not only classes

Symptom: uncertain whether a `const T &` parameter mangling generalizes
beyond class types to primitives like `float`/`int`.
Mechanism: `FootStamp_Base::Init__14FootStamp_BaseRC9objVectorRCfRCi` has
three by-const-reference parameters: a class (`RC9objVector` = `const
objVector &`) and two primitives (`RCf` = `const float &`, `RCi` = `const
int &`). The `R`/`C` letters compose the same way regardless of what
follows them — a primitive type letter (`f`, `i`, ...) or a `<len><name>`
class spelling.
Pathway: when a raw suffix shows `RC` followed by a primitive type letter
rather than a `<len><name>`, declare that parameter as `const <type> &`
directly — the same composition rule already established for `RC<len><name>`
(reference to const class) applies uniformly.
Verification: confirmed on a standalone probe
(`void Init(const objVector &, const float &, const int &) {}`) before
touching the real candidate, then again via `make verify-ee`.
Scope: GNU v2/cfront-style mangling on this EE GCC target.
Limits: only `float`/`int` confirmed as the primitive operands; other
primitive types are unverified but expected to follow the same rule.
References: [linkonce cluster task](tasks/LINKONCE_CLUSTER.md).

## A compiler's own codegen strategy reveals real alignment even without a byte match

Symptom: an aggregate-returning accessor's candidate body is the right field
and the right size in principle, but the compiler emits far more
instructions/bytes than the target (defensive `ldl`/`ldr`/`sdl`/`sdr`
unaligned-merge sequences instead of plain `ld`/`sd`).
Mechanism: `CCamera::GetViewMatrix`/`GetProjectionMatrix` return a 64-byte
`objMatrix` (16 floats) by hidden pointer. With `objMatrix` declared as a
plain `{ float m[16]; }` (natural 4-byte alignment), EE GCC 2.96 conservatively
assumes the aggregate might not be 8-byte aligned and emits paired
`ldl`/`ldr`+`sdl`/`sdr` merges, doubling the instruction count (136 bytes
instead of the target 72). Adding `__attribute__((aligned(8)))` to
`objMatrix` alone — no register, flag, or ABI change — makes the compiler
choose plain `ld`/`sd` and produces the exact target *size* (72 bytes) for
both getters. The compiler's own choice of instruction family is therefore
itself an alignment oracle: it reveals a genuine structural fact about the
type (`objMatrix` requires >=8-byte alignment) independent of whether the
exact bytes end up matching.
Pathway: when an aggregate-copy accessor's byte count is roughly double the
target with `ldl`/`ldr`/`sdl`/`sdr` present, don't just accept the mismatch —
try `aligned(8)` (or check existing evidenced alignment for that field) on
the aggregate type before concluding the case is unrecoverable. If the
instruction family changes to unaligned `ld`/`sd` and the size now matches,
that alignment fact is real, reusable evidence for the type's layout, even
if the exact register allocation still differs afterward (a separate,
independent gap — see `CAMERA_MATRIX_PROBE.md`).
Verification: `python3 tools/run_ee_probe.py` + `llvm-objdump-21` on the
standalone `objMatrix` probe, comparing with/without `aligned(8)`: without
it, 136 bytes with `ldl`/`ldr`/`sdl`/`sdr`; with it, 72 bytes with plain
`ld`/`sd`, matching the reference's exact size (byte content still differs —
see limits).
Scope: this compiler's alignment-driven choice between aligned and
defensive-unaligned aggregate copy codegen; likely generalizes to any GCC
targeting an ISA without efficient unaligned load/store.
Limits: size match is not a byte match — register allocation/scheduling for
the aligned case can still differ from the original (confirmed for this
exact pair, see `CAMERA_MATRIX_PROBE.md`). This technique establishes
alignment, not a complete recovery.
References: [camera matrix probe](tasks/CAMERA_MATRIX_PROBE.md),
[view rect probe](tasks/VIEW_RECT_PROBE.md).

## A class's own compiler-synthesized RTTI function calls its base class's RTTI function

Symptom: `config/camera_sections.txt`/`candidates/ee_camera` only recovers
member accessors; nothing in the recovered evidence base says which classes
derive from which, even though 440 classes' worth of that information turns
out to be sitting in a linkonce cluster nobody had disassembled yet.
Mechanism: every `__tf<len><Name>` (GNU v2/cfront RTTI "type-info accessor")
function in the boot ELF follows a guard-checked construct-on-first-use
pattern. A "root" (no polymorphic base) class's function calls one shared
helper with just its own name string. A class with a polymorphic base
instead calls that base class's *own* `__tf` function first (guaranteeing
the base's guard runs), then calls a different shared helper passing three
addresses: its own guard, its own name, and the base's guard. The base's
identity is therefore directly readable as a `jal` target address inside the
derived class's own machine code — confirmed on `CCamera` (calls
`C3dObject`'s `__tf` function) and `CCamera2` (calls `CCamera`'s), matching
the class family already in `candidates/ee_camera/CCamera.h`.
Pathway: for any class with a `__tf*` linkonce section, decode every `jal`
in that section's bytes (standard MIPS encoding: opcode 6, 26-bit
word-aligned target, top 4 bits from the delay slot's own address) and check
whether the target address falls inside another `__tf*` section's address
range. If it does, that other class is a base class of this one. Sections
with no such call (only a call to the shared one-argument helper) are root
classes for RTTI purposes. Never conflate this with full inheritance,
vtable layout, or object size — a non-polymorphic base contributes no such
call, and this reveals only what the compiler's own RTTI runtime tracked.
Verification: `tools/typeinfo_hierarchy.py` (tested in
`tests/test_typeinfo_hierarchy.py`, including a real boot-ELF byte sequence
as a regression anchor) decodes all 498 `__tf*` sections and finds 440
single-base edges and 58 roots; its pure-Python `jal` decoder was
cross-checked against `llvm-objdump-21`'s independent disassembly of the
same 498 sections (938 `jal` instructions, zero mismatches) before being
trusted as the tool's only decoding path.
Scope: GNU v2/cfront-style RTTI codegen on this compiler target; the
`jal`-decoding technique itself is standard MIPS and portable to any other
linkonce cluster on this binary.
Limits: only single-inheritance-shaped calls are decoded (no
two-`__tf*`-call shape was observed in this cluster, i.e. no confirmed
multiple-inheritance case); one 92-byte outlier (`CPrimList` -> `CPrim`)
uses a different shared helper with an extra literal-`1` argument, plausibly
but not confirmedly a virtual-base variant (single occurrence, left open).
References: [typeinfo sections task](tasks/TYPEINFO_SECTIONS.md),
[linkonce cluster task](tasks/LINKONCE_CLUSTER.md).
