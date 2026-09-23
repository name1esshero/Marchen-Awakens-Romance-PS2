# Current project status

Updated: 2026-09-22. Authority: [STANDARDS.md](STANDARDS.md).
Current contributor identity is session-specific; consult the relevant commit
trailers. Role/model attribution is per session and commit, not a permanent
assignment, and must follow STANDARDS.md §17's fail-closed identity rule.

## Verified scope

- The supplied ISO is pinned by SHA-256; its inventory has 41 files and one directory.
- A lossless workspace now recursively exposes the ISO, two AFS archives, the YFS
  archive, and observed PAC archives: 3,557 PAC, two AFS and one YFS containers,
  with 34,486 leaves. Six text/source leaves have reversible CP932 text companions; one
  nested `tex.pac` candidate with an unknown table field remains raw. See the
  tracked `reports/assets_census.json` and ignored
  `extracted/assets/catalog.json`. Translation-bearing evidence is tracked in
  `reports/translation_surfaces.json`.
- Both the initial and fully prepared 4,587,749,376-byte disc rebuilds from
  workspace files compare byte-for-byte with the pinned ISO; the streaming
  comparator authenticates both source hashes and whole-image equality. This
  proves lossless container round-trip for this image, not semantic recovery,
  relocation safety or game runtime behavior. See
  `reports/assets-roundtrip-prepared.json`.
- A synthetic ISO test carries an edited UTF-8 text companion through CP932
  encoding, member growth, ISO directory relocation, and volume-length update.
  `make build-mod-disc` provides the corresponding experimental workspace build
  command. No retail menu/dialogue table has yet been edited and tested in-game.
- One 20,452-byte `_msg.dat` message table now has a strict editable JSON
  representation with 229 entries and a tracked source at
  `localization/messages.json`. One save/start prompt has an initial English
  rendering; a 193-byte translation grew the 178-byte CP932 original by 15 bytes.
  The catalog-driven mod ISO inventories and reparses through ISO/YFS/PAC, with
  all 229 entries recovered and the English prompt at its relocated table record.
  The authenticated reference comparison reports the expected mismatch. Runtime
  line layout and acceptance remain untested. The append strategy grows the ISO
  by the full 428,967,936-byte YFS for this 15-byte message increase.
- The complete 3,445,204-byte boot ELF now rebuilds identically from repository
  text artifacts plus assembled code. `cmp` verifies every output byte.
- An isolated build containing no ISO, extracted files, reports, existing build
  outputs or downloaded compiler reproduces the pinned boot hash.
- Sixty-two accessors (496 bytes) across seven distinct classes (`CCamera`,
  `CCamera2`, `CCameraMv`, `CRender`, `CRender2`, `CGameCamera`, `C3dObject`) have verified assembly
  implementations.
- EE GCC `2.96-ee-001003-1` with the same single `-O2` flag compiles natural
  C++ candidates for all sixty-two into the same sections. Substituting them
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

- **3,444,708 bytes** of the boot ELF remain explicitly preserved as unrecovered
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
- No runtime/emulator test or gameplay validation has been performed. Asset leaves
  such as YPC geometry, texture payloads, audio, fonts and scripts remain binary;
  moved/grown assets have no runtime validation. The two catalog tables and the
  recovered `_msg.dat` table are translation-bearing surfaces; broader UI `.b`
  resources remain opaque. The message catalog has 1 initial translation and
  228 untranslated entries. DMY files, module internals and DVP
  overlay semantics remain open.
- Independent retail-dump authentication remains unestablished.

## Current gates

`make test`, `make verify-boot`, `make verify-source-only`, and `make verify-ee`.
Exact executed outcomes and investigation failures are recorded in
[the compiler task](tasks/COMPILER_PROBE.md) and the commit footer.
Asset gates are `make export-assets prepare-assets verify-disc`; the fully
prepared unchanged full-disc comparison passed again after structured message
source integration. The edited full-mod-image comparison and nested structural
verification are recorded in [message-table evidence](tasks/MESSAGE_TABLE.md).
See
[asset methodology](TASK_ASSET_WORKSPACE_METHODOLOGY.md).
Full-disc SHA-256 is checked by the streaming comparison gate.

The owner initialized Git in `8d5068a` after the initial bootstrap. Commits are
now authorized. New commits carry model, role, work type, actual verification and
knowledge-update trailers; old history is preserved.

Next actions: [work queue](WORK_QUEUE.md). Procedure:
[boot reconstruction](TASK_BOOT_RECONSTRUCTION_METHODOLOGY.md).
