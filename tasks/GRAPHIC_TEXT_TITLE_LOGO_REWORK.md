# DQ-38: Correct the English title logo artwork

Updated: 2026-09-24.

## Finding and correction

The in-game title capture showed repeated `ARM FIGHT DREAM` letterforms where
the franchise's distinctive `MÄR HEAVEN` mark belongs. The former English
siblings had reused lettering from the `sbttl` subtitle, then described those
letterforms as the native MÄR HEAVEN wordmark. That identification was wrong;
the title screen can show a separate `ARM FIGHT DREAM` subtitle, so preserve it
in that role.

The corrected artwork uses the owner-supplied reference
`T_TTL06.KCG_en.png` (256×256, SHA-256
`33cbe51d2ac9c5fa409ca023ab9147f67a78304ca9f25328932540b51643e947`). The
tracked `graphics/title/mar_heaven_logo_source.png` is its exact crop
`[16,0)-[224,89)`; the separate
`graphics/title/mar_heaven_wordmark_source.png` crop `[16,44)-[224,88)` keeps
the lettering available as an independent editable component. Both crops
retain the reference palette colors and black outlines. Palette index 0 alone
becomes transparent; palette index 48 is black outline artwork and stays
opaque. The full-logo crop is 208×89, RGBA PNG, SHA-256
`f81509310881637fce019abd17dc01b9f5c58e7d61d0e6fab5a7c57cd498462e`; the
wordmark crop is 208×44, SHA-256
`c3ab434d263175c7985feae2ec558c66f68c172e266245ec460e421166481424`.

`tools/title_logo_localize.py` uses the tracked crop, the existing English TGA,
explicit clear rectangles, and per-placement gray/color treatments to create
a full-canvas editable `*_eng_layer.png` and deterministic 512×512 English
sibling. It clears only the specified mark rectangles, composites at the
original pixel coordinates, and preserves the existing English credits,
subtitle, prompts, and other artwork. Do not feed it a Japanese baseline;
the `_jp.tga` remains the recovered artwork and is never modified.

## Replacements

| English sibling | Cleared/replaced regions | Treatment |
| --- | --- | --- |
| `graphics/title/00039_01559_0003_title_eng.tga` | `[99,118,334,149]` | Full MÄR HEAVEN mark, color |
| `graphics/title/00039_01565_0000_ttlprts_eng.tga` | `[0,0,438,216]`, `[0,270,438,113]`, `[0,398,438,113]` | Full mark, gray/color/gray |
| `graphics/title/00039_01566_0002_title_marh_eng.tga` | `[0,3,512,221]`, `[0,231,512,221]` | Full mark, gray/color |
| `graphics/user_interface/00039_00985_00000_title000_eng.tga` | `[88,0,315,123]` | Full mark, color |

All four Japanese baselines still match their exact `graphics/index.json`
SHA-256 values. Each English TGA remains 512×512 with the same 32-bit type-2
header and 1,048,594-byte extent. Comparing the new outputs to the previously
committed English siblings finds 48,781, 193,150, 226,199, and 28,268 changed
pixels respectively; zero changed pixels fall outside the listed rectangles.

| English sibling | Japanese TGA SHA-256 | Source TXC SHA-256 | Prior English SHA-256 | Corrected English SHA-256 | Layer SHA-256 |
| --- | --- | --- | --- | --- | --- |
| `00039_01559_0003_title_eng.tga` | `9779a775c176dcd842be884fd33a66e0e4b11334bfdb6bb30beb6737e63075f1` | `e2c3d2913e1999d7460881c3fb3ba5e31ff0cdeaa4960891792f7ea871d3d0fe` | `61d1b152fda99cc6d196ee8fdadec1f89bc922771429f06384faf2a7c9fe3c81` | `b5d41f822e5d72011eb5fa8198961c143f74762e68e7ab3ef363a024406a15cc` | `20909435fb9bac443e84baddf9354fd35c754122859a0789aca413da2dfbea26` |
| `00039_01565_0000_ttlprts_eng.tga` | `a528447c14929d7d16fc62254d6fdca90ff6d3f336c8b3a27b53f303d646542c` | `55b24160b8c3c56db4e02f8f2cd945594c5347c43685842d986a985427b556bb` | `eb3d226ace0f02b70eec514b993d027adf1e5a74bbc9b5bf15ad99914114ae88` | `be0a23b12ffdbe28cab4ca02d2d3c65d5573e60dee43f8fae23e5f0e80cb958f` | `e4fd6df763c864d6dd327bafe7f5a57d4bd8a0070bb8c58398f06209781ec260` |
| `00039_01566_0002_title_marh_eng.tga` | `e72a760fccf45ba7ab71d18e2b5f3c865a74cf9e827e6a93d37a619d2625052c` | `b67db2f3a834c05de583c3dbd360da3208384c4234072f0ed66b58711dcfc375` | `528d758732c3bffa9f5aad5c97d1a0bc556039afdf499b263cd90e155ed55f85` | `052ce3b9fb92c1a95e7c087299234685a0d2a49cca3d117d5d58031594210ad8` | `2ba37ccdd27e7c885b8502639b7f46c16b3dc12badb5e731d6ea16fb6a739681` |
| `00039_00985_00000_title000_eng.tga` | `19b66cfa3f6c69717e0250cca8c0cd89e5e195dfb2ecd3279d9f3ff4b34365e6` | `cfc91c5f6539f0240790c4ed2086d77ec4c853b309227461be5699e7dfadd15b` | `6851419b7b8db356435faa80dc7fba3536a695e9d2d2a51acc9dab11a3efa5bc` | `633af83b7af2fab3e99c65c046c06f407644e7ccebac841cf2491cd2b6b86b81` | `1a7d47c4b9df83f427a2ca87e2f5f19f1757e0ec0b6f60b493614f002a449add` |

## Verification and limits

The new compositor tests cover exact region clearing, alpha compositing,
grayscale conversion, dimensions, out-of-bounds rejection, and Japanese-baseline
path protection; all 126 tests in
`make test` pass. Static previews were reviewed for all four output atlases.
`make build-mod-disc` succeeded and wrote the 5,024,266,240-byte root
`mar_eng.iso`. `make verify-graphics-image` passed all 17 staged overrides
(1,501,632 TXC bytes total), including the four corrected title siblings:

| Reparsed TXC | Exact ISO-extracted SHA-256 |
| --- | --- |
| `0003_title.txc.bin` | `2bd222440f52c19e9fadc37e9313af50be47f741973b43d66774c009942fe1f8` |
| `0000_ttlprts.txc.bin` | `6364cdca5b59ce44e2d0cd0c77357de14dd13fc220e7e9c57349612aa1abd7c3` |
| `0002_title_marh_jp.txc.bin` | `594ce0c4f574c42f4d62aea709cc061e3fdfc0736f8244594eace763f96e30b3` |
| `00985.asset/00000.bin` (`title000`) | `a3660369d71995b2b64ef2b9b16e1191c696a6be9716c59e07290780c466279d` |

The verifier matched each ISO-extracted TXC byte-for-byte with its staged
override. No emulator, runtime UV, draw-order, or final in-game composition
claim is made here.

The reference is a still image from another MÄR game. It supports a consistent
franchise-style wordmark, but the game-specific UVs and title-animation layers
remain unresolved. Inspect the rebuilt title in the emulator when available.

References: [`title texture rendering evidence`](TITLE_TEXTURE_RENDERING.md),
[`graphic localization evidence`](GRAPHIC_TEXT_LOCALIZATION.md),
[`title-parts texture`](GRAPHIC_TEXT_TTLPRTS.md),
[`title000 texture`](GRAPHIC_TEXT_TITLE000.md), and
[`localization methodology`](../docs/LOCALIZATION_METHODOLOGY.md).
