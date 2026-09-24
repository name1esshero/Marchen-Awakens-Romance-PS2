# Effect texture text audit

Updated: 2026-09-23.

## Result

Visually reviewed all 27 indexed Japanese baselines in `graphics/effects/`.
No Japanese writing, English wording, digits, or other readable text was visible;
all 27 are effect, flame, lightning, flare, color-gradient, or frame-like imagery.
No text bounds apply. Several textures contain abstract curved or branching
strokes, but they do not form discrete readable glyphs in the exported images.
No English overrides were authored and no Japanese baseline was changed.

All 27 files are 32-bit uncompressed top-origin TGA images (type 2, descriptor
`0x28`) and their decoded dimensions and complete SHA-256 values match
`graphics/index.json`. They comprise 18 unique complete-file hashes; exact
repeated baselines are listed after the inventory. The table omits the common
`graphics/effects/` prefix.

| Japanese baseline | Dimensions | TGA bytes | SHA-256 | PSM | Visible text / bounds |
| --- | ---: | ---: | --- | --- | --- |
| `00039_00061_00009_00000_flame_00_jp.tga` | 128x64 | 32,786 | `4a4f1d61a0f60897d9fa0513f637186400481a5c619c774d838edbbad0a7d82b` | `psmt8` | None; orange/yellow flame sprite with no visible writing. |
| `00039_00100_00000_00007_thunder03_jp.tga` | 64x512 | 131,090 | `a22d8e77366ca7870f0b0cab8004ca031a3b3f6f26a54a7df1e8c981843e4c99` | `psmt8` | None; narrow yellow-white lightning stroke. |
| `00039_00110_00000_00007_thunder03_jp.tga` | 64x512 | 131,090 | `082f5704aa65202839f7ba81728b5f03c16f628dda001289f07f1cd7f4abd9cc` | `psmt8` | None; narrow blue-white lightning stroke. |
| `00039_00124_00013_00027_flame_00_jp.tga` | 128x64 | 32,786 | `db191729d8838b27fe13154ff08b66ccb22e3793416fcaee145ca3fe240b8831` | `psmt4` | None; orange/pink flame texture with no visible writing. |
| `00039_00127_00015_00013_thunder_jp.tga` | 128x256 | 131,090 | `0d9300de609ace5fad7560adbcea0cde551625fd5a92d34dd892bdd09c43c936` | `psmt4` | None; branching yellow-white lightning bolt. |
| `00039_00805_00002_flash_jp.tga` | 128x128 | 65,554 | `1012c32f10139254c96d7ca152c7f50aa574b2eb13186f8d025c147f587c238e` | `psmt4` | None; blue-centered multicolor flash burst. |
| `00039_00988_0002_flear_jp.tga` | 256x256 | 262,162 | `eb309ed460f2963bf4ac6210d252a3727a10dd3de9e9b19483e94bcd61f88cdc` | `psmt8` | None; radial blue/orange energy rays. |
| `00039_00991_0008_f_flame_jp.tga` | 64x64 | 16,402 | `208d0bdd59430b7b2fd6a2e2f0cc27e6a5bd282d83ea4b5746adfee80610a54e` | `psmt4` | None; small fire/flame sprite. |
| `00039_00991_0012_lab_bg_eff_jp.tga` | 256x256 | 262,162 | `50a46692ea1c1eaf2f61b848bc72a30abc2bc0a528e93e9409d386f3a82d4355` | `psmt4` | None; pale framed rectangular/background effect. |
| `00039_01521_0021_f_flame_jp.tga` | 64x64 | 16,402 | `23b6dc730f0153af3f8c95bc10c3ace97b0b3e9e6bbfa6190c5ca630936b0fb0` | `psmt4` | None; small fire/flame sprite; exact duplicate of `00039_01556_0005_f_flame_jp.tga`. |
| `00039_01556_0005_f_flame_jp.tga` | 64x64 | 16,402 | `23b6dc730f0153af3f8c95bc10c3ace97b0b3e9e6bbfa6190c5ca630936b0fb0` | `psmt4` | None; small fire/flame sprite; exact duplicate of `00039_01521_0021_f_flame_jp.tga`. |
| `00039_01569_0002_flear_jp.tga` | 256x256 | 262,162 | `d02da18a8d7e04320d8aaaba61bba41f953c936622818be1a14df48d68520e3b` | `psmt8` | None; colored radial energy rays. |
| `00039_01569_0008_rainbow_jp.tga` | 64x64 | 16,402 | `23e030abb8f1a44315b8980646813713bad7e1a47382f3757bb414bbbad8c609` | `psmt8` | None; small multicolor/rainbow effect. |
| `00039_01593_0003_door_eff_jp.tga` | 256x256 | 262,162 | `d22e5511ab33fd263f7e2c914dd372db888c1c40cb92855a26f8798260a29584` | `psmt8` | None; interwoven pink/white circular and spiral strokes, without discrete readable glyphs. |
| `00039_01593_0004_effect_jp.tga` | 256x256 | 262,162 | `48c17e2f5e65f72c6143e17ad3f9260691b943eb40a2618c5c8dbdc9cb084d6c` | `psmt8` | None; small white glow/flash fragment; exact duplicate of `00039_01631_0019_effect_jp.tga`. |
| `00039_01593_0005_f_flame_jp.tga` | 64x64 | 16,402 | `208d0bdd59430b7b2fd6a2e2f0cc27e6a5bd282d83ea4b5746adfee80610a54e` | `psmt4` | None; small fire/flame sprite; exact duplicate of `00039_00991_0008_f_flame_jp.tga`. |
| `00039_01596_0001_flare_jp.tga` | 512x512 | 1,048,594 | `aa682942f8fb160f919d8060c57b6b7f9a32c44ca2ca1cc7e497f663a3881b86` | `psmt8` | None; large multicolor radial/lacy flare effect, no readable characters. |
| `00039_01597_0022_safe_flame_jp.tga` | 64x64 | 16,402 | `f93f4987bb9f1fd1bf281ddc0c0ec29fb539f697c21db4cd05a20c77fcfe0e93` | `psmt8` | None; small pale flame/effect sprite; exact duplicates are listed below. |
| `00039_01621_0002_sel_flame_jp.tga` | 32x32 | 4,114 | `0591f3cd7ce8612b6e27ee2da5174a869f034653ef00a580515dddd39178803f` | `psmt4` | None; dark-blue selection/effect tile; exact duplicates are listed below. |
| `00039_01624_0031_sel_flame_jp.tga` | 32x32 | 4,114 | `0591f3cd7ce8612b6e27ee2da5174a869f034653ef00a580515dddd39178803f` | `psmt4` | None; dark-blue selection/effect tile; exact duplicates are listed below. |
| `00039_01629_0022_safe_flame_jp.tga` | 64x64 | 16,402 | `f93f4987bb9f1fd1bf281ddc0c0ec29fb539f697c21db4cd05a20c77fcfe0e93` | `psmt8` | None; small pale flame/effect sprite; exact duplicates are listed below. |
| `00039_01631_0019_effect_jp.tga` | 256x256 | 262,162 | `48c17e2f5e65f72c6143e17ad3f9260691b943eb40a2618c5c8dbdc9cb084d6c` | `psmt8` | None; small white glow/flash fragment; exact duplicate of `00039_01593_0004_effect_jp.tga`. |
| `00039_01631_0022_rainbow_jp.tga` | 64x64 | 16,402 | `70244888276b7379fca0bca7b0895a42bde761e411e0f1233a2187567c072705` | `psmt8` | None; rainbow gradient texture; exact duplicates are listed below. |
| `00039_01632_0000_rainbow_jp.tga` | 64x64 | 16,402 | `70244888276b7379fca0bca7b0895a42bde761e411e0f1233a2187567c072705` | `psmt8` | None; rainbow gradient texture; exact duplicates are listed below. |
| `00039_01633_00000_rainbow_jp.tga` | 64x64 | 16,402 | `70244888276b7379fca0bca7b0895a42bde761e411e0f1233a2187567c072705` | `psmt8` | None; rainbow gradient texture; exact duplicates are listed below. |
| `00039_01635_0049_safe_flame_jp.tga` | 64x64 | 16,402 | `f93f4987bb9f1fd1bf281ddc0c0ec29fb539f697c21db4cd05a20c77fcfe0e93` | `psmt8` | None; small pale flame/effect sprite; exact duplicates are listed below. |
| `00039_01635_0050_sel_flame_jp.tga` | 32x32 | 4,114 | `0591f3cd7ce8612b6e27ee2da5174a869f034653ef00a580515dddd39178803f` | `psmt4` | None; dark-blue selection/effect tile; exact duplicates are listed below. |

## Exact duplicate groups

Identical complete-file hashes make these instances the same raster bytes, not
merely visually similar textures:

- SHA-256 `208d0bdd59430b7b2fd6a2e2f0cc27e6a5bd282d83ea4b5746adfee80610a54e`: `00039_00991_0008_f_flame_jp.tga`, `00039_01593_0005_f_flame_jp.tga`.
- SHA-256 `23b6dc730f0153af3f8c95bc10c3ace97b0b3e9e6bbfa6190c5ca630936b0fb0`: `00039_01521_0021_f_flame_jp.tga`, `00039_01556_0005_f_flame_jp.tga`.
- SHA-256 `48c17e2f5e65f72c6143e17ad3f9260691b943eb40a2618c5c8dbdc9cb084d6c`: `00039_01593_0004_effect_jp.tga`, `00039_01631_0019_effect_jp.tga`.
- SHA-256 `f93f4987bb9f1fd1bf281ddc0c0ec29fb539f697c21db4cd05a20c77fcfe0e93`: `00039_01597_0022_safe_flame_jp.tga`, `00039_01629_0022_safe_flame_jp.tga`, `00039_01635_0049_safe_flame_jp.tga`.
- SHA-256 `0591f3cd7ce8612b6e27ee2da5174a869f034653ef00a580515dddd39178803f`: `00039_01621_0002_sel_flame_jp.tga`, `00039_01624_0031_sel_flame_jp.tga`, `00039_01635_0050_sel_flame_jp.tga`.
- SHA-256 `70244888276b7379fca0bca7b0895a42bde761e411e0f1233a2187567c072705`: `00039_01631_0022_rainbow_jp.tga`, `00039_01632_0000_rainbow_jp.tga`, `00039_01633_00000_rainbow_jp.tga`.

## Review method and limits

The file set was selected from the 27 filesystem TGAs and cross-checked against
all `effects/` records in `graphics/index.json`. TGA headers were validated;
every full-file hash and dimension agrees with its index record. All assets were
decoded in top-origin RGBA order, alpha-composited on a checkerboard, and
reviewed in labeled nearest-neighbor contact sheets. Tall or larger lightning,
door-effect, lab-background, and flare images were also inspected separately at
an enlarged scale. Exact duplicate hashes were recorded, while all 27 paths remain
individually inventoried above.

These are visual observations of flat exported textures only. The audit does not
establish how an effect is cropped, animated, layered, tinted, or drawn at runtime,
and makes no UV or screen-use claims. It found no confirmed translation-bearing
surface in this category, so no English override is recommended from this
texture-only evidence.

References: `graphics/index.json`, `tools/rtx3.py`,
[`localization methodology`](../docs/LOCALIZATION_METHODOLOGY.md),
[`title texture rendering evidence`](TITLE_TEXTURE_RENDERING.md),
[`background texture audit`](GRAPHIC_TEXT_BACKGROUNDS.md).
