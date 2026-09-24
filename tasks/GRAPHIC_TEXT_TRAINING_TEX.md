# `train_tex.b` Japanese texture text audit

## Scope and method

This read-only audit covers every Japanese TGA row in `graphics/index.json` whose `asset_path` is exactly `disc!/_DATA.YFS;1!/data/menu/train_tex.b`: 11 Japanese TGA exports. The task is to identify visible text-bearing artwork, record useful bounds and uncertainties, and compare apparent tutorial wording with `localization/messages.json` where a comparison is supportable. All 11 images were visually reviewed on a labeled contact sheet; the narrow parts atlas, gate, controller-help atlas, ornamental window and training title were also inspected enlarged.

Each file matches its indexed dimensions and full SHA-256. All have an 18-byte TGA header with image type 2 (uncompressed true-color), 32 bits per pixel, descriptor `0x28` (top-origin with 8 alpha bits), and an exact `18 + width × height × 4` file extent. Bounds below are source-image pixel coordinates, with half-open intervals unless an inclusive box is explicitly stated. Coarse bounds and uncertain readings are labeled as such.

## Findings

The `trng` image clearly spells `トレーニング` (“Training”) in multicolor lettering. The controller-help atlas also contains Japanese labels, including clearly readable `ARM セット` and `ランダム`, alongside controller symbols and Latin labels. Its Japanese text is confined to a broad mixed label area; this review does not claim per-label runtime use or a complete transcription of every small phrase. The arm-parts strip carries small Latin `SLOT` labels and numerals. The gate and window contain inscription-like marks that are too small or ornamental to read confidently and remain candidates, not recovered text.

The tutorial message catalog has 36 records of `kind == 3`. It contains tutorial wording for directional controls, sticks, buttons and actions; for example, `方向キー`, `左スティック`, and several button-name phrases. The exact visible terms `トレーニング`, `ARM セット`/`ARMセット`, and `ランダム` were not found in those records. This is a vocabulary-level comparison only; it does not establish that any texture label corresponds to a particular message record.

| Category | Indexed Japanese texture | Dimensions | SHA-256 | Visual finding |
|---|---|---:|---|---|
| `user_interface` | `00039_01593_0000_00_gnt_jp.tga` | 256×256 | `e2f6173432aec889d728ebc685f44f5ca5ab7e7eb72967bb55ef3cbc1260d0be` | Character illustration; no visible text. |
| `weapons` | `00039_01593_0001_armstprts_jp.tga` | 512×128 | `2df84469013e5dacd64f63fbf0810d370bded901e515f287547340b6195c77b6` | Thin transparent weapon/slot parts strip. Small Latin `SLOT` labels and numerals are visible in the approximate region `[0,220)×[44,117)`; no Japanese wording was confidently read. |
| `backgrounds` | `00039_01593_0002_bg_jp.tga` | 256×256 | `a379f27905c167b9d3b61d1455dbce234c2a039ad753bef82e3c6e62adeeeed0` | Blue gradient background; no text. |
| `effects` | `00039_01593_0003_door_eff_jp.tga` | 256×256 | `d22e5511ab33fd263f7e2c914dd372db888c1c40cb92855a26f8798260a29584` | Very faint transparent door/effect pixels; no readable text. |
| `effects` | `00039_01593_0004_effect_jp.tga` | 256×256 | `48c17e2f5e65f72c6143e17ad3f9260691b943eb40a2618c5c8dbdc9cb084d6c` | Sparse transparent effect/gradient pixels; no readable text. |
| `effects` | `00039_01593_0005_f_flame_jp.tga` | 64×64 | `208d0bdd59430b7b2fd6a2e2f0cc27e6a5bd282d83ea4b5746adfee80610a54e` | Small flame/effect shape; no text. |
| `characters` | `00039_01593_0006_faces_jp.tga` | 256×256 | `9bd6f0682241873b3c6558bf0d1967c61d8872332a009aed8b379dceb8f87548` | Character portrait grid; no visible text. |
| `environments` | `00039_01593_0007_gate_jp.tga` | 512×256 | `bd8e87c605e1d624947c321536fd181b167dbc031c53b80ab06136099f3cbc5a` | Ornate gate/door. Tiny inscription-like marks on its side columns, approximately `[75,145)×[34,212)` and `[370,441)×[34,212)`, are too small/ornamental for a confident reading. Candidate only. |
| `icon` | `00039_01593_0008_icon_jp.tga` | 256×256 | `5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9` | Mixed controller/button-help atlas. Japanese label groups occupy approximately `[56,256)×[0,224)` and include clearly visible `ARM セット` and `ランダム`; surrounding artwork includes button symbols and Latin labels such as `R1`, `R2`, `L1`, `L2`, `START`, and `SELECT`. Other tiny phrases are not fully transcribed here. |
| `user_interface` | `00039_01593_0009_window_jp.tga` | 128×128 | `a53fe384bbf276adaed7da83c8504a9e6968a90e3e54bd6214d89c9229e29087` | Curved multi-row ornamental/calligraphic marks across approximately `[0,128)×[0,91)`; no confident text reading. Candidate only. |
| `user_interface` | `00039_01593_0010_trng_jp.tga` | 256×64 | `2323318d0dc1ea71fc6713af798e6b5682abb9c1d505a439903d5f840e35b8f8` | Multicolor katakana `トレーニング` (“Training”); visible-pixel bounding box inclusive `(1,12)–(224,57)`, equivalent to half-open `[1,225)×[12,58)`. |

## Limits

This is a visual/catalog audit only. No Japanese baseline, graphics index, or override was changed. The export/index checks do not establish UV placement, draw order, runtime use, or a direct mapping to catalog records. No rebuild, ISO, emulator or runtime validation was performed. The gate/window marks and several small controller-atlas phrases remain uncertain and would benefit from in-game context before translation.
