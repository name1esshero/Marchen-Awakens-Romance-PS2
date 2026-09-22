# Current project status

Updated: 2026-09-22. Authority: [STANDARDS.md](STANDARDS.md).
Current manager: GPT-6 Astra Light (operator-provided session label), Initial Manager.
Role/model attribution is per session and commit, not a permanent assignment.

## Verified scope

- The supplied ISO is pinned by SHA-256; its inventory has 41 files and one directory.
- The complete 3,445,204-byte boot ELF now rebuilds identically from repository
  text artifacts plus assembled code. `cmp` verifies every output byte.
- An isolated build containing no ISO, extracted files, reports, existing build
  outputs or downloaded compiler reproduces the pinned boot hash.
- Eight camera accessors (64 bytes) have verified assembly implementations.
- EE GCC `2.96-ee-001003-1` with `-O2` compiles natural inline C++ accessor
  candidates into the same eight sections. Substituting them in the full ELF
  also passes byte comparison. The partial class remains a candidate.
- Research compiler distribution, hash and flags are pinned; the setup step is
  explicit and downloaded executables are ignored by Git.

## Remaining debt and limits

- **3,445,140 bytes** of the boot ELF remain explicitly preserved as unrecovered
  hex, including most code, data and ELF metadata. No authentic-source completion
  percentage is claimed; a source-artifact rebuild is not complete decompilation.
- Original game compiler version/flags are not proved. Eight middleware banners
  advertise `GCC2096 SCE3020`; those labels are not provenance for every object.
- Complete CCamera inheritance, virtual layout and size are unknown. Matching
  these small accessors is insufficient to promote the class to recovered source.
- No full-disc rebuild, archive round trip, runtime/emulator test or gameplay
  validation has been performed. Module internals and DVP overlay semantics remain open.
- Independent retail-dump authentication remains unestablished.

## Current gates

`make test`, `make verify-boot`, `make verify-source-only`, and `make verify-ee`.
Exact executed outcomes and investigation failures are recorded in
[the compiler task](tasks/COMPILER_PROBE.md) and the commit footer.
Full-disc SHA-256 was checked during initial bootstrap; routine source changes do
not reread the unchanged 4.6 GB input. `make verify-reference` checks it when needed.

The owner initialized Git in `8d5068a` after the initial bootstrap. Commits are
now authorized. New commits carry model, role, work type, actual verification and
knowledge-update trailers; old history is preserved.

Next actions: [work queue](WORK_QUEUE.md). Procedure:
[boot reconstruction](TASK_BOOT_RECONSTRUCTION_METHODOLOGY.md).
