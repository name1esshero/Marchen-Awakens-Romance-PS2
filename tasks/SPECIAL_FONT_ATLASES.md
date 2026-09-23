# Special-font atlas characterization

Updated: 2026-09-23. This is a read-only visual and metadata inventory of the
two `sp_font` textures. The shared `00039_00825_font_jp.tga` Latin atlas is
outside this task. Neither Japanese baseline was changed.

## Source records and raster properties

| Exported TGA | RTX3 source | Source SHA-256 | PSM | Export SHA-256 |
| --- | --- | --- | --- | --- |
| `graphics/text/00039_00806_00022_sp_font_jp.tga` | `disc!/_DATA.YFS;1!/data/cockpit/gm2d_tex.pac!/sp_font.txc` | `e4e3fce625247bc8483a9ec9859e257f310682b7ea010644f0c51c38a1f0e3c3` | PSMT8H | `f923835df20d287119d8f15ec7c9967a214844d38cfc8edc56b2ccf4fe69e3ab` |
| `graphics/text/00039_01556_0013_sp_font_jp.tga` | `disc!/_DATA.YFS;1!/data/menu/shop_tex.b` member `0013_sp_font.txc` | `afefd270a4c231e246b02632fa232acee928d5fc771b44098aa0525a697bc602` | PSMT8 | `4f4bb22afef3cc363b5c88e80cd46339dc9a7400d9a1b8e1d8391cedeef3376a` |

Both `graphics/index.json` image hashes match the files. Each image is a
128×64, 32-bit uncompressed true-color TGA (18-byte header plus 32,768 pixel
bytes; header image type 2, descriptor `0x28`, top-origin, eight alpha bits).
The TGA itself has no color map: palette lookup has already been expanded into
RGBA pixels. The index identifies two different 8-bit indexed source modes,
PSMT8H and PSMT8. In the current RTX3 implementation both use a 256-entry
(1,024-byte) RGBA CLUT and the same CLUT index permutation; exported GS alpha
is scaled from 0..128 to 0..255. This describes the recorded source modes and
current export path, not a runtime proof of GS sampling.

| Export | Alpha 0 | Partial alpha (1–254) | Alpha 255 | Distinct RGBA colors |
| --- | ---: | ---: | ---: | ---: |
| Cockpit PSMT8H | 3,008 | 1,968 | 3,216 | 256 |
| Shop PSMT8 | 2,984 | 2,240 | 2,968 | 256 |

The first raster has 81 distinct alpha values and the second has 74. All
intermediate alpha values in both are even; the 255 values are the saturated
endpoint. The images use mostly grayscale lettering/outlines with colored
PlayStation face-button marks. Their alpha channel includes transparent
background, opaque cores, and antialiased edges; treating the whole atlas as
opaque would erase that distinction.

## Observed atlas regions and glyph inventory

Coordinates below are pixel coordinates in the exported TGA, origin at the
upper left, with half-open intervals. Both images show three 16×16 rows of
visually separated cells at x boundaries 0, 16, 32, 48, 64, 80, 96, 112,
128. Treat this as a measured image layout, not a proven renderer cell stride
or character lookup table.

| Region | Contents visible in both exports | Confidence / unresolved mapping |
| --- | --- | --- |
| `y=[0,16)`; eight 16×16 cells | `x=[0,16)` circle, `[16,32)` cross, `[32,48)` triangle, `[48,64)` square; four additional single glyph-like marks fill `[64,80)`, `[80,96)`, `[96,112)`, `[112,128)` | Four face-button symbols are clear. The remaining marks look character-like/CJK-style at this resolution, but no code point, reading, or function was corroborated. |
| `y=[16,32)`; eight 16×16 cells | `x=[0,16)` R1, `[16,32)` R2, `[32,48)` up arrow, `[48,64)` down arrow, `[64,80)` left arrow, `[80,96)` right arrow, `[96,112)` plus, `[112,128)` small triangle | Labels and directions are visually clear; their game-side character IDs are unknown. |
| `y=[32,48)`; eight 16×16 cells | `x=[0,16)` L1, `[16,32)` L2; `[32,48)` one additional stylized control mark; `[48,64)` right arrow, `[64,80)` left arrow, `[80,96)` up arrow, `[96,112)` down arrow; `[112,128)` small triangle | The arrow silhouettes are clear. The first mark after L2 is not confidently identified. |
| `y=[48,64)`; full-width 128×16 region | Continuous horizontal grayscale gradient/stripe with a separate mottled lower band; it has no transparent gutters at the 16-pixel cell boundaries | It is texture content rather than evidenced individual character cells; runtime purpose is unknown. |

There is no evidenced A–Z/a–z or general numeric/punctuation repertoire here.
The only readable Latin/digit strings are the baked R1/R2/L1/L2 shoulder-button
labels. Do not use these atlases as a replacement for the shared Latin font or
as a general Japanese character map. The four unresolved character-like marks
are candidates for further mapping, not confirmed kana/kanji coverage.

## Relationship between the two variants

The layouts and most binary alpha-mask positions are closely related: their
nontransparent-mask intersection-over-union is 0.993096 (36 mask pixels
differ). The full RGBA rasters are not interchangeable: 2,550 of 8,192 pixels
differ, with most differences in color/alpha treatment; the alpha mask of the
bottom stripe is identical. Keep each exported baseline paired with its own
source TXC and palette if a later localized derivative is attempted.

Method: parsed both TGA headers and pixel channels with a read-only Python
inspection, compared the records and hashes against `graphics/index.json`,
and visually inspected native atlas previews plus coordinate-aligned enlarged
views. Temporary preview files were written under `/tmp`; no preview or
modified image was added to the repository.

Limits: texture pixels do not identify character codes, string-table mappings,
font metrics, fallback behavior, animation, UVs, blend state, or which game
screens consume either copy. No importer was run, no ISO was built, and no
runtime/emulator validation was performed. PSMT8H's game-side sampling behavior
remains subject to the existing RTX3/high-bit format limits.

References: `graphics/index.json`, both TGA files above,
[`LOCALIZATION_METHODOLOGY.md` §14](../docs/LOCALIZATION_METHODOLOGY.md),
`tools/rtx3.py`, and [`SUCCESSES.md`](../docs/SUCCESSES.md) under
“Special-font atlases contain button/control glyph sheets, not general fonts.”
