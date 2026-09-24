# Remaining small-menu texture text audit

## Scope and method

This read-only visual audit covers exactly the 13 `user_interface` rows in
`graphics/index.json` mapped to seven assets under
`disc!/_DATA.YFS;1!/data/menu/`: `esy_menu.tex`, `war_deci_01_tex.b`,
`war_deci_02_tex.b`, `war_dialog_tex.b`, `war_pad_tex.b`,
`war_sel_act_tex.b`, and `wgm_card7_txc.b`. All 13 exported Japanese-baseline
TGAs were visually reviewed, with alpha-composited previews enlarged by
nearest-neighbor scaling where useful. Repeated selector-frame images were
opened individually and byte-compared through their full-file hashes.

Each filename, dimension, and full TGA SHA-256 below matches its index row.
All 13 files are uncompressed true-color TGA image type 2, 32 bits per pixel,
top-origin descriptor `0x28`, and have exactly `18 + width × height × 4`
bytes. Bounds are source-pixel coordinates with an upper-left origin and
half-open intervals; they describe visible raster content, not UVs or screen
placement. The `window` texture's visible rows remain uncertain text candidates
and are not transcribed.

## Inventory and visual findings

| Bundle | Japanese-baseline TGA | Dimensions | Full-file SHA-256 | Visual finding |
| --- | --- | ---: | --- | --- |
| `war_deci_01_tex.b` | `00039_01611_0000_sel_frame_jp.tga` | 32×32 | `0591f3cd7ce8612b6e27ee2da5174a869f034653ef00a580515dddd39178803f` | Thin, light-gray square selection/frame border with transparent center; no wording. Exact raster duplicate of the other three `sel_frame` entries below. |
| `war_deci_02_tex.b` | `00039_01613_0000_sel_frame_jp.tga` | 32×32 | `0591f3cd7ce8612b6e27ee2da5174a869f034653ef00a580515dddd39178803f` | Exact full-file duplicate of `war_deci_01_tex.b`'s 32×32 border; no wording. |
| `war_dialog_tex.b` | `00039_01615_0000_sel_frame_jp.tga` | 32×32 | `0591f3cd7ce8612b6e27ee2da5174a869f034653ef00a580515dddd39178803f` | Exact full-file duplicate of the same 32×32 border; no wording. |
| `war_pad_tex.b` | `00039_01617_0001_sel_pl_com_jp.tga` | 256×64 | `777bcc1649078c23ac9dd730344ac2b69cc9820b6e806aa821f1b5a9fb609aa3` | Already-English mode labels: `PLAYER 1 VS COM` at `[27,177) × [4,17)`, `PLAYER 1 VS PLAYER 2` at `[28,228) × [24,37)`, and `COM VS COM` at `[78,178) × [44,57)`. No Japanese text found. |
| `war_pad_tex.b` | `00039_01617_0002_window_jp.tga` | 128×128 | `a53fe384bbf276adaed7da83c8504a9e6968a90e3e54bd6214d89c9229e29087` | Three outlined, calligraphic/Japanese-looking label rows occupy `[1,101) × [1,25)`, `[1,100) × [46,71)`, and `[5,123) × [76,97)`. Their exact characters are unresolved in this isolated view. A separate bottom band at `[0,128) × [110,120)` is frame artwork, not a confidently readable fourth label. |
| `war_sel_act_tex.b` | `00039_01619_0000_sel_frame_jp.tga` | 32×32 | `0591f3cd7ce8612b6e27ee2da5174a869f034653ef00a580515dddd39178803f` | Exact full-file duplicate of the other three 32×32 selection borders; no wording. |
| `wgm_card7_txc.b` | `00039_01629_0017_center_bar_jp.tga` | 128×64 | `f9f558f0d2ea2e4e3c122f46d0775118c5c5c11153911e988cca74adaa9eb574` | Dark, low-contrast patterned double strip/frame with block-like marks; no confident reading or text bounds. Keep the marks unresolved rather than treating them as confirmed Japanese. |
| `wgm_card7_txc.b` | `00039_01629_0018_draw_jp.tga` | 128×32 | `93710cb36d5099411faaef6a4eee727c602be21218d2ef080b3cb95cfd1e723d` | English `DRAW`, visible bounds `[5,123) × [3,29)`; no Japanese wording. |
| `wgm_card7_txc.b` | `00039_01629_0019_extb_jp.tga` | 256×64 | `2487b923ab690ca578a97f7d8066433860df1e939ed58e7417e8985a334b7d9c` | English `SUDDEN DEATH` lettering on two rows: upper `[6,249) × [5,27)`, lower `[4,253) × [36,61)`. |
| `wgm_card7_txc.b` | `00039_01629_0020_hurry_jp.tga` | 128×32 | `74692eb19350fb0367fd3bf7ad4b4e88133ae52d8a430f16f61aaafea6e88038` | English `HURRY UP!`, visible bounds `[7,121) × [6,26)`; no Japanese wording. |
| `wgm_card7_txc.b` | `00039_01629_0023_wait_jp.tga` | 128×32 | `7aba10f792ea80b4c2e94dd40f0a3d9fa23510dde66113a241763fd13d12d6aa` | English `Please Wait...`, visible bounds `[4,122) × [6,26)`; no Japanese wording. |
| `wgm_card7_txc.b` | `00039_01629_0024_wld_jp.tga` | 64×64 | `424a5c8599441b2844eede6d05619716eb802a1a8af74cee90c25b573a950e21` | English labels `Win` `[13,52) × [3,18)`, `Lose` `[13,51) × [24,38)`, and `Draw` `[8,58) × [45,59)`; no Japanese wording. |
| `esy_menu.tex` | `00039_00985_00000_title000_jp.tga` | 512×512 | `19b66cfa3f6c69717e0250cca8c0cd89e5e195dfb2ecd3279d9f3ff4b34365e6` | Japanese title mark/logo occupies approximately `[92,398) × [13,161)`; Japanese creator/publisher credit line is in `[8,352) × [436,450)`. The already-English `MÄRCHEN AWAKENS ROMANCE`, `PRESS START BUTTON`, and `© 2005 KONAMI` remain visible in their own lower/adjacent atlas regions. An `_eng.tga` sibling already exists and was not changed. |

## Findings and limits

The only clearly Japanese-bearing surface found in these 13 exports is the
`title000` mark and credit line; both already have an English sibling from
prior localization work. `war_pad` includes useful English control-mode labels
alongside the unresolved `window` label artwork. The six `wgm_card7_txc.b`
images contain five English text assets and one patterned bar with ambiguous
marks. The four selector-frame paths share one exact image hash.

No Japanese baseline, English override, graphics index, queue, or status file
was changed. This static image audit does not establish the `window` marks'
transcription, UVs, draw order, runtime visibility, or on-screen composition.
No bundle/ISO rebuild or emulator validation was run.

References: `graphics/index.json`,
[`title000 localization evidence`](GRAPHIC_TEXT_TITLE000.md),
[`title rendering methodology`](TITLE_TEXTURE_RENDERING.md), and
[`localization methodology`](../docs/LOCALIZATION_METHODOLOGY.md).
