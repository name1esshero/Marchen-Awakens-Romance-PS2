# Current project status

Updated: 2026-09-22. Authority: [STANDARDS.md](STANDARDS.md).
Current contributor: GPT-6, R&D contributor. Initial Manager: GPT-6 Astra
Light (operator-provided session label). Role/model attribution is per session
and commit, not a permanent assignment.

## Verified scope

- The supplied ISO is pinned by SHA-256; its inventory has 41 files and one directory.
- The complete 3,445,204-byte boot ELF now rebuilds identically from repository
  text artifacts plus assembled code. `cmp` verifies every output byte.
- An isolated build containing no ISO, extracted files, reports, existing build
  outputs or downloaded compiler reproduces the pinned boot hash.
- Nineteen accessors (152 bytes) across three distinct classes (`CCamera`,
  `CCamera2`, `CCameraMv`) have verified assembly implementations.
- EE GCC `2.96-ee-001003-1` with the same single `-O2` flag compiles natural
  C++ candidates for all nineteen into the same sections. Substituting them
  in the full ELF also passes byte comparison. The partial classes remain candidates.
- Research compiler distribution, hash and flags are pinned; the setup step is
  explicit and downloaded executables are ignored by Git.
- The boot ELF's `.text` ends exactly where a contiguous run of 1,694 named
  `.gnu.linkonce.t.*` sections begins (71,932 bytes, 497 classes by a
  naming-shape heuristic); 733 of those are the same trivial single-instruction
  shape already proven recoverable. See
  [the linkonce cluster task](tasks/LINKONCE_CLUSTER.md) and
  `reports/linkonce_text_inventory.json`.

## Remaining debt and limits

- **3,445,052 bytes** of the boot ELF remain explicitly preserved as unrecovered
  hex, including most code, data and ELF metadata. No authentic-source completion
  percentage is claimed; a source-artifact rebuild is not complete decompilation.
- Original game compiler version/flags are not proved. Eight middleware banners
  advertise `GCC2096 SCE3020`; those labels are not provenance for every object.
- Complete CCamera/CCamera2/CCameraMv inheritance, virtual layout and size are
  unknown. Matching these small accessors is insufficient to promote the
  classes to recovered source. Roughly 1,675 more census-identified linkonce
  sections (including ~733 same-shape trivial ones) remain unrecovered.
- `GetViewRect` now has a reproducible non-matching four-float aggregate probe:
  40 candidate bytes versus 24 original bytes, with unaligned versus aligned
  transfers. Member types/alignment require independent evidence; all original
  bytes remain preserved. See [the probe](tasks/VIEW_RECT_PROBE.md).
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
