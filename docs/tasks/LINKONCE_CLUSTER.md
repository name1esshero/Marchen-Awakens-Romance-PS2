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

## CMotion accessor batch — 2026-09-23

Agent: Claude Sonnet 5; role: Contributor. Same deliberate scoping.

All 14 remaining trivial 8-byte `CMotion` sections (`0x33c69c`–`0x33c774`)
were disassembled and confirmed trivial: nine field reads (int/float/pointer),
four field writes, and one address-return. Two enum-typed setter parameters
required exact-name enum definitions to match their mangled encoding —
`SetInterpolateType__7CMotion10InterpType` and
`SetTargetType__7CMotion16MotionTargetType` — the same "match the encoded
type exactly" lesson as the `P`/`R`/`G` class-parameter trap, but for enums:
a plain `enum InterpType { INTERP_TYPE_UNKNOWN };` (one placeholder
enumerator, since the definition must be nonempty to use the type) was
sufficient; unlike the `G` case, an enum does not need a non-trivial
constructor to mangle by its own name — it already does, being a value type.

`GetAttribute` (`lw`, offset `0xc`) and `GetNowAttributeClass` (`addiu`
address-of, same offset `0xc`) are another same-offset aliased pair, treated
as one `int attribute` field with two accessor bodies (one returning the
value, one returning its address) — the same pattern as `CCamera::GetViewAngle`
/`GetViewAngleDir` and `CChara::GetLocate`/`GetLocateV`.

The unmodified EE GCC `2.96-ee-001003-1` `-O2` invocation matched all 14 new
sections on the first attempt. Reconstruction now covers **200 sections /
1,600 bytes across twelve partial classes**; 3,443,604 bytes remain explicit
raw debt. `make test verify-boot verify-source-only verify-ee` passes (full
boot ELF and full EE-probe ELF both byte-identical).

Not recovered this batch: the remaining 533 still-untouched trivial 8-byte
sections, still excluding UI/menu/texture-adjacent classes.

## CGameCntrl accessor batch — 2026-09-23

Agent: Claude Sonnet 5; role: Contributor. Same deliberate scoping.

All 14 remaining trivial 8-byte `CGameCntrl` sections (`0x33d770`–`0x33d7dc`)
were disassembled: thirteen are stub-shaped (ignore all arguments; most do
nothing, a few return a fixed value, one — `GetStartCntrlMode` — returns the
constant `10`), and one (`GetActBoyake`, offset `0x40`) reads a real `int`
field. `CGameCntrl` is, like `CCharaBase` and `CWeapon`, almost entirely a
base-class-shaped stub surface.

The unmodified EE GCC `2.96-ee-001003-1` `-O2` invocation matched all 14 new
sections on the first attempt. Reconstruction now covers **214 sections /
1,712 bytes across thirteen partial classes**; 3,443,492 bytes remain
explicit raw debt. `make test verify-boot verify-source-only verify-ee`
passes (full boot ELF and full EE-probe ELF both byte-identical).

Not recovered this batch: the remaining 519 still-untouched trivial 8-byte
sections, still excluding UI/menu/texture-adjacent classes.

## CPAppear accessor batch — 2026-09-23

Agent: Claude Sonnet 5; role: Contributor. Same deliberate scoping.

All 13 remaining trivial 8-byte `CPAppear` sections (`0x33dbc0`–`0x33dc30`)
were disassembled: nine field reads (four pointers, one boolean-shaped int,
one float, plus two address-return "matrix/link" fields already seen
elsewhere in this cluster), and two no-argument-effect stub bodies
(`OnMotionJumpPre`/`OnMotionJumpAfter`).

Those two stubs' mangled names
(`OnMotionJumpPre__8CPAppearP9AprMotionT1`) use a compression shape not seen
before in this cluster: `T1` is a back-reference to an *already-mangled*
parameter type in the same list, used here because both parameters are the
same type (`AprMotion *, AprMotion *`) — confirmed on a standalone probe
before writing the real candidate; see the updated `SUCCESSES.md` entry.

The unmodified EE GCC `2.96-ee-001003-1` `-O2` invocation matched all 13 new
sections on the first attempt. Reconstruction now covers **227 sections /
1,816 bytes across fourteen partial classes**; 3,443,388 bytes remain
explicit raw debt. `make test verify-boot verify-source-only verify-ee`
passes (full boot ELF and full EE-probe ELF both byte-identical).

Not recovered this batch: the remaining 506 still-untouched trivial 8-byte
sections, still excluding UI/menu/texture-adjacent classes.

## CCharaDataSts accessor batch and a mangling-trap correction — 2026-09-23

Agent: Claude Sonnet 5; role: Contributor. Same deliberate scoping.

All 12 remaining trivial 8-byte `CCharaDataSts` sections (`0x33f2e4`–
`0x33f378`) were disassembled: ten are no-argument-effect stubs, one reads
an address (`GetPrgSts`, offset `0x180`), and one writes an int
(`SetNowMotNo`, offset `0xad0`) — another almost-entirely-stub class, like
`CCharaBase`/`CWeapon`/`CGameCntrl`.

**Correction to the P/R/G mangling entry.** One stub,
`CheckGatyaStsArm__13CCharaDataSts9SArmTypeD`, has a bare `9SArmTypeD`
parameter suffix (no `P`/`R`/`G` letter). Modeled first as an empty class
`class SArmTypeD {};` by analogy with the earlier `G`-prefixed cases — this
compiled cleanly but produced `G9SArmTypeD`, not the target. Standalone
probes then showed the previously recorded belief that `G` requires a
non-trivial constructor was never actually correct: a bare empty class and a
class with a plain data member both mangle by-value as `G<len><Name>` with
*no* constructor at all, and retesting the original `MotionNo` case with its
constructor removed reproduced the identical `G8MotionNoif`. So `G` simply
marks "class passed by value," full stop, and the bare (letterless)
`9SArmTypeD` here could not be a class parameter — it is an **enum**,
confirmed with a standalone probe declaring `enum SArmTypeD { ... };` and
reproducing the exact target name. `SUCCESSES.md`'s entry is corrected
accordingly (marked as a correction, not silently rewritten) and
`candidates/ee_camera/CCamera.h`'s `MotionNo` was simplified to drop its
now-shown-unnecessary constructor, reverified against `make verify-ee`
before this batch's own changes were layered on top.

The unmodified EE GCC `2.96-ee-001003-1` `-O2` invocation matched all 12 new
sections after the enum correction. Reconstruction now covers **239 sections
/ 1,912 bytes across fifteen partial classes**; 3,443,292 bytes remain
explicit raw debt. `make test verify-boot verify-source-only verify-ee`
passes (full boot ELF and full EE-probe ELF both byte-identical).

Not recovered this batch: the remaining 494 still-untouched trivial 8-byte
sections, still excluding UI/menu/texture-adjacent classes.

## ActionObject/CCol/CMotionC/ArmEffectBase batch — 2026-09-23

Agent: Claude Sonnet 5; role: Contributor. Same deliberate scoping: gameplay
logic only (collision, motion linkage, generic action/effect base classes).
Batched four classes together in one pass to cover more ground per
verification cycle, since the remaining candidate list spans many small
classes rather than a few large ones.

All 35 remaining trivial 8-byte sections across `ActionObject` (10), `CCol`
(9), `CMotionC` (8) and `ArmEffectBase` (8) were disassembled and confirmed
trivial. Two notable shapes:

- **`CCol::GetPos`-style "return this" accessor**: `ArmEffectBase::GetPos`
  is `jr $ra` / `move $2, $4` — it returns the object's own address
  unchanged (`return this;`), not a field.
- **The `T<n>` back-reference index is the 1-based position of the repeated
  parameter**, confirmed precisely this batch (refining the looser
  "repeats an earlier parameter" note from the `CPAppear` batch).
  `CCol::CallBack__4CColP4CColiiP14ColCheckResultT4` has five parameters;
  two standalone probes distinguished the hypotheses: `(CCol*, int, int,
  ColCheckResult*, CCol*)` (repeating parameter 1) mangled as `...T1`, while
  `(CCol*, int, int, ColCheckResult*, ColCheckResult*)` (repeating parameter
  4) mangled as `...T4` — an exact match. So `T<n>` always means "same type
  as parameter n," 1-based, counting every parameter (primitives included)
  in declaration order.

A hand-written (not generator-script-produced) first draft of the `CCol`
struct had fields out of ascending-offset order, which would have silently
produced wrong `lw`/`addiu` offsets in the compiled candidate. Caught before
the EE GCC compile step by re-deriving the struct with the same small
offset-sorting generator used for every other class in this task, rather
than trusting a manual field list — worth remembering as a process note:
prefer the generator for any struct beyond two or three fields, even under
time pressure.

The unmodified EE GCC `2.96-ee-001003-1` `-O2` invocation matched all 35
sections after the corrected `CCol` layout. Reconstruction now covers **274
sections / 2,192 bytes across nineteen partial classes**; 3,443,012 bytes
remain explicit raw debt. `make test verify-boot verify-source-only
verify-ee` passes (full boot ELF and full EE-probe ELF both byte-identical).

Not recovered this batch: the remaining 459 still-untouched trivial 8-byte
sections, still excluding UI/menu/texture/model/movie-adjacent classes.

## Labyrinth_ArmGet/CPDataArmObj/CActTgt/CSubObject batch — 2026-09-23

Agent: Claude Sonnet 5; role: Contributor. Same deliberate scoping and
four-class batching strategy as the previous entry.

All 24 remaining trivial 8-byte sections across `Labyrinth_ArmGet` (7),
`CPDataArmObj` (6), `CActTgt` (6) and `CSubObject` (5) were disassembled and
confirmed trivial. `Labyrinth_ArmGet::GetCheckChar` uses `lh` (load
halfword), the first 16-bit load seen in this cluster; modeled as `short`.
`CSubObject::GetBody` (address-of) and `GetVertexListNum` (value) read the
identical offset `0x10`, the same aliasing shape already established
elsewhere. All other sections are single plain `int`/address-return field
accessors.

The unmodified EE GCC `2.96-ee-001003-1` `-O2` invocation matched all 24
sections on the first attempt. Reconstruction now covers **298 sections /
2,384 bytes across twenty-three partial classes**; 3,442,820 bytes remain
explicit raw debt. `make test verify-boot verify-source-only verify-ee`
passes (full boot ELF and full EE-probe ELF both byte-identical).

Not recovered this batch: the remaining 435 still-untouched trivial 8-byte
sections, still excluding UI/menu/texture/model/movie-adjacent classes.

## CMotion2/CEffObject/CPAppear_PS2/CCharaCntrl/CPrim batch — 2026-09-23

Agent: Claude Sonnet 5; role: Contributor. Same deliberate scoping; five
classes batched together this pass.

All 25 remaining trivial 8-byte sections across `CMotion2` (5), `CEffObject`
(5), `CPAppear_PS2` (5), `CCharaCntrl` (5) and `CPrim` (5) were disassembled.
Two new instruction/type findings:

- **`CPrim` uses `ld`/`sd`** (64-bit load/store) for its `prim` and `tex0`
  fields. `SetTex0__5CPrimUl`'s mangled `Ul` (`unsigned long`) parameter
  compiling to `sd` confirms this compiler's `unsigned long` is **8 bytes**
  on this target, not 4 — consistent with the R5900/eabi64 ELF flags noted
  since the initial bootstrap. `GetTex0Addr` (address-of) and `GetTex0`
  (value) alias the same offset `0x10`, the same shape seen repeatedly in
  this cluster.
- **`CPAppear_PS2::GetChildNodeNo`'s parameter mangles as `PCc`** — pointer
  to const char, i.e. `const char *` — a builtin type needing no forward
  declaration, unlike every prior class/enum parameter case in this task.

The unmodified EE GCC `2.96-ee-001003-1` `-O2` invocation matched all 25
sections, including the 64-bit `unsigned long` fields, on the first attempt.
Reconstruction now covers **323 sections / 2,584 bytes across twenty-eight
partial classes**; 3,442,620 bytes remain explicit raw debt. `make test
verify-boot verify-source-only verify-ee` passes (full boot ELF and full
EE-probe ELF both byte-identical).

Not recovered this batch: the remaining 410 still-untouched trivial 8-byte
sections, still excluding UI/menu/texture/model/movie-adjacent classes.

## CStageSk/CWeaponPmv/CAlpha/CGameEffect_Base/CMCard2 batch — 2026-09-23

Agent: Claude Sonnet 5; role: Contributor. Same deliberate scoping; five
more classes batched together (stage background state, weapon
projectile-motion linkage, generic alpha-fade, generic active-effect base,
memory-card save-data metadata).

All 20 remaining trivial 8-byte sections were disassembled and confirmed
trivial: plain int/float field reads, two self-referencing pointer setters
on `CWeaponPmv` (the same pattern as `CMotionC`/`CMotion3`, no forward
declaration needed), and one address-return field. No new instruction or
mangling shapes this batch.

The unmodified EE GCC `2.96-ee-001003-1` `-O2` invocation matched all 20
sections on the first attempt. Reconstruction now covers **343 sections /
2,744 bytes across thirty-three partial classes**; 3,442,460 bytes remain
explicit raw debt. `make test verify-boot verify-source-only verify-ee`
passes (full boot ELF and full EE-probe ELF both byte-identical).

Not recovered this batch: the remaining 390 still-untouched trivial 8-byte
sections, still excluding UI/menu/texture/model/movie-adjacent classes.

## CFade/CBgCtrl/CGameCntrlGm/CMotionPMS/CPDataGef batch — 2026-09-23

Agent: Claude Sonnet 5; role: Contributor. Same deliberate scoping; the
remaining safe candidate list is now mostly classes with 1-3 sections each
(148 sections across ~100 classes, versus 238 sections still excluded
across 49 UI/texture/model/movie-adjacent classes).

All 15 remaining trivial 8-byte sections across `CFade` (3), `CBgCtrl` (3),
`CGameCntrlGm` (3), `CMotionPMS` (3) and `CPDataGef` (3) were disassembled
and confirmed trivial. `CFade::SetDispMode` takes a bare (letterless) enum
parameter (`ACTOBJ_TYPE`), the same enum shape already established.

A second occurrence of the hand-written-struct offset-ordering mistake (see
`CODE_FAILURES.md`) was caught before compiling: `CMotionPMS`'s first draft
inserted a spurious 4-byte gap between `directFlag` (`0x128`) and
`pmvMotSts` (`0x12c`), which the evidence does not support (the two fields
are contiguous). Re-derived with the offset-sorting generator and fixed
before the EE GCC step.

The unmodified EE GCC `2.96-ee-001003-1` `-O2` invocation matched all 15
sections after the fix. Reconstruction now covers **358 sections / 2,864
bytes across thirty-eight partial classes**; 3,442,340 bytes remain
explicit raw debt. `make test verify-boot verify-source-only verify-ee`
passes (full boot ELF and full EE-probe ELF both byte-identical).

Not recovered this batch: the remaining 375 still-untouched trivial 8-byte
sections, still excluding UI/menu/texture/model/movie-adjacent classes.

## CWeaponArm/CEffectArm/CCharCom/CObjList/CGefBirth/CHitEff/CArmEffect/CEffPrimObj/CActBoyake/CStage batch — 2026-09-23

Agent: Claude Sonnet 5; role: Contributor. Ten classes batched together
(27 candidate sections, 25 recovered, 2 explicitly deferred).

Three new mangling/codegen shapes appeared, all confirmed on standalone
probes before touching the real candidates:

- **A genuine computation, not a passthrough**:
  `GetSubNo__10CWeaponArmiii` is `addu $2, $7, $5` — for parameters
  `(a, b, c)`, that's `c + a` (register `$7`=`c`, `$5`=`a`), confirmed by
  testing both operand orders: `c + a` reproduced `addu $2, $7, $5` exactly,
  while `a + c` produced the reversed (and non-matching) `addu $2, $5, $7`.
  Every other recovered method in this cluster so far has been a field
  access, constant return, or no-op; this is the first with real (if
  trivial) arithmetic.
- **`Q<n>` qualified/nested name**: `SetTrainingStatus__8CCharComQ28CCharCom17ComTrainingStatus`
  is `CCharCom::SetTrainingStatus(CCharCom::ComTrainingStatus)` — a nested
  enum. `Q2` introduces a 2-component qualified name, each component a
  `<len><name>` pair (`8CCharCom`, `17ComTrainingStatus`). Modeled as a
  nested `enum ComTrainingStatus` inside `CCharCom`; matched on the first
  attempt.
- **`RC<len><name>`**: `GameEffectOn__10CArmEffectRC9objMatrix` is
  `(const objMatrix &)` — reference (`R`) to const (`C`) `objMatrix`,
  combining two letters already known individually. Matched on the first
  attempt.

**Deferred (not recovered)**: `CArmEffect::GetUpdateFlag` (`lb`) and
`GetHead` (`lw`) both address via `$gp` (`-0x60dc($gp)`, `-0x60e0($gp)`),
not `$this`/`$4` like every other section in this cluster — evidence of a
static or file-scope variable, not an instance field. An isolated EE GCC
probe cannot reproduce the exact `$gp`-relative offset without matching the
*entire original program's* small-data-segment layout, and manufacturing
that layout to force a match would violate STANDARDS.md's prohibition on
manufactured matches. Left as raw hex, excluded from
`config/camera_sections.txt`; `GameEffectOn` from the same class was still
recovered since its own body never touches the `$gp`-relative fields.

The unmodified EE GCC `2.96-ee-001003-1` `-O2` invocation matched all 25
integrated sections. Reconstruction now covers **383 sections / 3,064 bytes
across forty-two partial classes**; 3,442,140 bytes remain explicit raw
debt (2 bytes short of the theoretical maximum for this batch, held back by
the two deferred `$gp`-relative sections). `make test verify-boot
verify-source-only verify-ee` passes (full boot ELF and full EE-probe ELF
both byte-identical).

Not recovered this batch: the remaining ~108 still-untouched trivial 8-byte
sections in safe gameplay classes, plus the 2 deferred `$gp`-relative
sections noted above, plus the 238 still-excluded UI/menu/texture/model/
movie-adjacent sections.

## CStageWall/CPArm_PS2/CBabGun/CCharCol/CCharaMotion/CGefScene/CGameEffect_Ctrl/FireWall_Seed/FireStorm_Ptcl/FireStorm_Seed batch — 2026-09-23

Agent: Claude Sonnet 5; role: Contributor. Ten more classes batched (20
candidate sections, 19 recovered, 1 deferred).

At this point the remaining safe candidate list is entirely 1-2-section
classes; many names in this tail suggest UI/dialog/menu territory (e.g. the
`Mar*`/`DataBase*`/`Labyrinth_*` event-screen families, `CommandList`/
`KeyConfig`/`Train*`, `CString*`, `CockpitBase`/`CCharGauge`, `Char2DAnimCtrl*`)
and were skipped this batch even though they don't match the earlier
UI/texture/model/movie keyword filter, out of caution around the concurrent
localization session's territory — narrative/dialog screens are very likely
to display text drawn from the same message tables being translated.

A third `$gp`-relative section was found and deferred the same way as the
two in the previous batch: `CGameEffect_Ctrl::GetInstance` reads
`-0x60e4($gp)`, the classic singleton static-instance-pointer shape. Left
unrecovered for the same reason (see `docs/CODE_SUCCESSES.md`).
`CCharCol::GetColHitData` (address-of) and `SetProp` (value write) alias the
identical offset `0x70`, the same pattern seen repeatedly — modeled as one
plain `int` field, not the address-typed placeholder used for pure
address-of cases, since here the field is genuinely both read and written
as a scalar.

The unmodified EE GCC `2.96-ee-001003-1` `-O2` invocation matched all 19
integrated sections. Reconstruction now covers **402 sections / 3,216 bytes
across fifty-one partial classes**; 3,441,988 bytes remain explicit raw
debt. `make test verify-boot verify-source-only verify-ee` passes (full
boot ELF and full EE-probe ELF both byte-identical).

With the expanded caution keyword list (adding `Mar`/`DataBase`/`Labyrinth`/
`LabyEve`/`Command`/`KeyConfig`/`Train`/`String`/`Cockpit`/`Gauge`/`2DAnim`/
`Transition`/`type_info` to the original UI/texture/model/movie set), exactly
**44 sections across 40 classes** remain judged safe and untouched; 283
sections across the rest are now deliberately excluded, up from 238, and 3
sections total are deferred as `$gp`-relative statics (331 total remaining,
unchanged from the true census figure).

## Final safe-scope batch — 37 classes, completing the recoverable set — 2026-09-23

Agent: Claude Sonnet 5; role: Contributor. The last batch of the
originally-remaining 40 safe classes (41 candidate sections, 39 recovered,
2 more `$gp`-relative sections deferred).

Two further deferrals found and confirmed the same way as the earlier
three: `LoadAnimNormal::GetInstance` (`-0x6138($gp)`, a singleton
instance pointer) and `CGameEffect_FootStamp::GetpFootStamp`
(`-0x6020($gp)`). `CGameEffect_FootStamp::GameEffectOn` was still
recovered since its own body never touches the deferred field, the same
split already used for `CArmEffect`.

Two more evidenced shapes, both new to this cluster:

- **Unconditional field-zeroing, not a passthrough setter**:
  `CCharaPmv::RestartConvertStone` is `sw $zero, 0x63c($4)` and
  `CActTblC::DisableReversal` is `sw $zero, 0x5c($4)` — both write the
  literal constant zero to a field, taking no value from any argument
  (neither method even has a parameter). Modeled as
  `void RestartConvertStone() { convertStone = 0; }` and
  `void DisableReversal() { reversalFlag = 0; }`.
- **`RC` applied to a primitive type, not just a class**:
  `FootStamp_Base::Init` takes `RC9objVector`, `RCf`, and `RCi` — reference-
  to-const composed with a NEW class (`objVector`, forward-declared) *and*
  with primitive types (`const float &`, `const int &`). Confirmed on a
  standalone probe before touching the real candidate: `RC` composes with
  any type the same way, not only classes.

With this batch, **every trivial 8-byte section not judged UI/dialog/
texture/model/movie-adjacent has now been either recovered or explicitly
deferred as a `$gp`-relative static**. The remaining 5 sections in
"safe" classes are exactly the 5 deferred ones (`CArmEffect` ×2,
`CGameEffect_Ctrl` ×1, `LoadAnimNormal` ×1, `CGameEffect_FootStamp` ×1) —
none are unaddressed oversights. This is a natural completion point for
this session's scope: further progress requires either resolving the
`$gp`-relative static-layout problem, or extending into the deliberately
excluded UI/dialog/texture/model/movie territory (238+ sections across
~55 classes), which stays out of scope while the concurrent localization
session is active there.

The unmodified EE GCC `2.96-ee-001003-1` `-O2` invocation matched all 39
integrated sections on the first attempt after adding one missed method
(`CActFootStmp::GetDispPosE`, caught by `verify-ee`'s `KeyError` before any
byte-level claim was made). Reconstruction now covers **441 sections /
3,528 bytes across ninety-five partial classes**; 3,441,676 bytes remain
explicit raw debt. `make test verify-boot verify-source-only verify-ee`
passes (full boot ELF and full EE-probe ELF both byte-identical).

## First non-trivial (>8-byte) batch — 34 sections in 22 already-known classes — 2026-09-23

Agent: Claude Sonnet 5; role: Code Department Lead. With the trivial 8-byte
tier exhausted, this batch moves to the next size tier (12 bytes, three
instructions) within classes already partially recovered, surveyed from
`reports/linkonce_text_inventory.json`'s 334 remaining `member`-kind
sections sized above 8 bytes. 36 sections were disassembled; 34 recovered,
2 deferred.

New evidenced shapes:

- **Conditional move as a ternary**: `CPrim::ArgFilter` is
  `move $2,$4; jr $ra; movn $2,$5,$5` — `return value ? value : this;`,
  the first use of `movn` in this cluster. `movn`/`movz` are MIPS32R2, not
  in the pinned `-march=mips3` assembler's default set; enabled locally
  with `.set mips32r2` / `.set mips3` around just this one stanza in
  `asm/camera_accessors.s`, not as a global flag change.
- **Signed vs. unsigned zero-comparison changes the instruction**:
  `CChara::IsHitDmgCntChk` is `slt $2,$zero,$2` (signed `> 0`), not the
  `sltu $2,$zero,$2` (`!= 0`) already seen for every other boolified-int
  getter in this cluster. Modeled as `return hitDmgCnt > 0;`, not
  `!= 0`.
- **A masked-and-returned 64-bit field needs an unsigned return type**:
  `CPrim::GetPrimPRIM` is `ld $2,0x8($4); jr $ra; andi $2,$2,0x7` (12
  bytes). `int GetPrimPRIM() { return prim & 0x7; }` compiles to 20 bytes
  (extra `dsll32`/`dsra32` sign-extension pair) because narrowing a 64-bit
  masked value to a *signed* 32-bit return forces explicit sign extension;
  `unsigned long GetPrimPRIM() { return prim & 0x7; }` matches exactly.
- **A "setter" can return the pointer it was just given**:
  `CActTbl::SetActTbl` is `move $2,$5; jr $ra; sw $2,0x0($4)` (3
  instructions, not 2) — the assigned value is also the return value:
  `MOTNO_TBL *SetActTbl(MOTNO_TBL *value) { return actData = value; }`,
  not a `void` setter.
- **Independent-field-store order is neither source order nor offset
  order**: for two-statement `void` setters writing unrelated fields
  (`CActBoyake::DispOff`, `CChara::SetPadChk`, `CActReversal::SetRevMax`),
  the compiled instruction order did not match naive source-order
  assumptions in 2 of 3 first attempts. Confirmed empirically with an
  isolated two-field probe: the statement assigning the *first-declared*
  field must be written *last* in source for it to land in the delay slot
  matching the reference; get this from source-order experiments, not
  from re-deriving GCC's scheduler.
- **A hidden pointer field can be revealed by a sibling accessor**:
  `CBgCtrl::nowBg`, `CPAppear::nodeData`, `CActTbl::actData`, and
  `CCharaBase::charCol` were all previously modeled as plain `int`/`void*`
  fields (matching their own already-verified getter's raw passthrough)
  until a *different* method in the same class dereferenced the identical
  offset, revealing it as a typed pointer
  (`CBgCtrl::GetNowBgColGrp`, `CPAppear::GetType`, `CActTbl::SetActTbl`,
  `CCharaBase::GetColHitData`). Retyping the field is safe and does not
  reopen the sibling getter's existing match, since a raw pointer-value
  passthrough compiles identically regardless of the pointer's static
  type.
- **`objVector` is 8 bytes (two floats), not the 12-byte three-float
  vector any name alone would suggest**: `CWeapon::SetTgtPos`/
  `PositionInit`/`AddOffset` take `objVector` by value with a *completely
  empty* body, compiling to a bare 16-byte prologue/epilogue with zero
  load/store instructions. A 12-byte `{float x,y,z;}` hypothesis spills
  the unused value defensively (`ldl`/`ldr`, 36 bytes); only an 8-byte
  `{float x,y;}` reproduces the reference's zero-instruction body exactly
  on all three methods.
- **R5900 `LQ`/`SQ` quadword instructions confirmed on a second,
  independent, much smaller pair**: `CCharCom::SetMovePos` and
  `FireStorm_Seed::SetPos` (both taking `objVector` by const reference,
  12-byte sections) use the identical undecoded opcode-0x1E/0x1F
  (`LQ`/`SQ`) pattern already found on CCamera's 112-byte matrix setters,
  confirming this is a systemic tooling gap (no R5900-aware disassembler
  or assembler), not something specific to large aggregates. Both left
  deferred, matching the matrix-setter precedent; no candidate added.

Two sections deferred for the already-documented isolated-probe
register-allocation limitation (`CBgCtrl::GetNowBgColGrp`,
`CPAppear::GetType`, both `return field->member;` pointer chases that
reproduce size but reuse `$3` for the intermediate where the reference
reuses `$2` throughout) — see `docs/CODE_FAILURES.md`.

Reconstruction now covers **475 sections / 3,936 bytes across ninety-five
partial classes** (no new classes; all 34 recovered sections fell in
already-partially-modeled classes); 3,441,268 bytes remain explicit raw
debt. `make test verify-boot verify-source-only verify-ee` passes (full
boot ELF and full EE-probe ELF both byte-identical).

## Second non-trivial batch — 30 sections in 16 already-known classes — 2026-09-23

Agent: Claude Sonnet 5; role: Code Department Lead. Continues into the
16-byte tier (four instructions), surveyed the same way as the previous
batch. 32 sections disassembled; 30 recovered, 2 deferred.

New evidenced shapes:

- **Arrays embedded directly in the object, not behind a loaded pointer**:
  `CRender::GetVUEntryCV`/`GetVUEntryPrim`, `CBgCtrl::GetFilter`,
  `CCharaCntrl::SetNowChara`, `CCharaDataSts::GetStatusBuf`,
  `CCharaBase::SetPartsMdlSw`, `CMotionSts::GetStatus`/`GetStatusPre`/
  `SetStatus`/`SetStatusPre`, `CGameEffect_Ctrl::GetGameEffectBase`, and
  all five `Labyrinth_ArmGet` accessors compute `this + index*4 + offset`
  directly from `$4` (never loading a pointer field first) — a
  fixed-stride array whose first element sits at a byte offset *within
  the class itself*, not a separately-allocated buffer reached through a
  pointer. Modeled as `int fieldName[1];` at that offset (a one-element
  placeholder; declared array length never affects codegen for a runtime
  index).
- **The same shape through an actual pointer field** (contrast with the
  above): `CCharaBase::GetWeaponC`/`GetWeaponPmv`/
  `SetCurrentSubWeaponPmv`, `CMotion::SetMask` first `lw` a pointer field,
  *then* apply `index*stride` to the loaded value — declared as
  `T *fieldName[1];` (array of pointers) or `T *fieldName;` plus manual
  `sizeof`-driven pointer arithmetic (`CMotion::GetPose`/`GetColorPose`,
  stride 0x40/0x20 confirmed from the `sll` shift amount, both deferred —
  see below) or embedded-struct arrays returning an element's address
  (`CGameEffect_FootStamp::GetFootPos`/`GetOldFootPos`, stride 0x10).
- **`nor $2,$zero,$2` before `sltu`/`srl` is a bitwise-NOT idiom, not a new
  operator**: `CMotion3::IsChangeMotionNo`/`IsChangeMotionNoS` compute
  `~field` (via MIPS's standard "nor with zero" NOT idiom, since MIPS has
  no dedicated NOT instruction) then boolify with `sltu`, which is exactly
  `return field != -1;` (a "changed from its -1 sentinel" check, not a
  generic `!= 0`). `CChara::IsStartActPmv` instead follows the `nor` with
  `srl $2,$2,0x1f` (extract bit 31 of `~field`), which is
  `return field >= 0;` — the sign bit of the field's complement is the
  logical negation of the field's own sign bit.
- **A field read through two different bit-manipulation idioms in the
  same class needs two different types**: `CAlpha::IsFadeInDone`/
  `IsFadeOutDone` are `(flags >> 2) & 1` / `(flags >> 3) & 1` — `srl`
  (logical shift), which only reproduces with an `unsigned int` field;
  an `int` field compiles the identical source to `sra` (arithmetic
  shift, sign-extending), a silent mismatch that only shows up as a
  wrong opcode nibble, not a size or structural difference.
- **Independent 3-statement stores follow a scheduler pattern, confirmed
  by exhaustive testing, not derivable by inspection**: for
  `CWeapon::CreateModels` and `CCharCom::SetActTbl` (3 unrelated
  pointer/int fields set from 3 params) and `CFade::SetFadeColor` (3
  unrelated bytes), naive source order (matching either param order or
  field-declaration order) did not reproduce the reference on the first
  attempt in any of the 3 cases. A controlled 6-permutation probe (all
  orderings of 3 independent pointer-field assignments) found the
  reference's two distinct target shapes (ascending-offset-first vs.
  descending-offset-first instruction order) each correspond to exactly
  one specific, non-obvious source statement order (write the *second*
  field's statement first, the *third* field's statement second, and the
  *first* field's statement last, for an ascending-offset target; a
  different single permutation for the descending-offset target) — with
  no simpler rule (declaration order, param order, or "last touches the
  delay slot" alone) explaining all 3 cases at once.
- **A pointer-plus-sign-bit dual read needs a union, not two fields**:
  `CChara::actPmv` is read as a pointer by `StartActPmv` and as a raw
  signed 32-bit value by `IsStartActPmv`'s sign-bit test at the *same*
  offset; an anonymous `union { void *actPmv; int actPmvRaw; };`
  reproduces both accessors from one field without duplicating the
  offset or touching `StartActPmv`'s existing match.

Two sections deferred, both `CMotion` (`GetPose`, `GetColorPose`): the
exact source (`return &poseArray[index];`) reproduces the reference's
size, field offset and shift amount, but schedules the independent `sll`/
`lw` pair in the opposite order and reverses the final `addu`'s operands.
Confirmed unfixable by rephrasing across 3 independently-tested source
forms (`&array[i]`, `array+i`, `i+array`) — the same isolated-probe
register-allocation/scheduling limitation already logged for CCamera's
matrix accessors and the RTTI cluster, now also confirmed for
pointer-typed array-element address computation, not just field passthroughs.

Reconstruction now covers **505 sections / 4,416 bytes across ninety-five
partial classes** (no new classes); 3,440,788 bytes remain explicit raw
debt. `make test verify-boot verify-source-only verify-ee` passes (full
boot ELF and full EE-probe ELF both byte-identical).

## Third non-trivial batch — 10 sections in 8 already-known classes, plus a size correction — 2026-09-24

Agent: Claude Sonnet 5; role: Code Department Lead. Continues into the
20-byte tier (five instructions). 18 sections disassembled; 10 recovered,
1 size correction to already-committed evidence, 7 deferred (4 for the
isolated-probe register-allocation limitation, 1 for a genuine R5900
tooling gap, 1 for `$gp`-relative addressing, 1 that needed a size
correction and is itself still deferred after the correction).

**Correction (superseding `objVector`'s original 8-byte, two-float
definition from the first non-trivial batch):** `C3dObject::SetPosition`
(`position = value;` on `const objVector &`) copies exactly two *aligned*
8-byte doublewords (`ld`/`sd`, not the defensive `ldl`/`ldr`/`sdl`/`sdr` an
unaligned or wrong-size guess produces) — only a 16-byte, 8-byte-aligned
`objVector` reproduces this. The original 8-byte conclusion was never
actually disambiguated by its supporting evidence: a 16-byte aligned
`objVector` was tested and found to *also* reproduce the exact same
trivial empty body for `CWeapon::SetTgtPos`/`PositionInit`/`AddOffset`
byte-for-byte, meaning that evidence was compatible with either size all
along. `objVector` is now `{ float x, y, z, w; }`, `aligned(8)`; all three
previously-verified `CWeapon` sections were re-verified unaffected by the
type change (a by-value empty-body parameter's codegen doesn't depend on
the unused type's exact layout, only compatible sizes). `SetPosition`
itself is deferred despite the corrected type: it now matches the
reference's exact size and instruction sequence, but reuses register `$3`
for the second `ld`/`sd` pair where the reference reuses `$2` throughout —
the by-now-familiar isolated-probe scheduling limitation, confirmed even
with the full real header providing context.

Two more corrections to already-verified evidence, confirmed safe by full
gate re-runs before and after:

- **`MotionNo` needs a real member.** `CMotionC::SetMotionOnly(MotionNo,
  int)` stores the `MotionNo` parameter's register into a field
  (`sw $5, 0xbc($4)`); a fully empty class (sizeof 1, no state) generates
  *no store at all* for a by-value copy, so the original `class MotionNo
  {};` could never have reproduced this. Given `int value;`, the
  assignment compiles to the expected store. `CWeapon::SetSubMotion`'s
  existing empty-bodied use of `MotionNo` is unaffected, since that body
  never touches the parameter regardless of its layout.
- **`CMotion::mask` needs a signed element type.** `CMotion::GetMask`
  boolifies `mask[index]` via a signed `lb`, not `lbu`; the field was
  `unsigned char *` from the previous batch (matching `SetMask`, whose
  `sb` store doesn't care about signedness either way). Retyped to
  `char *`; `SetMask`'s existing section re-verified unaffected.

New evidenced shapes:

- **A four-independent-statement setter generalizes the three-statement
  scheduler rule found last batch**: `CActFilter::SetXYWH` and
  `CWeapon::SetWeaponType` (4 unrelated fields from 4 params) both want
  natural ascending-offset compiled order. An exhaustive-style probe (6
  permutations of 4 independent assignments) found the same "rotate
  declaration order left by one" rule already established for 3
  statements generalizes directly: source order (2nd; 3rd; 4th; 1st field)
  produces the ascending target, just as (2nd; 3rd; 1st) did for 3
  fields — a real, reusable pattern now confirmed at two different
  statement counts.
- **Array of structs reached through a loaded pointer, not embedded**:
  `CSubObject::GetVertexNum`/`GetVertex`/`GetNormal`/`GetBoneNum` all load
  a pointer field at a fixed offset, then index it with a 0x20-byte
  stride — a `SubObjectElement` array (name only, no other members
  evidenced) living behind `CSubObject::elements`, distinct from the
  in-object-embedded arrays found last batch.
- **Null-safe linked-list traversal reading a caller-supplied node's own
  field, not `this`'s**: `CObjList::GetNextObject`/`GetPrevObject` are
  `return object ? object->next : 0;` / `return object ? object->prev :
  0;` — a `beqz`+delay-slot-`move`(`daddu $2,$0,$0`, the established
  move-vs-daddu precedent) ternary reading the *parameter's* linked-list
  pointer, requiring a real `CObj { CObj *prev; CObj *next; };` rather
  than the opaque forward declaration the mangled parameter type alone
  would need. First branching (`beqz`) stanza in `asm/camera_accessors.s`;
  used a GNU-as numeric local label (`1f`/`1:`) since no prior stanza
  needed an intra-section branch target.

Deferred: `CSubObject::GetBoneList` and `CMotion::GetMask` (both the
established register-allocation limitation, same as `GetPose`/
`GetColorPose` last batch); `C3dObject::SetPosition` (register-allocation
limitation, see correction above); `CMCard2::GetSaveData` (uses a genuine
undecoded R5900-specific three-operand `MULT rd,rs,rt` variant that
writes a GPR directly, beyond standard MIPS `MULT`'s LO/HI-only semantics
— llvm-objdump-21 renders it `<unknown>`; a new, distinct R5900 tooling
gap from the already-documented `LQ`/`SQ` one); `ArmEffectBase::SetAirFlag`
(indexes a `$gp`-relative table using `this` itself as the index, the
same "don't force a whole-program static layout" deferral already
established, with the added twist of the pointer being scaled instead of
an ordinary integer index); `FireStorm_Ptcl::SetPos` (a partial `objVector`
field copy, `posX = value.x; posZ = value.z;`, skipping the middle field —
matches size but hits the same FP-register-allocation limitation, `$f1`
vs. reference's `$f0` reused, on the second `lwc1`/`swc1` pair).

Reconstruction now covers **515 sections / 4,616 bytes across ninety-five
partial classes** (no new classes); 3,440,588 bytes remain explicit raw
debt. `make test verify-boot verify-source-only verify-ee` passes (full
boot ELF and full EE-probe ELF both byte-identical).
