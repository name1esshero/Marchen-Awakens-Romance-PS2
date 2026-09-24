# Remaining Japanese title texture audit

Updated: 2026-09-23.

## Result

Reviewed all 13 tracked `graphics/title/*_jp.tga` baselines that have no
matching `_eng.tga` sibling. Ten show no visible writing; one contains the
existing Latin `MÄR` brandmark; two merit a cautious note: `thunder` has
fragmented magenta marks that cannot be read reliably as text, and `mg_circle`
has glyph-like decorative symbols around a ring but no recognizable Japanese
or other words. These two remain visual candidates rather than confirmed
translation omissions. No English overrides were authored and all Japanese
baselines remain unchanged.

All 13 are indexed PSMT4/PSMT8 graphics. Eleven map to
`disc!/_DATA.YFS;1!/data/menu/title_new_tex.b`; `title_bg` and `title_mar` map to
`disc!/_DATA.YFS;1!/data/menu/title_tex.b`. The table omits the common
`graphics/title/` prefix. SHA-256 covers each complete TGA and matches
`graphics/index.json`.

Bounds use a zero-based top-left origin and half-open `[x0,x1) × [y0,y1)`
coordinates. For `title_mar`, bounds include pixels with decoded TGA alpha >=128.
For the `thunder` candidate, the recorded bound is the outer extent of pixels
with alpha >=128, R >24, B >24, R >2G and B >2G; this measures the magenta
fragments, not proven lettering. For `mg_circle`, the gross ornament bounds
include pixels with
alpha >=128 and each RGB component >=180, including the circular outline. `None`
means no legible wording was identified during static visual review, not that the
texture has no visual content.

| Japanese baseline | Dimensions | TGA bytes | SHA-256 | Format / source bundle | Visible text or candidate / bounds |
| --- | ---: | ---: | --- | --- | --- |
| `00039_01565_0001_thunder_jp.tga` | 512x512 | 1,048,594 | `1b995392df5aa0d9df6f6ade2a6e5c8be604b8286cdb130e79a22fa3ca72646c` | `psmt8`; `title_new_tex.b` | No wording is reliably legible. Four horizontal bands contain fragmented magenta shapes on opaque black; they may be effect/sprite parts or text-like art. Ambiguous mark bounds x=[6,511), y=[3,504), threshold alpha >=128, R >24, B >24 and each >2G. |
| `00039_01565_0002_shade_jp.tga` | 128x128 | 65,554 | `642f953c755729965c94182c7ef43d4dc49ac6a047e89306db35fc8293b579b3` | `psmt8`; `title_new_tex.b` | None; dark concentric radial ring. |
| `00039_01565_0004_renzflear_jp.tga` | 128x128 | 65,554 | `b628a35c0659d943c7221061d89cbebe52ef7ab0ddc3fe2425eba21fa65f16ed` | `psmt8`; `title_new_tex.b` | None; isolated central glow. |
| `00039_01565_0005_mg_circle_jp.tga` | 256x256 | 262,162 | `963614bd9c28c7e0df7f2fa1cb0d37dcad4d5f21d11c24ca024ebb6b5de71096` | `psmt4`; `title_new_tex.b` | No readable Japanese or other words. White glyph-like ornaments encircle a ring; interpret as non-lexical decoration, not confirmed text. Gross visible ornament bounds x=[4,251), y=[5,251) using alpha >=128 and RGB >=180 (includes the ring). |
| `00039_01565_0006_getback_jp.tga` | 256x256 | 262,162 | `85491db876e197148873b76b059b55ae775eaa40eb3784d7186ff5fb163449d5` | `psmt8`; `title_new_tex.b` | None; blue radial burst. |
| `00039_01565_0007_flear_jp.tga` | 256x256 | 262,162 | `f74ac9557552543ed43380517adc7e6a034509129b65abcec1a566b3e849a249` | `psmt8`; `title_new_tex.b` | None; multicolor radial streaks. |
| `00039_01565_0008_flash_jp.tga` | 512x256 | 524,306 | `b4a007fd30f0fb5208ca6d2ae07486586c0f8c32c0a85978cb603fbdaa68bf71` | `psmt8`; `title_new_tex.b` | None; thin rays converging on a bright point. |
| `00039_01565_0009_effect_jp.tga` | 256x256 | 262,162 | `48c17e2f5e65f72c6143e17ad3f9260691b943eb40a2618c5c8dbdc9cb084d6c` | `psmt8`; `title_new_tex.b` | None; small white glow/cloud fragment. |
| `00039_01565_0010_circle_jp.tga` | 256x256 | 262,162 | `8188edaa31a6f1b22cbaa658e9f7f0e4a373aa34fd69c4cbfc612044dd09245e` | `psmt4`; `title_new_tex.b` | None; white circular outline. |
| `00039_01565_0011_center_jp.tga` | 64x64 | 16,402 | `47f86d5f306939f37a66ab196b1b6931b35a152383ff51669a90f4bd398fff94` | `psmt4`; `title_new_tex.b` | None; small central glow. |
| `00039_01565_0012_bg_win_jp.tga` | 256x256 | 262,162 | `51eebbb7c9c885c2261289ca9c8e4616dbc8dd520d961b48b406fda0757c9dc6` | `psmt8`; `title_new_tex.b` | None; blue swirl/background texture. |
| `00039_01566_0000_title_bg_jp.tga` | 512x512 | 1,048,594 | `e48388e9d1009cb983d2641012baf90c1caa42b0ce72b149fd7316d1d64833a2` | `psmt8`; `title_tex.b` | None; blue backdrop with an ornate border and corner motifs. |
| `00039_01566_0001_title_mar_jp.tga` | 512x512 | 1,048,594 | `24548d3ae1fdee7a3c36212592bc2a6005026353fee238ba09b56918e26dc112` | `psmt8`; `title_tex.b` | Visible Latin brandmark “MÄR”, already English/brand lettering rather than Japanese text. Alpha >=128 bounds x=[49,458), y=[42,472). |

## Review method and limits

The 13 names were selected by comparing files on disk with `graphics/index.json`
and checking that the sibling name formed by replacing `_jp.tga` with `_eng.tga`
does not exist. Every TGA header dimension and full-file hash was checked against
the index record. All images were decoded as 32-bit uncompressed top-origin TGA
(type 2, descriptor `0x28`) and visually reviewed in a checkerboard contact sheet;
ambiguous/larger artwork was also inspected at native or nearest-neighbor enlarged
scale. This confirms only the exported flat pixels.

The fragmented `thunder` marks cannot establish whether a Japanese phrase is
present beneath the effect-like appearance; revisit if an animation/frame map,
source art, or runtime view clarifies the texture. The `mg_circle` symbols are
not readable language in the recovered raster, but their intended meaning is
unknown. The `MÄR` brandmark already uses Latin lettering and was not treated as
an untranslated string. No runtime UV, draw order, animation timing, or screen
placement is inferred from these images alone.

References: `graphics/index.json`, `tools/rtx3.py`,
[`localization methodology`](../docs/LOCALIZATION_METHODOLOGY.md),
[`title texture rendering evidence`](TITLE_TEXTURE_RENDERING.md),
[`graphic localization evidence`](GRAPHIC_TEXT_LOCALIZATION.md).
