# `top_tex.b` Japanese texture audit

## Scope and method

This is a read-only visual/catalogue audit of the 12 `graphics/index.json`
entries whose `asset_path` is exactly
`disc!/_DATA.YFS;1!/data/menu/top_tex.b`. All rows point into
`00039.asset/01569.resources`. Every indexed TGA was opened and visually
reviewed, including close inspection of the compact lettering atlases. The
previews composite the stored alpha over a temporary checkerboard and use
nearest-neighbor enlargement; the tracked TGA files were not changed.

For each row, the filename, dimensions, and complete SHA-256 below match the
indexed `image`, `width`, `height`, and `image_sha256`. All files are uncompressed
type-2, 32-bit, top-origin TGAs (descriptor `0x28`) of exactly
`18 + width * height * 4` bytes. There are 12 distinct image hashes, totaling
3,244,248 TGA bytes.

## Inventory and visual findings

| Japanese baseline | Dimensions | SHA-256 | Visual finding |
| --- | ---: | --- | --- |
| `00039_01569_0000_ch_00_03_jp.tga` | 512×512 | `a2dd05447566482b80880eb5b56002ca7e596176e8108def359f23ee88d90854` | Four character cutouts. No confidently readable wording. One costume chest patch has tiny dark marks; they are too small/contextless to classify as text. |
| `00039_01569_0001_ch_04_07_jp.tga` | 512×512 | `0002f9dbbf0be5f8be6a64a5486b7e067741dd360733ddef2ef587c260e15f33` | Four character cutouts; no confidently readable text. Clothing details are not treated as lettering. |
| `00039_01569_0002_flear_jp.tga` | 256×256 | `d02da18a8d7e04320d8aaaba61bba41f953c936622818be1a14df48d68520e3b` | Colored flare/ray effect; no text. |
| `00039_01569_0003_icon_jp.tga` | 256×256 | `5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9` | Translation-bearing mixed control/text atlas. Japanese prompt/menu groups occupy broad bounds x=130–253, y=3–125, plus a mixed text area x=35–254, y=131–200. It also contains recognizable Latin labels (`R1`, `R2`, `L1`, `L2`, `ARM`, `GET`, `START`, `SELECT`), face buttons, and directional controls. Japanese wording was not transcribed without screen context. |
| `00039_01569_0004_juel_jp.tga` | 128×64 | `c2de96c2becdbb6ff959db3fc363af5e604324cbe5c6d0901590b58fd4d40fb4` | Eight colored orb/gem marks in two rows (alpha bounds x=6–121, y=6–25 and y=38–57); no text. |
| `00039_01569_0005_mg_scroll_jp.tga` | 256×32 | `adcd246e4d05445dff3f6999d0e6d4e9b3b4c8728652522bf7fc7d01ca87c96e` | Japanese sentence/label in a narrow blue strip; visible ink spans approximately x=0–255, y=5–25. It is too small and contextless here for a confident transcription. |
| `00039_01569_0006_mnmn_jp.tga` | 256×64 | `3dc57d8c485aef57bd05c35820bc2e8bdd61c9add6983560c5bf65c5fe4badfa` | Stylized katakana menu heading, read as `メニュー` (“Menu”), with a colored extruded/shadow treatment. Alpha-qualified text bounds x=2–253, y=15–57. |
| `00039_01569_0007_modename_jp.tga` | 256×128 | `c7bcfd31a391fab7557dffbd88c68ad92a926690da491a6358f6583cc92992da` | Japanese/Latin menu-mode label atlas. Four paired rows occupy approximately x=14–250, y=3–109; the bottom horizontal graphic at x=0–182, y=117–124 is not lettering. `ARM` is visible among the existing Latin wording. Individual Japanese labels remain untranslated pending contextual confirmation. |
| `00039_01569_0008_rainbow_jp.tga` | 64×64 | `23e030abb8f1a44315b8980646813713bad7e1a47382f3757bb414bbbad8c609` | Small color-transition/effect texture; no text. |
| `00039_01569_0009_sky_jp.tga` | 256×256 | `86eaf58abfe865cac8932c2b77313738a4f756f7126889360d40947ca1275179` | Cloud/sky background; no visible lettering. |
| `00039_01569_0010_trns_jp.tga` | 64×64 | `2eda80d4f411d76cef992dd5d8429ffec5c7f82b07452605a9a33fd34af11c76` | Vertical color/alpha gradient; no text. |
| `00039_01569_0011_window_jp.tga` | 128×128 | `a53fe384bbf276adaed7da83c8504a9e6968a90e3e54bd6214d89c9229e29087` | Four distinct outlined Japanese label rows. Alpha-qualified inclusive bounds: (1,1)–(100,26), (1,45)–(99,70), (5,76)–(122,98), and (0,110)–(127,123). Exact readings need menu context. |

For `icon`, the top prompt-like Japanese groups are around x=130–253, y=3–49;
additional mixed Japanese and Latin text rows occupy the right/lower-right
section down to y=227. The broad bound above avoids assigning glyphs to a
specific menu choice based on the isolated atlas. For `modename`, the visible
alpha-connected row bounds are x=31–250/y=3–25, x=23–249/y=32–53,
x=18–248/y=60–81, and x=14–250/y=87–109.

## Result and limits

Five clear text-bearing assets need contextual follow-up: the Japanese
control/menu copy in `icon`, the scrolling Japanese line in `mg_scroll`, and
the heading or label rows in `mnmn`, `modename`, and `window`. These should be
compared with catalogued menu strings and their rendering context before
drafting English siblings. The character sheets contain only an unresolved
tiny costume mark, not confirmed text; the remaining effect, orb, sky, and
gradient textures contain no visible wording.

This audit does not identify texture UVs, screen composition, animation use, or
runtime visibility. It makes no translation or rendering acceptance claim.
All `_jp.tga` baselines remain unchanged; no English override, bundle, ISO, or
runtime artifact was created or tested.
