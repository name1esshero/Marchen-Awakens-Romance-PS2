# Password-screen texture text audit

## Scope and method

This read-only review covers all 10 Japanese TGA exports indexed to
`disc!/_DATA.YFS;1!/data/menu/password_tex.b`. The bundle sidecar directory
`extracted/assets/00039.asset/01547.resources/` contains the 10 mapped TXC
members. For each entry, the member name and `source_sha256`, exported TGA
filename, dimensions, and full TGA SHA-256 were checked against
`graphics/index.json`. Each TGA is uncompressed true-color (type 2), 32 bits
per pixel, top-origin descriptor `0x28`, with exact `18 + width × height × 4`
length. All 10 source-member hashes and all 10 image hashes match the index;
all 10 TGA image hashes are distinct.

Every image was reviewed on an alpha-composited checkerboard. The 512×512
background was viewed at native size; smaller images were enlarged with nearest
neighbor. Text-like candidates received closer 4×–8× review. Coordinates below
use the image's upper-left origin and half-open ranges `[x0,x1) × [y0,y1)`;
lettering bounds are approximate except where explicitly measured from the
TGA alpha channel. They describe raster content only, not UVs, layout in a
screen, or runtime visibility.

## Inventory

| # | Bundle member | Japanese baseline TGA | Size | TGA SHA-256 | Visual finding |
| ---: | --- | --- | ---: | --- | --- |
| 01 | `0000_bg.txc.bin` | `backgrounds/00039_01547_0000_bg_jp.tga` | 512×512 | `b837cc6beb3ffeff130d8e100ea4b4c00f80de105870efa6725d3f58d44cea13` | Ornamental cross/radial background with a central ring; no readable writing or title mark. |
| 02 | `0001_center_lock.txc.bin` | `user_interface/00039_01547_0001_center_lock_jp.tga` | 64×64 | `da20ce0be17f5984522e1db8423f4d4235e28a27eba84fe5a350976f21894526` | Circular metallic lock-like pictogram; no readable writing. |
| 03 | `0002_icon.txc.bin` | `icon/00039_01547_0002_icon_jp.tga` | 256×256 | `5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9` | Controller/help atlas with Japanese command-caption groups in the right half, approximately `[129,255)×[1,202)`. `もどる` (“Back”) is a confident visual reading; other small labels are not fully transcribed. The sheet also has face-button glyphs, `R1/R2/L1/L2`, `START`, `SELECT`, `P1/P2`, and `COM`. |
| 04 | `0003_psswrdfnt.txc.bin` | `user_interface/00039_01547_0003_psswrdfnt_jp.tga` | 256×256 | `b18b30fb83bf78c52724e2d61928cdf352841adf6fe9a5145671a0ca0ac34a33` | Password-entry glyph atlas: Latin capitals A–Z, digits 0–9, and a small directional/key-like glyph. A Japanese `パスワード` sample/label appears near the bottom at approximately `[146,254)×[232,254)`; font-cell lookup and the label's UI role are not established. |
| 05 | `0004_pswd.txc.bin` | `user_interface/00039_01547_0004_pswd_jp.tga` | 256×64 | `a1bfc7091432fe493210dfd90476a38ecaa304315d882ea09b6d7c36f90cba18` | Stylized Japanese `パスワード` (“Password”) wordmark. Its nonzero-alpha extent is `[1,189)×[13,58)`. This is embedded artwork, distinct from the alphanumeric glyph atlas above. |
| 06 | `0005_pswdprts.txc.bin` | `user_interface/00039_01547_0005_pswdprts_jp.tga` | 128×128 | `1159504dc91aa34b30ef0e1b0f6d22cd5101c7d41f39eede9f7546ebc4ef2950` | Window/selection parts and three colored circular marks. The red/blue circles contain small glyph-like marks, but no word or confident character reading is visible; retain them as unresolved symbols, not confirmed text. |
| 07 | `0006_shade.txc.bin` | `user_interface/00039_01547_0006_shade_jp.tga` | 256×256 | `eb4c93135578d008c706a8edde748709f10ce752531116f384a62dc7250b66d2` | Radial shading/gradient texture; no readable writing. |
| 08 | `0007_shutter_lu.txc.bin` | `user_interface/00039_01547_0007_shutter_lu_jp.tga` | 64×64 | `123fb188720332b674ac9fdf454667f68404ec07d8c1a3969204b39c2643352c` | Diagonal shutter/wipe wedge; no readable writing. |
| 09 | `0008_shutter_ro.txc.bin` | `user_interface/00039_01547_0008_shutter_ro_jp.tga` | 64×64 | `510550ed72e53b8434550b26eaaf5f9a644d59031f40554f23e6a1d00a20d927` | Opposing diagonal shutter/wipe wedge; no readable writing. |
| 10 | `0009_window.txc.bin` | `user_interface/00039_01547_0009_window_jp.tga` | 128×128 | `a53fe384bbf276adaed7da83c8504a9e6968a90e3e54bd6214d89c9229e29087` | Repeating ornamental window/frame bands; no confidently readable wording. |

## Findings and limits

The confirmed translation-bearing artwork in this bundle is concentrated in
the controller/help atlas (#03) and the Japanese password wordmark (#05). The
font atlas (#04) contains English alphanumeric entry glyphs and a Japanese
password sample; verify the intended atlas usage before replacing that sample.
The three small marks in #06 remain candidate symbols only. The other seven
images show no confidently readable language-bearing content.

The Japanese baselines were preserved; no English override was authored. This
static audit does not identify glyph indices, codepoints, text segmentation,
UVs, draw order, the use of each atlas cell, or on-screen/runtime behavior. No
bundle rebuild, ISO build, emulator, or runtime validation was performed.
