# Training icon: `ARM SET` and `RANDOM`

This task adds English lettering to one recovered 256×256 training-control
icon. The Japanese export remains the immutable baseline. The English TGA and
its transparent source layer are separate siblings:

- Baseline: [`00039_01593_0008_icon_jp.tga`](../graphics/icon/00039_01593_0008_icon_jp.tga)
- English layer: [`00039_01593_0008_icon_eng_layer.png`](../graphics/icon/00039_01593_0008_icon_eng_layer.png)
- English texture: [`00039_01593_0008_icon_eng.tga`](../graphics/icon/00039_01593_0008_icon_eng.tga)

`graphics/index.json` maps the baseline to key
`00039.asset/01593.resources!/0008_icon.txc.bin` in
`disc!/_DATA.YFS;1!/data/menu/train_tex.b`, category `icon`, with source-TXC
SHA-256 `c1d333f74bf5d3e5e9d3f7c75c44f94f0e0f6aba284922b84a4daf4a6261d4d6`.
The baseline TGA is 256×256, 262,162 bytes, SHA-256
`5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9`. Its
header is `000002000000000000000000000100012028` (uncompressed 32-bit TGA,
top-origin with 8 alpha bits).

## Text and measured bounds

The edited source strings and clear rectangles use half-open pixel coordinates
`[x0,x1) × [y0,y1)`:

| Source wording | English wording | Cleared rectangle | English glyph bounds |
| --- | --- | --- | --- |
| `セット` after the existing `ARM` | `SET`, preserving the existing `ARM` pixels | `[194,248) × [81,103)` | `[196,246) × [83,100)` |
| `ランダム` | `RANDOM` | `[112,215) × [130,152)` | `[116,210) × [132,149)` |

The Japanese `セット` ink occupies x=194–246 and y=81–102; the Japanese
`ランダム` ink occupies x=112–213 and y=130–151. The complete perimeter of
each selected rectangle has zero alpha in the source, including the pixels
immediately outside all four edges. A first narrow crop began at x=132 and
clipped the first `ランダム` character; a wider coordinate review located its
true left edge at x=112 before the layer or English TGA was written. The final
second clear box includes all four kana and stops before the adjacent blue and
pink player controls beginning at x=219.

Only these two confirmed labels are changed. The existing `ARM` letters,
controller/button symbols, `R1`/`R2`/`L1`/`L2`, `START`/`SELECT`, player marks,
and all other icon artwork are preserved.

## Reusable glyph source and rendering parameters

No image-generation prompt was used. Uppercase glyphs were recovered from the
native 128×128 ASCII atlas
[`00039_00825_font_jp.tga`](../graphics/text/00039_00825_font_jp.tga), SHA-256
`069387c9d76ca200b576cdb59e095960cf717378a13c56016b7bf4e1bebbebb8`. The
visually observed cells are 8×16 pixels. Source cell origins are:

| Text | Glyph cell origins `(x,y)` |
| --- | --- |
| `SET` | `S (16,32)`, `E (32,16)`, `T (24,32)` |
| `RANDOM` | `R (8,32)`, `A (0,16)`, `N (104,16)`, `D (24,16)`, `O (112,16)`, `M (96,16)` |

Each character was cropped to its nontransparent pixels within its atlas cell,
then nearest-neighbor scaled without antialiasing. `SET` uses 16×17-pixel
glyphs with a 1-pixel gap at `(196,83)`, `(213,83)`, and `(230,83)`. `RANDOM`
uses 14×17-pixel glyphs with 2-pixel gaps at x=116, 132, 148, 164, 180, and
196, y=132. The source atlas shading was recolored to the icon's grayscale
palette; each original nontransparent pixel becomes opaque:

| Atlas RGB | Icon RGB |
| --- | --- |
| `(45,0,0)` | `(0,0,0)` |
| `(128,58,7)` | `(54,54,54)` |
| `(137,78,35)` or `(137,78,36)` | `(93,93,93)` |
| `(149,107,76)` | `(147,147,147)` |
| `(161,133,114)` | `(174,174,174)` |
| `(174,162,154)` | `(200,200,200)` |
| `(183,183,183)` | `(255,255,255)` |

The tracked PNG is an exact 256×256 RGBA canvas with alpha zero outside the two
English labels. Its SHA-256 is
`99ec0a8921cbf88a4dad7c4108ef71eed504a9c3cdc56a2a28f21a337d2112a0`.

## Exact recomposition and verification

Decode the Japanese TGA to top-origin RGBA using `tools/rtx3.py`, decode the
tracked PNG layer, and use the layer's unchanged 256×256 coordinates. Starting
from the Japanese pixels, clear each measured rectangle separately to
`(0,0,0,0)`, then source-over the layer at the same canvas origin. Since every
nontransparent layer pixel has alpha 255, source-over is an exact RGBA pixel
copy; no fit, crop, displacement, or rescale is applied during composition.
Write the result with `rtx3.write_tga(256, 256, rgba)`. The deterministic
English TGA is 262,162 bytes with the same TGA header as the baseline and
SHA-256 `e73fe69e257cef4f4e68ef83f44f61ec11197f07ba632ffd69d94605f452dc7f`.

Verification authenticated the baseline against `graphics/index.json`, checked
both TGA headers/extents and the PNG dimensions, and reconstructed every
expected output pixel from the baseline, two clear rectangles, and layer. No
decoded pixel outside those rectangles changed. The generated output was
re-read and visually inspected at native 256×256 size; `ARM SET` and `RANDOM`
are legible, with the player controls and surrounding icon content visible and
unchanged. The Japanese source hash remains pinned. No palette import, ISO
build, UV mapping, runtime, or emulator validation was performed; this evidence
is limited to the editable layer and static texture composition.
