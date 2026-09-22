# MARPS2 decompilation

Read [the standards](docs/STANDARDS.md) and
[agent environment](docs/AGENT_ENVIRONMENT.md) before working here.
Current evidence and the work queue are in [bootstrap notes](docs/tasks/BOOTSTRAP.md).
Follow [the bootstrap methodology](docs/TASK_BOOTSTRAP_METHODOLOGY.md).

The disc boots `SLPM_661.56`, an ELF32 little-endian MIPS executable
with R5900 flags and retained C++ section names. This is an initial investigation,
not a complete decompilation or a buildable game.

## Reproduce

Requires Python 3.11+, GNU Make, sha256sum and Clang/LLVM (tested: 21.1.8).
Place a `baserom.iso` at the repository root, then run:

```sh
make inventory       # validates image hash; inventories and explicitly extracts small files
make test            # synthetic parser/comparison tests and candidate syntax/layout checks
make verify-camera   # authenticates extracted ELF, assembles and compares 8 sections
```

`asm/` preserves eight accessors as instructions. `candidates/` contains their
readable but unverified C++ semantics. `reports/` contains reproducible inventories;
`config/` pins the observed reference hashes and comparison selection.
Extracted reference files and build outputs are ignored. No normal assembly build
reads the ISO. Comparison deliberately reads the reference executable.

The current gate verifies only 64 instruction bytes. Whole-executable and disc
source-only reconstruction, original compiler identification, archive recovery,
and full binary comparisons remain outstanding. Hashes identify this supplied
image; independent retail-dump provenance has not been established.
