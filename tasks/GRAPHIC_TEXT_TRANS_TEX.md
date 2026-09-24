# `trans_tex.b` Japanese texture text audit

## Scope and method

This read-only audit covers exactly the three `user_interface` rows in
`graphics/index.json` whose `asset_path` is
`disc!/_DATA.YFS;1!/data/menu/trans_tex.b`. Every scoped TGA was checked against
its indexed path, dimensions and complete SHA-256, then visually reviewed on a
checkerboard preview. The circular emblem was also inspected at enlarged,
nearest-neighbor scale to distinguish the small ring marks from readable text.

All three files have an 18-byte TGA header with image type 2 (uncompressed
true-color), 32 bits per pixel, descriptor `0x28` (top-origin with 8 alpha
bits), and exact `18 + width × height × 4` extents. Bounds use source-image
pixel coordinates and half-open intervals; the bounds of glyph-like marks are
visual estimates, not segmentation evidence.

## Findings

No confidently readable Japanese or English wording appears in these three
exports. The largest image contains a circular magenta/white emblem with a
central plus and arch-like symbol. Small irregular glyph-like marks follow its
rings, but they do not form a confident transcription and remain unresolved.
The second image is a monochrome radial mask/emblem with transparent cutouts;
the third is a uniform white swatch.

| Indexed Japanese texture | Dimensions | SHA-256 | Source TXC SHA-256 | Visual finding |
|---|---:|---|---|---|
| `00039_01596_0000_gt_grdn_jp.tga` | 512×512 | `7a4e40404a15c8822d1d060ca957de2ae1bbf45376239262710cc3044637d69e` | `f0fa3e5e1b32ab020a9d8c37dec6ea67da35d66ff8a3fbc4a8b65dbc0c0b40e4` | Circular magenta/white emblem; whole nontransparent artwork bounds are `[87,433)×[6,501)`. Irregular rune-like marks follow the circular bands, approximately within `[95,425)×[17,490)`. No word is confidently readable; retain the marks as an unresolved candidate, not confirmed Japanese text. |
| `00039_01596_0002_crown_mask_jp.tga` | 512×512 | `2c2fe94ad838f7d5f41417d2c406df10fa37bd6e82b9c9c59a0e39d7813031b8` | `e260b4e32c7e3e3fbbaeef4297e0f1dae618c094e7c556a8760a8816f8b23a38` | Black-channel radial mask with transparent central cutouts and a crown/face-like silhouette; alpha-bearing field spans `[0,512)×[0,512)`. No visible wording. |
| `00039_01596_0003_mat_jp.tga` | 16×16 | `1d6c155e8c3e7aa5efcbeb4c9adf0b205b07118daa93c9c03491bcba58e4eaf0` | `0df3b2c134bec6c08e9deb247fb0d60119585f776c7c935ba0e00bd5d0ccb61e` | Fully opaque uniform white 16×16 swatch; no text. |

## Limits

This is a flat-image audit of these three indexed exports only. It does not
establish the purpose of the glyph-like ring, UV placement, draw order, screen
composition, animation, or runtime use. No Japanese baseline, index, override,
bundle, ISO, or build output was changed; no translation override was authored.
