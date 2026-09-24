# `lib_char_sum.b` character-summary texture audit

## Scope and method

This read-only audit covers exactly the 16 `characters` rows in
`graphics/index.json` whose `asset_path` is
`disc!/_DATA.YFS;1!/data/menu/lib_char_sum.b`. Each mapped Japanese TGA was
opened individually in its indexed top-origin pixel order and visually
reviewed as a 4× nearest-neighbor enlargement over a temporary checkerboard.
The images are 64×64 pixel portraits/cropped character artwork, not an atlas
of wording.

Every filename, dimension, and complete TGA SHA-256 below matches the index.
All 16 are uncompressed true-color TGA image type 2 with no color map, 32 bits
per pixel, top-origin descriptor `0x28`, and the exact extent
`18 + 64 × 64 × 4 = 16,402` bytes. Every alpha sample is 255. The 16 full-file
hashes are distinct and the files total 262,432 bytes. Bounds are omitted
because no text-bearing region was found.

## Inventory and visual findings

| Japanese baseline TGA | Dimensions; extent | Full-file SHA-256 | Visual finding |
| --- | ---: | --- | --- |
| `00039_01518_0000_chr_s000_jp.tga` | 64×64; 16,402 B | `5a46cb4a0f4965fe873306cdd0d8b77992c38edbe6703291521ae044c16f41e6` | Close-cropped face with bright yellow/blond hair; no visible writing. |
| `00039_01518_0001_chr_s001_jp.tga` | 64×64; 16,402 B | `c4c98b567745d3abcd76e4f2b7ed6e5063cc3a55d24bff31be717ea82049ec9c` | Pink-haired face with blue eyes and a pale collar; no visible writing. |
| `00039_01518_0002_chr_s002_jp.tga` | 64×64; 16,402 B | `0d96941a9d9dfa837c29ba54efe17e7e80f16fa50cbe9543adb957b0c0e98cb3` | Dark-haired face with heavy brows and exposed ears; no visible writing. |
| `00039_01518_0003_chr_s003_jp.tga` | 64×64; 16,402 B | `5d53cb077b7ee4d8e4f0119b0405dd6fd531dd332c705f296f7c8d03f23c8ab1` | Blue-haired face with green eyes and an open mouth; no visible writing. |
| `00039_01518_0004_chr_s004_jp.tga` | 64×64; 16,402 B | `dfe115830c44c55c8f913183f7b3873d199fe7a547ea24249261a345a89ad59e` | Dark-haired, lined face with a subdued expression; no visible writing. |
| `00039_01518_0005_chr_s005_jp.tga` | 64×64; 16,402 B | `45322fe6e5c8aabc0b271ab49b5f4f44f08ba9d872ad837e8eee079d723cb7e9` | Blond-haired face with a red forehead band and blue garment; no visible writing. |
| `00039_01518_0006_chr_s006_jp.tga` | 64×64; 16,402 B | `85d6376b89073fed88719624d6f0e46b8429dd4708a03a55fe5bb9c12be79ae1` | Dark-purple-haired face with blue eyes; no visible writing. |
| `00039_01518_0007_chr_s007_jp.tga` | 64×64; 16,402 B | `b1b8456ba3ca076451f4d69b9020a63c11a13b5969e2fd6a27e050a37711eac8` | Pale-haired face with blue square-shaped eyes and red side details; no visible writing. |
| `00039_01518_0008_chr_s008_jp.tga` | 64×64; 16,402 B | `c65967e77fe09484027862e708c8734ea46bd6f4969559e977f586cac56d14ee` | Face partly obscured by black hair or shadow; no visible writing. |
| `00039_01518_0009_chr_s009_jp.tga` | 64×64; 16,402 B | `16726535ddb29ef34fb42e656561436fc8e51a752b4757c8a5730e8814c0131b` | Stylized pale mask-like face with purple hair and red eyes; no visible writing. |
| `00039_01518_0010_chr_s013_jp.tga` | 64×64; 16,402 B | `f25982346f885bb87901ed895abe60a06e6afd7623bc3686093eb62662dcb5bf` | Exaggerated gray face with large round eyes and exposed teeth; no visible writing. |
| `00039_01518_0011_chr_s010_jp.tga` | 64×64; 16,402 B | `9f696714b70dd121c15f14540e18ae2fb52df2b6367b1537c9f410cd5a4d9516` | Light-brown-haired face with a blue collar; no visible writing. |
| `00039_01518_0012_chr_s014_jp.tga` | 64×64; 16,402 B | `4ee7856791c1b9d341a6b857ef5b0582ea39f59a93363e16b961cd587a25aa84` | Brown-haired face with a red/gray diagonal facial marking; the marking reads as character artwork, not lettering. |
| `00039_01518_0013_chr_s011_jp.tga` | 64×64; 16,402 B | `8aa4b7ede6196c7d6e30a50e442815e63be2dd344397e78c778f1ed52e6805d0` | Red rounded mask/creature face with yellow eyes and green/white upper details; no visible writing. |
| `00039_01518_0014_chr_s012_jp.tga` | 64×64; 16,402 B | `823a2509d35b1e332a5b75c6bbb664e44023b0c6f13bc74fa66b83dca727de55` | Pale lavender-haired face in profile-like framing; no visible writing. |
| `00039_01518_0015_chr_s015_jp.tga` | 64×64; 16,402 B | `73e4034c4aab0b8fac76f13ab2f3fd6144469f891452ebe7437fe61b9703ed81` | Face behind oversized pale circular goggles or lenses; no visible writing. |

## Findings and limits

The scoped images are distinct character portrait artwork. None contains
readable Japanese or Latin names, captions, labels, or title marks in the
exported pixels. The facial mark in `chr_s014` and details on the mask-like
portraits are visual art, not supported text candidates. No Japanese baseline
was modified and no English override was created.

This review establishes only the visible contents of the 16 exported TGAs. It
does not identify characters by name or establish UVs, draw order, runtime
visibility, or screen composition. No bundle/ISO rebuild or emulator test was
performed.

References: `graphics/index.json`,
[`localization methodology`](../docs/LOCALIZATION_METHODOLOGY.md), and
[`lib_main_tex.b texture audit`](GRAPHIC_TEXT_LIB_MAIN_TEX.md).
