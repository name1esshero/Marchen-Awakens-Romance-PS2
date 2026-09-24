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
