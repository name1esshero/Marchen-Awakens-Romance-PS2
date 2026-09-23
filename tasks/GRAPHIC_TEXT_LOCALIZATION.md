# English UI graphics batch

Updated: 2026-09-23.

## Authored images

The Japanese `_jp.tga` files remain immutable recovered baselines. Seven
`_eng.tga` siblings are selected by the graphics build and staged as same-size
RTX3/TXC overrides:

| Japanese surface | English artwork |
| --- | --- |
| `00039_01559_0003_title_jp.tga` | Replaces the Japanese title mark with the established MÄR Heaven lettering; retains the surrounding ARM FIGHT DREAM artwork and English subtitle. |
| `00039_01566_0002_title_marh_jp.tga` | MÄR Heaven wordmark draft. |
| `00039_01566_0003_title_parts_jp.tga` | MÄR Heaven / ÄRM Fight Dream, English creator and publisher line; existing English subtitle and Konami mark retained. |
| `00039_01556_0010_shop_jp.tga` | ARM SHOP wordmark, preserving the source gradient and transparent surround. |
| `00039_01556_0014_subtitle_jp.tga` | BUY ITEM / SELL ITEM / ARM REPAIR, adapted from the three Japanese shop actions. |
| `00039_01569_0007_modename_jp.tga` | LABYRINTH / ARM SHOP; WAR GAMES / PASSWORD; TRAINING / BATTLE; ARM SET / OPTIONS. |
| `00039_01635_0028_field_name_jp.tga` | EARTH FIELD / WATER FIELD; FIRE FIELD / WOOD FIELD; WIND FIELD / THUNDER FIELD; SHADOW FIELD. |

The shop, mode, field, and shop-action UI images were authored from reviewed
English layouts and imported into their original PSMT8/PSMT4 palettes. The shop
labels' first two lines use concise action wording in the ARM-shop context; the
Japanese source says “buy ARM,” “sell ARM,” and “ARM repair.” The title-logo
replacement uses English lettering already present in the recovered game
artwork. These are localization drafts; no emulator or gameplay review has
occurred.

## Build and verification

`make build-mod-disc` wrote the root-level `mar_eng.iso` (5,020,790,784 bytes,
SHA-256
`1883a3a699edaa887b1358e5b3eb53dc115c1abd9a836a12092713c8ea2daf7a`). The
English ISO comparison in `reports/mar_eng_compare_7_graphics.json` authenticated the
pinned Japanese reference (`cc059a3acf818dfbd0a782a9d20ee67e020d167866cd1c4dca77e6eb9224e3ec`)
and found 755,346,929 differing bytes, as expected for a relocated localized
build; this is not a byte-match claim.

The standard export/staging pass covered all 30,397 indexed TXCs, retained 43
unresolved records, and staged seven English overrides. `make test` passed all
107 tests. `make verify-graphics-image` reparses each English texture from the built
ISO through ISO9660, YFS, BPE and UI resource tables and compares its complete
TXC bytes to the staged override. All seven passed (717,440 combined bytes).
Synthetic tests separately cover nested UI-table/BPE/PAC reinsertion and
relocation. A previous ISO reparse compared `_msg.dat`, `CardList.txt` and
`DataBase.txt` against bytes generated from their tracked catalogues; all three
matched exactly at 20,714, 14,120 and 3,320 bytes, respectively. Those inputs
were unchanged in this graphics rebuild.

The build grew to 5,020,790,784 bytes; relocation is supported by the observed
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
image for the 512x256 source. Neither result was imported. For the shop-action
texture, one edit returned oversized text on a 1280x1280 canvas; an earlier
draft's row spacing was corrected to match the source before palette import.
Rejected outputs and reasons are recorded in [`FAILURES.md`](../docs/FAILURES.md).

Continue with `00039_01565_0000_ttlprts`, `00039_01565_0003_sbttl`, and the
repeated title texture `00039_00985_00000_title000`. For `windisp`, confirm the
exact Japanese labels and their displayed regions, then use a controlled
glyph/layout edit that preserves its arrows, transparency and 512x256 canvas.
Texture previews alone do not establish UV use.
