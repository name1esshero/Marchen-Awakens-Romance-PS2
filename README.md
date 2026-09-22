# MARPS2 decompilation

Read [the standards](docs/STANDARDS.md) and
[agent environment](docs/AGENT_ENVIRONMENT.md) before working here.
Read [current status](docs/STATUS.md), [the work queue](docs/WORK_QUEUE.md), and
[the reconstruction methodology](docs/TASK_BOOT_RECONSTRUCTION_METHODOLOGY.md).
Initial evidence remains in [bootstrap notes](docs/tasks/BOOTSTRAP.md).

The disc boots `SLPM_661.56`, an ELF32 little-endian MIPS executable
with R5900 flags and retained C++ section names. Its complete boot ELF now
rebuilds byte-for-byte from repository artifacts. This is a bootstrap
reconstruction, not a complete decompilation or a rebuilt disc.

## Reproduce

Requires Python 3.12+, GNU Make, sha256sum, cmp and Clang/LLVM (tested: 21.1.8).
The normal build does not require the ISO:

```sh
make build-boot       # builds build/SLPM_661.56 from preserved text and assembly
make test            # parser/reconstruction/tool tests and candidate syntax checks
make verify-source-only  # isolated rebuild without reference files or cached objects
```

To compare directly with the original, place `baserom.iso` at the repository root:

```sh
make inventory       # validates image hash; inventories and explicitly extracts small files
make verify-boot     # authenticates extracted ELF, then compares the entire rebuilt file
```

For the historical compiler experiment (requires a Linux i386-compatible host):

```sh
make setup-ee        # downloads the hash-pinned research compiler; no system install
make verify-ee       # compiles 8 C++ accessor candidates and compares the full probe ELF
```

The wrapper stages old tools and source on a native temporary filesystem to avoid
their failures on this Windows-mounted workspace. See [compiler evidence and
limitations](docs/tasks/COMPILER_PROBE.md).

`asm/` preserves nineteen accessors across three classes (`CCamera`, `CCamera2`,
`CCameraMv`) as instructions. `candidates/` contains semantic models and a
byte-matching EE C++ probe; the complete classes remain unrecovered.
`preserved/boot/` explicitly retains 3,445,052 unrecovered bytes as hexadecimal
text, with the other 152 bytes supplied by the built object. A census of the
1,694-section, 71,932-byte named `.gnu.linkonce.t.*` cluster these accessors
belong to is in `reports/linkonce_text_inventory.json`; see
[the linkonce cluster task](docs/tasks/LINKONCE_CLUSTER.md). `reports/` contains inventories;
`config/` pins the observed reference hashes and comparison selection.
Extracted reference files, downloaded tools and build outputs are ignored.
The normal build reads no reference bytes. Comparison deliberately reads the reference executable.

The boot ELF equality and isolated build gates pass. Full-disc reconstruction,
authentic source/class recovery, original game compiler identification and archive
recovery remain outstanding. Hashes identify this supplied image; independent
retail-dump provenance has not been established.

New commits require the variable attribution/evidence footers in
[STANDARDS.md §17](docs/STANDARDS.md#17-commit-attribution-and-evidence-footers).
