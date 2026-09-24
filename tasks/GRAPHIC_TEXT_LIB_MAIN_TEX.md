# `lib_main_tex.b` Japanese UI texture text audit

## Scope and method

This read-only review covers exactly the five `user_interface` rows in
`graphics/index.json` whose `asset_path` is
`disc!/_DATA.YFS;1!/data/menu/lib_main_tex.b`. Each exported Japanese TGA was
checked against its indexed filename, dimensions, and complete image
SHA-256. All five are uncompressed true-color TGA (image type 2), 32-bit,
top-origin descriptor `0x28`, with exact `18 + width × height × 4` extents.
All five were visually reviewed as alpha-composited checkerboard previews;
`lbry`, `plt_001`, and `window` were enlarged for lettering review.

Two surfaces carry readable Japanese text. `lbry` appears to read
`ライブラリ` (“Library”), with nontransparent raster bounds `[1,190) × [12,58)`.
The metal nameplate `plt_001` appears to read `キャラの戦歴` (roughly,
“Character battle history”); its dark-ink core is bounded by
`[211,302) × [57,74)`. A separate small `014-007` tag appears on the plate at
approximately `[357,410) × [72,88)`. `window` has calligraphic-looking strokes,
but no characters can be transcribed confidently and it remains unresolved.

Bounds use source-pixel coordinates with an upper-left origin and half-open
intervals. They describe flat raster content, not UVs or screen placement.

## Inventory

| # | Japanese baseline TGA | Dimensions | Full-file SHA-256 | Visual finding |
| ---: | --- | ---: | --- | --- |
| 01 | `00039_01521_0000_00_gnt_1_jp.tga` | 512×256 | `d01eb4e3ef1f0328abaad51dfd5565c0fcb889770ed9f7aaf53a759e3d6761c0` | Character artwork with a large illustrated figure; no confidently readable wording. |
| 02 | `00039_01521_0023_fgr_00_jp.tga` | 256×128 | `ae6b4c588de1bfad8d3d5312697e3e2b05e3c890a497f747f1b4b259102f37c5` | Nighttime landscape/cavern scene with a distant structure; no visible text. |
| 03 | `00039_01521_0027_lbry_jp.tga` | 256×64 | `c8dadd2e5a87b3d46820e2778fc3070d4b3242cf67d977a72c5dc0598cfcc731` | Multicolor outlined katakana wordmark, visually read as `ライブラリ` (“Library”); nontransparent bounds `[1,190) × [12,58)`. |
| 04 | `00039_01521_0028_plt_001_jp.tga` | 512×128 | `33ec063d63645241a92294646cc9b67fbb620901afc4c1542ab8fa71cd473dc0` | Metal nameplate with central text visually read as `キャラの戦歴` (roughly, “Character battle history”), dark-ink core bounds `[211,302) × [57,74)`. The separate `014-007` tag is at approximately `[357,410) × [72,88)`. |
| 05 | `00039_01521_0029_window_jp.tga` | 128×128 | `50bf7bdf446cae7d3c2c0ba384612045d3f55b568d511fab4f97872f82eecab6` | Several outlined, calligraphic-looking forms above a dark strip; possible stylized lettering remains unresolved, with the forms approximately within `[0,128) × [2,91)`. |

## Findings and limits

The library-main bundle includes an explicit `ライブラリ` wordmark and a
character-history plate, rather than only illustrative menu artwork. These
visual readings are localization leads; this audit does not choose final
English wording or determine how the text is presented in-game. The `window`
marks are a separate unresolved candidate. The character illustration and
night scene contain no confidently readable wording.

No Japanese baseline was modified and no English override was created. This
review does not establish UVs, draw order, runtime visibility, or screen
composition. No bundle/ISO rebuild or emulator validation was performed.
