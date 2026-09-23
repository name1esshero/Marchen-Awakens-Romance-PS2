# Map texture text audit

Updated: 2026-09-23.

## Result

Reviewed all 16 tracked `_jp.tga` files in `graphics/maps/` against their
`graphics/index.json` records and visualized the full textures on a checkerboard
contact sheet. The six 256x256 `maze_lv` images show layered maze-like linework
and a spiral motif; no writing or Japanese labels were visible. The ten 64x64
`hdmp` thumbnails show a framed map-like graphic with a centered Arabic numeral
1 through 10. No Japanese characters or words are visible. These numerals are
language-neutral markers, not Japanese text to translate. No English overrides
were authored because this audit found no Japanese text-bearing map surface.

All entries are PSMT8 bundle textures. The `maze_lv1` through `maze_lv6` assets
map to `disc!/_DATA.YFS;1!/data/menu/Laby_BG_tex.b`; the ten `hdmp` assets map to
`disc!/_DATA.YFS;1!/data/menu/lib_map_sum.b`. The table omits the common
`graphics/maps/` directory prefix. SHA-256 values below cover each complete TGA.

Text bounds use a zero-based top-left origin and half-open `[x0,x1) × [y0,y1)`
coordinates. For the white numeral marks, the recorded bounds include pixels
with decoded RGBA alpha >= 128 and each RGB component >= 180; visual review
confirmed these bounds around the numerals. `none` means no visible text was
found in the reviewed image.

| Asset | Dimensions | TGA bytes | SHA-256 | Visible text / bounds |
| --- | ---: | ---: | --- | --- |
| `00039_00991_0018_maze_lv1_jp.tga` | 256x256 | 262,162 | `06a785fe64b63182cb91c9b319b07bcc16acfdd63e20386f12b9308e5a030ebd` | None; maze-like linework |
| `00039_00991_0019_maze_lv2_jp.tga` | 256x256 | 262,162 | `5e189e8f6af8206e56f0fa6f8509ed1bdda1530a9717f03d043960e935784b46` | None; maze-like linework |
| `00039_00991_0020_maze_lv3_jp.tga` | 256x256 | 262,162 | `885b6acaaec1b967b954b92075d3b690bd750fb5a6d296ee4c482ddd8dff1262` | None; maze-like linework |
| `00039_00991_0021_maze_lv4_jp.tga` | 256x256 | 262,162 | `2f5cd4c54aaaddc7a18b264cd10d734ea53a89074be24738cc8ff7e9fa45b220` | None; maze-like linework |
| `00039_00991_0022_maze_lv5_jp.tga` | 256x256 | 262,162 | `4556101cbb69f7541bd3d0f587bb51799e01af48d24327fc76662a899567488d` | None; maze-like linework |
| `00039_00991_0023_maze_lv6_jp.tga` | 256x256 | 262,162 | `c67139bceb3d8335a36c9f916452a30273f82276d27f687baf1b0ce3a6240067` | None; maze-like linework |
| `00039_01522_0000_hdmp_01_jp.tga` | 64x64 | 16,402 | `a129c6c1ec468914d103b423c9c4211399d535cb15ade0c7d333c74a254acf3b` | `1`; x=[26,34), y=[22,43) |
| `00039_01522_0001_hdmp_02_jp.tga` | 64x64 | 16,402 | `59167e6a7288625dc22df91b1369519f91c8e7527ddf778c2e5b1228d3633f4f` | `2`; x=[23,38), y=[21,43) |
| `00039_01522_0002_hdmp_03_jp.tga` | 64x64 | 16,402 | `ca487f5d21c15336ced8e442a53b64772b6048c12567ddd0209a2795a9787863` | `3`; x=[24,38), y=[22,44) |
| `00039_01522_0003_hdmp_04_jp.tga` | 64x64 | 16,402 | `bfdc957d2d26844fca42ea24c9bfdca55cbf09c9f35da77ef6bff0cda4d1cab7` | `4`; x=[23,38), y=[22,43) |
| `00039_01522_0004_hdmp_05_jp.tga` | 64x64 | 16,402 | `9efba2a0f61fcf7ae859c4b8abf8c292f32c45cc17a0305d405a77eefa0dec9c` | `5`; x=[24,38), y=[22,44) |
| `00039_01522_0005_hdmp_06_jp.tga` | 64x64 | 16,402 | `32c37cff6061455fd1f45c4e2d303866a5bbac34a714667391e0f9cc2d418bc5` | `6`; x=[23,38), y=[22,44) |
| `00039_01522_0006_hdmp_07_jp.tga` | 64x64 | 16,402 | `0844598e9ebe6a57279851be9c0c91a3ea97a541327ac31f4047842e97b8c291` | `7`; x=[23,38), y=[22,43) |
| `00039_01522_0007_hdmp_08_jp.tga` | 64x64 | 16,402 | `47bcde3c1debeac6af1893ff4d23f4a075e136ddf0523847016a44ecfa475b19` | `8`; x=[23,38), y=[21,44) |
| `00039_01522_0008_hdmp_09_jp.tga` | 64x64 | 16,402 | `acf4b1bb5852bf33bfcb2bab517ad7c151e952453c5ad3f9dafa97476474ae34` | `9`; x=[23,38), y=[21,43) |
| `00039_01522_0009_hdmp_10_jp.tga` | 64x64 | 16,402 | `f24a7870bf8dafc1ff84d6421adb8db50d7378d5d69e10c26417e31759665d7f` | `10`; x=[17,48), y=[21,44) |

## Verification and limits

An inventory check confirmed exactly 16 tracked map TGAs and a one-to-one set of
16 `maps/` records in `graphics/index.json`. For every file, decoded dimensions
and the complete TGA SHA-256 match the corresponding index record; all 16 are
indexed there as PSMT8 bundle resources. Each image was visually reviewed at
native scale or nearest-neighbor enlargement. The six maze textures were viewed
at 2x and the ten 64x64 thumbnails at 4x on a transparency checkerboard.

These observations classify only the flat exported textures. They do not prove
what the numbered thumbnails mean, how any image is cropped or layered at
runtime, or which map/screen displays it. No Japanese baseline was edited and
no runtime/UV conclusions are made.

References: `graphics/index.json`, `tools/rtx3.py`,
[`LOCALIZATION_METHODOLOGY.md`](../docs/LOCALIZATION_METHODOLOGY.md),
[`TITLE_TEXTURE_RENDERING.md`](TITLE_TEXTURE_RENDERING.md),
[`FAILURES.md`](../docs/FAILURES.md).
