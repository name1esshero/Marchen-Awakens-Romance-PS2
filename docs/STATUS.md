# Current project status

Updated: 2026-09-23. Authority: [STANDARDS.md](STANDARDS.md).
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
- The byte-weighted census in `reports/asset_recovery_census.json` reports
  disjoint physical-disc spans and a separate expanded logical payload. The
  4,587,749,376-byte image has 3,327,295,881 measured all-zero placeholder/gap
  bytes (72.5257%), 1,237,522,725 nonzero terminal-member bytes (26.9745%), and
  22,930,770 nonzero gap/structure bytes (0.4998%); these disjoint spans sum
  exactly to the image. Zero measurements do not establish historical intent.
  Expanded logical information payload Y is 1,303,947,016 bytes (28.4224% of
  physical image size) after BPE bundle expansion and de-duplication.
  Parser-backed structural coverage is Z/Y = 248,202,302/1,303,947,016
  (19.0347%); unchanged-source rebuildability is A/Y = 100%; semantic
  editability is B/Y = 239,532,814/1,303,947,016 (18.3698%); runtime-validated
  editability is C/Y = 0%. Of the 1,064,414,202 bytes remaining after B, video
  accounts for 64.3651%, model/geometry candidates 18.9430%, audio/sound
  candidates 14.6986%, animation/motion 1.1793%, and unresolved graphics 0.0132%;
  the report gives the full disjoint breakdown and evidence basis. These are
  separate preservation, structure, editability, and runtime measures, not a
  single decompilation or translation percentage. Regenerate with
  `make asset-census`.
- Both the initial and fully prepared 4,587,749,376-byte disc rebuilds from
  workspace files compare byte-for-byte with the pinned ISO; the streaming
  comparator authenticates both source hashes and whole-image equality. This
  proves lossless container round-trip for this image, not semantic recovery,
  relocation safety or game runtime behavior. See
  `reports/assets-roundtrip-prepared.json`.
- A synthetic ISO test carries an edited UTF-8 text companion through CP932
  encoding, member growth, ISO directory relocation, and volume-length update.
  `make build-mod-disc` provides the corresponding experimental workspace build
  command; it now writes `mar_eng.iso` in the workspace root for emulator testing.
  No retail menu/dialogue table has yet been edited and tested in-game.
- One 20,452-byte `_msg.dat` message table has a strict editable JSON
  representation with 229 entries and a tracked source at
  `localization/messages.json`. Initial English drafts now cover all 229 entries
  across save/load prompts, menus, tutorials, character profiles, battlefields,
  ARM descriptions, Magic Stones, and the none/unused labels. All message translations
  encode as CP932. An earlier build snapshot measured 20,702 bytes (+250); the
  current combined catalog build measures 20,700 bytes (+248). The current 5,016,748,032-byte catalog-driven mod ISO inventories as 42 entries
  and reparses all three catalog-applied resources through ISO/YFS/PAC.
  Current source sizes are 20,700 bytes for `_msg.dat` (+248), 13,567 bytes for
  `CardList.txt`, and 3,319 bytes for `DataBase.txt`. The 142-row card catalog
  has draft translations for all 142 names, all 51 character titles and all 141
  categories; all 142 captions remain Japanese. These are unreviewed English drafts. The 71-row database has 87/126 fields
  translated; 39 unlock-condition fields remain original pending semantic evidence.
  Runtime line layout and acceptance remain untested. Current append placement adds the
  full 428,967,936-byte YFS to the 5,016,748,032-byte ISO.
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
  such as YPC geometry, audio, fonts and scripts remain binary; moved/grown assets
  have no runtime validation. The two catalog tables and recovered `_msg.dat`
  table are translation-bearing surfaces. All 724 menu `.b` leaves now have a
  verified decoded-binary layer; 721 also have 3,084 individually extracted
  nested resources that rebuild byte-exactly when untouched. Three `.yma` payloads
  use a different unresolved layout. The graphics index covers all 30,397
  catalogued TXCs: 28,940 standalone archive leaves and 1,457 nested menu members.
  A full audit passed source hashes and TGA dimensions for 30,354 editable exports
  (99.8585% of records and 99.9413% of TXC bytes: 27,316 PSMT4, 1,654 PSMT8,
  677 PSMT8H, 690 PSMT4HL and 17 PSMT4HH); 43 PSMCT32 records remain unresolved
  because their bodies are eight bytes short of the declared extent. High-bit
  sample previews are coherent, but do not
  validate GS sampling, UV composition or runtime. Images sit directly
  in flat semantic folders: title, icon, user_interface, effects, characters,
  cards, backgrounds, maps, weapons, environments and text. Japanese baselines end
  in `_jp.tga`, stay unchanged, and are ignored as generated workspace files;
  authored `_eng.tga` siblings are Git-trackable and take precedence in
  `mar_eng.iso` builds. Indexed exports use linear pixel order, mapped PSMT8 CLUT
  indices and expanded 0..128 GS alpha. This candidate was visually compared on
  20 PSMT4/PSMT8 resources plus three separate high-bit samples; this is not
  proof of whole-corpus screen composition. Synthetic
  English-image tests now cover nested UI-table/BPE/PAC and standalone TXC/PAC
  reinsertion while preserving source files. AT/UV composition and runtime display
  remain unresolved. The AT inspector confirms all four title animation texture
  name references match TXC members.
  See [title rendering evidence](../tasks/TITLE_TEXTURE_RENDERING.md). All 229 messages have draft translations; names,
  mechanics, and display constraints need review. DMY files, module internals and DVP
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
