# Initial investigation — 2026-09-22

Historical initial snapshot. Current state: [STATUS.md](../STATUS.md).
Follow-up: [compiler probe and full ELF baseline](COMPILER_PROBE.md), then
[linkonce cluster census and broadened match](LINKONCE_CLUSTER.md).

Governed by [STANDARDS.md](../STANDARDS.md) and
[AGENT_ENVIRONMENT.md](../AGENT_ENVIRONMENT.md).

## Observed reference

- Input: user-supplied `baserom.iso`, 4,587,749,376 bytes.
- SHA-256: `cc059a3acf818dfbd0a782a9d20ee67e020d167866cd1c4dca77e6eb9224e3ec`.
- The ISO primary volume descriptor says `PLAYSTATION`; its declared volume
  size equals the file size. Volume label is blank.
- Root `SYSTEM.CNF;1` at LBA 310 (57 bytes) says
  `BOOT2 = cdrom0:\SLPM_661.56;1`, `VER = 1.02`, `VMODE = NTSC`.
- Boot executable: LBA 311, 3,445,204 bytes, SHA-256
  `9f562361510b2d82bc99bbc02306f63efc3c61d2ae3d1c484401eb60a46af672`.
- ELF32 little-endian, machine 8 (MIPS), entry `0x00100008`, flags
  `0x20924001`. GNU readelf decodes flags as `noreorder, 5900, eabi64, mips3`.
  These are header observations, not a complete ABI determination.
- 2,251 section headers; no SHT_SYMTAB. Names survive in section strings,
  including GNU linkonce C++ methods, type information and virtual tables.
  Main-ELF sections flagged executable total 2,445,484 bytes. This does not
  measure all disc code or establish every byte in those sections as instructions.
- Inventory: 41 files and one directory. Fourteen module files begin with ELF
  magic; `IOPRP300.IMG;1` still needs internal inventory.
- `MOVIE.AFS;1`, `BGM.AFS;1`, `_DATA.YFS;1` and twenty `DMY` files remain
  unclassified internally. Names alone do not prove format or padding content.

Full per-file extents and small-file hashes: `reports/disc.json`.
Section addresses, offsets, sizes and hashes: `reports/*.elf.json`.
Large files are not separately hashed; the full-image hash covers them.
This pins the supplied input, not independently authenticated retail provenance.

## First recovered operations

Eight named sections at `0x0033afa0` through `0x0033afdf` correspond to camera
accessors. File offsets are `0x23bfa0` through `0x23bfdf`. Each contains
`jr $ra` followed by a load/store in its branch delay slot.

| Method | Offset from object in `$4` | Operation |
| --- | --- | --- |
| GetNearClipPlane | 0x16c | `lwc1 $f0` |
| GetFarClipPlane | 0x170 | `lwc1 $f0` |
| SetFogMode | 0x184 | `sw $5` |
| GetFogMode | 0x184 | `lw $2` |
| SetFogDistance | 0x188 | `swc1 $f12` |
| GetFogDistance | 0x188 | `lwc1 $f0` |
| SetFogConcentration | 0x18c | `swc1 $f12` |
| GetFogConcentration | 0x18c | `lwc1 $f0` |

Names are verbatim evidence from `.gnu.linkonce.t.*`, not newly invented names.
The `i`/`f` name suffixes and instructions support int/float accessor semantics.
The candidate uses a partial layout with explicitly unknown bytes. It does not
claim the original inheritance, virtual dispatch, class size, const qualifiers,
or exact source spelling. At initial bootstrap no target compilation had been
run. The follow-up EE probe now matches these operations; the original game
compiler and complete class/ABI remain unresolved.

`asm/camera_accessors.s` is a lower-level preservation, not high-level recovery.
Clang 21.1.8 with `-target mipsel-none-elf -march=mips3 -mabi=32` reproduces
these eight instruction sequences. This narrow assembler choice does **not**
establish a project compiler/ABI or support for arbitrary R5900 instructions.
The selected sections contain no relocations; whole-object metadata is not matched.

## Verification

- Full input SHA-256 computed; declared ISO extents and dual-endian fields checked.
- Eighteen explicitly extracted small files compare byte-for-byte with their
  recorded ISO extents in a separate direct seek/read comparison.
- GNU readelf independently inspected main ELF headers; LLVM objdump independently
  decoded all eight accessor sequences.
- `make test`: seven tests pass; malformed extents, unsafe paths, directory cycles,
  multi-extent flags, endian disagreement, truncation and byte mismatches covered.
  C++ syntax and field-offset assertions pass on host Clang.
- `make verify-camera`: eight sections / 64 bytes match exactly after assembly
  from text. The extracted ELF hash is checked before comparison.
- At this initial checkpoint no complete ELF/disc build existed. The follow-up
  added full boot ELF reconstruction/comparison; disc/gameplay checks remain open.
- At initial bootstrap `.git` was empty and read-only. The owner subsequently
  initialized Git in `8d5068a` and authorized commits with attribution trailers.

## Work queue and blockers

This was the initial queue; [WORK_QUEUE.md](../WORK_QUEUE.md) is authoritative
for current task state. Item 2 now has a verified bootstrap implementation.

1. Establish original compiler family/version and flags from broader code and
   executable evidence. GNU-style C++ names suggest an older GNU toolchain;
   exact compiler version is still a hypothesis, not established fact.
2. Build explicit lossless ELF reconstruction from project-owned source artifacts,
   preserving headers, gaps and unknown regions. Add independent full ELF comparison.
   Keep raw regions visibly classified as debt. Do not copy reference bytes at build time.
3. Recover authentic CCamera declarations and ABI, then compile natural methods;
   only promote candidates after source authenticity and binary gates pass.
4. Inventory archive and IOP image internals; identify executable/overlay members.
5. Establish lossless full-disc reconstruction including system area, directories,
   file gaps, alignment and trailing bytes; extraction alone is insufficient.
6. Expand recovery into the main `.text` using callers and evidenced boundaries.

No decompilation completion percentage is assigned.
