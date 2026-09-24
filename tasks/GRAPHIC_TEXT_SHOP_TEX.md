# `shop_tex.b` UI texture audit

## Scope and method

This read-only review covers only the six `graphics/index.json` rows whose
`asset_path` is exactly `disc!/_DATA.YFS;1!/data/menu/shop_tex.b` and whose
category is `user_interface`. Other bundle categories are excluded, including
`text/00039_01556_0014_subtitle_jp.tga`, the separate three-action shop-text
surface already documented in the localization work.

All six Japanese TGA paths were viewed at source orientation with alpha shown
against a checkerboard; small surfaces were enlarged with nearest-neighbor
scaling. Bounds below are inclusive source-pixel coordinates. The filename,
dimensions, and complete SHA-256 for each TGA match its `graphics/index.json`
row. Every file is an uncompressed type-2, 32-bit, top-origin TGA (descriptor
`0x28`) with exact `18 + width * height * 4` byte extent. This subset has six
distinct image hashes and totals 491,628 TGA bytes.

## Inventory and visual findings

| Japanese baseline | Dimensions | SHA-256 | Visual finding |
| --- | ---: | --- | --- |
| `00039_01556_0004_equip_jp.tga` | 128×32 | `aaa7994fa1984beb3494ecf3b0cf036bfb383868e5c8adb187fc941a38c85ef9` | Japanese lettering occupies the upper band, alpha≥128 bounds (2,3)–(124,19); no confident transcription from this isolated strip. The horizontal lower rule/frame is (1,23)–(126,29), not a text row. |
| `00039_01556_0007_faceshop_jp.tga` | 128×128 | `5cdfc64638a6eab52148ac6d4d40d190930aff9bd58bdbf03bfcefb101cb4c8a` | 4×4 character-face icon grid with the final cell blank; no visible wording. |
| `00039_01556_0010_shop_jp.tga` | 256×64 | `5b2eb9c9dfadf4975a3494e8b9f6567de5206e88653915678ccac0f2e30323c1` | Gradient wordmark reads `ARMショップ` (“ARM Shop”); full alpha≥128 bounds (1,6)–(191,57). An `_eng.tga` sibling already exists and is not changed by this audit. |
| `00039_01556_0011_shop_girl_jp.tga` | 256×256 | `d371cbed59f31728b95f5df26385071d8b14cb2d5f78a4f3d132b8c2d1d219e9` | Female character portrait; no visible wording. |
| `00039_01556_0015_wdw_pause_jp.tga` | 64×64 | `82c7db0e0c8f17c30e5b5cca0b146e0b4427f9d0db5f0dfc98ec0001f588a8c0` | Three Japanese label rows, not confidently transcribed. Alpha≥128 bounds: (1,1)–(50,13), (0,23)–(49,35), and (3,38)–(60,49). The lower horizontal strip at (0,55)–(63,61) is a frame/band. |
| `00039_01556_0016_window_jp.tga` | 128×128 | `a53fe384bbf276adaed7da83c8504a9e6968a90e3e54bd6214d89c9229e29087` | Three Japanese-looking outlined label rows, with no confident reading. Alpha≥128 bounds: (1,1)–(100,26), (1,45)–(99,70), and (5,76)–(122,98). The bottom band at (0,110)–(127,123) is a frame, not a fourth row. Its full hash is shared by window textures in other menu bundles. |

## Result and limits

The `equip`, `wdw_pause`, and `window` images expose Japanese text candidates;
the `shop` wordmark contains Japanese `ショップ` alongside existing Latin
`ARM` lettering and already has a localized sibling. The face grid and shop
portrait contain no readable words. The six-file scope does not include the
previously translated `subtitle` action rows, and no wording or row placement
is inferred from that separate resource.

This review does not establish UV rectangles, draw order, screen composition,
animation, or runtime visibility. Japanese baselines remain unchanged. No
override, bundle, ISO, or emulator result was created or tested.
