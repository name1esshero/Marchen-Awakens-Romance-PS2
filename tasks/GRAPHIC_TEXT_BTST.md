# Battle Start label localization evidence

Updated: 2026-09-23.

## Source and translation

`graphics/text/00039_00991_0002_btst_txt_jp.tga` is the Japanese
`バトルスタート` label (“BATTLE START”) from
`disc!/_DATA.YFS;1!/data/menu/Laby_BG_tex.b`. Its TXC member is
`00039.asset/00991.resources/0002_btst_txt.txc.bin`, a 128×32 PSMT4 texture.
The Japanese TGA remains unchanged as the recovered baseline.

The English sibling is
`graphics/text/00039_00991_0002_btst_txt_eng.tga`. It contains the exact phrase
“BATTLE START” in uppercase, centered on the original 128×32 transparent canvas.
Only this texture's language-bearing lettering is replaced; there are no other
visible marks or background elements in this surface.

## Artwork and import

The built-in image-generation tool produced a transparent lettering crop from
the prompt below. The generated canvas was 2164×727, so it was not imported as
a full image. Only its correctly spelled English lettering was cropped,
resized into a centered 118×18 area on a transparent 128×32 canvas, and encoded
through the original PSMT4 palette with `tools/rtx3.py`. The final texture was
visually checked both at native size and enlarged for inspection.

Prompt: “Use case: text-localization. Asset type: small PlayStation 2 game UI
texture lettering source. Input image: Image 1 is the original Japanese game
label and is a style reference only. Create a transparent-background English
lettering crop containing exactly ‘BATTLE START’ in one horizontal line,
uppercase, bold compact arcade sans-serif, white face with a dark navy/black
outline and a subtle restrained shadow, closely matching the thick outlined
pixel-era lettering in the reference. Keep all letters crisp and legible at
small size, with moderate spacing, and fit the phrase on one line. Do not
include Japanese glyphs, any frame, panel, background, icons, watermark, or
extra text. The output will be composited over the preserved original texture
and mapped through its original game palette.”

## Hashes and verification

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Japanese baseline TGA | 16,402 | `25f748de8a11a853451a39665c339ea1adf943ebe83c4aedad2c535766aa0b21` |
| Source TXC | 2,176 | `e4a44a3dc6e4cd8faa16d97ce9040108275effce7e89820c7e58073b280bf09a` |
| English TGA | 16,402 | `f6b0bc414902301b7af3e6a856680a315cb0418097243c9c758c4e8a68b4bf8a` |
| Imported English TXC | 2,176 | `57cf1bd649038147717712a117a9ab255ea46a718f9b2b0e4e173a3813509879` |

`python3 tools/rtx3.py export` reproduced the Japanese baseline TGA byte-for-byte
from its source TXC (`cmp` passed). `python3 tools/rtx3.py import` accepted the
English TGA at the source dimensions and produced a TXC with the same length,
64-byte header, and palette bytes as the source; the changed TXC also exported
back to a correctly sized TGA for visual inspection. This confirms standalone
PSMT4 palette-import viability. It does not yet verify enclosing BPE/UI-bundle
reinsertion or the rebuilt ISO.

No emulator or gameplay check was performed. The exact on-screen UV rectangle,
display scale, and runtime readability remain unconfirmed.
