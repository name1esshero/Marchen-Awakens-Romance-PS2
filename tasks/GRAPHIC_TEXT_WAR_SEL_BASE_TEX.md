# `war_sel_base_tex.b` Japanese texture text audit

## Scope and method

This read-only review covers the 17 `user_interface` rows in
`graphics/index.json` whose `asset_path` is exactly
`disc!/_DATA.YFS;1!/data/menu/war_sel_base_tex.b`. The two non-UI bundle
members are outside this audit. Every indexed TGA filename, dimension, full
SHA-256, TGA header, and pixel extent was checked. All files are uncompressed
32-bit true-color TGA (type 2), top-origin descriptor `0x28`, with exact
`18 + width × height × 4` length.

The 17 paths reduce to two distinct image hashes. The 16 small 32×16 entries
were byte-compared: all are exact duplicates, and every pixel byte is zero
(transparent black). Their shared raster was reviewed once after verifying
every path, size, and hash. The separate 128×128 `window` raster was reviewed
on an alpha-composited checkerboard at native and nearest-neighbor enlarged
scale. Bounds are in source pixels, origin at the upper-left; they describe
visible raster content, not UVs or screen placement.

## Inventory

| # | Japanese baseline TGA | Dimensions | Full-file SHA-256 | Visual finding |
| ---: | --- | ---: | --- | --- |
| 01 | `00039_01621_0001_window_jp.tga` | 128×128 | `a53fe384bbf276adaed7da83c8504a9e6968a90e3e54bd6214d89c9229e29087` | Frame/window-like bands and looped ornamental linework occupy the image; no confidently readable Japanese or English wording. The mark-like strokes remain ambiguous without context, not confirmed text. |
| 02 | `00039_01621_0003_00_gnt_jp.tga` | 32×16 | `8720a89f8e3514f73e56b01a81e03c8729d3ce2b1026148ec7256be48d2d7b5b` | Fully transparent black raster (all pixel bytes zero); no visible text. |
| 03 | `00039_01621_0004_01_dor_jp.tga` | 32×16 | `8720a89f8e3514f73e56b01a81e03c8729d3ce2b1026148ec7256be48d2d7b5b` | Exact byte duplicate of #02; fully transparent black, no visible text. |
| 04 | `00039_01621_0005_02_jac_jp.tga` | 32×16 | `8720a89f8e3514f73e56b01a81e03c8729d3ce2b1026148ec7256be48d2d7b5b` | Exact byte duplicate of #02; fully transparent black, no visible text. |
| 05 | `00039_01621_0006_03_snw_jp.tga` | 32×16 | `8720a89f8e3514f73e56b01a81e03c8729d3ce2b1026148ec7256be48d2d7b5b` | Exact byte duplicate of #02; fully transparent black, no visible text. |
| 06 | `00039_01621_0007_04_arn_jp.tga` | 32×16 | `8720a89f8e3514f73e56b01a81e03c8729d3ce2b1026148ec7256be48d2d7b5b` | Exact byte duplicate of #02; fully transparent black, no visible text. |
| 07 | `00039_01621_0008_05_nns_jp.tga` | 32×16 | `8720a89f8e3514f73e56b01a81e03c8729d3ce2b1026148ec7256be48d2d7b5b` | Exact byte duplicate of #02; fully transparent black, no visible text. |
| 08 | `00039_01621_0009_06_alv_jp.tga` | 32×16 | `8720a89f8e3514f73e56b01a81e03c8729d3ce2b1026148ec7256be48d2d7b5b` | Exact byte duplicate of #02; fully transparent black, no visible text. |
| 09 | `00039_01621_0010_07_roc_jp.tga` | 32×16 | `8720a89f8e3514f73e56b01a81e03c8729d3ce2b1026148ec7256be48d2d7b5b` | Exact byte duplicate of #02; fully transparent black, no visible text. |
| 10 | `00039_01621_0011_08_ian_jp.tga` | 32×16 | `8720a89f8e3514f73e56b01a81e03c8729d3ce2b1026148ec7256be48d2d7b5b` | Exact byte duplicate of #02; fully transparent black, no visible text. |
| 11 | `00039_01621_0012_09_gir_jp.tga` | 32×16 | `8720a89f8e3514f73e56b01a81e03c8729d3ce2b1026148ec7256be48d2d7b5b` | Exact byte duplicate of #02; fully transparent black, no visible text. |
| 12 | `00039_01621_0013_10_ror_jp.tga` | 32×16 | `8720a89f8e3514f73e56b01a81e03c8729d3ce2b1026148ec7256be48d2d7b5b` | Exact byte duplicate of #02; fully transparent black, no visible text. |
| 13 | `00039_01621_0014_11_har_jp.tga` | 32×16 | `8720a89f8e3514f73e56b01a81e03c8729d3ce2b1026148ec7256be48d2d7b5b` | Exact byte duplicate of #02; fully transparent black, no visible text. |
| 14 | `00039_01621_0015_12_fan_jp.tga` | 32×16 | `8720a89f8e3514f73e56b01a81e03c8729d3ce2b1026148ec7256be48d2d7b5b` | Exact byte duplicate of #02; fully transparent black, no visible text. |
| 15 | `00039_01621_0016_13_orc_jp.tga` | 32×16 | `8720a89f8e3514f73e56b01a81e03c8729d3ce2b1026148ec7256be48d2d7b5b` | Exact byte duplicate of #02; fully transparent black, no visible text. |
| 16 | `00039_01621_0017_14_can_jp.tga` | 32×16 | `8720a89f8e3514f73e56b01a81e03c8729d3ce2b1026148ec7256be48d2d7b5b` | Exact byte duplicate of #02; fully transparent black, no visible text. |
| 17 | `00039_01621_0018_15_edo_jp.tga` | 32×16 | `8720a89f8e3514f73e56b01a81e03c8729d3ce2b1026148ec7256be48d2d7b5b` | Exact byte duplicate of #02; fully transparent black, no visible text. |

## Findings and limits

No visible character-selection label or other confidently readable text was
found among these 17 UI textures. Sixteen named 32×16 entries export as the
same fully transparent image; the remaining window/frame texture has ornate
but unresolved linework. Empty exports do not establish why those entries are
present or whether labels are supplied by another asset or drawn dynamically.

No Japanese baseline was modified, and no English override was created. This
flat-image review does not establish UVs, draw order, semantic meaning of the
ornamental marks, runtime visibility, or screen composition. No bundle/ISO
rebuild or emulator validation was performed.
