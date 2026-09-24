# `lib_voice_sum.b` character voice-summary texture audit (DQ-41)

## Scope and method

This is a read-only visual audit of exactly the 16 `characters` rows in
`graphics/index.json` whose `asset_path` is
`disc!/_DATA.YFS;1!/data/menu/lib_voice_sum.b`. Every indexed TGA was reviewed
in a numbered contact sheet, then the repeated pale balloon-like region was
inspected at nearest-neighbor enlargement. Previews used the stored RGBA data
over a temporary checkerboard; the source images are actually fully opaque
(all alpha samples are 255). No Japanese baseline, index, override, bundle, or
ISO was edited or built.

Each filename, dimension, and complete TGA SHA-256 below matches its index
row and was recomputed from the file. All 16 files are uncompressed type-2,
32-bit TGAs with descriptor `0x28`, zero ID/color-map fields, and zero x/y
origin. Their headers declare 64×64 pixels and each file has the exact extent
`18 + 64 * 64 * 4 = 16,402` bytes. The 16 TGA hashes are unique; the set
totals 262,432 bytes and has no image-hash duplicates among the 16 DQ-40
`lib_char_sum.b` rows.

## Inventory and visual findings

| Japanese baseline | Dimensions | TGA extent | SHA-256 | Visual finding |
| --- | ---: | ---: | --- | --- |
| `00039_01537_0000_voi_s000_jp.tga` | 64×64 | 16,402 bytes | `e184c71e6a4d51a37506e88b33d3e8568ccee31636ea9903abfa75a68e42c0dd` | Character portrait with a pale balloon-like overlay; no readable Japanese or Latin name/voice text. The overlay marks remain unresolved; see aggregate finding below. |
| `00039_01537_0001_voi_s001_jp.tga` | 64×64 | 16,402 bytes | `17c2d4993041c146d6c47365dd155cf56f18e029ddc94e62ad732db37ec806f6` | Character portrait with a pale balloon-like overlay; no readable Japanese or Latin name/voice text. The overlay marks remain unresolved; see aggregate finding below. |
| `00039_01537_0002_voi_s002_jp.tga` | 64×64 | 16,402 bytes | `194657cadd8f8d66c632bb541501b461d856ee4c9bae43a07c34a2f4070d3984` | Character portrait with a pale balloon-like overlay; no readable Japanese or Latin name/voice text. The overlay marks remain unresolved; see aggregate finding below. |
| `00039_01537_0003_voi_s003_jp.tga` | 64×64 | 16,402 bytes | `4b424555ff17d9dacef08d0f4c7c6843993532963a21ee2fafa4c9be29aab45e` | Character portrait with a pale balloon-like overlay; no readable Japanese or Latin name/voice text. The overlay marks remain unresolved; see aggregate finding below. |
| `00039_01537_0004_voi_s004_jp.tga` | 64×64 | 16,402 bytes | `8e4133f4ba431496c10321f50dd05a9a6b87b5401a907055bc2f996eac397eb8` | Character portrait with a pale balloon-like overlay; no readable Japanese or Latin name/voice text. The overlay marks remain unresolved; see aggregate finding below. |
| `00039_01537_0005_voi_s005_jp.tga` | 64×64 | 16,402 bytes | `d962d21bd43efd0dd4ef51a801ca63b9b6755f2d8929e8a945c362bcc7a8e54e` | Character portrait with a pale balloon-like overlay; no readable Japanese or Latin name/voice text. The overlay marks remain unresolved; see aggregate finding below. |
| `00039_01537_0006_voi_s006_jp.tga` | 64×64 | 16,402 bytes | `e816d17344b7165b7e9df1d2997925029c595ea0fa42504378a4a5c3db792c7b` | Character portrait with a pale balloon-like overlay; no readable Japanese or Latin name/voice text. The overlay marks remain unresolved; see aggregate finding below. |
| `00039_01537_0007_voi_s007_jp.tga` | 64×64 | 16,402 bytes | `80b570dcf79464457709cad1d7c6cc86fb1a5812cde0cc5d69f4051fdb288cca` | Character portrait with a pale balloon-like overlay; no readable Japanese or Latin name/voice text. The overlay marks remain unresolved; see aggregate finding below. |
| `00039_01537_0008_voi_s008_jp.tga` | 64×64 | 16,402 bytes | `dd1a1d5ef422f04c5c812f751971f9137909a13fd7c9ebaa44e71f83391bf2a8` | Character portrait with a pale balloon-like overlay; no readable Japanese or Latin name/voice text. The overlay marks remain unresolved; see aggregate finding below. |
| `00039_01537_0009_voi_s009_jp.tga` | 64×64 | 16,402 bytes | `752675b84298111fbc055c3e7e6fc46f00e61f63372d12d5311edd59dc5b5a55` | Character portrait with a pale balloon-like overlay; no readable Japanese or Latin name/voice text. The overlay marks remain unresolved; see aggregate finding below. |
| `00039_01537_0010_voi_s013_jp.tga` | 64×64 | 16,402 bytes | `e09572f370cb5524fe4e30dbe6814324fb6a3e4c1c8adbd8eb7f01de530c43af` | Character portrait with a pale balloon-like overlay; no readable Japanese or Latin name/voice text. The overlay marks remain unresolved; see aggregate finding below. |
| `00039_01537_0011_voi_s010_jp.tga` | 64×64 | 16,402 bytes | `1f4fafbf14effbcba78c80ddff3eb7de2d01407839b468ce652fab175238528e` | Character portrait with a pale balloon-like overlay; no readable Japanese or Latin name/voice text. The overlay marks remain unresolved; see aggregate finding below. |
| `00039_01537_0012_voi_s014_jp.tga` | 64×64 | 16,402 bytes | `449819cd5ea6c1ee676e20e7914b3a7a300e01890a415fad94a9a7e4a7f9d229` | Character portrait with a pale balloon-like overlay; no readable Japanese or Latin name/voice text. The overlay marks remain unresolved; see aggregate finding below. |
| `00039_01537_0013_voi_s011_jp.tga` | 64×64 | 16,402 bytes | `ecc9ac979d92288e18aabc06fb2253b428c8e654eb46686e2cea74f28e7fc22d` | Character portrait with a pale balloon-like overlay; no readable Japanese or Latin name/voice text. The overlay marks remain unresolved; see aggregate finding below. |
| `00039_01537_0014_voi_s012_jp.tga` | 64×64 | 16,402 bytes | `1afc97bdfd02fe9e52a2787352637ee28771249d280e7f9a2c59fe2b141d447e` | Character portrait with a pale balloon-like overlay; no readable Japanese or Latin name/voice text. The overlay marks remain unresolved; see aggregate finding below. |
| `00039_01537_0015_voi_s015_jp.tga` | 64×64 | 16,402 bytes | `8e4c85185ea49ff47ae6de518c819f9b4b6b4588e80c071cc9fe7618357050b3` | Character portrait with a pale balloon-like overlay; no readable Japanese or Latin name/voice text. The overlay marks remain unresolved; see aggregate finding below. |

## Result and limits

All 16 images are distinct close-up character portraits. Each has a small
pale, rounded balloon-like shape near the upper-left with a short cluster of
gray dash/dot strokes. Across the set, the marks fit approximately within
x=[5,28), y=[16,20) in raster coordinates. Enlarging the strokes did not
reveal kana, kanji, or Latin words; they remain unclassified rather than being
treated as Japanese voice copy. No character names or other readable labels
appear in the reviewed pixels. The separate image SHA-256 values also confirm
these are not duplicates of DQ-40's character-summary images.

This flat-image audit does not establish what the portrait set represents at
runtime, whether the marks encode an animation or state, or how the textures
are mapped to a screen. Bounds are approximate raster-space regions for the
unresolved strokes, not UV coordinates. No translation, texture import,
container rebuild, ISO, or emulator validation was performed. All `_jp.tga`
baselines remain unchanged; no English override was created.

References: [`graphics/index.json`](../graphics/index.json),
[`LOCALIZATION_METHODOLOGY.md`](../docs/LOCALIZATION_METHODOLOGY.md), and the
indexed source bundle `disc!/_DATA.YFS;1!/data/menu/lib_voice_sum.b`.
