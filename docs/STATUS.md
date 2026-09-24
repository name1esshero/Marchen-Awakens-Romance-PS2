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
- Bounded archive/overlay inventories now cover the 40 `.DVP` overlay sections
  and their 40 matching table rows, 14 standalone IOP IRX modules and 16 IOPRP
  module records, plus filename TOCs for both AFS archives. The AFS parser has
  malformed-input tests and an exact synthetic no-op rebuild. The IOPRP no-op
  reconstruction is exact. Overlay loader/fixup behavior, module semantics,
  detailed YFS internals and the AFS trailing 16-byte TOC fields remain
  unresolved. See `reports/dvp_overlay_inventory.json`,
  `reports/iop_module_inventory.json`, `reports/afs_inventory.json`, and their
  linked task notes.
- The byte-weighted census in [`reports/asset_recovery_census.json`](../reports/asset_recovery_census.json)
  and its [human-readable companion](../reports/asset_recovery_census.md) report
  disjoint physical-disc spans and a separate expanded logical payload. The
  4,587,749,376-byte image has 3,327,295,881 measured all-zero member/gap bytes
  (72.5257%), 1,237,522,725 nonzero terminal-member bytes (26.9745%), and
  22,930,770 nonzero gap/structure bytes (0.4998%); these disjoint spans sum
  exactly to the image. The all-zero measurement does not establish intentional
  padding, placeholder use, or historical purpose. Expanded logical
  information-bearing payload Y is 1,303,947,016 bytes (28.4224% of the image)
  after BPE bundle expansion and de-duplication. Container hierarchy addressing
  covers 100% of nonzero physical terminal members. Parser-backed structural
  coverage is Z/Y = 1,132,030,822/1,303,947,016 (86.8157%); unchanged-input
  no-op rebuildability is A/Y = 100%; semantic editability is
  B/Y = 888,328,887/1,303,947,016 (68.1261%); runtime-validated editability is
  C/Y = 0%. B comprises 239,444,320 texture source bytes, 88,494 text/message
  bytes, 33,583,536 editable YOBJ position/normal XYZ bytes, and 615,212,537
  MPEG-2 video elementary-stream bytes with a checked edit/reinsertion path. The
  non-editable queue Y-B is 415,618,129 bytes (31.8739% of Y), including
  243,701,935 structurally classified but not semantically editable bytes (Z-B). Strictly
  unclassified payload Y-Z is 171,916,194 bytes (13.1843%
  of Y), comprising audio/sound candidates 91.0058%, executables/modules
  2.3860%, animation/motion 2.1708%, model/geometry candidates 2.0591%, and
  other classes in the report. The full Y-B queue is largest in audio/sound
  candidates (51.9940%), model/geometry candidates (40.4335%), animation/motion
  (3.0201%), and movie container/packetization bytes (2.4677%). All 13 movies
  (685,111,296 bytes) export to editable MPEG-2 video and reinsert while
  preserving ADX and CRI metadata; 59,642,694 audio bytes and 10,256,065
  container/packetization bytes remain noneditable. Exact decoded video-frame
  and PCM-audio comparisons passed for all no-op remuxes. This is not emulator
  runtime evidence. A disposable full mod-ISO build with a test clip reparsed
  the changed movie and preserved its ADX audio; the test image was discarded.
  A validated AT3 envelope parser covers 723 direct
  and 1,605 nested resources (26,798 named nodes), all of which rebuild exactly;
  internal animation fields remain opaque. A YOBJ/POF0 envelope parser covers
  899 direct YMPs and 14 nested UI resources, all with exact no-op rebuilds and
  807,439 decoded pointer-slot entries. A same-count geometry editor exposes
  9,976 meshes / 1,399,314 vertices and only their XYZ position/normal fields;
  faces, UVs, materials, skinning, runtime interpretation and growth remain
  unresolved. The report gives the full disjoint breakdown and evidence basis.
  These are separate preservation, structure, editability,
  and runtime measures, not one decompilation or translation percentage. The 43
  incomplete RTX3 records are excluded from Z because their complete length
  contract fails. Regenerate with `make asset-census`.
- Both the initial and fully prepared 4,587,749,376-byte disc rebuilds from
  workspace files compare byte-for-byte with the pinned ISO; the streaming
  comparator authenticates both source hashes and whole-image equality. This
  proves lossless container round-trip for this image, not semantic recovery,
  relocation safety or game runtime behavior. See
  `reports/assets-roundtrip-prepared.json`.
- A synthetic ISO test carries an edited UTF-8 text companion through CP932
  encoding, member growth, ISO directory relocation, and volume-length update.
  `make build-mod-disc` provides the corresponding experimental workspace build
  command and writes `mar_eng.iso` in the workspace root. Repeated builds use an
  opt-in atomic replacement: the previous ISO remains until the replacement
  finishes successfully. A unit test verifies failed builds preserve the prior
  output. No edited asset has been runtime-tested in-game.
- One 20,452-byte `_msg.dat` message table has a strict editable JSON
  representation with 229 entries and a tracked source at
  `localization/messages.json`. Initial English drafts now cover all 229 entries
  across save/load prompts, menus, tutorials, character profiles, battlefields,
  ARM descriptions, Magic Stones, and the none/unused labels. All message translations
  encode as CP932. The current combined catalog build is recorded below.
  Current root-level `mar_eng.iso` is 5,023,940,608 bytes (SHA-256
  `9590a689a512d035e8073f44917eb78b6ee35841e549c61dd065641230e25e67`). The
  reusable `make verify-graphics-image` gate reparses all fourteen English TXCs
  through ISO/YFS/BPE/UI tables and confirms 1,400,064 bytes exactly match
  staged overrides. The graphics audit found fourteen overrides, 43 unresolved
  TXCs, and zero modified Japanese baselines. The authenticated pinned-reference
  comparison reports 758,496,753 differing bytes, expected for this translated
  and relocated image; see
  `reports/mar_eng_compare_14_graphics_database.json` and
  [`GRAPHIC_TEXT_LOCALIZATION.md`](../tasks/GRAPHIC_TEXT_LOCALIZATION.md).
  A direct current-ISO reparse confirmed `_msg.dat` (20,714 bytes,
  `b9385780ee9dee500ac134e29df4a6209e596ff41804cb41483c7653077fb0a9`),
  `CardList.txt` (14,120 bytes,
  `9d2dd08b3b686324884788d6ed1ca516353beddac8ea28b22afc6cdabb49ad7b`), and
  `DataBase.txt` (3,684 bytes,
  `cef6b975f4998bf00a7845e64a6519d92ad07bb67d7deaf58254cd52dfe17467`) against
  their catalog-generated CP932 outputs. The database now has 126/126 draft
  fields, including all 39 condition strings; hidden-flag wording remains
  literal, with runtime display and unlock semantics unverified. No edited image
  or text has been accepted in an emulator.
  The 142-row card
  catalog has English drafts for all 142 names, 51 character titles, 141
  categories, and 142 captions. All 142 captions received an initial source-to-draft
  editorial pass; names, titles and runtime layout remain under review. See the
  [CardList review evidence](../tasks/CARDLIST_TRANSLATION_REVIEW.md). The 71-row database now has 126/126 draft fields, including all 39
  condition phrases; their runtime display and unlock semantics remain unverified.
  Runtime line layout and acceptance remain untested. The latest append placement
  relocates the rebuilt YFS in the ISO. Updating `title_tex.b` through
  the current literal-identity BPE writer expands that wrapper from 301,071 to
  922,091 bytes; relocation remains valid but the build is space-heavy. No
  runtime display has been validated. The winner-screen `windisp` labels now have
  an English sibling; exact source text is recorded, while its runtime UV use and
  final screen placement remain unresolved. English siblings now also cover the
  title subtitle `sbttl` and `BATTLE START` UI label. The `ttlprts` atlas and
  repeated `title000` title texture are now localized and reinserted; details
  are in their linked task notes. The corpus-wide UI/title text audit remains
  open. The tracked English `EQUIP ARM` sibling is composed from a reusable,
  deterministic transparent-layer workflow. Password-menu and `top_tex.b`
  audits are integrated with visual review and full source/index hash checks;
  together they cover 22 textures and identify Japanese wordmark, control, and
  menu-label candidates. The 17-row war-selection audit is integrated; 16 paths
  are exact zero-payload duplicates and one frame remains unclassified.
  The winner-screen audit is integrated with 22 paths and seven unique raster
  hashes. The option-menu audit confirms `オプション` inside a 188×46-pixel
  label band; a tiny glyph-like strip in the separate window asset remains
  unresolved. The coordinator is building its `OPTIONS` sibling from a tracked
  transparent layer and measured-region compositor. War-common's 13-row audit
  is complete: the `wrgm` mark appears to read `ウォーハンター` (“War Hunter”),
  while the calligraphic marks in `window` remain unresolved. The five-row library-main
  audit found likely `ライブラリ` and `キャラの戦歴` marks plus `014-007`; its
  `window` marks remain unresolved. The 23-row library movie-summary audit
  found no readable text and all images were fully opaque. Shop-menu's
  six UI textures include Japanese text candidates in `equip`, `wdw_pause`, and
  `window`; `shop` reads `ARMショップ` and already has an English sibling.
  The `train_tex.b` audit is complete: its `trng` texture reads
  `トレーニング` (“Training”) and its controller atlas includes `ARM セット`
  and `ランダム`; the title's visible letters span `(1,12)`–`(224,57)`.
  DQ-34 queues an English title sibling. The GameOver audit is active in its
  verified isolated worktree. The queue holds five `READY` bounded asset cards
  for one active delegated worker (5.0 ready cards per active worker;
  reserve/capacity is 5/2 = 2.5).
  The completed
  title-remainder audit is integrated. Map,
  special-font, AFS suffix, background, and title-remainder audits are
  integrated. Training-text is complete and GameOver is active; transition-menu,
  TGS-menu, save/load, war-close, and training-title localization are ready. The
  coordinator's read-only PSMCT32
  investigation found a common eight-byte shortfall across 43 records but no safe decode; those
  records remain raw.
  The `ttlprts` and `title000` English siblings, task notes and success entries
  are integrated, locally round-trip, and reparse from the rebuilt ISO. None of
  the graphics has runtime validation. The worker procedure now requires each delegated task to
  record its reusable result or negative finding in `SUCCESSES.md` or
  `FAILURES.md` as applicable. See the
  [delegation-ready reserve](WORK_QUEUE.md#delegation-ready-reserve) and
  [worker procedure](AGENT_ENVIRONMENT.md#rolling-queue-for-delegated-work).
- The complete 3,445,204-byte boot ELF now rebuilds identically from repository
  text artifacts plus assembled code. `cmp` verifies every output byte.
- An isolated build containing no ISO, extracted files, reports, existing build
  outputs or downloaded compiler reproduces the pinned boot hash.
- 505 accessors (4,416 bytes) across ninety-five distinct classes (see
  `candidates/ee_camera/CCamera.h` for the full list) have verified assembly
  implementations: the original 441 trivial 8-byte sections, plus 64 from
  two non-trivial-tier batches (12- and 16-byte). Every trivial 8-byte linkonce
  section not judged UI/dialog/texture/model/movie-adjacent is now either
  recovered or explicitly deferred as a `$gp`-relative static (5 sections
  across 4 classes: `CArmEffect`, `CGameEffect_Ctrl`, `LoadAnimNormal`,
  `CGameEffect_FootStamp` — singleton/static instance pointers an isolated
  probe cannot reproduce without manufacturing a whole-program static
  layout). Of the non-trivial (>8-byte) sections surveyed, 68 have now been
  examined across two batches: 64 recovered, 4 deferred for the same
  isolated-probe register-allocation/scheduling limitation, and 2 more
  (`CCharCom::SetMovePos`, `FireStorm_Seed::SetPos`) confirmed to use
  undecoded R5900 `LQ`/`SQ` instructions, the same tooling gap already found
  on CCamera's matrix setters. Roughly 270 non-trivial sections remain
  unexamined. See [the linkonce cluster task](tasks/LINKONCE_CLUSTER.md).
- EE GCC `2.96-ee-001003-1` with the same single `-O2` flag compiles natural
  C++ candidates for all 505 into the same sections. Substituting them
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

- **3,440,788 bytes** of the boot ELF remain explicitly preserved as unrecovered
  hex, including most code, data and ELF metadata. No authentic-source completion
  percentage is claimed; a source-artifact rebuild is not complete decompilation.
- Original game compiler version/flags are not proved. Eight middleware banners
  advertise `GCC2096 SCE3020`; those labels are not provenance for every object.
- Complete class inheritance, virtual layout and size are unknown for all
  ninety-five partial classes above. Matching these small accessors is
  insufficient to promote the classes to recovered source. 5 explicitly
  deferred `$gp`-relative-static sections remain (singleton/static instance
  pointers an isolated probe cannot reproduce without manufacturing a
  whole-program static layout; see
  [the linkonce cluster task](tasks/LINKONCE_CLUSTER.md)), plus 283 sections
  deliberately excluded as UI/menu/dialog/texture/model/movie-adjacent,
  across classes including `MenuFrameUI`/`MenuFrame`/`MenuFrameSimpleUI`/
  `MenuEsy` and `CTexData`.
- `GetViewRect` now has a reproducible non-matching four-float aggregate probe:
  40 candidate bytes versus 24 original bytes, with unaligned versus aligned
  transfers. Member types/alignment require independent evidence; all original
  bytes remain preserved. See [the probe](tasks/VIEW_RECT_PROBE.md).
- No runtime/emulator test or gameplay validation has been performed. YPC model
  candidates, most YOBJ body data, audio, fonts and scripts remain semantically
  opaque; moved/grown assets have no runtime validation. The two catalog tables
  and recovered `_msg.dat` table are translation-bearing surfaces. All 724 menu `.b` leaves now have a
  verified decoded-binary layer; 721 also have 3,084 individually extracted
  nested resources that rebuild byte-exactly when untouched. Three `.yma` payloads
  use a different unresolved layout. The graphics index covers all 30,397
  catalogued TXCs: 28,940 standalone archive leaves and 1,457 nested menu members.
  The earlier full audit passed source hashes and TGA dimensions for 30,354 editable exports
  (99.8585% of records and 99.9413% of TXC bytes: 27,316 PSMT4, 1,654 PSMT8,
  677 PSMT8H, 690 PSMT4HL and 17 PSMT4HH); 43 PSMCT32 records remain unresolved
  because their bodies are eight bytes short of the declared extent. High-bit
  sample previews are coherent, but do not
  validate GS sampling, UV composition or runtime. Images sit directly
  in flat semantic folders: title, icon, user_interface, effects, characters,
  cards, backgrounds, maps, weapons, environments and text. All 30,354 editable
  TGA baselines and the index are version-controlled in `graphics/`. Japanese
  baselines end in `_jp.tga`, stay unchanged, and remain the recovered artwork;
  authored `_eng.tga` siblings are version-controlled localization assets and
  take precedence in `mar_eng.iso` builds. Fourteen English graphics, including
  the `EQUIP ARM` weapon command and button-help labels, reinsert byte-exactly
  from the rebuilt ISO (1,400,064 TXC bytes); see the build report and task
  evidence for the full set. The subtitle
  draft reuses native
  English lettering, but possible repeated
  branding and AT/UV screen composition remain unresolved. Indexed exports use
  linear pixel order, mapped PSMT8 CLUT
  indices and expanded 0..128 GS alpha. This candidate was visually compared on
  20 PSMT4/PSMT8 resources plus three separate high-bit samples; this is not
  proof of whole-corpus screen composition. Synthetic
  English-image tests now cover nested UI-table/BPE/PAC and standalone TXC/PAC
  reinsertion while preserving source files. AT/UV composition and runtime display
  remain unresolved. The AT inspector confirms all four title animation texture
  name references match TXC members. Node envelopes now parse across all 2,328
  direct and nested AT3 resources and rebuild byte-exactly; property fields and UV
  semantics remain unresolved.
  See [title rendering evidence](../tasks/TITLE_TEXTURE_RENDERING.md). All 229 messages have draft translations; names,
  mechanics, and display constraints need review. DMY files, module internals and DVP
  overlay semantics remain open.
- Independent retail-dump authentication remains unestablished.

## Current gates

`make test`, `make verify-boot`, `make verify-source-only`, and `make verify-ee`.
Exact executed outcomes and investigation failures are recorded in
[the compiler task](tasks/COMPILER_PROBE.md) and the commit footer.
Asset gates are `make export-assets prepare-assets verify-disc`; following this
census refresh, a fresh source-only build with `--replace-existing` followed by
`make compare-disc` again matched the complete 4,587,749,376-byte pinned image
with zero differing bytes.
The edited full-mod-image comparison and nested structural
verification are recorded in [message-table evidence](tasks/MESSAGE_TABLE.md).
See
[asset methodology](TASK_ASSET_WORKSPACE_METHODOLOGY.md).
Full-disc SHA-256 is checked by the streaming comparison gate.

The owner initialized Git in `8d5068a` after the initial bootstrap. Commits are
now authorized. New commits carry model, role, work type, actual verification and
knowledge-update trailers; old history is preserved.

Next actions: [work queue](WORK_QUEUE.md). Procedure:
[boot reconstruction](TASK_BOOT_RECONSTRUCTION_METHODOLOGY.md).
