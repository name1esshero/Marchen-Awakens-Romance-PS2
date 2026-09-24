# Icon texture text audit

Updated: 2026-09-23.

## Result

All 194 indexed Japanese baselines under `graphics/icon/` were reviewed. Twenty-nine file instances across eight exact raster hashes contain visible Japanese label/command text, generally packed alongside English words and controller glyphs in small UI sprite atlases. These are definite follow-up localization surfaces. The other 165 images show pictograms, equipment/item art, character portraits, effect/status marks, arrows, or empty UI frames without readable words. No Japanese baselines were edited, and no English overrides were created.

The eight text-bearing hashes are reviewed by group below; each inventory row identifies every corresponding file, with identical-hash copies inheriting the same exact raster/text bounds. In total, the category has 129 unique full-file hashes and 12 repeated-hash groups. All source images are uncompressed 32-bit top-origin TGA (`type 2`, descriptor `0x28`).

Coordinates are approximate source-pixel bounds, origin at upper-left, half-open `[x0,x1) × [y0,y1)`. They bound visible label/wording regions in the sprite atlas, not runtime UV rectangles. Japanese wording is visibly present but is not transcribed here: these textures combine dense pixel-font kana/kanji and other glyphs, and this pass classifies surfaces rather than making localization copy decisions.

## Text-bearing groups

| Group | Hash prefix / instances | Visible content and approximate Japanese text bounds |
| --- | --- | --- |
| A | `5492b8956e6c` / 16 | Full 256×256 command/control atlas. Japanese labels form the right-side text rows, approximately `[100,255) × [1,202)`; Latin/control labels include `ARM`, `P1`, `P2`, `COM`, `CON`, `R1/R2`, `L1/L2`, `START`, and `SELECT`. |
| B | `7e7746dc1f13` / 5 | 256×256 alternate/short atlas variant; Japanese labels occupy approximately `[100,255) × [1,127)`, with button/control pictograms. |
| C | `f8da25f8a3fa` / 1 | 128×128 bilingual label sprite: Japanese wording approximately `[1,127) × [1,50)`; English `GET!`/`New` artwork follows at about `[2,127) × [52,72)`. |
| D | `2528971563da` / 2 | 128×128 related bilingual label variant: Japanese wording approximately `[1,127) × [1,50)`; English `GET!`/`New` marks about `[2,127) × [53,71)`. |
| E | `f29cb5aa8430` / 1 | 256×256 command/control atlas variant; Japanese rows approximately `[100,255) × [1,202)`, alongside pictograms and Latin/control labels. |
| F | `b34feb0715cb` / 1 | 256×256 dimmed/alternate control-atlas art; Japanese rows approximately `[100,255) × [1,127)`, alongside controller/control imagery. |
| G | `95ec03aede5e` / 2 | 256×256 partial atlas; Japanese labels approximately `[100,255) × [1,148)`, with adjacent controller/control glyphs. |
| H | `f1f99d4fd157` / 1 | 256×256 command/control atlas variant; Japanese label area approximately `[100,255) × [1,218)`, with English/control text and pictograms. |

The large atlases are collections of separate glyph/label sprites, not proof that a single full phrase is drawn as one text run. The label bounds should be remeasured per individual component before replacing words, and existing graphics/palette import constraints should be preserved. Prioritize groups A–H for layout-aware English equivalents only after code/UV or screen captures establish which rows are actually sampled.

## Inventory

This table includes all 194 indexed paths. The common directory prefix `graphics/icon/` is omitted. `P` means no readable wording was observed and the image is pictorial/symbolic; group letters reference the text-bearing findings above.

| # | Japanese baseline | Dimensions | TGA bytes | SHA-256 | Finding |
| ---: | --- | ---: | ---: | --- | --- |
| 001 | `00039_00917_0000_arm001_jp.tga` | 128×128 | 65,554 | `fbab754f4b92ad512a5739938e08c45766d14c912b627086ffe8ed1d13b2364b` | No readable wording; pictogram/art. |
| 002 | `00039_00917_0001_arm001_jp.tga` | 128×128 | 65,554 | `fbab754f4b92ad512a5739938e08c45766d14c912b627086ffe8ed1d13b2364b` | No readable wording; pictogram/art. |
| 003 | `00039_00917_0002_arm002_jp.tga` | 128×128 | 65,554 | `f11db087f2fa02404b5ead561f7dc51df74f942a8d8f7a22bd3ddf4f89595b16` | No readable wording; pictogram/art. |
| 004 | `00039_00917_0003_arm003_jp.tga` | 128×128 | 65,554 | `ccec409c1be2e99b0ba8ecb94032330e7d22d91fb20e8b5f235d320127148096` | No readable wording; pictogram/art. |
| 005 | `00039_00917_0004_arm004_jp.tga` | 128×128 | 65,554 | `fdcbea2bd75b11408c14ef582c664222e15cd5021271873d96e09ff0e6be9bd9` | No readable wording; pictogram/art. |
| 006 | `00039_00917_0005_arm005_jp.tga` | 128×128 | 65,554 | `06638da7b7416ebc780a5695647e356c0b0bfb1a51a8a7e7942baed30de7c6cb` | No readable wording; pictogram/art. |
| 007 | `00039_00917_0006_arm006_jp.tga` | 128×128 | 65,554 | `f11db087f2fa02404b5ead561f7dc51df74f942a8d8f7a22bd3ddf4f89595b16` | No readable wording; pictogram/art. |
| 008 | `00039_00917_0007_arm007_jp.tga` | 128×128 | 65,554 | `ccec409c1be2e99b0ba8ecb94032330e7d22d91fb20e8b5f235d320127148096` | No readable wording; pictogram/art. |
| 009 | `00039_00917_0008_arm008_jp.tga` | 128×128 | 65,554 | `fdcbea2bd75b11408c14ef582c664222e15cd5021271873d96e09ff0e6be9bd9` | No readable wording; pictogram/art. |
| 010 | `00039_00917_0009_arm009_jp.tga` | 128×128 | 65,554 | `fbab754f4b92ad512a5739938e08c45766d14c912b627086ffe8ed1d13b2364b` | No readable wording; pictogram/art. |
| 011 | `00039_00917_0010_arm010_jp.tga` | 128×128 | 65,554 | `f11db087f2fa02404b5ead561f7dc51df74f942a8d8f7a22bd3ddf4f89595b16` | No readable wording; pictogram/art. |
| 012 | `00039_00917_0011_arm011_jp.tga` | 128×128 | 65,554 | `ccec409c1be2e99b0ba8ecb94032330e7d22d91fb20e8b5f235d320127148096` | No readable wording; pictogram/art. |
| 013 | `00039_00917_0012_arm012_jp.tga` | 128×128 | 65,554 | `fdcbea2bd75b11408c14ef582c664222e15cd5021271873d96e09ff0e6be9bd9` | No readable wording; pictogram/art. |
| 014 | `00039_00917_0013_arm013_jp.tga` | 128×128 | 65,554 | `fbab754f4b92ad512a5739938e08c45766d14c912b627086ffe8ed1d13b2364b` | No readable wording; pictogram/art. |
| 015 | `00039_00917_0014_arm014_jp.tga` | 128×128 | 65,554 | `f11db087f2fa02404b5ead561f7dc51df74f942a8d8f7a22bd3ddf4f89595b16` | No readable wording; pictogram/art. |
| 016 | `00039_00917_0015_arm015_jp.tga` | 128×128 | 65,554 | `ccec409c1be2e99b0ba8ecb94032330e7d22d91fb20e8b5f235d320127148096` | No readable wording; pictogram/art. |
| 017 | `00039_00917_0016_arm016_jp.tga` | 128×128 | 65,554 | `fdcbea2bd75b11408c14ef582c664222e15cd5021271873d96e09ff0e6be9bd9` | No readable wording; pictogram/art. |
| 018 | `00039_00917_0017_arm017_jp.tga` | 128×128 | 65,554 | `fbab754f4b92ad512a5739938e08c45766d14c912b627086ffe8ed1d13b2364b` | No readable wording; pictogram/art. |
| 019 | `00039_00917_0018_arm018_jp.tga` | 128×128 | 65,554 | `f11db087f2fa02404b5ead561f7dc51df74f942a8d8f7a22bd3ddf4f89595b16` | No readable wording; pictogram/art. |
| 020 | `00039_00917_0019_arm019_jp.tga` | 128×128 | 65,554 | `ccec409c1be2e99b0ba8ecb94032330e7d22d91fb20e8b5f235d320127148096` | No readable wording; pictogram/art. |
| 021 | `00039_00917_0020_arm020_jp.tga` | 128×128 | 65,554 | `fdcbea2bd75b11408c14ef582c664222e15cd5021271873d96e09ff0e6be9bd9` | No readable wording; pictogram/art. |
| 022 | `00039_00917_0021_arm021_jp.tga` | 128×128 | 65,554 | `fbab754f4b92ad512a5739938e08c45766d14c912b627086ffe8ed1d13b2364b` | No readable wording; pictogram/art. |
| 023 | `00039_00917_0022_arm022_jp.tga` | 128×128 | 65,554 | `f11db087f2fa02404b5ead561f7dc51df74f942a8d8f7a22bd3ddf4f89595b16` | No readable wording; pictogram/art. |
| 024 | `00039_00917_0023_arm023_jp.tga` | 128×128 | 65,554 | `ccec409c1be2e99b0ba8ecb94032330e7d22d91fb20e8b5f235d320127148096` | No readable wording; pictogram/art. |
| 025 | `00039_00917_0024_arm024_jp.tga` | 128×128 | 65,554 | `fdcbea2bd75b11408c14ef582c664222e15cd5021271873d96e09ff0e6be9bd9` | No readable wording; pictogram/art. |
| 026 | `00039_00917_0025_arm025_jp.tga` | 128×128 | 65,554 | `fbab754f4b92ad512a5739938e08c45766d14c912b627086ffe8ed1d13b2364b` | No readable wording; pictogram/art. |
| 027 | `00039_00917_0026_arm026_jp.tga` | 128×128 | 65,554 | `f11db087f2fa02404b5ead561f7dc51df74f942a8d8f7a22bd3ddf4f89595b16` | No readable wording; pictogram/art. |
| 028 | `00039_00917_0027_arm027_jp.tga` | 128×128 | 65,554 | `ccec409c1be2e99b0ba8ecb94032330e7d22d91fb20e8b5f235d320127148096` | No readable wording; pictogram/art. |
| 029 | `00039_00917_0028_arm028_jp.tga` | 128×128 | 65,554 | `fdcbea2bd75b11408c14ef582c664222e15cd5021271873d96e09ff0e6be9bd9` | No readable wording; pictogram/art. |
| 030 | `00039_00917_0029_arm029_jp.tga` | 128×128 | 65,554 | `fbab754f4b92ad512a5739938e08c45766d14c912b627086ffe8ed1d13b2364b` | No readable wording; pictogram/art. |
| 031 | `00039_00917_0030_arm030_jp.tga` | 128×128 | 65,554 | `f11db087f2fa02404b5ead561f7dc51df74f942a8d8f7a22bd3ddf4f89595b16` | No readable wording; pictogram/art. |
| 032 | `00039_00917_0031_arm031_jp.tga` | 128×128 | 65,554 | `ccec409c1be2e99b0ba8ecb94032330e7d22d91fb20e8b5f235d320127148096` | No readable wording; pictogram/art. |
| 033 | `00039_00917_0032_arm032_jp.tga` | 128×128 | 65,554 | `fdcbea2bd75b11408c14ef582c664222e15cd5021271873d96e09ff0e6be9bd9` | No readable wording; pictogram/art. |
| 034 | `00039_00917_0033_arm033_jp.tga` | 128×128 | 65,554 | `fbab754f4b92ad512a5739938e08c45766d14c912b627086ffe8ed1d13b2364b` | No readable wording; pictogram/art. |
| 035 | `00039_00917_0034_arm034_jp.tga` | 128×128 | 65,554 | `f11db087f2fa02404b5ead561f7dc51df74f942a8d8f7a22bd3ddf4f89595b16` | No readable wording; pictogram/art. |
| 036 | `00039_00917_0035_arm035_jp.tga` | 128×128 | 65,554 | `ccec409c1be2e99b0ba8ecb94032330e7d22d91fb20e8b5f235d320127148096` | No readable wording; pictogram/art. |
| 037 | `00039_00917_0036_arm036_jp.tga` | 128×128 | 65,554 | `fdcbea2bd75b11408c14ef582c664222e15cd5021271873d96e09ff0e6be9bd9` | No readable wording; pictogram/art. |
| 038 | `00039_00917_0037_arm037_jp.tga` | 128×128 | 65,554 | `fbab754f4b92ad512a5739938e08c45766d14c912b627086ffe8ed1d13b2364b` | No readable wording; pictogram/art. |
| 039 | `00039_00917_0038_arm038_jp.tga` | 128×128 | 65,554 | `f11db087f2fa02404b5ead561f7dc51df74f942a8d8f7a22bd3ddf4f89595b16` | No readable wording; pictogram/art. |
| 040 | `00039_00917_0039_arm039_jp.tga` | 128×128 | 65,554 | `ccec409c1be2e99b0ba8ecb94032330e7d22d91fb20e8b5f235d320127148096` | No readable wording; pictogram/art. |
| 041 | `00039_00917_0040_arm040_jp.tga` | 128×128 | 65,554 | `fdcbea2bd75b11408c14ef582c664222e15cd5021271873d96e09ff0e6be9bd9` | No readable wording; pictogram/art. |
| 042 | `00039_00917_0041_arm041_jp.tga` | 128×128 | 65,554 | `fbab754f4b92ad512a5739938e08c45766d14c912b627086ffe8ed1d13b2364b` | No readable wording; pictogram/art. |
| 043 | `00039_00917_0042_arm042_jp.tga` | 128×128 | 65,554 | `f11db087f2fa02404b5ead561f7dc51df74f942a8d8f7a22bd3ddf4f89595b16` | No readable wording; pictogram/art. |
| 044 | `00039_00917_0043_arm043_jp.tga` | 128×128 | 65,554 | `ccec409c1be2e99b0ba8ecb94032330e7d22d91fb20e8b5f235d320127148096` | No readable wording; pictogram/art. |
| 045 | `00039_00917_0044_arm044_jp.tga` | 128×128 | 65,554 | `fdcbea2bd75b11408c14ef582c664222e15cd5021271873d96e09ff0e6be9bd9` | No readable wording; pictogram/art. |
| 046 | `00039_00921_0023_icon_jp.tga` | 256×256 | 262,162 | `5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9` | Japanese/English text group A; bounds below. |
| 047 | `00039_00921_0024_icon_armset_jp.tga` | 128×128 | 65,554 | `a5a5b7fa691c81bd03ec59a8cb83d04bace2ae768596c2acf58118382693ea08` | No readable wording; pictogram/art. |
| 048 | `00039_00922_0000_arm000_jp.tga` | 128×128 | 65,554 | `d01b6456e1bbca281c0f3ed76cf7e189bc7c191bcf394c0ac23da820ce3a6d32` | No readable wording; pictogram/art. |
| 049 | `00039_00922_0001_arm001_jp.tga` | 128×128 | 65,554 | `d011f4a1546f95dcb3f1ae0ef551b29a08cac715836bb6fe75746a951faa7af0` | No readable wording; pictogram/art. |
| 050 | `00039_00922_0002_arm002_jp.tga` | 128×128 | 65,554 | `f62504df839e5224b223fbca26c86a84b9808e8f7db21815b199e6e50a661915` | No readable wording; pictogram/art. |
| 051 | `00039_00922_0003_arm003_jp.tga` | 128×128 | 65,554 | `63c1eecf045ce5692a3a553dc202a1a736ed8769a558614431a6e7245a629609` | No readable wording; pictogram/art. |
| 052 | `00039_00922_0004_arm004_jp.tga` | 128×128 | 65,554 | `99eccb7e992cc1704bfc157cd16197b50e3ad84bcaff60132458f32685122b3c` | No readable wording; pictogram/art. |
| 053 | `00039_00922_0005_arm005_jp.tga` | 128×128 | 65,554 | `5ebfdd946291bf83591866485b8d09c77f16bc9b7ce77700f2839f4b25d11db4` | No readable wording; pictogram/art. |
| 054 | `00039_00922_0006_arm006_jp.tga` | 128×128 | 65,554 | `561b4497abdf29c3f9598c5944428e130f168002d876dda102cca0072d44f060` | No readable wording; pictogram/art. |
| 055 | `00039_00922_0007_arm007_jp.tga` | 128×128 | 65,554 | `99b6f11306dac95fdc0843b39e910a0262ea407e9d92458f08c87331568609fb` | No readable wording; pictogram/art. |
| 056 | `00039_00922_0008_arm008_jp.tga` | 128×128 | 65,554 | `c7fe75bfd906def17846ae47e955039f508ca4a6fd98e1361c9d802dbc556f01` | No readable wording; pictogram/art. |
| 057 | `00039_00922_0009_arm009_jp.tga` | 128×128 | 65,554 | `654a629bf73687eaaf1d914ad52d91ca9846f8c8c37870fdc45cc8b55adf8a8e` | No readable wording; pictogram/art. |
| 058 | `00039_00922_0010_arm010_jp.tga` | 128×128 | 65,554 | `1c00a742a1326ab89465ee974c8d091878c8166676549f960a51927a058de797` | No readable wording; pictogram/art. |
| 059 | `00039_00922_0011_arm011_jp.tga` | 128×128 | 65,554 | `e1381051d9dfed38fd936b6b7aa2d4d9c9924170bf8502c4f11a7d97eeec11fd` | No readable wording; pictogram/art. |
| 060 | `00039_00922_0012_arm012_jp.tga` | 128×128 | 65,554 | `079f605bf77de42190913fdb8e769a0bc323da88def34ec19f4cb23c5ee0f8e1` | No readable wording; pictogram/art. |
| 061 | `00039_00922_0013_arm013_jp.tga` | 128×128 | 65,554 | `c7c7584bc33ea76c5f29685e45b732a5fa792c36aad4ef6ad7ac4f0af9dd52db` | No readable wording; pictogram/art. |
| 062 | `00039_00922_0014_arm014_jp.tga` | 128×128 | 65,554 | `dea774e8a267061d970849f9cb8b041925c1258db91f5fac30dda05ca8c2fe49` | No readable wording; pictogram/art. |
| 063 | `00039_00923_0000_arm015_jp.tga` | 128×128 | 65,554 | `caa520bb57f78a4b6b0879cd7de5e4c1e636cf788c8b164e1f19a69a8f3602cd` | No readable wording; pictogram/art. |
| 064 | `00039_00923_0001_arm016_jp.tga` | 128×128 | 65,554 | `b3d282a71b47562836cfc16c0a1f7b923751a8c07f096c61333dd304e23e3256` | No readable wording; pictogram/art. |
| 065 | `00039_00923_0002_arm017_jp.tga` | 128×128 | 65,554 | `65bd4d08eff3ebc76f0d45bec77ba2f05d70ff154154840f61656b5464c7c0f2` | No readable wording; pictogram/art. |
| 066 | `00039_00923_0003_arm018_jp.tga` | 128×128 | 65,554 | `1afa53a4a7ec5225660cba3bb721587d021e947830d2c74ce8f750feb56df040` | No readable wording; pictogram/art. |
| 067 | `00039_00923_0004_arm019_jp.tga` | 128×128 | 65,554 | `6f4488191997f5a56701f7a9d7873a87e4e27d06942b6c24b86c18643691d487` | No readable wording; pictogram/art. |
| 068 | `00039_00923_0005_arm020_jp.tga` | 128×128 | 65,554 | `695bdd141df8cac1e0bd54473f07387b37bcc5d88df2132d49dad06b7ec86a3c` | No readable wording; pictogram/art. |
| 069 | `00039_00923_0006_arm021_jp.tga` | 128×128 | 65,554 | `8a0458e40e5dd4d4e0aa54b92cd747a652bfac0759576550ea2fa13b96209ccb` | No readable wording; pictogram/art. |
| 070 | `00039_00923_0007_arm022_jp.tga` | 128×128 | 65,554 | `13bada49dd14d98580b0ddfbbaf1b2966245fe825c72835c2b2d3d53646ed486` | No readable wording; pictogram/art. |
| 071 | `00039_00923_0008_arm023_jp.tga` | 128×128 | 65,554 | `2790ecce4066a9453d4e1fa633369db3141ed25f38a41da749f8fb28a8d86455` | No readable wording; pictogram/art. |
| 072 | `00039_00923_0009_arm024_jp.tga` | 128×128 | 65,554 | `330b2709351400da58e1d912d10932d711f05cff185c9a3f82b984a0ea33d67e` | No readable wording; pictogram/art. |
| 073 | `00039_00923_0010_arm025_jp.tga` | 128×128 | 65,554 | `66c6b45b2a48ee217cad5b4c85a37969560e58c3a739144656ba124dbb2b733d` | No readable wording; pictogram/art. |
| 074 | `00039_00923_0011_arm026_jp.tga` | 128×128 | 65,554 | `2ab8fcccce34235ac2d3f806816e54a0a559e6d9e8e1fa90d82ff874c9c90623` | No readable wording; pictogram/art. |
| 075 | `00039_00923_0012_arm027_jp.tga` | 128×128 | 65,554 | `7d49dd7631fcc0aecdb5d8fb0b7726f932a8acb7b17facaa1735ed7f49da0321` | No readable wording; pictogram/art. |
| 076 | `00039_00923_0013_arm028_jp.tga` | 128×128 | 65,554 | `32beb431ff76bf6f975ada6fdd427e64616e26a4f5e86a239e81c079323c3e28` | No readable wording; pictogram/art. |
| 077 | `00039_00923_0014_arm029_jp.tga` | 128×128 | 65,554 | `dded34aa39968496453cc2639637519589a2c0ed8e90c81feb95130efa22f753` | No readable wording; pictogram/art. |
| 078 | `00039_00924_0000_arm030_jp.tga` | 128×128 | 65,554 | `fcd23738e59a002e8798c9ff425fbf43fbace667e516e988125b1f1baa401d02` | No readable wording; pictogram/art. |
| 079 | `00039_00924_0001_arm031_jp.tga` | 128×128 | 65,554 | `26086bd703f7c5ae845e3c6bb8445a0cf0a352f83b9849591503a45740bbe587` | No readable wording; pictogram/art. |
| 080 | `00039_00924_0002_arm032_jp.tga` | 128×128 | 65,554 | `385be48d0f7c847bbd7b67b6cc896a26fe5e0eaae90f0ab54cffb38d754f8ff3` | No readable wording; pictogram/art. |
| 081 | `00039_00924_0003_arm033_jp.tga` | 128×128 | 65,554 | `736b14eb933f2a4da2b7684f9f3f8d00e7e563fc79ca8dd25b1c75482a0fa103` | No readable wording; pictogram/art. |
| 082 | `00039_00924_0004_arm034_jp.tga` | 128×128 | 65,554 | `48ae6a09e761a12903d487a07b021c1bfec4d4f22d10e4f83794324a8e7bcdad` | No readable wording; pictogram/art. |
| 083 | `00039_00924_0005_arm035_jp.tga` | 128×128 | 65,554 | `db9cc83067675880202a29b8214537af358aa0cc5e8e62559d771fb1f4f5efb7` | No readable wording; pictogram/art. |
| 084 | `00039_00924_0006_arm036_jp.tga` | 128×128 | 65,554 | `d75f8ee7d8d8646dff078462ff14539b65754ef06b9a39318d5356bd76fba759` | No readable wording; pictogram/art. |
| 085 | `00039_00924_0007_arm037_jp.tga` | 128×128 | 65,554 | `59b6ed297bc63f89e4a3fad8b7d47a79efb0cc28693711b056fce87041e2c03a` | No readable wording; pictogram/art. |
| 086 | `00039_00924_0008_arm038_jp.tga` | 128×128 | 65,554 | `d9c06c83ff95bd55ead839077895aa6bbacad3bfeac8f6964e1028c2053e5c90` | No readable wording; pictogram/art. |
| 087 | `00039_00924_0009_arm039_jp.tga` | 128×128 | 65,554 | `eab5f75d951e9992607242ce16497d2e082a9a92df14fd5effac4b21d274dee1` | No readable wording; pictogram/art. |
| 088 | `00039_00924_0010_arm040_jp.tga` | 128×128 | 65,554 | `64457963d3ddb3cfb83e38ddc9ecceb11d4e367718a0158202dc0390d924f7a3` | No readable wording; pictogram/art. |
| 089 | `00039_00924_0011_arm041_jp.tga` | 128×128 | 65,554 | `c9cdf8ecaf4e74fa447a859b1e8ce0df56ce5f165530b6267399b732fd87d7bf` | No readable wording; pictogram/art. |
| 090 | `00039_00924_0012_arm042_jp.tga` | 128×128 | 65,554 | `5e05ab1e322899e6fe091cec1f488608b5de7de7b6b4b1dcfc6a067740d0c10b` | No readable wording; pictogram/art. |
| 091 | `00039_00924_0013_arm043_jp.tga` | 128×128 | 65,554 | `d793ccd92ca55f8fc67d9d4f0cfeb0cfb43ebb37eaae98d60cf58e9745a17da2` | No readable wording; pictogram/art. |
| 092 | `00039_00924_0014_arm044_jp.tga` | 128×128 | 65,554 | `1ec6098632897a786807ff5d8c46485fd70da6d4e0cc48f0fc9898e6cbc78198` | No readable wording; pictogram/art. |
| 093 | `00039_00925_0000_arm045_jp.tga` | 128×128 | 65,554 | `1aab276de7603accc1e3801cfcef87e8216544a25ac48139eaa26018057f2f1c` | No readable wording; pictogram/art. |
| 094 | `00039_00925_0001_arm046_jp.tga` | 128×128 | 65,554 | `a373e8bbd7a219554a10c21592634092b3b73e7f24047ff92929af2eab8777bb` | No readable wording; pictogram/art. |
| 095 | `00039_00925_0002_arm047_jp.tga` | 128×128 | 65,554 | `93e1096903df53fbfdd919b955d49d5101ca231431e1bd7bb260f3eeda7dd533` | No readable wording; pictogram/art. |
| 096 | `00039_00925_0003_arm048_jp.tga` | 128×128 | 65,554 | `4c903bf095a3f42f779d0413de7ad839fac5062572ab57f0f27a7d9240ccb1bc` | No readable wording; pictogram/art. |
| 097 | `00039_00925_0004_arm049_jp.tga` | 128×128 | 65,554 | `632d7310cb6ffaf23ae2c66c449462a734706dfece1b84cb4c8ca00ac0df6a0c` | No readable wording; pictogram/art. |
| 098 | `00039_00925_0005_arm050_jp.tga` | 128×128 | 65,554 | `74464348963ea93fd689da9ab21aa78b11d9b1368035ba30a1231c58f62c7fca` | No readable wording; pictogram/art. |
| 099 | `00039_00925_0006_arm051_jp.tga` | 128×128 | 65,554 | `1253b4c6f7312799043f2a1bc355ed9f607d608aee62a4730f5f0d832df597bb` | No readable wording; pictogram/art. |
| 100 | `00039_00925_0007_arm052_jp.tga` | 128×128 | 65,554 | `6f595caf244630fc718d181e14e04c10cd82ce8c161032601028829057ed7da9` | No readable wording; pictogram/art. |
| 101 | `00039_00925_0008_arm053_jp.tga` | 128×128 | 65,554 | `4d3eb24135bea3129898f5f71faa843171d7c766f3f6210e1a0e594572e89669` | No readable wording; pictogram/art. |
| 102 | `00039_00925_0009_arm054_jp.tga` | 128×128 | 65,554 | `fabdc7eb82c027b6fc28aa2ec65e216a9c8fde74a371f8b5b4b6e11b137634d4` | No readable wording; pictogram/art. |
| 103 | `00039_00925_0010_arm055_jp.tga` | 128×128 | 65,554 | `31ce8624f7aeff2cdd01be4b8a76ae34594547936e3b38c0a042ae1e1e6b2e66` | No readable wording; pictogram/art. |
| 104 | `00039_00925_0011_arm056_jp.tga` | 128×128 | 65,554 | `04ade7091d5d7631db816d8c9c22261b6970bdef877ea695b5ce46b30a0c0ff4` | No readable wording; pictogram/art. |
| 105 | `00039_00925_0012_arm057_jp.tga` | 128×128 | 65,554 | `71c36753476ba429437abbe8794db861d5e27be492ba438f7a084919421bae32` | No readable wording; pictogram/art. |
| 106 | `00039_00925_0013_arm058_jp.tga` | 128×128 | 65,554 | `d8bcfb3a67070011fe07698302aaceac44e33eb596842a522450c0d775583be4` | No readable wording; pictogram/art. |
| 107 | `00039_00925_0014_arm059_jp.tga` | 128×128 | 65,554 | `7decb8d1cf41fa2258a72e9cda0cf03562b2975cd990e4be0e0ee34f2f9fd1c9` | No readable wording; pictogram/art. |
| 108 | `00039_00926_0000_arm060_jp.tga` | 128×128 | 65,554 | `850b6e2dcb301a9379b37da6e67d357d97942a9c0481d1501bfa54db270ad0fd` | No readable wording; pictogram/art. |
| 109 | `00039_00926_0001_arm061_jp.tga` | 128×128 | 65,554 | `cca8e3fea2dfd6f9435e76dcdfceff0de7f88318f9e603848c721c51897038b3` | No readable wording; pictogram/art. |
| 110 | `00039_00926_0002_arm062_jp.tga` | 128×128 | 65,554 | `c5312d70866be296ad4a6a8de3e6996005abb2bc6f6f59bb4fcd9f1750633e9d` | No readable wording; pictogram/art. |
| 111 | `00039_00926_0003_arm063_jp.tga` | 128×128 | 65,554 | `72be25cc63b4900aa2a17ac2644cd7eb3e3945631e6d0a154eaae94ac342ef5f` | No readable wording; pictogram/art. |
| 112 | `00039_00926_0004_arm064_jp.tga` | 128×128 | 65,554 | `569a83f2a9194a04cc36a6a12df190c98248a54a17dfcfccb1508f8940cf8570` | No readable wording; pictogram/art. |
| 113 | `00039_00926_0005_arm065_jp.tga` | 128×128 | 65,554 | `bfae0a042c0d5c76b17db7aaa29e6ae7463540c306b244b9db4ec5f455ac20d6` | No readable wording; pictogram/art. |
| 114 | `00039_00926_0006_arm066_jp.tga` | 128×128 | 65,554 | `6ed2571aee1ec91d34296ce8c612f5d4de9a81e718127ed59c9f23668205840a` | No readable wording; pictogram/art. |
| 115 | `00039_00926_0007_arm067_jp.tga` | 128×128 | 65,554 | `cd9e171dcbeb4e99650901eed418d6a55a54c30aa54e310fcae4202488938a56` | No readable wording; pictogram/art. |
| 116 | `00039_00926_0008_arm068_jp.tga` | 128×128 | 65,554 | `3242a6e3d1ec9cd9a9f5c04b3cd5e00b1e46e9afa7c981f665ebce3759f97ceb` | No readable wording; pictogram/art. |
| 117 | `00039_00926_0009_arm069_jp.tga` | 128×128 | 65,554 | `ed6e767c0717b181c982a1fc6295f9a82c255a99e64adadb30615fe3d2e71b3f` | No readable wording; pictogram/art. |
| 118 | `00039_00926_0010_arm070_jp.tga` | 128×128 | 65,554 | `8b6388a27b36de3356ccf4fc7ebce035639ba1c028b09c1e8e45559b546511c6` | No readable wording; pictogram/art. |
| 119 | `00039_00926_0011_arm071_jp.tga` | 128×128 | 65,554 | `5ef6d58b4d87b415b55e49f5c352a5c70c8ec706c1d31df8b7a523e20cbcda5f` | No readable wording; pictogram/art. |
| 120 | `00039_00926_0012_arm072_jp.tga` | 128×128 | 65,554 | `f7857eb9e910e40d2b4dfa7eee66213cd0c8b6d1676183e7e5dea1950741280a` | No readable wording; pictogram/art. |
| 121 | `00039_00926_0013_arm073_jp.tga` | 128×128 | 65,554 | `4d5729328eece3695f27ed4e6d33cd034a99ec9ace9795d96f97993763eca468` | No readable wording; pictogram/art. |
| 122 | `00039_00926_0014_arm074_jp.tga` | 128×128 | 65,554 | `40d39c644770c5ca00c008169bcab7a322caab0cc90893bfe509a8ff0c1fa037` | No readable wording; pictogram/art. |
| 123 | `00039_00927_0000_arm075_jp.tga` | 128×128 | 65,554 | `859df0392977b3fa8e3037370f7c8598bc223a1ed65c074b53ad2ffdd9ca8d5a` | No readable wording; pictogram/art. |
| 124 | `00039_00934_0004_icon_jp.tga` | 256×256 | 262,162 | `7e7746dc1f1317ed1e40e5f42f730ba28aa1608cab2b7721e1d267ccd3762db7` | Japanese/English text group B; bounds below. |
| 125 | `00039_00934_0005_icon_armset_jp.tga` | 128×128 | 65,554 | `f8da25f8a3fa2a63285e2d14712415329117171640234246f3e06d30fe0bb550` | Japanese/English text group C; bounds below. |
| 126 | `00039_00940_0006_icon_jp.tga` | 256×256 | 262,162 | `5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9` | Japanese/English text group A; bounds below. |
| 127 | `00039_00940_0007_icon_armset_jp.tga` | 128×128 | 65,554 | `2528971563da1c8ec68bd65aed6776aae13fa0790c60fbd52056feb7976b7946` | Japanese/English text group D; bounds below. |
| 128 | `00039_00991_0010_icon_jp.tga` | 256×256 | 262,162 | `f29cb5aa84303176aab56e981f7ea0ab9f8597e1bf2b8e4680448d8e14d7f151` | Japanese/English text group E; bounds below. |
| 129 | `00039_01006_0000_arm_jp.tga` | 64×64 | 16,402 | `b85644007edd18cda6a259870df48018e0e79ff300f8859ad92e8a69eb0455cc` | No readable wording; pictogram/art. |
| 130 | `00039_01006_0001_battle_jp.tga` | 64×64 | 16,402 | `bd3ec05e1fd2d735d705c10c4e145050bbce27f210b2a9e9e2df48cf54737cba` | No readable wording; pictogram/art. |
| 131 | `00039_01006_0002_bt_geo_jp.tga` | 64×64 | 16,402 | `2364034bcf55b2251692a98e84f96acdbc64c767d305afafae0bc0d9bd6b165c` | No readable wording; pictogram/art. |
| 132 | `00039_01006_0003_cursor_jp.tga` | 128×128 | 65,554 | `c1bb90a2d1275d1e417fe3f94c8328a4d89a8a03585c2fe0b384aff9b60df6d9` | No readable wording; pictogram/art. |
| 133 | `00039_01006_0004_door_cls_jp.tga` | 64×64 | 16,402 | `045bb6605a3c574e6d026cd12563d2a26e0ee00ea56b1a054c7d566d56dea4fc` | No readable wording; pictogram/art. |
| 134 | `00039_01006_0005_door_op_a_jp.tga` | 64×64 | 16,402 | `f381c83494e6e647d15126f62a03277f45c63b1dfebcd872926ba73dfcecedcd` | No readable wording; pictogram/art. |
| 135 | `00039_01006_0006_door_op_b_jp.tga` | 64×64 | 16,402 | `cc6e5742f53c5664b4263361ebbbf853c64ec3196f5acfed335f84efb29f7e82` | No readable wording; pictogram/art. |
| 136 | `00039_01006_0007_dr_geo_jp.tga` | 128×128 | 65,554 | `3fbd4a6d7f93a23160dc998e78c743f641fcb45e4c6b87e61c26a4cab98a1e6e` | No readable wording; pictogram/art. |
| 137 | `00039_01006_0008_eff_000_jp.tga` | 64×64 | 16,402 | `33ca1fda6511d8ac662510e9f90e66b9f45b7a07e51d3b3a1c451acd69f823db` | No readable wording; pictogram/art. |
| 138 | `00039_01006_0009_eff_001_jp.tga` | 128×128 | 65,554 | `54a1da705dcc51e30861cb7d3628af57c33461dda3097a4c5c20a405c639a8a0` | No readable wording; pictogram/art. |
| 139 | `00039_01006_0010_eff_002_jp.tga` | 64×64 | 16,402 | `386409c167b6f45e5fa98b8fa5c9f6385b07f83f24a13d2f4ee2ec3f36b6866d` | No readable wording; pictogram/art. |
| 140 | `00039_01006_0011_eff_003_jp.tga` | 64×64 | 16,402 | `6026011b010834b8ad27e130731bf2c872037bdafcab7ab8ec26448b852f9d1f` | No readable wording; pictogram/art. |
| 141 | `00039_01006_0012_eff_004_jp.tga` | 128×128 | 65,554 | `0e3ae96fde9966b45341f5f240cf7e840d71925d4aba9175aed55659397d686a` | No readable wording; pictogram/art. |
| 142 | `00039_01006_0013_eff_005_jp.tga` | 64×64 | 16,402 | `db40de4c24b57501abf5b952b75776d7b2e0bc30f90eaff1a42adc8e0e91e135` | No readable wording; pictogram/art. |
| 143 | `00039_01006_0014_eff_006_jp.tga` | 64×64 | 16,402 | `03e9743aa707bbf20c5562b71bc58054d61b5adb7f30457597c123e94e25bd1c` | No readable wording; pictogram/art. |
| 144 | `00039_01006_0015_eff_007_jp.tga` | 64×64 | 16,402 | `dd7a8778532b8501d5b4a306f3e995e99079cfe167f21c7d4bbf8de6c1e64e08` | No readable wording; pictogram/art. |
| 145 | `00039_01006_0016_eff_008_jp.tga` | 32×32 | 4,114 | `d5e3c987018198f1dc6f8ab49ceca6f6a34d77b8a9e0812da3b17453f390bd30` | No readable wording; pictogram/art. |
| 146 | `00039_01006_0017_eff_009_jp.tga` | 32×32 | 4,114 | `38b13275b077f9fdc20ed999d04c17214b1f6a85634cb3f80191231eaba66b00` | No readable wording; pictogram/art. |
| 147 | `00039_01006_0018_eff010_jp.tga` | 64×32 | 8,210 | `e647de2318442f06d4eab38a25a62faea39040a7a44e9ce7621a5b3ba49b27e0` | No readable wording; pictogram/art. |
| 148 | `00039_01006_0019_event_a_jp.tga` | 64×64 | 16,402 | `36e1bf8ef836c5188e99fe6ce28f9aa225113825889e1da3a33db686de1e11f4` | No readable wording; pictogram/art. |
| 149 | `00039_01006_0020_event_b_jp.tga` | 64×64 | 16,402 | `6be08081a2fd7f309f160ad6fc3b95e0b6fdc207c8474cd832d49b9bf625a599` | No readable wording; pictogram/art. |
| 150 | `00039_01006_0021_gate_jp.tga` | 128×128 | 65,554 | `f16a098addd6d1bd108c196cc6419de09065eb07d86393fd4f914353120d442f` | No readable wording; pictogram/art. |
| 151 | `00039_01006_0022_geo_bt_jp.tga` | 64×64 | 16,402 | `4a473ea87fc24b5ba861d39b086324e2623bece720deed4ca4ee1a89f6b06b93` | No readable wording; pictogram/art. |
| 152 | `00039_01006_0023_geo_dr_jp.tga` | 128×128 | 65,554 | `7a80cb100527c720c015c1c70d6416d499a51f4d84314d76ba0e087d21d218f9` | No readable wording; pictogram/art. |
| 153 | `00039_01006_0024_geo_em_jp.tga` | 64×64 | 16,402 | `ef5e9888a381c23308e70cd79c9e49557e1f1da822b5502ab79539466e2bb570` | No readable wording; pictogram/art. |
| 154 | `00039_01006_0025_geo_get_jp.tga` | 64×64 | 16,402 | `92e23fd14a7bd8f14f3375ca49fe990940bb11b1beb440e69ef5a27c877ab0ae` | No readable wording; pictogram/art. |
| 155 | `00039_01006_0026_geo_inout_jp.tga` | 128×128 | 65,554 | `d2ab99fd05a39db1f93f95dbff6caa66a7959af1a2bd18d2a353e5c11e9ea046` | No readable wording; pictogram/art. |
| 156 | `00039_01006_0027_geo_mr_jp.tga` | 128×128 | 65,554 | `2fb7095e3fe6ac84e3a8b92c959344dca82267399501cf1be99d39abff00aa18` | No readable wording; pictogram/art. |
| 157 | `00039_01006_0028_geo_ms_jp.tga` | 128×128 | 65,554 | `ad18d6d92dc999bc4f0f849d14f03e83647ea3b1ea7fc1043c531a1d7d9827c0` | No readable wording; pictogram/art. |
| 158 | `00039_01006_0029_get_geo_jp.tga` | 64×64 | 16,402 | `92e23fd14a7bd8f14f3375ca49fe990940bb11b1beb440e69ef5a27c877ab0ae` | No readable wording; pictogram/art. |
| 159 | `00039_01006_0030_inout_geo_jp.tga` | 128×128 | 65,554 | `d2ab99fd05a39db1f93f95dbff6caa66a7959af1a2bd18d2a353e5c11e9ea046` | No readable wording; pictogram/art. |
| 160 | `00039_01006_0031_load_s_jp.tga` | 32×32 | 4,114 | `e1798081041f3b5f71492aeafb6da1caee83fea1f3baf548e12047ef5234c5a2` | No readable wording; pictogram/art. |
| 161 | `00039_01006_0032_load_w_jp.tga` | 32×32 | 4,114 | `3ced93351f6c9a8b77b00e0f4e3d40561c3fe1d70bf18ac414b0c56f6a1cffd0` | No readable wording; pictogram/art. |
| 162 | `00039_01006_0033_mar_symbol_jp.tga` | 64×64 | 16,402 | `abefbcd58b195e28b0b03ac962b073893f2974c16cdce1f0d2172344894db644` | No readable wording; pictogram/art. |
| 163 | `00039_01006_0034_mirror_jp.tga` | 256×256 | 262,162 | `3a75a0c9eee0c646e1234697da9a106357383d8c99eb27e4304b211d2e35ecc1` | No readable wording; pictogram/art. |
| 164 | `00039_01006_0035_misson_jp.tga` | 64×64 | 16,402 | `08d9fe1bfe9902dcfd2238e11a2bbe71b3601c34ba88256fd98c713d8926241e` | No readable wording; pictogram/art. |
| 165 | `00039_01006_0036_money_jp.tga` | 64×64 | 16,402 | `0f57ea153c5574ad58d619f63faa74cdd17aa8df2ac448e4d6159e9e3b3c6c94` | No readable wording; pictogram/art. |
| 166 | `00039_01006_0037_ms_geo_jp.tga` | 128×128 | 65,554 | `ad18d6d92dc999bc4f0f849d14f03e83647ea3b1ea7fc1043c531a1d7d9827c0` | No readable wording; pictogram/art. |
| 167 | `00039_01006_0038_mych_fm_jp.tga` | 32×64 | 8,210 | `8eb905ffeadfdb47a0191c17ceee6c2d8b3ad4bae6a66c6387b9d3fee2f45781` | No readable wording; pictogram/art. |
| 168 | `00039_01006_0039_mych_ml_jp.tga` | 32×64 | 8,210 | `68cc86908e73e5c7ab2a8e6e321d15dfc5ff3394a792cd0c1b79ac05451c2bf6` | No readable wording; pictogram/art. |
| 169 | `00039_01006_0040_mv_arrow_jp.tga` | 64×16 | 4,114 | `872a97ea22a6d2f7e57b3d6d84e7f0ac0bcd73da900a714434c0c266c9a22761` | No readable wording; pictogram/art. |
| 170 | `00039_01015_0002_icon_jp.tga` | 256×256 | 262,162 | `5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9` | Japanese/English text group A; bounds below. |
| 171 | `00039_01016_0002_icon_jp.tga` | 256×256 | 262,162 | `5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9` | Japanese/English text group A; bounds below. |
| 172 | `00039_01017_0002_icon_jp.tga` | 256×256 | 262,162 | `5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9` | Japanese/English text group A; bounds below. |
| 173 | `00039_01018_0002_icon_jp.tga` | 256×256 | 262,162 | `5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9` | Japanese/English text group A; bounds below. |
| 174 | `00039_01521_0024_icon_jp.tga` | 256×256 | 262,162 | `5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9` | Japanese/English text group A; bounds below. |
| 175 | `00039_01521_0025_icon_armset_jp.tga` | 128×128 | 65,554 | `a5a5b7fa691c81bd03ec59a8cb83d04bace2ae768596c2acf58118382693ea08` | No readable wording; pictogram/art. |
| 176 | `00039_01521_0026_iconguide_jp.tga` | 64×64 | 16,402 | `8becc696ad41bb534345e4a06866bb44b99d5bb3163655277d7d29fe837a3c29` | No readable wording; pictogram/art. |
| 177 | `00039_01539_0000_icon_jp.tga` | 256×256 | 262,162 | `b34feb0715cbf10cd62be572b51917c3c5ff4864268c2a46ba651e0f8e5b689c` | Japanese/English text group F; bounds below. |
| 178 | `00039_01544_0002_icon_jp.tga` | 256×256 | 262,162 | `5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9` | Japanese/English text group A; bounds below. |
| 179 | `00039_01547_0002_icon_jp.tga` | 256×256 | 262,162 | `5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9` | Japanese/English text group A; bounds below. |
| 180 | `00039_01551_0000_icon_jp.tga` | 256×256 | 262,162 | `5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9` | Japanese/English text group A; bounds below. |
| 181 | `00039_01556_0008_icon_jp.tga` | 256×256 | 262,162 | `5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9` | Japanese/English text group A; bounds below. |
| 182 | `00039_01556_0009_icon_armset_jp.tga` | 128×128 | 65,554 | `2528971563da1c8ec68bd65aed6776aae13fa0790c60fbd52056feb7976b7946` | Japanese/English text group D; bounds below. |
| 183 | `00039_01559_0000_icon_jp.tga` | 256×256 | 262,162 | `95ec03aede5efb6a83314a8777996965c0a5e4249ab396973052686f8b984c6d` | Japanese/English text group G; bounds below. |
| 184 | `00039_01569_0003_icon_jp.tga` | 256×256 | 262,162 | `5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9` | Japanese/English text group A; bounds below. |
| 185 | `00039_01593_0008_icon_jp.tga` | 256×256 | 262,162 | `5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9` | Japanese/English text group A; bounds below. |
| 186 | `00039_01597_0021_icon_jp.tga` | 256×256 | 262,162 | `5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9` | Japanese/English text group A; bounds below. |
| 187 | `00039_01600_0019_icon_jp.tga` | 256×256 | 262,162 | `7e7746dc1f1317ed1e40e5f42f730ba28aa1608cab2b7721e1d267ccd3762db7` | Japanese/English text group B; bounds below. |
| 188 | `00039_01606_0019_icon_jp.tga` | 256×256 | 262,162 | `7e7746dc1f1317ed1e40e5f42f730ba28aa1608cab2b7721e1d267ccd3762db7` | Japanese/English text group B; bounds below. |
| 189 | `00039_01617_0000_icon_jp.tga` | 256×256 | 262,162 | `7e7746dc1f1317ed1e40e5f42f730ba28aa1608cab2b7721e1d267ccd3762db7` | Japanese/English text group B; bounds below. |
| 190 | `00039_01621_0000_icon_jp.tga` | 256×256 | 262,162 | `7e7746dc1f1317ed1e40e5f42f730ba28aa1608cab2b7721e1d267ccd3762db7` | Japanese/English text group B; bounds below. |
| 191 | `00039_01624_0012_icon_jp.tga` | 256×256 | 262,162 | `5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9` | Japanese/English text group A; bounds below. |
| 192 | `00039_01629_0021_icon_jp.tga` | 256×256 | 262,162 | `5492b8956e6c53da77e6aa699411071ea6b2b3c2f39c9680242043086ea7c8b9` | Japanese/English text group A; bounds below. |
| 193 | `00039_01631_0020_icon_jp.tga` | 256×256 | 262,162 | `f1f99d4fd15761377f37d963565aa94864cd17c9a83e9c63bc4ac9f9d73768a6` | Japanese/English text group H; bounds below. |
| 194 | `00039_01635_0033_icon_jp.tga` | 256×256 | 262,162 | `95ec03aede5efb6a83314a8777996965c0a5e4249ab396973052686f8b984c6d` | Japanese/English text group G; bounds below. |

## Review and limits

The 194 filesystem files were matched one-to-one with the 194 `category: icon` Japanese-image rows in `graphics/index.json`; every complete SHA-256 and dimension matched. A bounded header/extent check covered all files, and all were present on numbered nearest-neighbor contact sheets composited over a checkerboard. The eight text-bearing hashes were opened at enlarged scale for bounds review. Repeated images remain individually inventoried rather than being counted as recovered strings only once.

The result is a static texture review. It does not establish glyph encoding, string segmentation, UI composition, texture UVs, screen use, draw order, or runtime readability. The text-bearing rows should be checked against renderer/code or an in-game capture before translation artwork is finalized. No ISO build or emulator validation was run.

References: `graphics/index.json`, `tools/rtx3.py`, [`localization methodology`](../docs/LOCALIZATION_METHODOLOGY.md), [`asset methodology`](../docs/TASK_ASSET_WORKSPACE_METHODOLOGY.md), [`effect audit`](GRAPHIC_TEXT_EFFECTS.md), [`background audit`](GRAPHIC_TEXT_BACKGROUNDS.md), [`weapon audit`](GRAPHIC_TEXT_WEAPONS.md).
