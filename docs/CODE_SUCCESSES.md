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

## A sibling accessor's dereference reveals a field's true (pointer) type

Symptom: a field already modeled as a plain `int`/`void*` (because its own
getter just does a raw `lw`+`jr` passthrough, which compiles identically
either way) turns out to be read at a *nonzero offset* by a different
method in the same class, which the plain-type model cannot express.
Mechanism: `CBgCtrl::nowBg`, `CPAppear::nodeData`, `CActTbl::actData`, and
`CCharaBase::charCol` were all first recovered from their own simple
getter alone, with no reason yet to suspect they were anything but a flat
value. A later method in the *same class* (`GetNowBgColGrp`, `GetType`,
`SetActTbl`, `GetColHitData`) turned out to load through that same field
plus a fixed offset (`lw $2,off($4); lw $2,extra($2)` or
`addiu $2,$2,extra`), which only makes sense if the field is a pointer to
a struct with a member/sub-object at `extra`.
Pathway: when a new method's first load reads a field you already have
modeled as `int`/`void*`, and the method then dereferences or offsets that
loaded value, retype the field to a pointer (to a small helper struct
with just enough padding + the needed member, named only to reproduce the
offset — not a real recovered layout). This is safe to do to an
already-committed, already-verified field: a raw pointer-value passthrough
getter (`return field;`) compiles to the identical bytes whether `field`
is declared `int`, `void*`, or a real pointer type, so retyping never
reopens an existing match — confirm this with `verify-ee`/`compare_sections.py`
after the change rather than assuming it, but expect it to still pass.
Verification: all four retypes verified via `make verify-boot verify-ee`
after the change; each sibling getter's own section still matched byte-for-
byte with no modification to its own source line.
Scope: general to any accessor-recovery project where a class's fields are
reconstructed incrementally, one method at a time, with no ground truth for
field types beyond what each accessor's own body demands.
Limits: only establishes that the field is *a* pointer with a member at
the observed offset; the pointed-to type's other members, its total size,
and the field's original name remain unevidenced beyond that.
References: [linkonce cluster task](tasks/LINKONCE_CLUSTER.md).

## Conditional move, signed-vs-unsigned zero tests, and narrowing all leave distinct evidence

Symptom: three different "looks like the usual pattern" guesses each
produced a wrong or oversized result on the first attempt in the same
batch of non-trivial accessors.
Mechanism, three independent cases:
1. `CPrim::ArgFilter(PRIMINF*)` is `move $2,$4; jr $ra; movn $2,$5,$5` —
   a ternary (`return value ? value : this;`) compiled with MIPS32R2's
   `movn` (conditional move), not an `if`/branch. This is the first `movn`
   in this cluster; nothing about the method's one-pointer-in/one-pointer-
   out signature suggested a ternary until the disassembly was read.
2. `CChara::IsHitDmgCntChk` boolifies a field with `slt $2,$zero,$2`
   (signed), where every other `return field != 0;` boolify already in
   this cluster used `sltu $2,$zero,$2` (unsigned). `slt` only appears for
   a *signed greater-than-zero* test (`return field > 0;`), which rejects
   negative values that `!= 0` would accept — a real semantic difference,
   not an equivalent rephrasing.
3. `CPrim::GetPrimPRIM` masks a 64-bit field and returns it in 12 bytes
   (`ld`, `jr`, `andi`); returning the masked value as `int` (signed)
   costs 8 extra bytes (`dsll32`/`dsra32` sign-extension), while
   `unsigned long` return type matches exactly, since a signed narrowing
   conversion from a 64-bit masked value needs explicit sign-extension
   that an unsigned return does not.
Pathway: don't default to `if`-shaped or `!= 0`-shaped or `int`-returning
models for every conditional-looking or boolean-looking or masked
accessor. Read the actual opcode: `movn`/`movz` means a ternary/conditional
assignment, not a branch; `slt` vs `sltu` distinguishes `> 0` from `!= 0`;
extra sign-extension instructions around a masked 64-bit field mean the
return type should be unsigned, not signed.
Verification: `make verify-ee`/`compare_sections.py`, all three exact
after correcting to the evidence-driven model above; `movn`/`movz` needed
a local `.set mips32r2` / `.set mips3` bracket in `asm/camera_accessors.s`
around only the one affected stanza (MIPS32R2 conditional-move
instructions are not in the pinned `-march=mips3` assembler's default
instruction set; this is a local directive, not a global compiler-flag
change, and does not affect the byte-exactness gate's meaning).
Scope: general MIPS/GCC codegen conventions; not specific to this
compiler beyond the `-march=mips3` assembler default excluding MIPS32R2
opcodes.
Limits: only one example of each shape is confirmed in this cluster.
References: [linkonce cluster task](tasks/LINKONCE_CLUSTER.md).

## `objVector` is an 8-byte, two-float vector, confirmed by three independently-matching empty bodies

Symptom: `CWeapon::SetTgtPos`/`PositionInit`/`AddOffset` all take
`objVector` by value with a body that reproduces the reference's bare
16-byte prologue/epilogue (zero load/store instructions) only for a
specific guessed size, and a wrong guess still compiles and "looks"
plausible (same section, same mangled name) while being the wrong size.
Mechanism: a 12-byte `objVector { float x,y,z; }` hypothesis compiles the
same empty-body methods to 36 bytes (defensive `ldl`/`ldr` spill of the
unused by-value struct argument onto the stack, the same alignment-driven
codegen difference already seen for `objMatrix`), while an 8-byte
`objVector { float x,y; }` reproduces the reference's exact bare
prologue/epilogue on all three independently-checked methods.
Pathway: for a `G<len><Name>`-mangled by-value class parameter whose
method body is provably empty in the reference (checked by comparing byte
count to the minimal empty-body-with-frame baseline), don't assume the
type's size from its name or a prior similar type (`objMatrix`'s 64 bytes
does not imply `objVector` is proportionally sized) — binary-search the
size empirically against the exact reference byte count, since a
too-large or misaligned guess triggers visible defensive spill code you
can detect immediately, and a correct guess reproduces a suspiciously
trivial, easy-to-verify all-zero-instruction body.
Verification: `python3 tools/run_ee_probe.py` on an isolated 3-method
probe; 8 bytes matched exactly (byte-for-byte, all three methods) on the
first attempt after the 12-byte hypothesis was rejected by size alone.
Scope: this compiler's by-value-class-parameter spill/dead-code behavior;
likely generalizes to any GCC of this era with conservative "always spill
non-trivial-looking class parameters" behavior (see the register-
allocation-context entries in `CODE_FAILURES.md` for the companion
limitation once a body is *not* empty).
Limits: field names `x`/`y` are a plausible guess from the class's
apparent purpose, not independently confirmed; no method in this batch
reads or writes an individual `x`/`y` component.
References: [linkonce cluster task](tasks/LINKONCE_CLUSTER.md).

## A helper function's vtable-pointer constant identifies its runtime class via the linkonce data section at that address

Symptom: three tiny shared helper functions each write a small object and
return, with no name, symbol, or debug info to say which C++ class each
object actually is.
Mechanism: each helper computes an absolute address (`lui`+`addiu`) and
stores it into the object's second word — the classic MIPS o32 vtable-pointer
initialization idiom. That absolute address is not itself meaningful in
isolation, but it exactly matches the load address of a real,
named `.gnu.linkonce.d._vt$<len><Name>` vtable data section elsewhere in
the same ELF. Looking up which named vtable section owns that address turns
an anonymous "helper at 0x32c1f8" into a confirmed "field-initializer for
`__user_type_info`" — the same technique already used throughout this
project to identify classes from field offsets, just applied to a vtable
pointer's target instead of a `this`-relative field.
Pathway: when a disassembled function's only distinguishing content is a
computed absolute address stored into an object (not a `jal`/branch
target), look that address up against the ELF's own section table before
guessing at its purpose from the calling context alone. A `.gnu.linkonce.d._vt$*`
section hit gives a definitive class name; other section kinds may need
different follow-up.
Verification: `tools/bootstrap.py`'s `elf_sections` used to confirm
`0x3e7020`/`0x3e6ff0`/`0x3e6fc0` are the exact load addresses of
`.gnu.linkonce.d._vt$16__user_type_info`,
`.gnu.linkonce.d._vt$14__si_type_info`, and
`.gnu.linkonce.d._vt$17__class_type_info` respectively — three distinct,
unambiguous section-name matches, not a coincidence of nearby addresses
(each vtable section is 48 bytes and the constants land exactly at each
section's start).
Scope: general technique for any vtable-pointer-initializing code on a
platform whose linker keeps named vtable sections (as this GNU v2/cfront
linkonce-heavy build does); not specific to RTTI helpers.
Limits: only resolves the *class identity* of the object being initialized,
not its full member layout or virtual function table contents. All four
vtable-pointer constants found in this cluster (three `__tf*`-registration
helpers plus one destructor-dispatch helper) resolved cleanly to named
sections in this pass; an address that does not land exactly on a linkonce
vtable section's start would need a different follow-up (e.g. it could be
mid-vtable, or a non-vtable constant entirely).
References: [RTTI runtime helpers task](tasks/RTTI_RUNTIME_HELPERS.md).

## `this + index*stride [+ offset]` with no preceding load means the array lives inside the object itself

Symptom: an `int GetX(int index)` accessor's first instruction scales the
index (`sll $5,$5,N`) and adds it directly to `$4` (`this`), with no `lw`
anywhere before the final dereference — the usual "load a pointer field,
then index it" shape doesn't apply, and there's no field to attribute
the array to.
Mechanism: eleven sections across seven classes in one batch
(`CRender::GetVUEntryCV`/`GetVUEntryPrim`, `CBgCtrl::GetFilter`,
`CCharaCntrl::SetNowChara`, `CCharaDataSts::GetStatusBuf`,
`CCharaBase::SetPartsMdlSw`, all four `CMotionSts` status accessors,
`CGameEffect_Ctrl::GetGameEffectBase`, all five `Labyrinth_ArmGet`
accessors) share this exact shape: `sll $5,$5,shift; addu $5,$5,$4;
lw/sw $2,offset($5)`. Since `$4` (`this`) is used as the base directly, the
indexed array's first element is a fixed byte offset *inside the class's
own layout*, not behind a pointer member.
Pathway: when an accessor's first two instructions are `sll` (scale index)
+ `addu` with `$4` as one operand (not a loaded register), model it as
`ElementType fieldName[1];` (a one-element placeholder; a declared array's
length never affects codegen for a runtime-variable index, so the
placeholder is exactly as byte-accurate as any larger guess) at the byte
offset the final `lw`/`sw` uses, and the accessor as `return
fieldName[index];` or `fieldName[index] = value;`. Contrast with the same
shape reached through an actual pointer field (`lw` first, then `addu` to
the *loaded* register, not `$4`) — that case needs `ElementType
*fieldName;` or `ElementType *fieldName[1];` instead, and is a materially
different claim about the class's layout (a separately-allocated buffer
vs. an inline array).
Verification: all eleven sections matched byte-for-byte via
`make verify-ee`/`compare_sections.py` on the first attempt using this
model, including two array-of-pointer variants
(`CCharaBase::GetWeaponC`/`GetWeaponPmv`/`SetCurrentSubWeaponPmv`) that
needed the "loaded pointer, not $4" variant instead — confirming both
shapes are real and distinguishable from the disassembly alone.
Scope: general MIPS/GCC array-indexing codegen; likely applies anywhere in
this cluster an accessor takes an `int index` parameter.
Limits: does not establish the array's actual length or element count,
only that element 0 starts at the observed offset with the observed
stride.
References: [linkonce cluster task](tasks/LINKONCE_CLUSTER.md).

## `nor $rd,$zero,$rs` is MIPS's bitwise-NOT idiom, not a new comparison operator

Symptom: a boolean-returning accessor's disassembly includes `nor` before
the already-familiar `sltu`/`srl` boolify step, and it's unclear what C++
source produces a `nor` that wasn't asked for.
Mechanism: MIPS has no dedicated bitwise-NOT instruction; GCC (and every
MIPS compiler) synthesizes `~x` as `nor $rd, $zero, $rs` (since
`~(0 | x) = ~x`). `CMotion3::IsChangeMotionNo` (`nor` then `sltu
$2,$zero,$2`) is therefore `return (~field) != 0;`, algebraically
`return field != -1;` — a "changed from sentinel -1" check, not a generic
nonzero test. `CChara::IsStartActPmv` (`nor` then `srl $2,$2,0x1f`,
extracting bit 31) is `return field >= 0;` — the sign bit of `~field` is
the logical negation of `field`'s own sign bit.
Pathway: when `nor $rd,$zero,$rs` (or `nor $rd,$rs,$zero`) appears, read it
as `~rs`, then read whatever follows it as an ordinary boolify/extract of
that complemented value — `!= 0` after `nor` means `!= -1` on the original;
`srl ...,31` after `nor` means `>= 0` on the original. Don't model these as
a new, unexplained instruction shape; they compose from two already-known
idioms (bitwise-NOT-via-nor, then the existing boolify/sign-extract
patterns).
Verification: both reproduced byte-exactly via `make verify-ee` using
`return field != -1;` and `return field >= 0;` respectively, no additional
rephrasing needed once decoded this way.
Scope: general MIPS codegen convention (any compiler on an ISA without a
dedicated NOT instruction); not specific to this compiler.
Limits: only these two compositions (`nor`+`sltu`, `nor`+`srl 31`) are
confirmed; other post-`nor` operations are unverified but expected to
decode the same way (complement, then interpret normally).
References: [linkonce cluster task](tasks/LINKONCE_CLUSTER.md).

## A field read two different ways at the same offset is a union, not two fields or a cast

Symptom: one accessor treats a field as a pointer (`StartActPmv`), another
accessor at the *identical* offset treats it as a raw signed integer for a
sign-bit test (`IsStartActPmv`), and C++ doesn't allow two differently-typed
member declarations at the same offset without an explicit union — nor
does pointer-to-integer casting on this target reliably preserve "just
reinterpret the bits" semantics (pointers are 32-bit, `long` is 8 bytes
per earlier evidence in this project).
Mechanism: `CChara::actPmv` is loaded as a plain 32-bit value and compared
via `nor`+`srl 31` (a signed sign-bit test, see above) by
`IsStartActPmv`, and used as a genuine pointer by the already-verified
`StartActPmv`/`GetActPmvTgt`-adjacent code. An anonymous
`union { void *actPmv; int actPmvRaw; };` gives both accessors their own
correctly-typed name for the same 4 bytes without duplicating the offset
or risking a cross-size-class cast.
Pathway: when two evidenced accessors read/write the identical offset with
genuinely incompatible types (pointer vs. arithmetic int, not just
`void*` vs. a more specific pointer as in the sibling-accessor case
already logged), use an anonymous union rather than picking one type and
casting at the call site — a cast risks silently changing codegen
(e.g. a pointer-to-`long`-to-`int` cast chain could touch more bytes than
intended on a target where `long` is wider than a pointer), while a union
member access compiles to the same raw load/store either way.
Verification: `IsStartActPmv() { return actPmvRaw >= 0; }` matched
byte-for-byte via `make verify-ee`; `StartActPmv`'s existing verified
section was unaffected (confirmed by the same full-suite rerun).
Scope: general C++/MIPS technique; applies whenever two already-evidenced
accessors disagree on a field's type at the same offset.
Limits: only one instance in this cluster; the union does not claim which
interpretation (pointer or raw flag test) reflects the "true" original
field type, only that both are real, evidenced accesses.
References: [linkonce cluster task](tasks/LINKONCE_CLUSTER.md).
