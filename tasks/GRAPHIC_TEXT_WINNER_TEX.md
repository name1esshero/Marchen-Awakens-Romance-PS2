# `winner_tex.b` UI texture audit

## Scope and method

This read-only review covers the 22 `graphics/index.json` rows whose
`asset_path` is exactly `disc!/_DATA.YFS;1!/data/menu/winner_tex.b`, whose
category is `user_interface`, and which are not `0025_windisp` (already covered
by existing localization evidence). The four non-UI members and the excluded
`0025_windisp` are outside this report. Every one of the 22 corresponding
Japanese TGA paths was inspected; the 16 32×32 paths with one identical full
hash were retained individually in the inventory.

The previews display source alpha over a checkerboard and enlarge small art
with nearest-neighbor scaling. Bounds below are inclusive source-pixel
coordinates. For the three rows in `window`, bounds use alpha values ≥128 to
separate the lettering from the transparent canvas and footer strip.

Every filename, dimension, and full-file SHA-256 below matches its index row.
All 22 files are uncompressed type-2, 32-bit, top-origin TGAs (descriptor
`0x28`) with exact `18 + width * height * 4` extents. The set has 7 distinct
image hashes and totals 704,908 TGA bytes.

## Inventory and findings

| Japanese baseline | Dimensions | SHA-256 | Visual finding |
| --- | ---: | --- | --- |
| `00039_01631_0000_00_gnt_jp.tga` | 32×32 | `60072f7a2a7b78920c358b389eeeadee5cedd162951bbeada3c68315d5da6f9e` | Shared low-contrast, three-band gray mark (alpha max 128) repeated by rows 0001–0015. No confident reading; unresolved rather than confirmed text. |
| `00039_01631_0001_01_dor_jp.tga` | 32×32 | `60072f7a2a7b78920c358b389eeeadee5cedd162951bbeada3c68315d5da6f9e` | Exact byte duplicate of row 0000; same unresolved three-band mark. |
| `00039_01631_0002_02_jac_jp.tga` | 32×32 | `60072f7a2a7b78920c358b389eeeadee5cedd162951bbeada3c68315d5da6f9e` | Exact byte duplicate of row 0000; same unresolved three-band mark. |
| `00039_01631_0003_03_snw_jp.tga` | 32×32 | `60072f7a2a7b78920c358b389eeeadee5cedd162951bbeada3c68315d5da6f9e` | Exact byte duplicate of row 0000; same unresolved three-band mark. |
| `00039_01631_0004_04_arn_jp.tga` | 32×32 | `60072f7a2a7b78920c358b389eeeadee5cedd162951bbeada3c68315d5da6f9e` | Exact byte duplicate of row 0000; same unresolved three-band mark. |
| `00039_01631_0005_05_nns_jp.tga` | 32×32 | `60072f7a2a7b78920c358b389eeeadee5cedd162951bbeada3c68315d5da6f9e` | Exact byte duplicate of row 0000; same unresolved three-band mark. |
| `00039_01631_0006_06_alv_jp.tga` | 32×32 | `60072f7a2a7b78920c358b389eeeadee5cedd162951bbeada3c68315d5da6f9e` | Exact byte duplicate of row 0000; same unresolved three-band mark. |
| `00039_01631_0007_07_roc_jp.tga` | 32×32 | `60072f7a2a7b78920c358b389eeeadee5cedd162951bbeada3c68315d5da6f9e` | Exact byte duplicate of row 0000; same unresolved three-band mark. |
| `00039_01631_0008_08_ian_jp.tga` | 32×32 | `60072f7a2a7b78920c358b389eeeadee5cedd162951bbeada3c68315d5da6f9e` | Exact byte duplicate of row 0000; same unresolved three-band mark. |
| `00039_01631_0009_09_gir_jp.tga` | 32×32 | `60072f7a2a7b78920c358b389eeeadee5cedd162951bbeada3c68315d5da6f9e` | Exact byte duplicate of row 0000; same unresolved three-band mark. |
| `00039_01631_0010_10_ror_jp.tga` | 32×32 | `60072f7a2a7b78920c358b389eeeadee5cedd162951bbeada3c68315d5da6f9e` | Exact byte duplicate of row 0000; same unresolved three-band mark. |
| `00039_01631_0011_11_har_jp.tga` | 32×32 | `60072f7a2a7b78920c358b389eeeadee5cedd162951bbeada3c68315d5da6f9e` | Exact byte duplicate of row 0000; same unresolved three-band mark. |
| `00039_01631_0012_12_fan_jp.tga` | 32×32 | `60072f7a2a7b78920c358b389eeeadee5cedd162951bbeada3c68315d5da6f9e` | Exact byte duplicate of row 0000; same unresolved three-band mark. |
| `00039_01631_0013_13_orc_jp.tga` | 32×32 | `60072f7a2a7b78920c358b389eeeadee5cedd162951bbeada3c68315d5da6f9e` | Exact byte duplicate of row 0000; same unresolved three-band mark. |
| `00039_01631_0014_14_can_jp.tga` | 32×32 | `60072f7a2a7b78920c358b389eeeadee5cedd162951bbeada3c68315d5da6f9e` | Exact byte duplicate of row 0000; same unresolved three-band mark. |
| `00039_01631_0015_15_edo_jp.tga` | 32×32 | `60072f7a2a7b78920c358b389eeeadee5cedd162951bbeada3c68315d5da6f9e` | Exact byte duplicate of row 0000; same unresolved three-band mark. |
| `00039_01631_0017_center_jp.tga` | 64×64 | `a083442c1660385bd1f35b63eef441665794251cfedf9a5ab44018c434bc6af8` | Pale segmented circular motif; no confidently readable text. |
| `00039_01631_0018_circle_jp.tga` | 256×256 | `a562bb14c230c660ecc8ac57214814410c37757f717a4f122c97f17953699757` | Thin circular outline; no visible wording. |
| `00039_01631_0021_mg_circle_jp.tga` | 256×256 | `61b25a6cb6efce5cef4460c30426e5342e89475016269d18ab855968a699d767` | Circular band of small glyph-like ornaments, alpha bounds x=4–250, y=5–250. No confident Japanese reading; keep as an unresolved decorative/text candidate. |
| `00039_01631_0023_win_back_jp.tga` | 128×32 | `003e204d30241ea74505d1d8952914cbbc7d033e262e877cb47d3d6d097c9c21` | Repeating magenta stepped/pixel pattern across the strip; no recognizable wording. |
| `00039_01631_0024_win_back2_jp.tga` | 128×32 | `8ee5ebc02b1a1015e9f05e6a6a669aa62e7da7961925bdb4659ec24a131e565b` | Pale fragmented marks span the 128×32 canvas. They form several line-like bands but do not resolve into readable words; text status remains uncertain. |
| `00039_01631_0026_window_jp.tga` | 128×128 | `3fbd5203048a1dcfbca7046992ee3a07bc7bebb85e3338006dc9797b3519f1fb` | Three outlined Japanese-looking label rows; no confident transcription. Inclusive alpha≥128 bounds: (1,1)–(100,26), (1,45)–(99,70), and (5,76)–(122,98). The bottom band (x=0–127, y=110–123) is a horizontal frame, not a fourth text row. |

## Result and limits

The clearest language-bearing candidate is the three-row `window` texture.
The repeated 32×32 mark, `mg_circle` ring, and `win_back2` band remain
unresolved: their pixel forms alone do not justify transcription or a claim
that they are Japanese. The circular outline and magenta pattern read as
language-neutral decoration. No localized variants were generated.

This flat-image review does not establish the resources' UV rectangles, draw
order, screen composition, animation, or runtime visibility. All Japanese
baselines remain unchanged; no bundle or ISO was rebuilt and no emulator test
was run.
