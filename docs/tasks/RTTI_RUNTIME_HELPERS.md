# The `__tf*` cluster's shared RTTI helper functions (DQ-18)

Authority: [standards](../STANDARDS.md). Contributor: Claude Sonnet 5, code
department lead. Parent-Agent: none (lead work).
State: read-only research; no section at any address in this document was
added to `config/camera_sections.txt` or `preserved/boot/`.

## What the three confirmed helpers actually do

Disassembling `0x32c1b0`–`0x32c20c` directly (`llvm-objdump-21
--start-address=0x32c100 --stop-address=0x32c220
'extracted/SLPM_661.56;1'`) shows all three `__tf*`-registration helpers
identified in [`TYPEINFO_SECTIONS.md`](TYPEINFO_SECTIONS.md) are tiny,
guard-free field-initializers, not general-purpose registration routines:

```text
0x32c1f8 (root, 1 arg: $4=object, $5=name):
    beqz $4, +0x14
    lui  $2, 0x3e
    sw   $5, 0x0($4)       ; object.name = name
    addiu $2, $2, 0x7020   ; $2 = &vtable for __user_type_info
    sw   $2, 0x4($4)       ; object.vtable = $2
    jr   $ra

0x32c1d8 (single-base, 3 args: $4=object, $5=name, $6=base):
    beqz $4, +0x14
    lui  $2, 0x3e
    sw   $6, 0x8($4)       ; object.base = base
    addiu $2, $2, 0x6ff0   ; $2 = &vtable for __si_type_info
    sw   $5, 0x0($4)
    sw   $2, 0x4($4)
    jr   $ra

0x32c1b0 (CPrimList's outlier, 4 args: $4=object, $5=name, $6=base, $7=flag):
    beqz $4, +0x1c
    lui  $2, 0x3e
    sw   $7, 0xc($4)       ; object.attr = flag
    addiu $2, $2, 0x6fc0   ; $2 = &vtable for __class_type_info
    sw   $5, 0x0($4)
    sw   $2, 0x4($4)
    sw   $6, 0x8($4)
    jr   $ra
```

Each writes exactly a `{name, vtable, [base], [attr]}` object and returns —
these are field-initializer bodies for three different, differently-sized
compiler-runtime classes, not one generic "registration" routine reused
three ways. The three vtable-pointer constants resolve to three real,
independently-named linkonce data sections in the same boot ELF:

| Helper | Target vtable section | Object size |
| --- | --- | --- |
| `0x32c1f8` | `.gnu.linkonce.d._vt$16__user_type_info` | 8 bytes (`name`, `vtable`) |
| `0x32c1d8` | `.gnu.linkonce.d._vt$14__si_type_info` | 12 bytes (+ `base`) |
| `0x32c1b0` | `.gnu.linkonce.d._vt$17__class_type_info` | 16 bytes (+ `base`, `attr`) |

This resolves the "root vs. single-base vs. outlier" split from
`TYPEINFO_SECTIONS.md` to concrete, named GCC 2.x runtime classes:
`__user_type_info` (no base tracked — the plain/root case), `__si_type_info`
("single inheritance type info" — exactly one public, non-virtual base,
matching every non-outlier single-base `__tf*` section), and
`__class_type_info` (the general case). `__class_type_info`'s own
constructor, visible in the surrounding linkonce cluster as
`.gnu.linkonce.t.__17__class_type_infoPCcPCQ217__class_type_info9base_infoUi`
(`__class_type_info(const char*, const base_info*, unsigned int)`), takes an
*array* of `base_info` entries plus a count — general multiple inheritance.
`CPrimList`'s `__tf` function instead directly pokes a single `base`/`attr`
pair inline (the same "skip the general constructor, write fields directly"
pattern the other two helpers use), consistent with `CPrimList` having
exactly one base that is not the *simple* public/non-virtual case
`__si_type_info` covers — most plausibly `class CPrimList : virtual public
CPrim` (virtual inheritance), though this is not independently confirmed
without a second `__class_type_info`-shaped example to compare `attr`
values against, and no such second example exists in this cluster.

## Two related, separately-observed addresses

`0x32c170` and `0x32c138` (noted as unverified in `TYPEINFO_SECTIONS.md`)
were also disassembled directly:

- **`0x32c170`** is `bool type_info::operator==(const type_info&) const`
  reconstructed in full: return `true` immediately if the two `type_info`
  pointers (`$4`, `$5`) are identical; otherwise load each object's `name`
  field (offset 0) and call `jal 0x330e74` (a `strcmp`-shaped two-pointer
  call), returning `true` only if the names compare equal. This is the
  well-documented GCC RTTI technique for tolerating duplicate `type_info`
  instances across translation/shared-object boundaries by falling back to
  name comparison — genuinely useful, confirmed evidence about this
  binary's RTTI implementation, but unrelated to the `__tf*` registration
  shape itself (it is `type_info`'s comparison operator, called from
  `.gnu.linkonce.t.__ne__C9type_infoRC9type_info`).
- **`0x32c138`** sets a vtable pointer at offset 4 of an object when a low
  flag bit is set, then tail-calls (`j`, not `jal`) `0x32d0c8`. The fourth
  constant it writes (`&vtable + 0x7090`) resolves the same way as the
  three above: it is the exact load address of
  `.gnu.linkonce.d._vt$9type_info` — `type_info`'s own vtable, `type_info`
  being `__user_type_info`'s base per the constructor-chain evidence in
  `TYPEINFO_SECTIONS.md`. The flag-bit gate and tail call match the classic
  pre-standard G++ "deleting vs. non-deleting destructor" (`D0`/`D1`)
  dispatch shape: called from destructor sections such as
  `.gnu.linkonce.t._$_16__user_type_info`, this re-stamps the object's
  vtable pointer back to its base class `type_info` (standard C++ behavior
  during destructor unwinding, where the dynamic type steps up the
  hierarchy as each derived destructor body finishes) before tail-calling a
  shared deallocation routine at `0x32d0c8`. The vtable identification is
  confirmed the same way as the other three; the specific claim that
  `0x32d0c8` is a deallocation routine is not independently confirmed here.

## Byte-reproducibility: not achievable with this repository's current toolchain

DQ-18 asked whether the pinned EE GCC `2.96-ee-001003-1` distribution ships
matching runtime object/archive files these helpers could be
byte-compared against. It does not:

```sh
find .tools -iname '*.a' -o -iname '*.o'
```

returns nothing under the pinned compiler's ~18 MB installation — it is a
compiler front end/codegen only, with no bundled `libstdc++`/`libio`
archive. There is therefore no source or object file in this project's
possession to compile or link against for a byte-exact comparison of
`0x32c138`/`0x32c170`/`0x32c1b0`/`0x32c1d8`/`0x32c1f8`; they can currently
only be studied via disassembly of the already-linked reference binary, as
done above. This is recorded so a future worker does not re-attempt sourcing
a bundled runtime archive that is not present.

## What this does not establish

- Not a claim that `CPrimList` uses virtual inheritance — only that its
  `__class_type_info`-shaped registration is consistent with a non-simple
  single base, with virtual inheritance as the most plausible (not sole)
  explanation.
- Not a full reconstruction of `__user_type_info`/`__si_type_info`/
  `__class_type_info`'s own member layout beyond the fields these three
  helpers write; their constructors, destructors, and other members
  (already present as separate linkonce sections) were not analyzed here.
- `0x32c138`'s destructor-dispatch reading is a plausible interpretation of
  the shape (flag-gated vtable restamp + tail call), not confirmed against
  a second independent example; only the vtable identification itself
  (`0x3e7090` = `.gnu.linkonce.d._vt$9type_info`) is on the same firm footing
  as the other three.

## Reproduction

```sh
llvm-objdump-21 -d --start-address=0x32c100 --stop-address=0x32c220 \
  'extracted/SLPM_661.56;1'
python3 -c "
import sys; sys.path.insert(0, 'tools')
from bootstrap import elf_sections
data = open('extracted/SLPM_661.56;1', 'rb').read()
for s in elf_sections(data)['sections']:
    if s['address'] in (0x3e7020, 0x3e6ff0, 0x3e6fc0):
        print(s['name'], hex(s['address']), s['size'])
"
find .tools -iname '*.a' -o -iname '*.o'
```
