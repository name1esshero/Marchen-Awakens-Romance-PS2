# Linkonce accessor cluster: census and initial recovery — 2026-09-22

Authority: [STANDARDS.md](../STANDARDS.md).
Agent: Claude Sonnet 5; role: Contributor. Work type: R&D, bootstrap extension.
Current state: [STATUS.md](../STATUS.md). Builds on
[BOOTSTRAP.md](BOOTSTRAP.md) and [COMPILER_PROBE.md](COMPILER_PROBE.md).

## Discovery

The main `.text` section (address `0x100000`, size 2,338,584 bytes) ends at
exactly `0x33af18`, the address of the first `.gnu.linkonce.t.*` section. From
there to `0x34d330` the boot ELF contains **1,694 named, nonempty
`.gnu.linkonce.t.*` sections totaling 71,932 bytes** — far more than the eight
camera accessors originally identified. This is evidence of a distinct linker
region (GNU linkonce COMDAT-style folding of inline/template members), not
part of the "raw main .text" debt.

`tools/linkonce_inventory.py` (new; tested in
`tests/test_linkonce_inventory.py`) parses each section's GNU v2/cfront-style
mangled name by shape — member function, const member function, constructor,
destructor, or compiler-synthesized type-info accessor (`__tf...`) — and
extracts a class name where the shape supports it. This is a **naming-shape
heuristic, not a demangler**: it does not decode parameter/return types and
leaves ambiguous or template-shaped names (`t12CStringStack1i_256_`, etc.)
explicitly `unparsed` rather than guessing. Reproduce with:

```sh
python3 tools/linkonce_inventory.py 'extracted/SLPM_661.56;1' > reports/linkonce_text_inventory.json
```

Census result (`reports/linkonce_text_inventory.json`):

- 1,694 sections across **497 distinct class names** (by the naming heuristic).
- By kind: 972 member functions, 123 const member functions, 497 type-info
  accessors, 65 destructors, 30 constructors, 7 unparsed.
- Size histogram: **733 sections are exactly 8 bytes** — the same
  `jr $ra` + one delay-slot instruction shape already proven recoverable for
  the original eight camera accessors. Other common sizes (88, 84, 52, 12, 16
  bytes, …) correspond to type-info thunks, small structs-of-calls, and
  slightly larger accessors/stubs.
- Largest classes by section count: `CCharaBase` (60), `CChara` (56),
  `CWeapon` (34), `MenuFrameUI` (27), `C3dObject` (26).

This single census is the most valuable outstanding lead for the "Reduce main
ELF raw regions" and "Broaden compiler identification" work-queue items: most
of the 733 trivial sections are plausibly recoverable by the exact method
already validated (disassemble the two instructions, write a natural
one-line accessor, verify with `compare_sections.py`).

## Recovered this session

Within the existing `CCamera` cluster (`0x33af18`–`0x33b778`), eleven more
trivial sections were disassembled with `llvm-objdump-21 -j <section>` against
the extracted reference ELF and confirmed to follow the same
two-instruction pattern as the original eight. The mangled names' embedded
class-name lengths (`__7CCamera`, `__8CCamera2`, `__9CCameraMv`) show these
belong to **three distinct classes**, not overloads of one class — a
correction to any assumption that all camera accessors share one type.

| Section | Class | Instructions |
| --- | --- | --- |
| `GetViewScaleX__7CCamera` | CCamera | `jr $ra` / `lwc1 $f0, 0x17c($4)` |
| `GetViewScaleY__7CCamera` | CCamera | `jr $ra` / `lwc1 $f0, 0x180($4)` |
| `GetViewAngle__C7CCamera` | CCamera (const) | `jr $ra` / `lwc1 $f0, 0x178($4)` |
| `GetViewAngleDir__C7CCamera` | CCamera (const) | `jr $ra` / `lwc1 $f0, 0x178($4)` (same offset as above) |
| `Draw__7CCameraP7CRender` | CCamera | `jr $ra` / `addiu $2, $0, 1` (ignores its `CRender*` argument) |
| `CameraControl__8CCamera2f` | CCamera2 | `jr $ra` / `nop` (empty body, ignores its float argument) |
| `GetAngleY__8CCamera2` | CCamera2 | `jr $ra` / `lwc1 $f0, 0x15c($4)` |
| `GetAngleX__8CCamera2` | CCamera2 | `jr $ra` / `lwc1 $f0, 0x160($4)` |
| `DebugCamera__8CCamera2ii` | CCamera2 | `jr $ra` / `nop` (empty body, ignores both int arguments) |
| `GetTgtChr__9CCameraMv` | CCameraMv | `jr $ra` / `lw $2, 0x294($4)` |
| `GetCamType__9CCameraMv` | CCameraMv | `jr $ra` / `lw $2, 0x234($4)` |

`GetViewAngle` and `GetViewAngleDir` read the identical field; the evidence
does not establish whether the original source used one field with two
accessor names or two fields that happen to hold equal values at this
snapshot. Modeled as one field with two accessor names (the simpler claim).

`Draw`, `CameraControl` and `DebugCamera` are stub-shaped: they take
arguments they never use and either return a fixed constant or do nothing.
This is presented as observed behavior, not a claim about why the original
function is a stub (e.g. an unfinished feature, a disabled debug path, or a
base-class override that legitimately does nothing).

Not recovered this pass (documented as follow-up, still raw hex): the larger
`GetViewRect` (24 bytes, struct-copy via `ld`/`sd`), `GetViewMatrix` /
`SetViewMatrix` / `GetProjectionMatrix` / `SetProjectionMatrix` (72–112 bytes,
likely 4×4 matrix copies), and every `__tf*` type-info accessor. These need
more careful ABI/aggregate-return modeling than the single-instruction
accessors and are left as explicit debt rather than rushed.

### Assembly and object-file changes

`asm/camera_accessors.s` gained eleven more `.section` stanzas using only
previously-validated instructions (`jr`, `lwc1`, `lw`, `addiu`, `nop`).
`config/camera_sections.txt` now selects all 19 sections. `build/camera_accessors.o`
(Clang, `-target mipsel-none-elf -march=mips3 -mabi=32`) reproduces all 19
sections' 152 bytes exactly (`make verify-camera`, invoked by `make verify-boot`).

### EE GCC broadened match

`candidates/ee_camera/CCamera.h` now declares `CCamera` with the corrected
field layout (an evidenced 4-byte unknown gap at `0x174`, then `viewAngle`,
`viewScaleX`, `viewScaleY`) plus new classes `CCamera2` and `CCameraMv` with
partial layouts for their evidenced fields only. `probe.cpp` takes addresses
of all eleven new methods (same harness technique as before: forces
out-of-line emission without adding codegen attributes or literal
instructions). EE GCC `2.96-ee-001003-1` with the same single `-O2` flag,
**unmodified from the original eight-accessor experiment**, reproduces all 19
sections' 152 bytes and the complete probe ELF (`make verify-ee`). This
broadens the compiler-identification evidence from 8 to 19 matching sections
across 3 classes, including const member functions, a pointer-argument stub,
and two no-argument-effect void methods — a wider variety of code shapes than
the original set, though still all trivial one-instruction bodies.

`candidates/camera_accessors.cpp` (the host-only semantic model, not part of
either build) was extended in parallel with `offsetof` static assertions for
every new field, verified with `clang++ -std=c++17 -fsyntax-only`.

## Verification

- `make test`: **PASS**, 27 tests (20 existing plus 7 new for
  `linkonce_inventory.py`'s name-shape classifier).
- `make verify-boot`: **PASS**, 19 sections / 152 bytes match; full boot ELF
  `cmp` byte-identical.
- `make verify-source-only`: **PASS**, isolated rebuild (no ISO, no reports,
  no cached objects) matches the pinned boot hash.
- `make verify-ee`: **PASS**, EE GCC 2.96 candidate sections and full probe
  ELF match.
- Raw-interval accounting was checked by direct byte comparison before
  deleting the old monolithic hex file: the regenerated five-fragment split
  plus the 88 newly recovered bytes reproduce the old single 1,102,324-byte
  interval exactly.

## Remaining debt and next steps

- **3,445,052 bytes** remain raw hex (down from 3,445,140), across five
  intervals instead of two (the new gaps around the recovered sections).
- The census identifies roughly 733 more trivial 8-byte sections across ~497
  classes as candidates for the same recovery method. This is a lead, not a
  promise: each still needs individual disassembly and verification, and
  some may turn out to have more complex bodies than their size suggests
  once the *offset target* is inspected (e.g. two 8-byte "accessors" could
  still touch different structures via different base registers).
- `GetViewRect`, the two view/projection matrix pairs, and all `__tf*`
  type-info accessors in the camera cluster remain open; they need
  aggregate-return and RTTI-shape research beyond this session's scope.
- No claim is made about `CCamera`, `CCamera2`, or `CCameraMv`'s complete
  size, inheritance, or virtual layout. Only the specific evidenced fields
  above are established.

## CRender accessor batch — 2026-09-22

Ten additional 8-byte sections in the same linkonce cluster were recovered for
`CRender` (`0x33b1c4`–`0x33b254`, interleaved with unrecovered sections). Direct
disassembly establishes one `jr $ra` delay-slot operation per method:

| Method | Observed operation |
| --- | --- |
| `GetPRMODE` | address of `$4 + 0x4a0` |
| `GetFrame` | `lw` from `$4 + 0x4c8` |
| `GetCamera` | `lw` from `$4 + 0x4e0` |
| `GetFrameBufferMode`, `GetZBufferMode` | `lw` from `0x4e4`, `0x4e8` |
| `GetFrameField`, `GetScreenWidth`, `GetScreenHeight` | `lw` from `0x4f4`, `0x4f8`, `0x4fc` |
| `GetFreeList`, `GetOldOddEven` | `lw` from `0x554`, `0x55c` |

The partial `CRender` candidate uses natural inline getters and unknown byte
ranges between the evidenced offsets. Names support candidate integer/pointer
interpretations, but only the load width, offset, const qualification encoded in
the section name, and `GetPRMODE` address calculation are established. In
particular, the pointed-to types and full class layout are not recovered.

An initial candidate placed `oldOddEven` at `0x558`; the EE object instead
emitted `lw $2, 0x558($4)`, differing from the reference's `0x55c`. The direct
disassembly established the omitted four-byte gap, after which the unchanged
common EE GCC `2.96-ee-001003-1` `-O2` probe matched all ten sections. This is
ordinary layout correction from evidence, not compiler steering.

`asm/camera_accessors.s` and the reconstruction selection now contain 29
sections / 232 bytes across four partial classes. The explicit bootstrap export
splits the affected raw interval around every selected section; 3,444,972 bytes
remain raw. `make test verify-boot verify-source-only verify-ee` passes, with
full byte comparison for both assembled and EE-probe boot ELFs.

## CRender2 accessor batch — 2026-09-22

Fourteen further 8-byte sections establish direct field operations for a new
partial `CRender2` class: six address returns (`0x30`, `0x360`, `0x3e0`,
`0x420`, `0x460`, `0x548`), six integer loads (`0x4c4`, `0x534`, `0x578`,
`0x610`, `0x740`, with the near-clip field read by two names), and two integer
stores (`0x600`, `0x610`). The method count includes the paired get/set methods
and two names reading `0x534`.

The natural EE probe uses one word at each address-return target only to model
the observed address calculation; it does not establish the pointed-to object
types, full member sizes, inheritance, or class extent. The same unmodified EE
GCC `2.96-ee-001003-1` `-O2` invocation matches all fourteen sections. The
assembly and probe reconstruction now cover 43 sections / 344 bytes across five
partial classes, leaving 3,444,860 explicitly raw bytes. `make test
verify-boot verify-source-only verify-ee` passes.

## CGameCamera accessor batch — 2026-09-22

Six direct methods add a separate partial `CGameCamera` layout: float loads at
`0x17c`, `0x180`, and `0x404`; integer/pointer-word loads at `0x1a0` and
`0x3fc`; and a float store at `0x408`. Although two offsets match `CCamera`
accessors, no inheritance relationship is claimed. The EE probe first exposed
an incorrect contiguous-field hypothesis; preserving the observed four-byte gap
at `0x400` made all six sections match under unchanged `-O2`.

The reconstruction now contains 49 sections / 392 bytes across six partial
classes and 3,444,812 explicit raw bytes. `make test verify-boot
verify-source-only verify-ee` passes.

## C3dObject accessor batch — 2026-09-22

Thirteen direct methods establish a partial scene-object layout: parent and
first-child words at `0x0` and `0x4`, a next-child word read through the explicit
`C3dObject*` argument at `0x8`, a `objMatrix*` field at `0x10`, and address
returns at `0x20` and `0x60`. The exact mangled parameter spelling on
`SetLinkBoneMat` independently requires `objMatrix*`; an initial untyped-pointer
candidate emitted the wrong section name and was corrected before promotion.

The address-return targets' full matrix sizes, tree ownership semantics, and
meaning of the ignored integer parameters are not established. The unchanged EE
GCC probe matches all thirteen sections. Reconstruction now covers 62 sections
/ 496 bytes across seven partial classes; 3,444,708 bytes remain explicit raw
debt. `make test verify-boot verify-source-only verify-ee` passes.

## CChara and CCharaBase accessor batch — 2026-09-23

Agent: Claude Sonnet 5; role: Contributor. A gameplay character-code area,
chosen deliberately because another concurrent session was localizing
text/graphics assets at the time; this batch touches only `asm/`,
`candidates/ee_camera/`, `config/camera_sections.txt` and `preserved/boot/`,
none of which overlap the localization/graphics/asset trees.

Seventy-nine direct 8-byte sections (41 `CCharaBase`, 38 `CChara`) were
disassembled with `llvm-objdump-21 -j <section>` and confirmed to follow the
same `jr $ra` + one delay-slot instruction shape already established. Field
reads/writes (`lw`/`sw`/`lwc1`/`swc1`), embedded-member address returns
(`addiu $2, $4, N`), and one previously-unseen shape were all present:

- **Zero-register moves via `daddu`, not `move`/`or`.** The reference binary
  encodes `move $2, $5` and `move $2, $zero` as `daddu $rd, $rs, $0`
  (`2d 10 ...`). Clang's `move` pseudo-op for this target instead assembles
  to `or $rd, $rs, $0` (`25 10 ...`) — same semantics, different bytes. This
  only affects the hand-preserved `.s` assembly layer (the assembler's own
  instruction-selection default for a pseudo-op); the real EE GCC 2.96
  compile of equivalent C++ (`return value;`, `return 0;`) independently
  chose `daddu` on its own and needed no correction. Fix for the `.s` layer:
  write `daddu $rd, $rs, $0` explicitly instead of `move`.
- **`mov.s $f0, $f12`**, a float pass-through register move, for
  `CalcDamage(float damage, int) { return damage; }` — assembles and compiles
  identically on the first attempt, no correction needed.
- **A second confirmed case of the class-named-pointer-parameter mangling
  trap** already seen with `C3dObject::SetLinkBoneMat`'s `objMatrix*`
  parameter: `SetCurrentStatus__10CCharaBaseiiP12TypeArmParami` requires a
  parameter of an opaque forward-declared `TypeArmParam` class, not `void *`
  — `void *` mangles as `Pv` and silently compiles a same-shaped section
  under a *different* name, so the target section is simply absent (a
  missing-key error from `compare_sections.py`, not a byte mismatch). This
  has now happened independently in two different sessions/classes; see the
  new `SUCCESSES.md` entry.

Many `CCharaBase` methods (`SetCurrentAct`, `SetCurrentStatus`,
`SetCurrentOwnCtrl`, `SetCurrentMove`, `GetActTblC`, `GetActTblBase`,
`GetTargetModel`, `CheckPadPress`, `CheckPadOn`, `HitCheckAll`, `ActionCntrl`,
`IsDoukiAct`, `ActionCntrlExcute`, `PreUpdatePmv`, `PreNutralMotionJump`,
`PreAction2`) are stub-shaped: they ignore all arguments and either do nothing
or return a fixed zero. This is presented as observed behavior only — it is
plausible evidence of unfinished/disabled functionality or of a base-class
default meant to be overridden elsewhere, but neither is established here.
Two pairs of accessors alias the same field under different names, as with
the earlier `CCamera::GetViewAngle`/`GetViewAngleDir`: `CChara::GetLocate`/
`GetLocateV` (both `0x600`) and `CChara::GetTarget`/`GetTargetModel` (both
`0xcf4`).

`asm/camera_accessors.s`, `candidates/ee_camera/CCamera.h` and `probe.cpp`
were extended with the same harness technique as every prior batch (address-
taking to force out-of-line emission; no codegen attributes, register
pinning or literal instruction bytes). The unmodified EE GCC
`2.96-ee-001003-1` `-O2` invocation matches all 79 new sections on the first
compile after the `TypeArmParam` fix. Reconstruction now covers **141
sections / 1,128 bytes across nine partial classes**; 3,444,076 bytes remain
explicit raw debt. `make test verify-boot verify-source-only verify-ee`
passes (107 tests; full boot ELF and full EE-probe ELF both byte-identical).

Not recovered this batch (left as future candidates, per the wider census):
CWeapon (27), MenuFrameUI/MenuFrame/MenuFrameSimpleUI/MenuEsy (93 combined —
skipped deliberately this batch since they are UI/menu-adjacent and the
concurrent session was working on UI localization), CMotion3, CTexData,
CMotion, CGameCntrl, and the rest of the 592 still-untouched trivial 8-byte
sections (`reports/linkonce_text_inventory.json`, recomputed against the
current `config/camera_sections.txt`).

## CWeapon accessor batch — 2026-09-23

Agent: Claude Sonnet 5; role: Contributor. Continues the same deliberate
scoping: gameplay logic only, no UI/menu/graphics classes, since a concurrent
session remained active on text and graphics localization throughout.

All 27 remaining trivial 8-byte `CWeapon` sections (`0x33ff28`–`0x340064`)
were disassembled and confirmed to follow the established shapes: six field
reads (`GetArmParam`, `GetChara` at offsets `0x0`/`0x8`, both pointers;
`GetLinkBoneType`, `GetArmType`, `GetTblNo`, `IsSubWeapon` — plain ints at
`0xc`/`0x14`/`0x18`/`0x1c`), one field write (`SetPmv` at `0x20`), and twenty
stub bodies (empty or fixed-zero-return, ignoring all arguments) — `CWeapon`
is, like `CCharaBase`, mostly a base-class-shaped stub surface with only a
handful of real fields near offset zero.

This batch produced a second, distinct parameter-mangling correction beyond
the pointer-type trap already in `SUCCESSES.md`:
`SetSubMotion__7CWeaponG8MotionNoif`'s `G8MotionNo` is **not** a reference
(`R`) as first guessed — a standalone probe showed `MotionNo &` compiles to
`R8MotionNoif`, a different name. `G` is this compiler's encoding for a class
passed **by value** whose non-trivial (here, merely user-declared, empty)
constructor forces old-ABI hidden-reference argument passing. Confirmed via
a minimal isolated probe before touching the real candidate; see the updated
`SUCCESSES.md` entry for the full three-way `P`/`R`/`G` distinction.

`asm/camera_accessors.s`, `CCamera.h` and `probe.cpp` were extended with the
same harness technique as every prior batch. The unmodified EE GCC
`2.96-ee-001003-1` `-O2` invocation matches all 27 new sections after the `G`
correction. Reconstruction now covers **168 sections / 1,344 bytes across ten
partial classes**; 3,443,860 bytes remain explicit raw debt. `make test
verify-boot verify-source-only verify-ee` passes (full boot ELF and full
EE-probe ELF both byte-identical).

Not recovered this batch: the rest of the 592-minus-27 still-untouched
trivial 8-byte sections, still excluding all UI/menu-adjacent classes.

## CMotion3 accessor batch — 2026-09-23

Agent: Claude Sonnet 5; role: Contributor. Same deliberate scoping as every
prior batch: gameplay logic only.

All 18 remaining trivial 8-byte `CMotion3` sections (`0x33c8fc`–`0x33c9d8`)
were disassembled and confirmed to follow the established shapes: sixteen
field reads (mostly `int`, one `float` at `0xb0`, one `void*` at `0xa4`), one
field write (`SetNextJumpDC`, a self-referencing `CMotion3 *` at `0xb8`), and
one no-argument-effect stub (`OnOpenNewMotion`). `SetNextJumpDC`'s parameter
mangles as `P8CMotion3` — the class referencing its own (still-incomplete at
that point in its own body) type by pointer, which C++ permits without any
special handling, unlike the `CWeapon`/`CCharaBase` cases needing a separate
forward-declared class.

`asm/camera_accessors.s`, `CCamera.h` and `probe.cpp` were extended with the
same harness technique as every prior batch; the unmodified EE GCC
`2.96-ee-001003-1` `-O2` invocation matched all 18 new sections on the first
attempt (no mangling correction needed this time). Reconstruction now covers
**186 sections / 1,488 bytes across eleven partial classes**; 3,443,716 bytes
remain explicit raw debt. `make test verify-boot verify-source-only
verify-ee` passes (full boot ELF and full EE-probe ELF both byte-identical).

Not recovered this batch: the remaining ~547 still-untouched trivial 8-byte
sections, still excluding all UI/menu-adjacent and texture-adjacent classes
(`MenuFrame*`, `MenuEsy`, `CTexData`, `CTexGroup`) given the concurrent
localization session's territory.
