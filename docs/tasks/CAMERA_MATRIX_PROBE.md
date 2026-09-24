# CCamera view/projection matrix probe — 2026-09-23

Authority: [standards](../STANDARDS.md). Contributor: Claude Sonnet 5, code.
State: non-matching candidate; all original bytes remain preserved hex.

## Evidence and hypothesis

The pinned boot ELF contains four adjacent `CCamera` linkonce sections whose
mangled names and sizes are:

| Section | Size |
| --- | --- |
| `.gnu.linkonce.t.GetViewMatrix__7CCamera` | 72 |
| `.gnu.linkonce.t.SetViewMatrix__7CCameraG9objMatrix` | 112 |
| `.gnu.linkonce.t.GetProjectionMatrix__7CCamera` | 72 |
| `.gnu.linkonce.t.SetProjectionMatrix__7CCameraG9objMatrix` | 112 |

The `G9objMatrix` parameter mangling establishes `objMatrix` is passed by
value (any class, per the corrected `P`/`R`/`G` rule already in
`SUCCESSES.md`), and `objMatrix` is an existing forward-declared class
elsewhere in `CCamera.h` (used only as a pointer/reference type before this
investigation). `GetViewMatrix__7CCamera` disassembles to a 16-`ld`/`sd`-pair
aggregate copy of 0x40 (64) bytes from `this` into a hidden return-value
pointer, using the same "hidden destination before `this`" ABI shape already
established for `GetViewRect`. A 64-byte aggregate matches a 4x4 `float`
matrix (16 floats). The hypothesis tested: `objMatrix { float m[16]; }`,
`aligned(8)`, with `GetViewMatrix`/`SetViewMatrix`/`GetProjectionMatrix`/
`SetProjectionMatrix` as trivial passthrough accessors on two `objMatrix`
members of `CCamera`. It uses the existing pinned EE GCC `2.96-ee-001003-1`
and unchanged common `-O2` flag. No register assignments, pointer/integer
casts, or assembly were introduced.

Without the `aligned(8)` attribute the candidate emits defensive
`ldl`/`ldr`/`sdl`/`sdr` unaligned-merge sequences (136 bytes for the 72-byte
getters), the same failure mode already documented for `GetViewRect`. Adding
`aligned(8)` is a real, falsifiable structural claim about `objMatrix` (the
compiler's own codegen choice reacts to it) and is retained; it is not a
flag or register change and does not by itself force a byte match.

## Observed mismatch

### Getters: size matches, register allocation does not

With `aligned(8)`, `GetViewMatrix` and `GetProjectionMatrix` both compile to
exactly 72 bytes, matching the reference size. The reference
(`extracted/SLPM_661.56;1`, `.gnu.linkonce.t.GetViewMatrix__7CCamera`
at `0x33b018`):

```text
move $2, $4
ld   $3, 0xf0($5)
sd   $3, 0x0($2)
ld   $3, 0xf8($5)
sd   $3, 0x8($2)
...
ld   $3, 0x128($5)
jr   $ra
sd   $3, 0x38($2)
```

reuses only `$2`/`$3` throughout: `$4` (the hidden return pointer) is moved
into `$2` once, and every load/store pair reuses `$3`. The candidate
(`build/ee_camera_matrix.o`, same section):

```text
ld   $6, 0xf0($5)
move $2, $4
sd   $6, 0x0($4)
ld   $3, 0xf8($5)
sd   $3, 0x8($4)
...
ld   $3, 0x128($5)
jr   $ra
sd   $3, 0x38($4)
```

alternates `$6`/`$3` for the loads and stores directly through `$4` (never
adopting the reference's `move`-then-reuse-`$2` pattern). Same size (72
bytes), same instruction mix (`move`, 8x `ld`, 8x `sd`, `jr`), same field
offsets — different register-allocation/scheduling decisions by GCC 2.96's
instruction scheduler. The first differing byte is at section offset `0x4`.
This is the identical mechanism already noted for other trivial accessors
where genuine byte-exact register allocation could not be reproduced without
pinning registers, which `STANDARDS.md` forbids.

### Setters: a materially different codegen strategy, not just scheduling

`SetViewMatrix`/`SetProjectionMatrix` are worse off. The reference
(`.gnu.linkonce.t.SetViewMatrix__7CCameraG9objMatrix` at `0x33b060`, 112
bytes) spills the by-value parameter to the stack via 8 `ld`/`sd` pairs, then
finishes with:

```text
addiu $4, $4, 0xf0
<unknown>   (7b a6 00 00)
<unknown>   (7b a7 00 10)
<unknown>   (7b a8 00 20)
<unknown>   (7b a9 00 30)
ext   $6, $4, 0x0, 0x1     (misdecoded; encoding is 7c 86 00 00)
<unknown>   (7c 87 00 10)
<unknown>   (7c 88 00 20)
<unknown>   (7c 89 00 30)
jr    $ra
```

The four `<unknown>` opcodes at `0x7b`/`0x7c` fall in the R5900 quadword
load/store space (`LQ`/`SQ`, 128-bit-GPR instructions unique to the EE and
outside the MIPS III ISA `llvm-objdump-21`'s generic `mips` target decodes;
the `ext` line is very likely a `SQC2`/`QMFC2`-family EE instruction that
happens to alias a MIPS32R2 `ext` encoding in the generic decoder, not an
actual `ext`). The candidate instead keeps the whole `objMatrix` parameter in
plain 64-bit GPRs (`$2`,`$3`,`$6`-`$11`) and stores each field individually
into `this` with ordinary `sd`, redundantly re-spilling to the stack
afterward, for 104 bytes total (still 8 bytes short of the reference's 112).
This is not a scheduling nuance: the reference uses R5900-specific
128-bit-quadword move instructions that this repository's disassembler
cannot even name, so byte-exact reproduction of the setters is blocked on
tooling (an R5900-aware disassembler/assembler), not on source or flag
changes.

## Reproduction and verification

```sh
python3 tools/run_ee_probe.py --sources candidates/ee_camera_matrix --output build/ee_camera_matrix.o
python3 tools/compare_sections.py 'extracted/SLPM_661.56;1' build/ee_camera_matrix.o candidates/ee_camera_matrix/sections.txt
llvm-objdump-21 -d --section=.gnu.linkonce.t.GetViewMatrix__7CCamera build/ee_camera_matrix.o
llvm-objdump-21 -d --section=.gnu.linkonce.t.GetViewMatrix__7CCamera 'extracted/SLPM_661.56;1'
llvm-objdump-21 -d --section=.gnu.linkonce.t.SetViewMatrix__7CCameraG9objMatrix build/ee_camera_matrix.o
llvm-objdump-21 -d --section=.gnu.linkonce.t.SetViewMatrix__7CCameraG9objMatrix 'extracted/SLPM_661.56;1'
```

The comparison is expected to fail with `byte mismatch (72 vs 72 bytes)` on
the first selected section; this research candidate is excluded from the
passing reconstruction gates. No compiler flag was changed and no register
was pinned to attempt to force a match, per `STANDARDS.md`.

Executed outcomes:

- Historical compilation of the checked-in candidate: PASS.
- Selected comparison: expected FAIL, `GetViewMatrix__7CCamera` 72 vs 72
  bytes (content mismatch, not size mismatch).
- `clang++ -std=c++98 -fsyntax-only candidates/ee_camera_matrix/probe.cpp`: PASS.
- `make test verify-boot verify-source-only verify-ee`: PASS (114 unit tests,
  existing candidate syntax checks, 441 matching sections / 3,528 bytes, full
  boot comparison, isolated pinned-hash rebuild, and existing EE probe
  comparison) — all unaffected, since this candidate lives outside
  `config/camera_sections.txt` and outside `candidates/ee_camera/`.
- `git diff --check`: PASS.

No reference hash, selected reconstruction section, or preserved byte was
changed. `objMatrix`'s size (64 bytes) and 8-byte alignment requirement are
genuine, reusable evidence about `CCamera`'s layout even without a byte
match, and are recorded in `docs/CODE_SUCCESSES.md`. This result does not
reject EE GCC 2.96 for the game; it identifies two independent, unresolved
gaps: GCC 2.96's instruction-scheduling/register-allocation nondeterminism
relative to whatever built the original (getters), and an R5900 MMI/quadword
disassembly gap in the project's current tooling (setters).
