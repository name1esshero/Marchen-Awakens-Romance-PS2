# `war_common_tex.b` Japanese UI texture text audit

## Scope and method

This read-only audit covers exactly the 13 `user_interface` records in
`graphics/index.json` whose `asset_path` is
`disc!/_DATA.YFS;1!/data/menu/war_common_tex.b`. Every exported Japanese TGA
was checked against its indexed filename, dimensions, and full-file SHA-256.
All 13 files are uncompressed true-color TGA (image type 2), 32-bit, top-origin
descriptor `0x28`, with the exact `18 + width × height × 4` byte extent. The
contact sheet used alpha-composited checkerboard previews at native or
nearest-neighbor enlarged scale; every image was visually reviewed. The
`cas_front`, `window`, and `wrgm` images also received enlarged review.

One clear text-bearing image is `wrgm`: its multicolor Japanese katakana
wordmark appears to read `ウォーハンター` (“War Hunter”). Its nontransparent
pixel bounds in source coordinates are `[20, 235) × [13, 60)` (x, y). The
`window` texture contains outlined, calligraphic-looking forms, but no
confident character reading; treat them as an unresolved localization
candidate rather than confirmed text. The other eleven images have no
confidently readable wording.

## Inventory

Bounds, when given, are source-pixel coordinates with an upper-left origin and
half-open intervals. They describe visible raster content only, not UVs or
screen placement.

| # | Japanese baseline TGA | Dimensions | Full-file SHA-256 | Visual finding |
| ---: | --- | ---: | --- | --- |
| 01 | `00039_01606_0001_cas_front_jp.tga` | 256×256 | `8274f75123b46c52cd49e9f0fca059ccd0ede4bc617061fa924def0a8351c523` | Busy gray patterned surface with a small red-and-white framed inset near the lower center; no confidently readable wording. The inset contents remain too small/ambiguous to classify as text. |
| 02 | `00039_01606_0002_cas_parts_jp.tga` | 64×64 | `d500ca11bc3bff73b1145a23371fb216536f6b3b955ed2ab0468e203bd5d96a0` | Dark, blocky gray graphic with stepped divisions; no readable text. |
| 03 | `00039_01606_0003_cas_slate_jp.tga` | 128×128 | `f55f4a6c4568d94db9077354d62957578f2d903f48991330669b3310617c2fd7` | Blue patterned panel/frame-like surfaces with repeated rectangular motifs; no readable text. |
| 04 | `00039_01606_0005_flore_jp.tga` | 128×128 | `ce0f451b1637c565f93f16da19264105bf879ef7f20f0333e87aa7f8e9d21cdf` | Nearly uniform gray surface with scattered darker pixels; no readable text. |
| 05 | `00039_01606_0006_heventower_jp.tga` | 64×64 | `19f8cabf8d358060f27120d2fa48457e4e0b2b644c9bfedd128468e9ee51350d` | Small pixel-art tower/building facade; no readable lettering. |
| 06 | `00039_01606_0009_shade_01_jp.tga` | 32×32 | `fcce9979f412359f25697f2337ef011b2350578aceb96fa3b951f0b914657731` | Low-resolution monochrome shading graphic; no readable text. |
| 07 | `00039_01606_0010_shade_02_jp.tga` | 64×64 | `336d8541e6b3e264421fdbbc97da644a2b6789d3335b472c3e15520863331b83` | Soft-edged gray shading silhouette over transparency; no readable text. |
| 08 | `00039_01606_0011_shade_03_jp.tga` | 32×32 | `dd05f50e90e09dfd7df1f126885a1ada4fc6b2f4c20903129726db0812bece1f` | Compact translucent gray shading patch; no readable text. |
| 09 | `00039_01606_0012_shade_04_jp.tga` | 32×64 | `e42deb596985b4be1af4356f6dea833257c15c04dadff1497139628e2cd55576` | Narrow, upright gray shading shape with soft edges; no readable text. |
| 10 | `00039_01606_0015_step_jp.tga` | 32×32 | `4880b8532918a43f429ff3903c44cb7d51a7fe1f79535115010140048c7d7c54` | Repeated horizontal gray/brown bands; no lettering. |
| 11 | `00039_01606_0020_trns_jp.tga` | 64×64 | `2eda80d4f411d76cef992dd5d8429ffec5c7f82b07452605a9a33fd34af11c76` | Mostly black field with a soft gray vertical gradient along the right side; no readable text. |
| 12 | `00039_01606_0021_window_jp.tga` | 128×128 | `a53fe384bbf276adaed7da83c8504a9e6968a90e3e54bd6214d89c9229e29087` | Three bands of outlined, calligraphic-looking marks above a dark horizontal strip. The marks could be stylized lettering, but no characters can be transcribed confidently; candidate region is approximately `[0,128) × [4,90)`. |
| 13 | `00039_01606_0022_wrgm_jp.tga` | 256×64 | `af5aa527013b999cbce865ee0587ecd41a74b491051ef21a99107494cb6f6c77` | Multicolor outlined katakana wordmark, visually read as `ウォーハンター` (“War Hunter”); nontransparent bounds `[20,235) × [13,60)`. |

## Findings and limits

The bundle includes one clearly text-bearing katakana wordmark and one
separate, unresolved calligraphic-looking image. The remaining eleven exports
show patterned panels, a small facade, shading/transition graphics, or bands
without confidently readable words. These are raster observations; they do
not establish the `window` marks' identity or the `wrgm` logo's in-game role.

No Japanese baseline was modified and no English override was created. This
review does not establish UVs, draw order, runtime visibility, or screen
composition. No bundle/ISO rebuild or emulator validation was performed.
