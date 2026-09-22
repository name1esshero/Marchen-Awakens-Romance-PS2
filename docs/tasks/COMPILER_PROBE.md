# EE compiler investigation and full ELF baseline — 2026-09-22

Authority: [STANDARDS.md](../STANDARDS.md).
Agent: GPT-6 Astra Light (operator-provided label); role: Initial Manager.
Work type: R&D, Bootstrap. Current state: [STATUS.md](../STATUS.md).
Follow-up: [linkonce cluster census and broadened match](LINKONCE_CLUSTER.md).

## Direct evidence

The boot ELF contains eight literal `Append: GCC2096 SCE3020` strings in `.rodata`.
Their file offsets are `0x305c9a`, `0x307695`, `0x308474`, `0x3084c5`, `0x30852d`,
`0x3085d5`, `0x308dd9`, `0x309a5d`. The preceding strings identify MWSFD, CRI SFD,
CRI CFT, CRI MPS, CRI MPV, CRI M2V, ADXT and CRI CFG library builds dated
September 3, 2004. The reproducible report is `reports/compiler_evidence.json`:

```sh
python3 tools/compiler_evidence.py 'extracted/SLPM_661.56;1' > reports/compiler_evidence.json
```

**Observed:** library build labels and GNU-style C++ method names exist.
**Candidate pathway:** evaluate an EE GCC 2.96 compiler.
**Not established:** that the game or every linked object used this compiler,
that `SCE3020` identifies the game's SDK, or that optimization flags are known.

## Tool provenance and experiment

Retrieved the compiler distribution from
[decomp.me's compiler repository](https://github.com/decompme/compilers), using its
[EE GCC 2.96 release asset](https://github.com/decompme/compilers/releases/download/compilers/ee-gcc2.96.tar.xz).
Archive size: 2,754,768 bytes. SHA-256:
`0590d2ca9da8f5903889d66761220d14b47a8d14ba987ca53db84a1650a1fd0a`.
This hash pins the downloaded distribution; it is not vendor attestation.
The tools report `gcc version 2.96-ee-001003-1` and
`GNU assembler 2.10-ee-001003-1`. The host binaries are Linux i386 executables.

The [GCC project's note on 2.96](https://gcc.gnu.org/gcc-2.96.html) cautions that
2.96 was a development designation, not an official release. Record the full
EE tool version and archive hash; the number alone cannot identify a toolchain.

`candidates/ee_camera/CCamera.h` expresses the eight accessors as natural inline
methods over an explicitly partial layout. A separate probe takes their addresses
to require out-of-line definitions. The pointers are harness data, not claimed game
data, and are excluded from both selected comparisons and reconstructed output.

One common experimental optimization setting (`-O2`) was used. There are no
register assignments, codegen attributes, inline assembly, literal instructions,
or per-function compiler settings in this C++ probe. Method section names, calling
sequences and all 64 instruction bytes match the original.

**Limit:** these trivial methods do not discriminate compiler versions or establish
complete original declarations. Unknown class bytes, inheritance and object size
remain unresolved. The normal build continues to use preserved assembly.

## Investigated failures

1. Unreferenced inline methods produced no method sections, even with
   `-fkeep-inline-functions`. Section comparison failed because the selected name
   was absent. Explicit address-taking in the harness made the definitions required;
   the final experiment uses only `-O2`, without that unsuccessful extra flag.
2. Installing/running the old tools directly on the Windows-mounted workspace
   failed with `cannot exec cc1plus`. An absolute driver path and `-B` paths did not
   fix it. Executing the compiler from `/tmp` but reading source from this workspace
   instead produced `Value too large for defined data type` and a legacy compiler
   internal error. The local compiler inode was `1970324837575679`, while the
   temporary copy's inode was `64731`. This is strong evidence of legacy file-metadata
   limits; no syscall trace was captured, so the exact failing stat call is unproven.
   Staging both tools and source in native temporary storage fixed the real probe
   without changing source bytes or target flags.

## Full reconstruction baseline

`preserved/boot/layout.json` partitions all 3,445,204 original file bytes into
ten contiguous intervals: eight required object sections (64 bytes) and two explicit
unrecovered hex intervals (3,445,140 bytes). These preserve ELF headers/section
tables, code/data, overlay metadata and gaps. They are not high-level recovery.
The original selected instruction bytes are absent from the raw intervals.

The normal build consumes only preserved text plus an independently assembled
object. An optional build consumes the EE C++ probe object instead. Both reproduce
the entire original ELF; neither output is produced by copying or patching a
reference executable at build time. The builder has no reference input in build mode.

Tests reject gaps/overlaps, size changes, duplicate/missing sections and unapplied
relocations, and prove a changed object instruction propagates into output.
GNU `cmp` independently compares complete output files with the authenticated
reference. The isolated build uses no ISO, extracted files, reports or old objects.

## Verification and next decisions

- `make test`: **PASS**, 20 parser/comparison/reconstruction/installer/staging tests
  plus host C++ syntax/layout checks.
- `make verify-boot`: **PASS**, assembly section match and complete ELF `cmp`.
- `make verify-source-only`: **PASS**, isolated rebuild equals the pinned boot hash.
- `make verify-ee`: **PASS**, compiled method section match and complete probe ELF `cmp`.
- Fresh temporary export: **PASS**, generated layout and both raw intervals equal
  the checked-in source artifacts byte-for-byte.
- No full-disc rebuild/comparison or emulator/gameplay test was performed.

Next investigate nontrivial named methods and CCamera constructors/callers to
discriminate ABI/compiler hypotheses and justify class structure. Preserve assembly
until authentic recovery has stronger evidence than eight trivial local matches.
Track remaining work in [WORK_QUEUE.md](../WORK_QUEUE.md).
