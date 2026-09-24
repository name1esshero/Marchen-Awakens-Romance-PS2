# `__tf*` RTTI linkonce cluster — byte structure and inheritance evidence (DQ-07)

Authority: [standards](../STANDARDS.md). Contributor: Claude Sonnet 5, code
department lead. Parent-Agent: none (lead work).
State: read-only research; no `__tf*` section added to
`config/camera_sections.txt` or `preserved/boot/`; no vtable layout or object
size claimed for any class.

## Scope and method

The boot ELF's `.gnu.linkonce.t.*` cluster contains 498 `__tf*`-named
sections (the census in `reports/linkonce_text_inventory.json` had estimated
497; the exact count from a fresh section-table scan is 498, including one
template instantiation, `__tft12CStringStack1i_256_`, which the existing
naming-shape classifier in `tools/linkonce_inventory.py` correctly leaves
`unparsed` rather than misattributing). `__tf<len><Name>` is GNU v2/cfront-era
g++'s per-class RTTI "type-info accessor": a small function, emitted once per
polymorphic class wherever it is referenced, that lazily constructs and
returns a pointer to that class's runtime type-info object.

`tools/typeinfo_hierarchy.py` (new; tested in
`tests/test_typeinfo_hierarchy.py`) disassembles nothing — it decodes the
standard MIPS `jal` instruction directly from each `__tf*` section's own
bytes (opcode 6, 26-bit word-aligned target, top 4 bits taken from the delay
slot's own address) and checks whether any call target address falls inside
another `__tf*` section. This is the same encoding used throughout this
project's other MIPS evidence; the decoder is cross-checked against
`llvm-objdump-21`'s independent disassembly of all 498 sections (938 `jal`
instructions, zero mismatches) before being relied on. Run it with:

```sh
python3 tools/typeinfo_hierarchy.py 'extracted/SLPM_661.56;1'
```

The full structured output is saved at `reports/typeinfo_hierarchy.json`.

## Byte-size histogram and the two/three code shapes

| Size (bytes) | Count | Shared helper called |
| --- | --- | --- |
| 52 | 56 | `0x32c1f8` |
| 64 | 2 | `0x32c1f8` |
| 80 | 14 | `0x32c1d8` |
| 84 | 182 | `0x32c1d8` |
| 88 | 243 | `0x32c1d8` |
| 92 | 1 | `0x32c1b0` |

Every section fits exactly one of three shapes, distinguished by which
shared, non-`__tf*` helper address it calls (not by its class's actual name
or apparent complexity):

1. **Root shape** (58 sections, sizes 52/64): guard-check, then on first call
   only, one `jal` to `0x32c1f8` passing the class's name-string pointer.
   No call to any other `__tf*` section. Example
   (`.gnu.linkonce.t.__tf6CBgCol`):
   ```text
   addiu $sp, $sp, -0x10
   sd    $ra, 0x0($sp)
   addiu $4, $gp, -0x3f28      ; this class's own guard/type-info slot
   lw    $2, 0x0($4)
   bnez  $2, +0x24
   nop
   lui   $5, 0x41
   jal   0x32c1f8              ; shared "root" registration helper
   addiu $5, $5, 0x1480        ; $5 = name-string pointer
   addiu $2, $gp, -0x3f28
   ld    $ra, 0x0($sp)
   jr    $ra
   addiu $sp, $sp, 0x10
   ```
2. **Single-base shape** (439 sections, sizes 80/84/88): guard-check, then on
   first call, a `jal` directly to another class's own `__tf*` function
   (ensuring that class's guard runs first), then a `jal` to `0x32c1d8` with
   three arguments: this class's guard address, its name-string pointer, and
   the other class's guard address. Example (`.gnu.linkonce.t.__tf7CCamera`
   at `0x33af4c`, first call `jal 0x33b744` = `.gnu.linkonce.t.__tf9C3dObject`).
3. **One outlier** (`.gnu.linkonce.t.__tf9CPrimList`, 92 bytes): the same
   single-base shape, but the shared helper is `0x32c1b0` and receives a
   fourth argument, a literal `1` (`addiu $7, $zero, 0x1`), after first
   calling `.gnu.linkonce.t.__tf5CPrim`'s own `__tf` function. Single
   occurrence in the whole cluster; consistent with (but not confirmed as) a
   distinct registration path for a virtual base, since the historical
   libg++ RTTI runtime is known to use extra flag arguments for that case.
   Left explicitly open pending a second example.

**Size does not indicate base-class count beyond this coarse three-way
split.** All of 80/84/88 call the identical `0x32c1d8` helper in the
identical shape; disassembling one of each (`__tf8bad_cast` at 80,
`__tf7CCamera` at 84, `__tf8CCamera2` at 88) shows the only difference is how
many separate `lui` instructions the guard/name/base-guard address
computations need, which depends on whether consecutive absolute addresses
happen to share the same upper 16 bits — an address-layout coincidence, not
a structural difference. The same coincidence-driven variance shows up even
between two root-shape (52-vs-64-byte) sections that are the identical
C++ shape: `__tf9type_info` (a compiler-runtime class, see below) spills an
extra callee-saved register that `__tf6CBgCol` does not, for no reason
traceable to the class itself. Register-allocation/instruction-count
variance between originally co-compiled sections of the identical shape is
therefore a real, general property of this cluster, not just a probe-vs-full-
binary artifact (see `docs/CODE_FAILURES.md`).

## Base-class relationship evidence (440 edges)

For the 439 single-base-shape sections (plus the one 92-byte outlier), the
`__tf*` function called before the shared registration helper **is** that
class's own registration function. Interpreting that call as "this class was
compiled with a runtime type-info reference to that other class" follows
directly from the shared helper's own observed argument shape (this guard,
this name, *other class's guard*) — the same kind of operand-level
disassembly reasoning already used throughout this project's recovered
accessors, not a name-similarity guess. It is deliberately not phrased as a
complete inheritance graph: a class can have more base classes than are
type-info-tracked this way (e.g. a non-polymorphic base contributes no
`__tf*` call), and this only ever shows a single call per section (no
multiple-inheritance shape with two `__tf*` calls was observed anywhere in
the cluster).

Two directly confirmed examples used as spot checks:

- `CCamera` calls `C3dObject`'s `__tf` function before registering itself.
- `CCamera2` calls `CCamera`'s `__tf` function before registering itself —
  consistent with the existing partial layouts in `candidates/ee_camera/CCamera.h`
  and the class family documented in `docs/tasks/LINKONCE_CLUSTER.md`.

The full 440-edge table is in `reports/typeinfo_hierarchy.json` (`edges`
array: `class_name`, `base_class`, `size`). 89 distinct classes serve as a
base for at least one other class; the highest-fanout examples are
`MenuFrameSimpleUI` (111), `CScriptTask` (42), `CEasyMenu` (29),
`ActionObject` (26), `CGameEffect_Base` (18), `CCharCom` (15), `CMcFunc`
(11), `AttackEffect` (8), and `type_info` itself (8) — the last confirming
the standard-library RTTI classes described below are genuinely linked into
this cluster, not an artifact of the classifier.

## The root-shape cluster includes GCC 2.96's own RTTI runtime, not just game classes

Several root- and single-base-shape sections are the compiler's own
pre-standard `libstdc++`/`libg++` RTTI support classes, not game code:
`type_info`, `exception`, `bad_exception`, `bad_cast`, `bad_typeid`,
`__user_type_info`, `__si_type_info`, `__class_type_info`,
`__pointer_type_info`, `__attr_type_info`, `__builtin_type_info`,
`__func_type_info`, `__ptmf_type_info`, `__ptmd_type_info`, and
`__array_type_info` all appear as `__tf*` sections with matching
constructor/destructor linkonce sections alongside them, and their observed
single-base chain (e.g. `__si_type_info` -> `__user_type_info`) matches the
well-known GCC 2.x RTTI class hierarchy. This means the shared helper
addresses (`0x32c138`, `0x32c170`, `0x32c1b0`, `0x32c1d8`, `0x32c1f8`) most
likely belong to that same statically-linked compiler runtime library rather
than to game logic — a potentially independently reproducible chunk of the
"raw hex" boot region if the pinned EE GCC's own bundled runtime object
files can be obtained, which this task did not attempt (out of scope for a
read-only characterization pass; recorded as a discovered task, see below).

## Natural-candidate reproduction (structural, not byte-exact)

Per this card's deliverable, an unmodified `class CBgCol { public: virtual
~CBgCol() {}; };` was compiled with the pinned, unmodified EE GCC
`2.96-ee-001003-1` `-O2` probe harness (`tools/run_ee_probe.py`) in a
throwaway location outside `candidates/`, never added to any gate. It
produces a `.gnu.linkonce.t.__tf6CBgCol` section with the exact same
root-shape structure (guard-check, conditional one-argument call to the
shared registration helper, return the guard address) confirming the
hypothesis that this shape is tied to the class being polymorphic. The byte
count differs (60 vs. the reference's 52) for the same
register-allocation-context reason documented above and in
`docs/CODE_FAILURES.md`; this is a structural match, not a byte match, and
is not filed as a candidate under `candidates/` since there is no full class
recovery attached to it (unlike `ee_view_rect`/`ee_camera_matrix`, which
pair a mismatch with a specific class's real evidenced layout).

## What this does not establish

- Not a complete inheritance graph: only single-base, type-info-visible
  relationships are captured; non-polymorphic bases and any true
  multiple-inheritance shape (none observed) would not appear here.
- Not vtable layout, virtual function count/order, or object size for any
  class — no such claim is made or needed by this evidence.
- The `CPrimList` outlier's fourth argument is not confirmed to mean
  "virtual base"; it is recorded as an open, single-instance shape.
- The shared helper addresses are not verified against the pinned compiler's
  own runtime library objects in this pass (see discovered follow-up below).

## Discovered follow-up (bounded, independent, queued separately)

Identifying and attempting to reproduce the five shared helper functions
(`0x32c138`, `0x32c170`, `0x32c1b0`, `0x32c1d8`, `0x32c1f8`) from the pinned
EE GCC `2.96-ee-001003-1`'s own bundled runtime library objects is a
separate, bounded task, queued as DQ-18 in `docs/WORK_QUEUE.md` for any
worker in the code pool (including a future run of this same lead).
