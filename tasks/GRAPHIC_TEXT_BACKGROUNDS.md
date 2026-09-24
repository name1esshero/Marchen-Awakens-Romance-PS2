# Background texture lettering audit

## Scope and method

This is a read-only visual/catalogue review of all 46 `graphics/backgrounds/*_jp.tga`
files present in this worktree. Each image was reviewed on a checkerboard or
neutral background at native or nearest-neighbor enlarged scale. The 46 source
dimensions and complete TGA SHA-256 values below were also checked against their
`graphics/index.json` records; every file has one matching record. All inspected
files are uncompressed true-color TGA (type 2), 32 bits per pixel, with an
18-byte header and top-origin descriptor `0x28`.

Coordinates are approximate source-image pixel bounds, origin at the upper-left,
and use half-open ranges `[x0,x1) × [y0,y1)`. They describe visible texture
content only; they are not recovered UV rectangles. A visual reading is not a
codepoint/font lookup or proof that the full texture is displayed. Japanese
transcriptions below are marked as visual readings where applicable.

## Inventory

| # | Japanese baseline | Size | SHA-256 | Visual finding |
|---:|---|---:|---|---|
| 01 | `00039_00122_00012_00006_sky_jp.tga` | 256×256 | `c89e5a7ddbd45c440602470e45426de7dfef9c958e00bfc59f127051964e7ac7` | Cloud/sky texture; no visible writing or title mark. |
| 02 | `00039_00123_00012_00013_sky_jp.tga` | 256×256 | `248869750fc2087976c9fc6d8e9cf2acc5cf5f998b33ecc358b3f001febbc973` | Cloud/sky texture; no visible writing or title mark. |
| 03 | `00039_00126_00012_00022_sky_jp.tga` | 256×256 | `abdc42ed72bc0d010e9f87b71b1983f65ed606c84901cf2aa934c4cdd7879d48` | Cloud/sky texture; no visible writing or title mark. |
| 04 | `00039_00127_00015_00011_sky_jp.tga` | 256×256 | `c5373be230a50b5ff545372eeb40600e92cd284715d87f216089f76c92943849` | Cloud/sky texture; no visible writing or title mark. |
| 05 | `00039_00988_0000_bg_00_jp.tga` | 512×512 | `b5f44d200170a09f276da0f331962e76fb24da7247af53226b04f4989ff26d9b` | Transparent `GAME OVER` lettering cut through a dark horizontal band, approximately `[61,451)×[220,291)`. The rest of the image is dark/transparent texture. |
| 06 | `00039_00988_0001_bg_01_jp.tga` | 512×512 | `3ccf712ebc41f28498a5618f4adce392e3747fcc11061df3382945b0ed509745` | Same visible English wording, `GAME OVER`, cut through a dark horizontal band, approximately `[64,451)×[221,290)`. Its raster/hash differs from #05. |
| 07 | `00039_00991_0000_00_gnt_jp.tga` | 512×256 | `ae9fb2249eb3508aa2407630dd4e36db290f522002bc5a03f326c4e9ed83df88` | Character illustration; no visible writing. |
| 08 | `00039_00991_0001_accbns_jp.tga` | 256×64 | `d9496f0cc96c7a1fdc927ecf673219f15959d3702e01e9f1e408d633287e9ccb` | English `ACCIDENT BONUS` lettering, approximately `[3,220)×[5,60)`. |
| 09 | `00039_00991_0004_chsmark_jp.tga` | 128×128 | `0c6bc2c8236e3331dad49fe30d5c6a2b4ca48bce3f81b928a8b8216c96087a75` | Shield/skull-style crest pictogram; no visible letters. |
| 10 | `00039_00991_0005_cl_new_mark_jp.tga` | 64×64 | `e833e95a5e85fbadaa7411eb0346bc8864e923f67dc8460c8705528a2e33f4ae` | Two English status words, `Clear` and `New`, on separate rows; visible mark occupies roughly `[0,64)×[0,53)`. |
| 11 | `00039_00991_0006_event_a_jp.tga` | 64×64 | `9356185dcd9ba69b357d902f103f71439d73f1088ebd44880b3ac24487b57b53` | Colored orb/event pictogram; no visible writing. |
| 12 | `00039_00991_0007_event_b_jp.tga` | 64×64 | `9d2f31f4508e4c8fb33ad05d20acff149da985404da58b953b601a517d6e8e57` | Colored orb/event pictogram; no visible writing. |
| 13 | `00039_00991_0011_lab_bg_jp.tga` | 128×128 | `407ea304793d3679589dbac94ee55c1997044200b9e0f67918db5001e39c837c` | Pink radial/translucent effect texture; no visible writing. |
| 14 | `00039_00991_0015_lbrn_jp.tga` | 256×64 | `e37e87842d070810fd0f9c07cf5469de31598b6c88ff59ddc71bf84a3a9d1dae` | Colored Japanese title wordmark (visual reading: `メルヘヴン`) at approximately `[2,188)×[15,46)`; a small embedded English tagline occupies about `[1,185)×[45,60)`. Both bands are part of the image. |
| 15 | `00039_00991_0016_load_s_jp.tga` | 32×32 | `67ffa599cba82ffb5f4bf9b9da4c2f6f6932a5377cf57fcfec0881d6d38774a0` | Thin horizontal bar/line symbol; no readable lettering. |
| 16 | `00039_00991_0017_load_w_jp.tga` | 32×32 | `6717e42014a26bbe13b0cc413183991e0a76fd9ceba4627d041f00820fcc5ef1` | Horizontal bar with opposing/animated arrow-like accents; no readable lettering. |
| 17 | `00039_00991_0024_mv_arrow_jp.tga` | 64×16 | `9336aefd8f44c64bcf5eb3d9894ef5fda9f7509be22034fbd6490f7acab32b6c` | Right-pointing arrow symbol; no words. |
| 18 | `00039_00991_0025_sand_jp.tga` | 32×64 | `a34127e6a6ce234dc1c00aa3c151fc59806b688ea6fce92ff33aa7273e90581e` | Repeating sand/noise pattern; no visible writing. |
| 19 | `00039_00991_0026_sdwcgs_jp.tga` | 32×64 | `f274da62c0d762e38f653bb68bc3bb0ae03c6dbdf9d5489ab1fd06a472e077a1` | Shadow/gradient texture; no visible writing. |
| 20 | `00039_00991_0027_sndwtch_jp.tga` | 64×128 | `454d83f3f2fee13720a2021c5696efaec3621dbf3bccb5d18cc1ad98bdfc697f` | Hourglass pictogram; no visible writing. |
| 21 | `00039_00991_0028_tmover_jp.tga` | 128×32 | `6e382d625613bd7c0d0c58861d1462f1faa9d4070c9b9143db8c2e3db71cea79` | English `TIME OVER` lettering over a patterned gray field, approximately `[7,123)×[7,27)`. |
| 22 | `00039_00991_0029_window_jp.tga` | 128×128 | `a53fe384bbf276adaed7da83c8504a9e6968a90e3e54bd6214d89c9229e29087` | Ornate window/frame texture; no visible writing. |
| 23 | `00039_00991_0030_btnhlptxt_jp.tga` | 128×64 | `f8ce181acf8a5e3bab090c564f5cc5e50d36075c0f85014387c27cf02d69ce3f` | Three rows of Japanese control/help lettering, approximately `[2,20)×[0,20)`, `[1,104)×[23,44)`, and `[0,81)×[45,63)`. The middle row also includes a button-like pictogram and separators. Exact glyph/codepoint mapping is not established here. |
| 24 | `00039_00991_0031_tmdisp_jp.tga` | 128×64 | `a8a8920e02369199f177fef92328f765553fc5ff7d8ae32f85d1c46fba84a928` | Small outlined digit atlas: `0–4` on the first row, `5–9` on the second, plus a dash and a Japanese glyph visually read as `分` on the bottom row (approx. `[5,42)×[40,63)`). Unit interpretation/lookup remains unverified. |
| 25 | `00039_01015_0000_bg_001_jp.tga` | 512×512 | `5d0f9604e017682c8947ea0b488d657f4f7e0065a5bcb4b4dfded9f7d6f28976` | Temple/door scene with repeated rows of small carved or inscription-like marks, roughly `[190,330)×[140,385)`. They are not confidently identifiable as Japanese or readable text; preserve as unresolved authored marks, not a confirmed localization string. |
| 26 | `00039_01015_0001_bg_hide_jp.tga` | 256×256 | `6f9b60f1618f2153832e06289f64593dbea95052e7bc8008cfde120ab9c0f6ae` | Dark radial/translucent overlay; no visible writing. Exact byte duplicate of #28, #30, and #32. |
| 27 | `00039_01016_0000_bg_002_jp.tga` | 512×512 | `a54787fa71348abcd619d4ae49884a8850b5530724c4fe229ed8d34f04fe15fe` | Portal/arch and fog scene texture; no visible writing. |
| 28 | `00039_01016_0001_bg_hide_jp.tga` | 256×256 | `6f9b60f1618f2153832e06289f64593dbea95052e7bc8008cfde120ab9c0f6ae` | Dark radial/translucent overlay; no visible writing. Exact byte duplicate of #26, #30, and #32. |
| 29 | `00039_01017_0000_bg_plus_jp.tga` | 512×512 | `757e53261bd13d64ea661932327adb66fdb4fd411ea20e04d9c46e7e78e020a4` | Gate/corridor scene; no visible writing. |
| 30 | `00039_01017_0001_bg_hide_jp.tga` | 256×256 | `6f9b60f1618f2153832e06289f64593dbea95052e7bc8008cfde120ab9c0f6ae` | Dark radial/translucent overlay; no visible writing. Exact byte duplicate of #26, #28, and #32. |
| 31 | `00039_01018_0000_bg_000_jp.tga` | 512×512 | `9a9dd812b89313252bbcb0eb1e7b1e10c661e159d078748fa46d8700340dbd79` | Open-door scene with repeated rows of small carved or inscription-like marks, roughly `[190,330)×[120,385)`. They are not confidently identifiable as Japanese or readable text; preserve as unresolved authored marks, not a confirmed localization string. |
| 32 | `00039_01018_0001_bg_hide_jp.tga` | 256×256 | `6f9b60f1618f2153832e06289f64593dbea95052e7bc8008cfde120ab9c0f6ae` | Dark radial/translucent overlay; no visible writing. Exact byte duplicate of #26, #28, and #30. |
| 33 | `00039_01018_0003_window_jp.tga` | 128×128 | `a53fe384bbf276adaed7da83c8504a9e6968a90e3e54bd6214d89c9229e29087` | Ornate window/frame texture; no visible writing. Exact byte duplicate of #22. |
| 34 | `00039_01521_0003_bg_jp.tga` | 512×512 | `289cfb8a9cd8c1da060961491afb6bf388690b5ee1654adc40e5f58ac66c153b` | Gray ornamental cross/axis motif; no visible writing. |
| 35 | `00039_01521_0004_bg_001_jp.tga` | 512×512 | `296473cdaa2431478cd2e0ca022fff9c3d32e96d94d9135a3dd6998e7cd20c0b` | Fire texture; no visible writing. |
| 36 | `00039_01539_0001_lab_bg_jp.tga` | 256×256 | `0b74442cc0f13061f3727fda18b9c88acbb022890bc096451871fb7a0d62c52c` | Pink translucent radial/smoke effect; no visible writing. Exact byte duplicate of #40. |
| 37 | `00039_01547_0000_bg_jp.tga` | 512×512 | `b837cc6beb3ffeff130d8e100ea4b4c00f80de105870efa6725d3f58d44cea13` | Gray/silver ornamental frame with repeated curls; no legible writing. |
| 38 | `00039_01551_0001_svld_bg_jp.tga` | 512×256 | `9f8f96f72f83b7903d552de5f0437c07a3c513fb42f9148471e0b14937c34320` | Grayscale Japanese title wordmark (visual reading: `メルヘヴン`) and embedded English tagline `MÄRCHEN AWAKENS ROMANCE`; combined logo occupies approximately `[228,502)×[64,196)`. |
| 39 | `00039_01556_0012_shopbg_jp.tga` | 512×512 | `613b0de3f0d0efab2363ff5d19fffca394a7899685aa01af4a22425e4abbe39e` | Shop interior with illustrated/icon-like wall panels and display objects; no readable text observed. |
| 40 | `00039_01559_0001_lab_bg_jp.tga` | 256×256 | `0b74442cc0f13061f3727fda18b9c88acbb022890bc096451871fb7a0d62c52c` | Pink translucent radial/smoke effect; no visible writing. Exact byte duplicate of #36. |
| 41 | `00039_01569_0009_sky_jp.tga` | 256×256 | `86eaf58abfe865cac8932c2b77313738a4f756f7126889360d40947ca1275179` | Blue sky/cloud texture; no visible writing. |
| 42 | `00039_01593_0002_bg_jp.tga` | 256×256 | `a379f27905c167b9d3b61d1455dbce234c2a039ad753bef82e3c6e62adeeeed0` | Dark blue swirl/gradient texture; no visible writing. |
| 43 | `00039_01606_0013_sky_jp.tga` | 256×256 | `9f9b399815fdf8a0c766af24035af110a789367041c24b897470e2dafb70633b` | Blue sky/cloud texture; no visible writing. |
| 44 | `00039_01624_0035_sky_jp.tga` | 256×256 | `0d90066e538086f26ccf81e43d00c89a0417f40447aa7f98d1047b2b27063530` | Grayscale cloud texture; no visible writing. Exact byte duplicate of #46. |
| 45 | `00039_01631_0016_bg_win_jp.tga` | 256×256 | `c1cf9d41c1af10b85586083e283516636932c17fd9104f72986d89fa2987533c` | Red radial burst/win effect texture; no visible writing. |
| 46 | `00039_01635_0054_sky_jp.tga` | 256×256 | `0d90066e538086f26ccf81e43d00c89a0417f40447aa7f98d1047b2b27063530` | Grayscale cloud texture; no visible writing. Exact byte duplicate of #44. |

## Findings and limits

Nine images contain clearly visible lettering, a Japanese title mark, Japanese
control text, or a digit/unit atlas: #05, #06, #08, #10, #14, #21, #23, #24,
and #38. The embedded English strings/status marks are not Japanese translation
targets, but are still catalogued because these are editable graphics. The two
door scenes #25 and #31 contain prominent inscription-like marks whose script
and meaning remain unresolved; visual appearance alone is insufficient to
classify them as Japanese text. The other 35 images show scene art, symbols,
ornamental frames, or effect/sky textures without readable lettering.

Byte-identical groups found by SHA-256 are #22/#33, #26/#28/#30/#32, #36/#40,
and #44/#46. No Japanese baseline was changed and no English override was
authored. No UV rectangles, draw order, runtime usage, text lookup table, or
on-screen display behavior is inferred from these flat textures. No ISO build
or emulator/runtime validation was performed.

References: `graphics/index.json`,
[`LOCALIZATION_METHODOLOGY.md`](../docs/LOCALIZATION_METHODOLOGY.md),
[`TITLE_TEXTURE_RENDERING.md`](TITLE_TEXTURE_RENDERING.md),
[`GRAPHIC_TEXT_LOCALIZATION.md`](GRAPHIC_TEXT_LOCALIZATION.md).
