# English UI graphics batch

Updated: 2026-09-23.

## Authored images

The Japanese `_jp.tga` files remain immutable recovered baselines. Ten
`_eng.tga` siblings are selected by the graphics build and staged as same-size
RTX3/TXC overrides:

| Japanese surface | English artwork |
| --- | --- |
| `00039_00991_0002_btst_txt_jp.tga` | BATTLE START, replacing the Japanese katakana label on the same 128x32 canvas. |
| `00039_01559_0003_title_jp.tga` | Replaces the Japanese title mark with the established MÄR Heaven lettering; retains the surrounding ARM FIGHT DREAM artwork and English subtitle. |
| `00039_01566_0002_title_marh_jp.tga` | MÄR Heaven wordmark draft. |
| `00039_01566_0003_title_parts_jp.tga` | MÄR Heaven / ÄRM Fight Dream, English creator and publisher line; existing English subtitle and Konami mark retained. |
| `00039_01556_0010_shop_jp.tga` | ARM SHOP wordmark, preserving the source gradient and transparent surround. |
| `00039_01556_0014_subtitle_jp.tga` | BUY ITEM / SELL ITEM / ARM REPAIR, adapted from the three Japanese shop actions. |
| `00039_01569_0007_modename_jp.tga` | LABYRINTH / ARM SHOP; WAR GAMES / PASSWORD; TRAINING / BATTLE; ARM SET / OPTIONS. |
| `00039_01565_0003_sbttl_jp.tga` | ARM FIGHT DREAM, replacing the katakana subtitle while preserving the title artwork. |
| `00039_01635_0028_field_name_jp.tga` | EARTH FIELD / WATER FIELD; FIRE FIELD / WOOD FIELD; WIND FIELD / THUNDER FIELD; SHADOW FIELD. |
| `00039_01631_0025_windisp_jp.tga` | MÄR TEAM / CHESS TEAM; REMATCH / EXIT; NEXT BATTLE / WAR GAMES. |

The shop, mode, field, and shop-action UI images were authored from reviewed
English layouts and imported into their original PSMT8/PSMT4 palettes. The shop
labels' first two lines use concise action wording in the ARM-shop context; the
Japanese source says “buy ARM,” “sell ARM,” and “ARM repair.” The title-logo
replacement uses English lettering already present in the recovered game
artwork. The winner-screen `windisp` override preserves its 512x256 source canvas,
left logo, arrows, existing player labels, and PSMT4 palette. Only the Japanese
label bands were cleared and replaced with English lettering, mapped back through
the original palette. The War Games term follows the project glossary. These are
localization drafts; no emulator or gameplay review has occurred. The subtitle
override reuses uppercase letter shapes from the game's
`00039_00825_font_jp.tga` atlas. The `btst_txt` override has its own source and
palette measurements in [`GRAPHIC_TEXT_BTST.md`](GRAPHIC_TEXT_BTST.md).

## Winner-screen label edit

`00039_01631_0025_windisp` is a 512x256 PSMT4 texture in
`disc!/_DATA.YFS;1!/data/menu/winner_tex.b`. The extracted 65,664-byte TXC has
SHA-256 `b929f05b2f28090770d3cb0d0f1e6275bc440f59314b8c85596b89212ed6c7dd`;
the recovered Japanese baseline TGA remains SHA-256
`a924e7056ae1f20819634908e90ade4d69d2dc3af46bb8786e8f9ed37f6c65f8`.

The visible label translations are `メルチーム` → `MÄR TEAM`, `チェスチーム` →
`CHESS TEAM`, `リマッチ` → `REMATCH`, `終了` → `EXIT`, `ネクストバトル` →
`NEXT BATTLE`, and `ウォーゲーム` → `WAR GAMES`. The latter uses the glossary's
publisher-backed plural name. Original mapped-preview bounds were measured before
replacement. The two team labels stay in their original rows at y=5 and y=35; the
action labels occupy source bounds x=336–427 and x=453–503 at y=154, respectively;
the final two labels are positioned at x=332 and x=351 in their source rows at y=184
and y=213.
Player/team labels, left-side MÄRchen logo, arrows, canvas and alpha outside the
Japanese text areas are retained. The final English TGA is 512x256, 524,306 bytes,
SHA-256 `52a8a4cc7e08aaf4e97d36db1ad64a4b8b950ff372e349576e7f26fcf5e985dd`;
palette import produces a 65,664-byte TXC with SHA-256
`a727d554971d876a5fe7c0690add70042fdcd16714c95a43720f4acf6473f2d1`.

The image-generation edit changed the whole composition and enlarged the canvas,
so only its English lettering crops were reused. The source artwork was restored
before placement and import. Static texture review confirms the label spacing and
palette mapping; it does not establish the game's runtime UV rectangle or final
screen composition.

## Title subtitle label edit

`00039_01565_0003_sbttl` is a 512x128 texture in
`disc!/_DATA.YFS;1!/data/menu/title_tex.b`. Its Japanese source text is
`アーム ファイト ドリーム`, represented as “ARM FIGHT DREAM.” The source TXC is
66,624 bytes, SHA-256
`ef51e198b1b52dbbe4f149e9ef345509e2581565beb13792e81ce21eb16e0fd7`; the
unchanged Japanese baseline TGA is SHA-256
`0f0f115297c76f02407e1ae0f2b299b6190e775ea021c633e58ee07de74bcc89`.

The measured subtitle band (x=155–354, y=90–109) was cleared and replaced with
uppercase glyphs sampled from the native 8x16 ASCII atlas
`graphics/text/00039_00825_font_jp.tga` (SHA-256
`069387c9d76ca200b576cdb59e095960cf717378a13c56016b7bf4e1bebbebb8`). The
surrounding logo and 512x128 canvas remain. The English TGA is 262,162 bytes,
SHA-256 `2b40af4d25c56d4166d482d1468438391d964b35d044023fef7e8c65d2fff714`;
palette import produced a 66,624-byte TXC, SHA-256
`09634dd20da8f76e674bd60a4ece841ec6f02f10f55c96e999dd038d671a2295`.
Reparse from the ISO matched this complete TXC hash. Static review confirms the
phrase and surrounding composition, not runtime UV placement or display.

## Build and verification

`make build-mod-disc` wrote the root-level `mar_eng.iso` (5,023,174,656 bytes,
SHA-256 `b5344203f78392318dfe37fa9118ca3046e1b3f52bc88ab38c3b73ac2ae50842`).
The comparison in `reports/mar_eng_compare_10_graphics.json` authenticated the
pinned Japanese reference
(`cc059a3acf818dfbd0a782a9d20ee67e020d167866cd1c4dca77e6eb9224e3ec`) and found
757,730,801 differing bytes, as expected for a relocated localized build; this
is not a byte-match claim.

The fresh graphics audit covered all 30,397 indexed TXCs, retained 43 unresolved
records, found ten English overrides, and reported zero modified Japanese
baselines. `make verify-graphics-image` reparsed all ten English textures from
the built ISO through ISO9660, YFS, BPE and UI resource tables and compared each
complete TXC byte-for-byte to its staged override. All ten passed (851,904
combined bytes), including exact hashes for `sbttl` and `btst_txt` above.
Synthetic tests separately cover nested UI-table/BPE/PAC reinsertion and
relocation. A previous ISO reparse compared `_msg.dat`, `CardList.txt` and
`DataBase.txt` against bytes generated from their tracked catalogues; all three
matched exactly at 20,714, 14,120 and 3,320 bytes, respectively. Those inputs
were unchanged in this graphics rebuild.

The build grew to 5,023,174,656 bytes; relocation is supported by the observed
container writers, but no emulator/runtime validation has been done. The
literal-identity BPE writer also expands edited `.b` bundles. See
[`TITLE_TEXTURE_RENDERING.md`](TITLE_TEXTURE_RENDERING.md) for unresolved UV,
composition and runtime questions.

## Rejected atlas edits

Image-generation edits of `00039_01565_0003_sbttl`,
`00039_01631_0025_windisp`, and the shop-action labels were rejected or needed
controlled layout repair. The first replaced the title
composition with an oversized ARM FIGHT DREAM logo and an extra MÄR HEAVEN mark
instead of changing only the subtitle. The second replaced the team-label
layout and arrows with oversized MÄR/Chess wordmarks and returned a 1774x887
image for the 512x256 source. That generated composition was rejected. English
lettering crops were later placed only in measured source label bands over the
unchanged `windisp` base; the generated logo and layout were discarded. For the shop-action
texture, one edit returned oversized text on a 1280x1280 canvas; an earlier
draft's row spacing was corrected to match the source before palette import.
Image-generated lettering-only attempts for `sbttl` also showed horizontal
scanline artifacts at native size and were rejected; the shipped draft uses
the game's own font-atlas glyphs. No rejected image was imported.
Rejected outputs and reasons are recorded in [`FAILURES.md`](../docs/FAILURES.md).

Continue with `00039_01565_0000_ttlprts`, the repeated title texture
`00039_00985_00000_title000`, and a corpus-wide UI/title text audit. Their source
label bounds and runtime appearance remain unconfirmed; texture previews alone
do not establish UV use.
