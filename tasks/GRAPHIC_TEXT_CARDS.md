# Card texture text-surface audit (DQ-13)

**Scope:** read-only review of the 672 exported Japanese baselines under `graphics/cards/` and their rows in `graphics/index.json`. No Japanese baseline, English override, catalogue, asset tool, queue/status page, or ISO was modified.

## Method and verification

- Matched all 672 `*_jp.tga` files one-to-one with category `cards` entries in index version 4 (`updated: 2026-09-23`). Recomputed SHA-256 from each complete file and checked it against `image_sha256`; also checked indexed width/height, TGA type 2, no color map, 32-bit pixels, top-origin descriptor `0x28`, and exact `18 + width × height × 4` file length.
- Made six direct-TGA contact sheets covering all 615 unique byte hashes; reviewed them visually. Made four native-pixel close-up sheets for all 145 distinct `plt_*` path records and full-size checks of representative framed card art, illustrated backgrounds, English labels, the low-contrast center strip, and the three code-bearing nameplates. No swizzle, UV mapping, or runtime composition was applied.
- For Japanese nameplate core bounds, counted fully opaque (`A > 220`) near-black (`max(R,G,B) < 40`) pixels in the central plate window `[115,410) × [45,85)`. Bounds are top-left-origin half-open raster pixel coordinates for the dark ink core; faint antialias fringes may extend slightly beyond them. Bounds were found for all 145 nameplates and none touches the measurement window edge. English label bounds below are approximate visible-glyph extents from native TGA previews.

## Findings

| Surface class | Count | Finding |
|---|---:|---|
| Japanese name/caption plates (`plt_*`) | 145 files; 129 unique images | All show Japanese kana/kanji lettering, commonly a short name plus a longer bracketed caption/dialogue. The text core spans `[120,401) × [52,81)` across the family. Sixteen files are byte-identical repeats of another plate. Three final variants also show the alphanumeric code `01A-007`. |
| Existing English text | 5 files | `HURRY UP!`, `Please Wait...`, `DRAW`, `EXTRA TITLE` / `EXTRA BATTLE`, and `Win` / `Lose` / `Draw`. These are already English and are not Japanese translation candidates. |
| Unresolved low-contrast strip | 1 file | `center_bar` is a dark patterned strip with faint block-like content after contrast expansion; no Japanese script or words are confidently readable from this raster alone. Keep as a candidate for contextual review, not as a confirmed Japanese-text surface. |
| No readable writing found | 521 files | Card illustrations, scenery/abstract backgrounds, small character portraits/sprites, and a flame/effect image contain no readable localized wording at the exported raster scale. |

The card family therefore exposes **145 confirmed Japanese text-bearing paths** (21.6% of these 672 images by path count), while exact-byte deduplication reduces those to 129 distinct label rasters. This is an image-path count, not a runtime-use or game-wide coverage percentage. The exact Japanese strings are not transcribed or translated by this audit; a dedicated localization pass should work from these immutable `_jp.tga` sources and verify each English sibling against the measured text area.

No UV placement, sampling mode, draw order, on-screen composition, or runtime use is established by the flat TGA export. The complete per-file catalogue follows.

## Complete inventory

`ID` is the stable row identifier used to point from exact duplicates to their first identical file. The SHA-256 is the full digest of the exported TGA bytes.

| ID | File | Dimensions | SHA-256 | Visual finding |
|---:|---|---:|---|---|
| 001 | `00039_01025_0000_card_001_jp.tga` | 512×512 | `8101bff1e562a0153913835526a2ada35c7b3b68138ed3d42c6488df1cf0d2fb` | Framed card/character illustration; no readable writing. |
| 002 | `00039_01026_0000_card_002_jp.tga` | 512×512 | `efdca600bced8529536dcfdef182b255893d40a205b2e26bee6664c29420d3a0` | Framed card/character illustration; no readable writing. |
| 003 | `00039_01027_0000_card_003_jp.tga` | 512×512 | `a17cf40036a0b265fd029bed76db8f32b92c59c5fff9dea9b9d88948f433c4c0` | Framed card/character illustration; no readable writing. |
| 004 | `00039_01028_0000_card_004_jp.tga` | 512×512 | `84cc96a4fc9c4b2ee789b9bedb4031b4b80eda7cff87b9cba700f14dd6378c84` | Framed card/character illustration; no readable writing. |
| 005 | `00039_01029_0000_card_005_jp.tga` | 512×512 | `5d90fb482364becd11cb18a033a18078381dd5ce46dcbffe9a74f0a28ecbcc06` | Framed card/character illustration; no readable writing. |
| 006 | `00039_01030_0000_card_006_jp.tga` | 512×512 | `1eadad45da75824ad65161a478cdb9f64d1ba2225941aaf98b42720d38de86af` | Framed card/character illustration; no readable writing. |
| 007 | `00039_01031_0000_card_007_jp.tga` | 512×512 | `9b95e5f4d9c8976f080da40c427730e73b94955091150524e29c2ec09c82abf4` | Framed card/character illustration; no readable writing. |
| 008 | `00039_01032_0000_card_008_jp.tga` | 512×512 | `d982d6b50cdae5ff14b28d1da3b6dc51cb325ca471b8ef90205351c56f0cc112` | Framed card/character illustration; no readable writing. |
| 009 | `00039_01033_0000_card_009_jp.tga` | 512×512 | `3ee8d8a7e566617876e214e0c5276391ca80c264045e8158b654a9b214518906` | Framed card/character illustration; no readable writing. |
| 010 | `00039_01034_0000_card_010_jp.tga` | 512×512 | `bae8b291195d6024fbad26ed1c5c0b9dda70f9a11ce5a22d0ba629d9cc5cf617` | Framed card/character illustration; no readable writing. |
| 011 | `00039_01035_0000_card_011_jp.tga` | 512×512 | `17d42d73a347bf3795f5f809309b575287115f8146fb8b65cf3390dab2ddc487` | Framed card/character illustration; no readable writing. |
| 012 | `00039_01036_0000_card_012_jp.tga` | 512×512 | `469528da1a1b0518b7516a172f45a9b7257f1e4fd0f6959e2a39c5c565d97941` | Framed card/character illustration; no readable writing. |
| 013 | `00039_01037_0000_card_013_jp.tga` | 512×512 | `dcd338dd0443251e6e1cc85d9b9ac33c32bced4d7219af5d6828e504a5deb056` | Framed card/character illustration; no readable writing. |
| 014 | `00039_01038_0000_card_014_jp.tga` | 512×512 | `33f1a8a1f0493957e2100a8952c5e075b6c7b1eaf8d16b52f6eaef82a3a5dc97` | Framed card/character illustration; no readable writing. |
| 015 | `00039_01039_0000_card_015_jp.tga` | 512×512 | `80de6712ce3f0de8a671b498c5efbc625f2b116ff764d17122e56ea3fc35b840` | Framed card/character illustration; no readable writing. |
| 016 | `00039_01040_0000_card_016_jp.tga` | 512×512 | `daaae2460e672992e6b536324017df0b46a4d6946d690fb685e3455809a0cf1e` | Framed card/character illustration; no readable writing. |
| 017 | `00039_01041_0000_card_017_jp.tga` | 512×512 | `30b64c616a5eb9a0cb76cfa9239572b08ed32efcea658c4f6f40fb81d6f55668` | Framed card/character illustration; no readable writing. |
| 018 | `00039_01042_0000_card_018_jp.tga` | 512×512 | `4e9f8d42c791c1422e0517208f7dcfb0e843c1b93575e7adea86830cbbbf2fb8` | Framed card/character illustration; no readable writing. |
| 019 | `00039_01043_0000_card_019_jp.tga` | 512×512 | `5579a0b3eea2c1e793e10bb23bc81afceaeace4f409827b38355b42f325676e5` | Framed card/character illustration; no readable writing. |
| 020 | `00039_01044_0000_card_020_jp.tga` | 512×512 | `9b996cfb21c28ff0694cc1668870e3e23c2942729fa42d566209b487d958f08b` | Framed card/character illustration; no readable writing. |
| 021 | `00039_01045_0000_card_021_jp.tga` | 512×512 | `c30ddbc1e70e8ce4f24f9a233cc6e3980bed1a9c76a99700f0399d061d323664` | Framed card/character illustration; no readable writing. |
| 022 | `00039_01046_0000_card_022_jp.tga` | 512×512 | `7efb6a7456dc494f76b1b5b19025e2062a3a32b3f452871c7c3e8c7dc53c9b3a` | Framed card/character illustration; no readable writing. |
| 023 | `00039_01047_0000_card_023_jp.tga` | 512×512 | `fa42f644b198bf0f2035b46f0ddbf85ed8e80c381b42b3d19287a12e5de42c26` | Framed card/character illustration; no readable writing. |
| 024 | `00039_01048_0000_card_024_jp.tga` | 512×512 | `a8a38270df581f0169b724f1f2459a420240d4921cca23c77d38d018c48bc380` | Framed card/character illustration; no readable writing. |
| 025 | `00039_01049_0000_card_025_jp.tga` | 512×512 | `4fceb7da2964c291c8af1aac65d836a85c11559c457409c5d421f4031b210c21` | Framed card/character illustration; no readable writing. |
| 026 | `00039_01050_0000_card_026_jp.tga` | 512×512 | `59bf9ab99f6b0ecf43c614205d17d7dfc077db74cd4cac573337b8160c71df1d` | Framed card/character illustration; no readable writing. |
| 027 | `00039_01051_0000_card_027_jp.tga` | 512×512 | `311ae99e89660f0831216d4b52627af450d77d9c6739e5121b37b21dc9306bf3` | Framed card/character illustration; no readable writing. |
| 028 | `00039_01052_0000_card_028_jp.tga` | 512×512 | `5ec4f4de0d4fc6124ed0f6983d681b817af752b18f7d3526556dc2970dd01ba5` | Framed card/character illustration; no readable writing. |
| 029 | `00039_01053_0000_card_029_jp.tga` | 512×512 | `08c4a1846eecc1b941fde30f56f5f7991a7830c2399988e5407d6afd6bc0e785` | Framed card/character illustration; no readable writing. |
| 030 | `00039_01054_0000_card_030_jp.tga` | 512×512 | `4ab7f7869d512338fff328b7faa149c00ccd1f3cceca007f78a6d498255f7278` | Framed card/character illustration; no readable writing. |
| 031 | `00039_01055_0000_card_031_jp.tga` | 512×512 | `fd382b43daab42594a1f1afafa91f5acb9670668eb9786b666fe3622f569f000` | Framed card/character illustration; no readable writing. |
| 032 | `00039_01056_0000_card_032_jp.tga` | 512×512 | `f63bb1d4093cf2167d17766bc9fb70ab4c5586cb4ef731ab287a6a2546e70216` | Framed card/character illustration; no readable writing. |
| 033 | `00039_01057_0000_card_033_jp.tga` | 512×512 | `b33c14394b916e1e68ebd4a522b2245f51641b6630c78a1d95a11045dcf207f5` | Framed card/character illustration; no readable writing. |
| 034 | `00039_01058_0000_card_034_jp.tga` | 512×512 | `e56c4eee86c7a9c11eab1fd2d26245ac6949a5d70f777311aaa3a959d7cd6b73` | Framed card/character illustration; no readable writing. |
| 035 | `00039_01059_0000_card_035_jp.tga` | 512×512 | `a85916f9c5e5942b979a28a17946ba963853b6a45740a09e3dfc0df8fd739fda` | Framed card/character illustration; no readable writing. |
| 036 | `00039_01060_0000_card_036_jp.tga` | 512×512 | `ed1fb3042a288a4b87f6803ae9a119baf2378ba28c911ab2de3da5703e257ca4` | Framed card/character illustration; no readable writing. |
| 037 | `00039_01061_0000_card_037_jp.tga` | 512×512 | `725cb44cdce5ef47d49115bce3db8123c2ed26cd10b3ce2a41818cac0c880980` | Framed card/character illustration; no readable writing. |
| 038 | `00039_01062_0000_card_038_jp.tga` | 512×512 | `2919642c20d3d660215a799b4c927c2fb49275271ec614106533d6af1b9e4a6e` | Framed card/character illustration; no readable writing. |
| 039 | `00039_01063_0000_card_039_jp.tga` | 512×512 | `e3538923b55ff72b350b62ca4cbb984dd5808f894f7b4792c85e0c2665132e9c` | Framed card/character illustration; no readable writing. |
| 040 | `00039_01064_0000_card_040_jp.tga` | 512×512 | `03f52fd76032b33fa88d23dabde025adee599b0910594a175b56c516bb62ee38` | Framed card/character illustration; no readable writing. |
| 041 | `00039_01065_0000_card_041_jp.tga` | 512×512 | `d926e64d740051ed87378da7d358902bd36f8b7f5d5c2d3307be2611254a20b0` | Framed card/character illustration; no readable writing. |
| 042 | `00039_01066_0000_card_042_jp.tga` | 512×512 | `e608583187f4051a767ab9e7fc0615ea56b237fb1978779a22e43f447743f6f1` | Framed card/character illustration; no readable writing. |
| 043 | `00039_01067_0000_card_043_jp.tga` | 512×512 | `ed1069a3060094a8908eee7716ec4f0e58bc9078ad71b2491cf4df071febe44b` | Framed card/character illustration; no readable writing. |
| 044 | `00039_01068_0000_card_044_jp.tga` | 512×512 | `fe746d18c1bf1e6bd97a91598951abb7eb29fcf765742aaeffba9278ccb9912a` | Framed card/character illustration; no readable writing. |
| 045 | `00039_01069_0000_card_045_jp.tga` | 512×512 | `3222205b94a7080c8e672547ed406354de9915e2ff8776a377d48946a5ac5b73` | Framed card/character illustration; no readable writing. |
| 046 | `00039_01070_0000_card_046_jp.tga` | 512×512 | `c4bb13f28ba46a81d1dbdf8ac4e2b2085dff318faa96b208d09880c44adc9171` | Framed card/character illustration; no readable writing. |
| 047 | `00039_01071_0000_card_047_jp.tga` | 512×512 | `864b709f28d9a9cff073540e427a6a8065bc4a5d7a405b3ecfe1e3d59cc4df67` | Framed card/character illustration; no readable writing. |
| 048 | `00039_01072_0000_card_048_jp.tga` | 512×512 | `911aaa4e7ca8e6a02185efb950c9ec583bd77379a732744ca2bf5d66cd5532b5` | Framed card/character illustration; no readable writing. |
| 049 | `00039_01073_0000_card_049_jp.tga` | 512×512 | `fe2d19727c7490478d1d3188131f981a53ab25aa67221c1b4c37a9042b5799fb` | Framed card/character illustration; no readable writing. |
| 050 | `00039_01074_0000_card_050_jp.tga` | 512×512 | `79f8c6f4e5fb747a90ce7f3daae8736a4e3efbc8633e3519ba2e5513f8d14bc3` | Framed card/character illustration; no readable writing. |
| 051 | `00039_01075_0000_card_051_jp.tga` | 512×512 | `d9adac27a95b912c4f538611cb5bc18fc7748fbfd138010dd4a7ee3fbf5fa84a` | Framed card/character illustration; no readable writing. |
| 052 | `00039_01076_0000_card_052_jp.tga` | 512×512 | `2f6d28aa061d011df5ff889f9a1b7c4d3e4e79e16cb221442b411420df0c13c5` | Framed card/character illustration; no readable writing. |
| 053 | `00039_01077_0000_card_053_jp.tga` | 512×512 | `f7a8b36033382373c742c3f646842097cdf1b5d52c1c66cb06184cbbab70004b` | Framed card/character illustration; no readable writing. |
| 054 | `00039_01078_0000_card_054_jp.tga` | 512×512 | `8db38702cea1652b7d93372d15ebd904c4195a1ee2d2f97a560e0c65a2a4fd4c` | Framed card/character illustration; no readable writing. |
| 055 | `00039_01079_0000_card_055_jp.tga` | 512×512 | `031a952736c517c1bd0fc362d19e63501bf6813c45377daea1fc6338e8b69199` | Framed card/character illustration; no readable writing. |
| 056 | `00039_01080_0000_card_056_jp.tga` | 512×512 | `427a063005cbc2aa58a9f416db8b18a57f2e3c98582b56e32c2e52ee61cf2f68` | Framed card/character illustration; no readable writing. |
| 057 | `00039_01081_0000_card_057_jp.tga` | 512×512 | `fa0f0a120b6679a562ea3a71dd0386ca9c448c545d235984625b8f203035a29d` | Framed card/character illustration; no readable writing. |
| 058 | `00039_01082_0000_card_058_jp.tga` | 512×512 | `c638c9466bd6e30781b0e2769ca8a3dc553e0c9aa9aa2281b5e5f95a1d76918b` | Framed card/character illustration; no readable writing. |
| 059 | `00039_01083_0000_card_059_jp.tga` | 512×512 | `2366a14f1838382bf92d8e88a885408b49afee5bc558736aaa0e9718a9050ba8` | Framed card/character illustration; no readable writing. |
| 060 | `00039_01084_0000_card_060_jp.tga` | 512×512 | `096d51d11c78e834f77b89c014584b548169cbc85a1ff238caf1417dfb229349` | Framed card/character illustration; no readable writing. |
| 061 | `00039_01085_0000_card_061_jp.tga` | 512×512 | `41efce15cec54d52897f2b84355640783793ce4c0ae9ad60cac23ae78eb4909a` | Framed card/character illustration; no readable writing. |
| 062 | `00039_01086_0000_card_062_jp.tga` | 512×512 | `c17d0d06cf85e6bb6702de0f833fb5747f1fad97f12272b6ff01cd6067c2072e` | Framed card/character illustration; no readable writing. |
| 063 | `00039_01087_0000_card_063_jp.tga` | 512×512 | `1811f349aba6a70f23393485b0145eee01b7d05b24562fb0ef873d78b1a69c34` | Framed card/character illustration; no readable writing. |
| 064 | `00039_01088_0000_card_064_jp.tga` | 512×512 | `ae39f148fdd2c26b7300b0523462989298b8e32c6ac97aa8b0009fea85789a82` | Framed card/character illustration; no readable writing. |
| 065 | `00039_01089_0000_card_065_jp.tga` | 512×512 | `d552e51e9283de93d52bcb591c7d8762dcc01f904cee75ab8761d1339a976d0c` | Framed card/character illustration; no readable writing. |
| 066 | `00039_01090_0000_card_066_jp.tga` | 512×512 | `208ea0d52849ccf88ae893b4d2ec37217bd73e091b821a01b5037728469bd4a3` | Framed card/character illustration; no readable writing. |
| 067 | `00039_01091_0000_card_067_jp.tga` | 512×512 | `4754c5cf6a30521d753b4f1a6a78a39386f4f920b1acecba5682e122085306a4` | Framed card/character illustration; no readable writing. |
| 068 | `00039_01092_0000_card_068_jp.tga` | 512×512 | `d22fa1e6bc7961c0813f587d86e06ab24fcbaa9bfad8b82a5d64f2aec3ed4faf` | Framed card/character illustration; no readable writing. |
| 069 | `00039_01093_0000_card_069_jp.tga` | 512×512 | `c24e29a11510386cb2711cb0c8fdeaadaa02afc29100aad3fb246ddc8ac86e7d` | Framed card/character illustration; no readable writing. |
| 070 | `00039_01094_0000_card_070_jp.tga` | 512×512 | `7b4de4f4a1947e8a399a15b3b25f6307c5819b4211093eea6934670a11d6e5d3` | Framed card/character illustration; no readable writing. |
| 071 | `00039_01095_0000_card_071_jp.tga` | 512×512 | `87629f10c6c4f4f19340f3372ac9357971f1d6830cfd237f1371a8a965ec0d34` | Framed card/character illustration; no readable writing. |
| 072 | `00039_01096_0000_card_072_jp.tga` | 512×512 | `7aa48a06894e591d4381d82d4b127af238829c57d917e7ca7486b817d16761b9` | Framed card/character illustration; no readable writing. |
| 073 | `00039_01097_0000_card_073_jp.tga` | 512×512 | `22b7382e2b8524b0c6e9a8b1bfd2acc2e6e4f85d3d4378ec1b232aa5223afa1b` | Framed card/character illustration; no readable writing. |
| 074 | `00039_01098_0000_card_074_jp.tga` | 512×512 | `f3c8681a07c01ea9414ed9b3b8e05da2d64b617d8ac078e77ecddf86e2d6262b` | Framed card/character illustration; no readable writing. |
| 075 | `00039_01099_0000_card_075_jp.tga` | 512×512 | `a9fba09b3fd46b30aacb0c81ff01adaa9d5e289ebfb759907c5d88b5aedf5a02` | Framed card/character illustration; no readable writing. |
| 076 | `00039_01100_0000_card_076_jp.tga` | 512×512 | `806c902d8fb11ddc2fe6d41c4e6498ae7a972711d6bef9186e2fb44184147467` | Framed card/character illustration; no readable writing. |
| 077 | `00039_01101_0000_card_077_jp.tga` | 512×512 | `054d3ba9bdef418b6254b14c0d46f65a658d562555f7700002474252552ccef6` | Framed card/character illustration; no readable writing. |
| 078 | `00039_01102_0000_card_078_jp.tga` | 512×512 | `b884f894f912f50ff804c1bfea63f3d5c575381b5f511dad30f4f4807119c5f1` | Framed card/character illustration; no readable writing. |
| 079 | `00039_01103_0000_card_079_jp.tga` | 512×512 | `c9925575352aa9529ccf4585c07e76da77c5cf8ed3d3f85defe349093b5a0dca` | Framed card/character illustration; no readable writing. |
| 080 | `00039_01104_0000_card_080_jp.tga` | 512×512 | `6c1ec28e430aa200e455509cacd49399618baad58db8226f1a8ad6f807767d67` | Framed card/character illustration; no readable writing. |
| 081 | `00039_01105_0000_card_081_jp.tga` | 512×512 | `cb3f813a939d471bf09591a027fb49315ac9a64ab18368435fe1b6b4f784e7d5` | Framed card/character illustration; no readable writing. |
| 082 | `00039_01106_0000_card_082_jp.tga` | 512×512 | `4a213f526dcf326ff9bd0f110689e841abaecd6522fcb1c56540b8d493da398e` | Framed card/character illustration; no readable writing. |
| 083 | `00039_01107_0000_card_083_jp.tga` | 512×512 | `60207fc1b4c5fb79fc8433cb2ea861d73c66a260849d3795cf5eeaad5d3bbc61` | Framed card/character illustration; no readable writing. |
| 084 | `00039_01108_0000_card_084_jp.tga` | 512×512 | `b703421ec0b702f405d9b194f5fa6efc146c3fa4685d2b41e457f4580b80b372` | Framed card/character illustration; no readable writing. |
| 085 | `00039_01109_0000_card_085_jp.tga` | 512×512 | `c584601749eeb8a4369a1d0a0973d6972ba6fef1674a16b2a75596ca1133602a` | Framed card/character illustration; no readable writing. |
| 086 | `00039_01110_0000_card_086_jp.tga` | 512×512 | `3bdc57443fd433e8091df212915973aa46002648a2f06a80f74758c259626e1f` | Framed card/character illustration; no readable writing. |
| 087 | `00039_01111_0000_card_087_jp.tga` | 512×512 | `00a89da49b37456ea49ce59e40ecec43db0c41b94e7b9cd3fdbc4f51929f26cc` | Framed card/character illustration; no readable writing. |
| 088 | `00039_01112_0000_card_088_jp.tga` | 512×512 | `ed611f27c31e0153e408359926dfd4c7738b6752345d02600164a80d9b917fc9` | Framed card/character illustration; no readable writing. |
| 089 | `00039_01113_0000_card_089_jp.tga` | 512×512 | `bb2cd9bae563a92f713639e9799d9188f905a26caa611a8506946d606d912ac9` | Framed card/character illustration; no readable writing. |
| 090 | `00039_01114_0000_card_090_jp.tga` | 512×512 | `8cab04c20cbeaf36182306ed2148e6c708393ab3b428a5f2e83cee621680d526` | Framed card/character illustration; no readable writing. |
| 091 | `00039_01115_0000_card_091_jp.tga` | 512×512 | `20a1fbcd2fdd59d91e3af422dde9a203410e6b8c5cb8aff2656923fc7e4d0506` | Framed card/character illustration; no readable writing. |
| 092 | `00039_01116_0000_card_092_jp.tga` | 512×512 | `ff0ad33035893193ad2a688a398b837c65d943b769f0a69add06dacfcd6e406d` | Framed card/character illustration; no readable writing. |
| 093 | `00039_01117_0000_card_093_jp.tga` | 512×512 | `ad346ae5d48bfa0f3936dc8012c9a60287e01043aca8ada13f0ccd3ea544343d` | Framed card/character illustration; no readable writing. |
| 094 | `00039_01118_0000_card_094_jp.tga` | 512×512 | `3e2a149bba0c09d4d24b8f47a80e6cf052a25b297182e4c554d22eb50a815421` | Framed card/character illustration; no readable writing. |
| 095 | `00039_01119_0000_card_095_jp.tga` | 512×512 | `3c3223e8d8232080b4c5fa9134afebb65f5308b7db57bafa0e349a395c9a9f39` | Framed card/character illustration; no readable writing. |
| 096 | `00039_01120_0000_card_096_jp.tga` | 512×512 | `487cb5437968f6a854cf1fb3667004282a8a73f1aa1f8ff9c26bca3528ed100c` | Framed card/character illustration; no readable writing. |
| 097 | `00039_01121_0000_card_097_jp.tga` | 512×512 | `1df5eede5b2eafd0abfd1ffe07889ee5084b64b440b9c61d96f72032241ff4ff` | Framed card/character illustration; no readable writing. |
| 098 | `00039_01122_0000_card_098_jp.tga` | 512×512 | `41de390d0bf86e8dbd3afe77402e7ec8f3a0cf33d728819f8cfd580d42d070eb` | Framed card/character illustration; no readable writing. |
| 099 | `00039_01123_0000_card_099_jp.tga` | 512×512 | `8dddacb889bb86427518e55dd8c461d66f03808587a07dc2d2a30cf8798ffcf2` | Framed card/character illustration; no readable writing. |
| 100 | `00039_01124_0000_card_100_jp.tga` | 512×512 | `399a660bb93a230e571f9ea3275b1ebf3bbfa1d08bf41184d828e4ca73741c23` | Framed card/character illustration; no readable writing. |
| 101 | `00039_01125_0000_card_101_jp.tga` | 512×512 | `3dde28d86fc87ac66827825a344d11d7ecc2f5007dbcd7800f0c2eec7f319a95` | Framed card/character illustration; no readable writing. |
| 102 | `00039_01126_0000_card_102_jp.tga` | 512×512 | `b29ceed0570f4633535a29a8b6132309ffa49743224e6b34f8a5c8f4bff26879` | Framed card/character illustration; no readable writing. |
| 103 | `00039_01127_0000_card_103_jp.tga` | 512×512 | `4d7d5e27ffdec24c30a2a8f71007b6c8419154fc87fef1091db4edab54985eed` | Framed card/character illustration; no readable writing. |
| 104 | `00039_01128_0000_card_104_jp.tga` | 512×512 | `f9bd6d21fe2dc8068acb6d0723e0b85820a185ad9f9be1a28817f2dbec4b71c7` | Framed card/character illustration; no readable writing. |
| 105 | `00039_01129_0000_card_105_jp.tga` | 512×512 | `cff0c86bb40dca69859ade618476acb13dd551633915237063a12e0675e2b26c` | Framed card/character illustration; no readable writing. |
| 106 | `00039_01130_0000_card_106_jp.tga` | 512×512 | `3afae9980dfd095a6f9b6501be72ddde62d7148d81a091117d17eb779c109af4` | Framed card/character illustration; no readable writing. |
| 107 | `00039_01131_0000_card_107_jp.tga` | 512×512 | `fd6c6b257d4c7090a67886ef6402fcb084aa38777aac28a517da7f53f3c1d097` | Framed card/character illustration; no readable writing. |
| 108 | `00039_01132_0000_card_108_jp.tga` | 512×512 | `8106c98b2eb3a397073e45c5bd1427d8f61789e39bd818f6c12287292c4952f3` | Framed card/character illustration; no readable writing. |
| 109 | `00039_01133_0000_card_109_jp.tga` | 512×512 | `d5155d08e64bafe26610844cd2eb77f78730ce3ccfa98c13068390fb51795742` | Framed card/character illustration; no readable writing. |
| 110 | `00039_01134_0000_card_110_jp.tga` | 512×512 | `eebd120d189d3c97dafe0ec88bc1cf9a7b3129b1485a6fe66fe592bb097bf242` | Framed card/character illustration; no readable writing. |
| 111 | `00039_01135_0000_card_111_jp.tga` | 512×512 | `fab28b99cc34ad5d836b4286c183a71eaf577444beb197e355fe62ba67ad1c80` | Framed card/character illustration; no readable writing. |
| 112 | `00039_01136_0000_card_112_jp.tga` | 512×512 | `2739c5b973277a511276d6be8985010a0211abbebeb4961d8d1d94005da75ab6` | Framed card/character illustration; no readable writing. |
| 113 | `00039_01137_0000_card_113_jp.tga` | 512×512 | `51b33d558041b73afb384c53502b97ce7edd45cdf02f06a03106988409aff0c7` | Framed card/character illustration; no readable writing. |
| 114 | `00039_01138_0000_card_114_jp.tga` | 512×512 | `dcebb44ae11d2f272431fd6cd3f652c379e16f94a680c2dfd57d58a787388c19` | Framed card/character illustration; no readable writing. |
| 115 | `00039_01139_0000_card_115_jp.tga` | 512×512 | `71356599f1936cb3a2dcc4bec442d9e21656a2c3fad397396eb92a7cecb0262a` | Framed card/character illustration; no readable writing. |
| 116 | `00039_01140_0000_card_116_jp.tga` | 512×512 | `c07878854a4b8abc54c2dfe9bbd6d169af2149ba67ba6c7bbd8216e5777f96a1` | Framed card/character illustration; no readable writing. |
| 117 | `00039_01141_0000_card_117_jp.tga` | 512×512 | `65c1ad69f1158aa0532108e1e2f11219f3d2443ff29413f34c7a7d967ec90b4e` | Framed card/character illustration; no readable writing. |
| 118 | `00039_01142_0000_card_118_jp.tga` | 512×512 | `7f6b92f54c89e42048945a0fec1179d49e5acb2d6a15da90ed093c248a9f3754` | Framed card/character illustration; no readable writing. |
| 119 | `00039_01143_0000_card_119_jp.tga` | 512×512 | `2d2f820ff2801b8437e1af6d7eb873a1b400cdc29d01c1f058e9dfc122efbd9b` | Framed card/character illustration; no readable writing. |
| 120 | `00039_01144_0000_card_120_jp.tga` | 512×512 | `38be1d6c23323ca56f75bcc43a03c856c318aeb770b19d76218040e7fe766fa7` | Framed card/character illustration; no readable writing. |
| 121 | `00039_01145_0000_card_121_jp.tga` | 512×512 | `34ba0794c66b32d02af0c02976e95f5f551feb58ba686083db23ebc0f6fa776c` | Framed card/character illustration; no readable writing. |
| 122 | `00039_01146_0000_card_122_jp.tga` | 512×512 | `233c2357990d8b79eace13f1da08f79d857dd0eab61898ce660499c5280d420f` | Framed card/character illustration; no readable writing. |
| 123 | `00039_01147_0000_card_123_jp.tga` | 512×512 | `19da92364af9e301bb5da4595534e1e03fdfadce5b3c9151cc9fd5145d0118f4` | Framed card/character illustration; no readable writing. |
| 124 | `00039_01148_0000_card_124_jp.tga` | 512×512 | `4a831ecff4c80bdb0bfb8258461b26cee4f3cff03896451158605e846ad59970` | Framed card/character illustration; no readable writing. |
| 125 | `00039_01149_0000_card_125_jp.tga` | 512×512 | `039c9a08fe74888c41fe5f8bd5d0797b54809020756ffd7ab1ec70c11c06557f` | Framed card/character illustration; no readable writing. |
| 126 | `00039_01150_0000_card_126_jp.tga` | 512×512 | `5d4a55fd2ebbbdab0f1dacc2d29845b2ef7dc851f485e57fb03da172001b72b5` | Framed card/character illustration; no readable writing. |
| 127 | `00039_01151_0000_card_127_jp.tga` | 512×512 | `531c4105b2c5a0fa852dadb848d6b6e9645f5d992609ca31d4a2d7f9aa19e7f2` | Framed card/character illustration; no readable writing. |
| 128 | `00039_01152_0000_card_128_jp.tga` | 512×512 | `922957103bdca11e95f26c816f257e59b99109ce28e3c5d2c8409d8bf7a2fcf7` | Framed card/character illustration; no readable writing. |
| 129 | `00039_01153_0000_card_129_jp.tga` | 512×512 | `fa6478f24315b00bf6b56db6d86f3c1ae727f2fb63eb62323e950b9fa6c1351c` | Framed card/character illustration; no readable writing. |
| 130 | `00039_01154_0000_card_130_jp.tga` | 512×512 | `ba678d40f30ec3d1beb482083c56c521ecb4a19a454be88b1236579b3c2ab342` | Framed card/character illustration; no readable writing. |
| 131 | `00039_01155_0000_card_131_jp.tga` | 512×512 | `00084e6df1ee6ef000ce64e19ef2c2d9b4ed523d778b3817c4c612c2e8850c9e` | Framed card/character illustration; no readable writing. |
| 132 | `00039_01156_0000_card_132_jp.tga` | 512×512 | `5c878d4ba7d445122f0ad30775452c9160dc12906051624e7bbfc8d5b1873db7` | Framed card/character illustration; no readable writing. |
| 133 | `00039_01157_0000_card_133_jp.tga` | 512×512 | `6ba064304fe1dd9be22fdd8e8063d25f6b341982dddc828f58217d3029ca0873` | Framed card/character illustration; no readable writing. |
| 134 | `00039_01158_0000_card_134_jp.tga` | 512×512 | `047f9e408ee0bd921ac82163e47d761248d970fc7168b410dd11b330c694c151` | Framed card/character illustration; no readable writing. |
| 135 | `00039_01159_0000_card_135_jp.tga` | 512×512 | `8aed30e282fed8893307c32fdd410ca92db773b93297576021a32238f67ec8ac` | Framed card/character illustration; no readable writing. |
| 136 | `00039_01160_0000_card_136_jp.tga` | 512×512 | `06706f6096c88ca5c2f2096580d174da30d8bdaf6f69e83395f420303579e28c` | Framed card/character illustration; no readable writing. |
| 137 | `00039_01161_0000_card_137_jp.tga` | 512×512 | `4bc91d661676e183fc1ee6eceebefad5f2ca9c4efcabd017cb52b3ee1e6721d1` | Framed card/character illustration; no readable writing. |
| 138 | `00039_01162_0000_card_138_jp.tga` | 512×512 | `d400b98c4c3a198713974c34a12454788bac476a63307ea4e6f49d1ba2fb73d1` | Framed card/character illustration; no readable writing. |
| 139 | `00039_01163_0000_card_139_jp.tga` | 512×512 | `7aeb1af20540f8ef7c9e6126f7d551061224b24c298656dc62ec2f1855e99146` | Framed card/character illustration; no readable writing. |
| 140 | `00039_01164_0000_card_140_jp.tga` | 512×512 | `5e9d00ec7907b91bc7860acde48f8ca6e98f37946679fe4878acc4709a3dbfe3` | Framed card/character illustration; no readable writing. |
| 141 | `00039_01165_0000_card_141_jp.tga` | 512×512 | `9483e48fe494f9c3b932fb60219f3531d7d064d2c58ce63d6b2d6e0ab9f82547` | Framed card/character illustration; no readable writing. |
| 142 | `00039_01166_0000_card_142_jp.tga` | 512×512 | `ae42f8570a76c2c56b2b75dec64acfbffd419a440686cc7022dec358d9008574` | Framed card/character illustration; no readable writing. |
| 143 | `00039_01167_0000_card_143_jp.tga` | 1024×512 | `ce8a36809bf51eada64ee99d253eda5765d505b2a392424a2d21e036ef572aed` | Framed card/character illustration; no readable writing. |
| 144 | `00039_01168_0000_card_gba_jp.tga` | 512×512 | `7aeb1af20540f8ef7c9e6126f7d551061224b24c298656dc62ec2f1855e99146` | Framed card/character illustration; no readable writing. Exact byte duplicate of #139 `00039_01163_0000_card_139_jp.tga`. |
| 145 | `00039_01169_0000_card_sunday_jp.tga` | 512×512 | `6aa8809a321defec738e5ca6793306993482044c0a5e9c526d3efdae2d4d7843` | Small card portrait/sprite artwork; no readable writing. |
| 146 | `00039_01170_0000_bg_001_jp.tga` | 512×512 | `e7c490b555c8cfa8f38eafc87bc9deace91de3d3bf7dd19942d229afad37021e` | Scenery or abstract card background; no readable writing. |
| 147 | `00039_01171_0000_bg_002_jp.tga` | 512×512 | `f3919aaa65be2e6259dd5880f763d65ab6e15d56c41de987a37193bcc80bc388` | Scenery or abstract card background; no readable writing. |
| 148 | `00039_01172_0000_bg_003_jp.tga` | 512×512 | `d7b4d848c5959a743fbfb417937921f5070d9acf7fb24f52899b53c6c8acaa91` | Scenery or abstract card background; no readable writing. |
| 149 | `00039_01173_0000_bg_004_jp.tga` | 512×512 | `ab978464370bfd67a597f2572ab6b61a952a5e42e144da36f5854c1d8da1d384` | Scenery or abstract card background; no readable writing. |
| 150 | `00039_01174_0000_bg_005_jp.tga` | 512×512 | `25f201a4ab912058d8bef1420fdc47ecd370061068cdb710a7a02adc2abeb35a` | Scenery or abstract card background; no readable writing. |
| 151 | `00039_01175_0000_bg_006_jp.tga` | 512×512 | `4e2ac990da840391350b6c90988895d608784954409d17a98b227a500d909279` | Scenery or abstract card background; no readable writing. |
| 152 | `00039_01176_0000_bg_007_jp.tga` | 512×512 | `c535c4a20311d60a23a3479a357d13425d792169b86b0d0ac1e73db504944c49` | Scenery or abstract card background; no readable writing. |
| 153 | `00039_01177_0000_bg_008_jp.tga` | 512×512 | `5f40e2e25c7604673d6efa437eda10a87fbcc02f65e71c9f32068bda094dca7a` | Scenery or abstract card background; no readable writing. |
| 154 | `00039_01178_0000_bg_009_jp.tga` | 512×512 | `85a2c24593ee15ed173ee8fd1263b7cc5bd6320b1e47aae8159cb4f7eb4ece65` | Scenery or abstract card background; no readable writing. |
| 155 | `00039_01179_0000_bg_010_jp.tga` | 512×512 | `a391eefe7cfb30ed078ccdb6f10cca206f0089ae582565004f847e6a5f093a53` | Scenery or abstract card background; no readable writing. |
| 156 | `00039_01180_0000_bg_011_jp.tga` | 512×512 | `110bb0b5b40b8d12c475d8c881e9b0eacdc87364b821a2f72258ff2574abc23f` | Scenery or abstract card background; no readable writing. |
| 157 | `00039_01181_0000_bg_012_jp.tga` | 512×512 | `10aaaec3f751c3ba56c139c0593e2946e38f5b28b17444a2ba6262bffc58cdb3` | Scenery or abstract card background; no readable writing. |
| 158 | `00039_01182_0000_bg_013_jp.tga` | 512×512 | `04afb61429d35f30f5b663287cd904ef2b88cb6d94ace88169577c8bef58157e` | Scenery or abstract card background; no readable writing. |
| 159 | `00039_01183_0000_bg_014_jp.tga` | 512×512 | `a5cbd6d09cc0a6c83176d6785470e1d25666e0aa21c3742b933d382f6bd9ac51` | Scenery or abstract card background; no readable writing. |
| 160 | `00039_01184_0000_bg_015_jp.tga` | 512×512 | `e8c76de44d97833bedb4bad58e60aecadbc1c3eac026e80259f3c22168f33a9b` | Scenery or abstract card background; no readable writing. |
| 161 | `00039_01185_0000_bg_016_jp.tga` | 512×512 | `b67efc4c482ba46509553d03dc0a6175738076aec8cb27785dc4b7a7b95d8290` | Scenery or abstract card background; no readable writing. |
| 162 | `00039_01186_0000_bg_017_jp.tga` | 512×512 | `7f6b64a2e881400e3a598983ec8e45887213219c4f5646c7da54d434588a3b29` | Scenery or abstract card background; no readable writing. |
| 163 | `00039_01187_0000_bg_018_jp.tga` | 512×512 | `f525ee416aea8c86979d997c381c40b9b7eed9470207d82c1e961f9bc39f249b` | Scenery or abstract card background; no readable writing. |
| 164 | `00039_01188_0000_bg_019_jp.tga` | 512×512 | `b5cc9048a2308947fb27205e344c4d3c740a66ef4d999e3956f9c57b4832f9a4` | Scenery or abstract card background; no readable writing. |
| 165 | `00039_01189_0000_bg_020_jp.tga` | 512×512 | `357f9c31c535f5067b755a6c15342faa1bfdb82fa6dff93f527f4177083120f3` | Scenery or abstract card background; no readable writing. |
| 166 | `00039_01190_0000_bg_021_jp.tga` | 512×512 | `e60be2fa84e57b6358819939653f763817c8e090d9fa0ee714a462b3f63a4fe2` | Scenery or abstract card background; no readable writing. |
| 167 | `00039_01191_0000_bg_022_jp.tga` | 512×512 | `0863368f233bad510000eb970b34fb54c7fbf83d3a3d44eeb936d7044fbd3b53` | Scenery or abstract card background; no readable writing. |
| 168 | `00039_01192_0000_bg_023_jp.tga` | 512×512 | `13b0d0f80d20462ea8c333585e35506cff8d055deeb595627ee831f981d11bae` | Scenery or abstract card background; no readable writing. |
| 169 | `00039_01193_0000_bg_024_jp.tga` | 512×512 | `47fcab11f8995ef607ad968ac5b4d4cd0d2066738b2fe48b18244726bda83ccc` | Scenery or abstract card background; no readable writing. |
| 170 | `00039_01194_0000_bg_025_jp.tga` | 512×512 | `4ef2cb7b4dc1e33bd1bffd59e3fc681da1e4fe3c5da14d0e353dc7066838273d` | Scenery or abstract card background; no readable writing. |
| 171 | `00039_01195_0000_bg_026_jp.tga` | 512×512 | `081ca0a2c477c678f3eb1fe954866e21663693b801e6f064bef882db217bf23f` | Scenery or abstract card background; no readable writing. |
| 172 | `00039_01196_0000_bg_027_jp.tga` | 512×512 | `bd6a98a47469f04c593bef7de6a593a5fa1250fbea433943ab45af6770ef9870` | Scenery or abstract card background; no readable writing. |
| 173 | `00039_01197_0000_bg_028_jp.tga` | 512×512 | `1d46f021de84240612074e49438f64160f869eba1154e4c2d2defdda1bb68880` | Scenery or abstract card background; no readable writing. |
| 174 | `00039_01198_0000_bg_029_jp.tga` | 512×512 | `53e69123b68ccb2138ce6010a157e36cff762d08bf9be6b357b2c58f29d6f8ba` | Scenery or abstract card background; no readable writing. |
| 175 | `00039_01199_0000_bg_030_jp.tga` | 512×512 | `67bd8e0f4d21610f3d30c3c7defb6c5f415721f0fecc2fd7fa2ce0f57f2900dd` | Scenery or abstract card background; no readable writing. |
| 176 | `00039_01200_0000_bg_031_jp.tga` | 512×512 | `c88890547112b907f91ffaa35e4f62498e069a02fbe0ca21dfa1515e743cf5e7` | Scenery or abstract card background; no readable writing. |
| 177 | `00039_01201_0000_bg_032_jp.tga` | 512×512 | `f9f12511dd4f7879ca82b5c7f2938ce142f32353eec3d8ce54708596926036c7` | Scenery or abstract card background; no readable writing. |
| 178 | `00039_01202_0000_bg_033_jp.tga` | 512×512 | `8ee697373d6b09adc25c3a5531b0e20813ac941dde68ef34b7f30e78a297135f` | Scenery or abstract card background; no readable writing. |
| 179 | `00039_01203_0000_bg_034_jp.tga` | 512×512 | `7655c7a277164c9988fb2e7685cfa8d9b86d5ed21c0a28bfa8f5e4f8a7010c83` | Scenery or abstract card background; no readable writing. |
| 180 | `00039_01204_0000_bg_035_jp.tga` | 512×512 | `8f91c875a44f9f11b7d6677d1c183738c7306cdb98e2ad35f358c5d1be8bd8e5` | Scenery or abstract card background; no readable writing. |
| 181 | `00039_01205_0000_bg_036_jp.tga` | 512×512 | `ccf3b66980b563be9da338a6c68644895712b63e1de5c7978fd1b582e750a587` | Scenery or abstract card background; no readable writing. |
| 182 | `00039_01206_0000_bg_037_jp.tga` | 512×512 | `e46ffee7191d4ce7329ccacd91fa5f6b2148f8c7871b5f3eb615a8c27b927b0b` | Scenery or abstract card background; no readable writing. |
| 183 | `00039_01207_0000_bg_038_jp.tga` | 512×512 | `9ac650eb1bfc98277b2b12bed6a6ed1f2fd5dccceeaca247ebf85b6c7ab970ee` | Scenery or abstract card background; no readable writing. |
| 184 | `00039_01208_0000_bg_039_jp.tga` | 512×512 | `e1a642236321654e94f00aacfe9f87ac31a6c24566540ad8a7e43891fbfd8b7d` | Scenery or abstract card background; no readable writing. |
| 185 | `00039_01209_0000_bg_040_jp.tga` | 512×512 | `c565ec872b9b742bc5b48c0946df27e72e9ea8a2f01194697410fda9ac7fece2` | Scenery or abstract card background; no readable writing. |
| 186 | `00039_01210_0000_bg_041_jp.tga` | 512×512 | `b5503f647af7ac29f25f212074d504bd21f6e7e2871bedbada058a3234c4991c` | Scenery or abstract card background; no readable writing. |
| 187 | `00039_01211_0000_bg_042_jp.tga` | 512×512 | `450990da1fed21d4030d7a48cc1a0035227877ee171e26cbd16ed34b480bc35b` | Scenery or abstract card background; no readable writing. |
| 188 | `00039_01212_0000_bg_043_jp.tga` | 512×512 | `fa33c72cf058526b2799cc867f1b23e4a0ae6088ac6d9faf79fd2985d75b5a3d` | Scenery or abstract card background; no readable writing. |
| 189 | `00039_01213_0000_bg_044_jp.tga` | 512×512 | `bf23385e5016fd0f1c6830f55c77591d30b712d7b3408d5248ff99c25575fa82` | Scenery or abstract card background; no readable writing. |
| 190 | `00039_01214_0000_bg_045_jp.tga` | 512×512 | `c486b507cb1b9878d6a6b0452ebd577b3a9516522c5533905ee7bd3b1da0bca6` | Scenery or abstract card background; no readable writing. |
| 191 | `00039_01215_0000_bg_046_jp.tga` | 512×512 | `3feb885194bbf2e915ec246f55be11fbe5a6e32e12daa96b1a919ea6971c35ff` | Scenery or abstract card background; no readable writing. |
| 192 | `00039_01216_0000_bg_047_jp.tga` | 512×512 | `84823d7d7d38ef1d16d834249a43055df42e6698fab562a2bdd781cc35d916df` | Scenery or abstract card background; no readable writing. |
| 193 | `00039_01217_0000_bg_048_jp.tga` | 512×512 | `a7bcb67f9f5dd14bb851d2b989b65e32ff28a5782b4b9be313ac23af349c14a9` | Scenery or abstract card background; no readable writing. |
| 194 | `00039_01218_0000_bg_049_jp.tga` | 512×512 | `ad24a52470ed1b4eab2d7b5a7a64eb4306e0c8f9e9120a9dc503ff7665d42d1f` | Scenery or abstract card background; no readable writing. |
| 195 | `00039_01219_0000_bg_050_jp.tga` | 512×512 | `62801d8824cd371c3abbb841b75f3d7659ed0d7f66729e7d1df1659ea90352b1` | Scenery or abstract card background; no readable writing. |
| 196 | `00039_01220_0000_bg_051_jp.tga` | 512×512 | `56d56e3faa6cdc378dd5fe41ec6792984a917500629d63e03913e7178aa9b24c` | Scenery or abstract card background; no readable writing. |
| 197 | `00039_01221_0000_bg_052_jp.tga` | 512×512 | `aadd2a51f1b752c484fcb8a34def83e007b3e39a8ca56a8152245cc7fd38d794` | Scenery or abstract card background; no readable writing. |
| 198 | `00039_01222_0000_bg_053_jp.tga` | 512×512 | `0d76420d3645fa971767b97be65d83603f053452c9276c8b85e177ec864c9a5d` | Scenery or abstract card background; no readable writing. |
| 199 | `00039_01223_0000_bg_054_jp.tga` | 512×512 | `f3dcca8ec8ea1dbb8ca4b8a4589887f76c53e4bf2a0ed6706b5c47363032a1f6` | Scenery or abstract card background; no readable writing. |
| 200 | `00039_01224_0000_bg_055_jp.tga` | 512×512 | `54d1527919092a584c39b0ffc6ddc4c4682404da764a4758ec6d77c50c4f0aef` | Scenery or abstract card background; no readable writing. |
| 201 | `00039_01225_0000_bg_056_jp.tga` | 512×512 | `0f6570877ce15f6daa1c69aaabd4dcf639f9cec16d71614b20f746b6ad9fecb4` | Scenery or abstract card background; no readable writing. |
| 202 | `00039_01226_0000_bg_057_jp.tga` | 512×512 | `0c842aa1ac073672c359af7af13b4022baa20fd28be1e59b453d0997e03b9b5d` | Scenery or abstract card background; no readable writing. |
| 203 | `00039_01227_0000_bg_058_jp.tga` | 512×512 | `a4ede45106c4d17af8f8c29aff9d11abc9e1a98c45fe644b23ef1b622e02af56` | Scenery or abstract card background; no readable writing. |
| 204 | `00039_01228_0000_bg_059_jp.tga` | 512×512 | `26fe46dd15ece0d851f06f78b31e6d4e1279ead2b819de6614464a1b1c3446bb` | Scenery or abstract card background; no readable writing. |
| 205 | `00039_01229_0000_bg_060_jp.tga` | 512×512 | `15b03c031d108f83a7cb0662cd91cd5df6b04f7ae00b1a047b2aa35de58b9eea` | Scenery or abstract card background; no readable writing. |
| 206 | `00039_01230_0000_bg_061_jp.tga` | 512×512 | `7c35870d9509787bbc766860d8f0ab09dddb55c2b25529f59f22975d00174953` | Scenery or abstract card background; no readable writing. |
| 207 | `00039_01231_0000_bg_062_jp.tga` | 512×512 | `d99c8eeb7f534014d71c6f2432b35433f91205fb0542705ec576f87d03500304` | Scenery or abstract card background; no readable writing. |
| 208 | `00039_01232_0000_bg_063_jp.tga` | 512×512 | `07f4f49209e31fb124be9fcd6cac51c90af0cd07e03da7863dd74e303410e92d` | Scenery or abstract card background; no readable writing. |
| 209 | `00039_01233_0000_bg_064_jp.tga` | 512×512 | `8869b2371b8a155917fc945fbe7059c4c882fa22d88702e52571fc9e4444cbfc` | Scenery or abstract card background; no readable writing. |
| 210 | `00039_01234_0000_bg_065_jp.tga` | 512×512 | `06944505c0abef2926a8b063dfbcd6f425e7a6f7451f74e1185dac0a900fd6ea` | Scenery or abstract card background; no readable writing. |
| 211 | `00039_01235_0000_bg_066_jp.tga` | 512×512 | `51c82c6fdc148d11349f63975dffa852effb580f44212a3b46789da0283acaa9` | Scenery or abstract card background; no readable writing. |
| 212 | `00039_01236_0000_bg_067_jp.tga` | 512×512 | `0fe4e0b51938a99d5b5b277c1bd0a1f789956fd6dc705c513e597d2697036fa8` | Scenery or abstract card background; no readable writing. |
| 213 | `00039_01237_0000_bg_068_jp.tga` | 512×512 | `d76f7ab15dad7e4fd07971bf1071d9019603bc280a1790e523a0363ecb4cee66` | Scenery or abstract card background; no readable writing. |
| 214 | `00039_01238_0000_bg_069_jp.tga` | 512×512 | `8cd85e09c555001866cb129246ab2efa8690a68c1a19a0b58a628883d3babc13` | Scenery or abstract card background; no readable writing. |
| 215 | `00039_01239_0000_bg_070_jp.tga` | 512×512 | `78c5053f3c0e035744b0d338596e814e7815beb58bb5fa8955dfd7dc92b94b60` | Scenery or abstract card background; no readable writing. |
| 216 | `00039_01240_0000_bg_071_jp.tga` | 512×512 | `ef9565d228360c0ff7e355db388f0e033b484dfb832549e9fcf0a5f4a5ddf907` | Scenery or abstract card background; no readable writing. |
| 217 | `00039_01241_0000_bg_072_jp.tga` | 512×512 | `2ee2ad39f9de0d85e5f3dd737d21f6c108885ec39c64062841efa26a7fceb5b7` | Scenery or abstract card background; no readable writing. |
| 218 | `00039_01242_0000_bg_073_jp.tga` | 512×512 | `eaa97a70ecb7fae38b86696454c2ae12570db5c63ffb0bda7ac16ba723fedd43` | Scenery or abstract card background; no readable writing. |
| 219 | `00039_01243_0000_bg_074_jp.tga` | 512×512 | `761424a9130987180235b14e6bbb05ed066e99c4e032a2bd7285f9cc188a7279` | Scenery or abstract card background; no readable writing. |
| 220 | `00039_01244_0000_bg_075_jp.tga` | 512×512 | `16bbcfa11a15f4309b0fe239b0e98c65112a03bcc7bdd0f424b01e3f21c2211d` | Scenery or abstract card background; no readable writing. |
| 221 | `00039_01245_0000_bg_076_jp.tga` | 512×512 | `38baae574af31747f91d39e532be9c6aa5c56c7a2132294df0f2ed0992c14c8f` | Scenery or abstract card background; no readable writing. |
| 222 | `00039_01246_0000_bg_077_jp.tga` | 512×512 | `bbd600535a675a858a729ec03055efd7a535f6faf981f292195af6cbbe0a044e` | Scenery or abstract card background; no readable writing. |
| 223 | `00039_01247_0000_bg_078_jp.tga` | 512×512 | `493b1a62eb811d7bb7a1bbe2db9d30ca24a493cf09111674fbbc256f2338bcfc` | Scenery or abstract card background; no readable writing. |
| 224 | `00039_01248_0000_bg_079_jp.tga` | 512×512 | `b743567fd3f6edeee4163fb25f111c3d27e5439b18d93ce13ca83a5fc0aedbd5` | Scenery or abstract card background; no readable writing. |
| 225 | `00039_01249_0000_bg_080_jp.tga` | 512×512 | `f9b4af3c0f854699bf2cd09fdef17bc49ff2bae6f5ca876fe9f2a627bde48b90` | Scenery or abstract card background; no readable writing. |
| 226 | `00039_01250_0000_bg_081_jp.tga` | 512×512 | `69baf0c1418acb72ac68d788e0685d87448f1c072257fa20fa1f87ccec1cfcd8` | Scenery or abstract card background; no readable writing. |
| 227 | `00039_01251_0000_bg_082_jp.tga` | 512×512 | `a0e87d043765464a2ce0fd9c47ed33ceff7f1ddfe179641f6375d08a8d382bba` | Scenery or abstract card background; no readable writing. |
| 228 | `00039_01252_0000_bg_083_jp.tga` | 512×512 | `c755c194c0d1db44189704249997073537edf3d8757e00213e0b43e092b6a209` | Scenery or abstract card background; no readable writing. |
| 229 | `00039_01253_0000_bg_084_jp.tga` | 512×512 | `d3cc0cfe0dcb73210b5882b49ef3765c8d2c9a580342bb29a0324d34e2d8d165` | Scenery or abstract card background; no readable writing. |
| 230 | `00039_01254_0000_bg_085_jp.tga` | 512×512 | `e7557222cefe090e22de497a001f62bb77b507579ed83c15ca5a0f54c77df8a4` | Scenery or abstract card background; no readable writing. |
| 231 | `00039_01255_0000_bg_086_jp.tga` | 512×512 | `1bafcace205520109bd4d9153622c4fef622b9d472169b73e3f7be7229fddd3c` | Scenery or abstract card background; no readable writing. |
| 232 | `00039_01256_0000_bg_087_jp.tga` | 512×512 | `43b23a8630c28e45cbd25a90e53d43f66b131e7ed34e35ddf8f58897302fb705` | Scenery or abstract card background; no readable writing. |
| 233 | `00039_01257_0000_bg_088_jp.tga` | 512×512 | `e97e00f04ccd6b7954d333f88071a1b925f6a0c7f2d624615daca8b9036f34da` | Scenery or abstract card background; no readable writing. |
| 234 | `00039_01258_0000_bg_089_jp.tga` | 512×512 | `4204d1d6106688db67887124bcfc66e22693e86b07ae994ddb2fa392e6de1f5c` | Scenery or abstract card background; no readable writing. |
| 235 | `00039_01259_0000_bg_090_jp.tga` | 512×512 | `ebdb2df743ab5dc2152f5050f7ca09ff5783c9b2eafeef613a5222c703e92d38` | Scenery or abstract card background; no readable writing. |
| 236 | `00039_01260_0000_bg_091_jp.tga` | 512×512 | `79cc8d46ec586a48f14c0225c16897d7dd4f913dd43c0d8aaca7549ec90ad561` | Scenery or abstract card background; no readable writing. |
| 237 | `00039_01261_0000_bg_092_jp.tga` | 512×512 | `ca1a5deda79fcdcc8037b39c6fb14c10cd9268739ab60126b2031081fa9c799c` | Scenery or abstract card background; no readable writing. |
| 238 | `00039_01262_0000_bg_093_jp.tga` | 512×512 | `7991fe043c15ae271a847a127052e692fe8df581117e789aa0e39d336d566261` | Scenery or abstract card background; no readable writing. |
| 239 | `00039_01263_0000_bg_094_jp.tga` | 512×512 | `7efe54d5290d4ebc2b5e85b7a9a516f90819c501a73c206a342d29f809a16f0f` | Scenery or abstract card background; no readable writing. |
| 240 | `00039_01264_0000_bg_095_jp.tga` | 512×512 | `0680ba203eea3b6fa99ad4770367d2d81dd2c97b749c851e43ba52d4590576a2` | Scenery or abstract card background; no readable writing. |
| 241 | `00039_01265_0000_bg_096_jp.tga` | 512×512 | `ddeeaacf1564b7e2ecfe2f2e88d10c1652477c779c267589569261ec145bef31` | Scenery or abstract card background; no readable writing. |
| 242 | `00039_01266_0000_bg_097_jp.tga` | 512×512 | `5dd6a48dabaa5a77d62dbdb762ef9cc3bd2916188e903cafbb6384576f4b16a7` | Scenery or abstract card background; no readable writing. |
| 243 | `00039_01267_0000_bg_098_jp.tga` | 512×512 | `37d605bfc853bd81ff24ab09f354426367a8d761f86375f36df748d86e97c01f` | Scenery or abstract card background; no readable writing. |
| 244 | `00039_01268_0000_bg_099_jp.tga` | 512×512 | `5f0e2d2b7756d29f5e1918235435d289ecd84e3676e513d1200d9ac5b30eb620` | Scenery or abstract card background; no readable writing. |
| 245 | `00039_01269_0000_bg_100_jp.tga` | 512×512 | `f425b24cc178029b574fce4c730073d1b3ec8866e688da71d6f42cd9721697c5` | Scenery or abstract card background; no readable writing. |
| 246 | `00039_01270_0000_bg_101_jp.tga` | 512×512 | `2cc39882d823b06e59ecc20b3559beabda60c5915534321190ca7293e1259c4f` | Scenery or abstract card background; no readable writing. |
| 247 | `00039_01271_0000_bg_102_jp.tga` | 512×512 | `b1be2d2de9d0081bbfc12af10838505fa4f720a25795609f4dbc1daef0bd3022` | Scenery or abstract card background; no readable writing. |
| 248 | `00039_01272_0000_bg_103_jp.tga` | 512×512 | `a450b23e4d64589cd999f3a39fba7f443bf839989f0fd1721f57a568ce66cfeb` | Scenery or abstract card background; no readable writing. |
| 249 | `00039_01273_0000_bg_104_jp.tga` | 512×512 | `a782f4a43e72cbdbee476f4bf3193de88d8940a0355d79cf3968b2f69e69cca6` | Scenery or abstract card background; no readable writing. |
| 250 | `00039_01274_0000_bg_105_jp.tga` | 512×512 | `3d2e92ca32fc95c27a6397e3e818074b79905158cc57931d8aed06631af71ebb` | Scenery or abstract card background; no readable writing. |
| 251 | `00039_01275_0000_bg_106_jp.tga` | 512×512 | `f90556e34983939d04e6615a61a456abfe47c6d48ed450d4f03a05b658732564` | Scenery or abstract card background; no readable writing. |
| 252 | `00039_01276_0000_bg_107_jp.tga` | 512×512 | `e9cb53a0cc04db09485e135a53a0960a7db191ea7cbaa535047bb594ccadc466` | Scenery or abstract card background; no readable writing. |
| 253 | `00039_01277_0000_bg_108_jp.tga` | 512×512 | `f737073fabfef71459cef0fbdbacfd34d9844091cab218fac9cad64d5e39b948` | Scenery or abstract card background; no readable writing. |
| 254 | `00039_01278_0000_bg_109_jp.tga` | 512×512 | `5202710edd6721b7f33cd83743fc665f2b725c50b03176e1d910d5d625319210` | Scenery or abstract card background; no readable writing. |
| 255 | `00039_01279_0000_bg_110_jp.tga` | 512×512 | `747d937bb600232b2c9ddbf8c52c8672e12e38174a7286d834f722bb71b52cb9` | Scenery or abstract card background; no readable writing. |
| 256 | `00039_01280_0000_bg_111_jp.tga` | 512×512 | `61c55d1636ca8c6933147865f937870712387a14233e6f658f2982782ef13d7f` | Scenery or abstract card background; no readable writing. |
| 257 | `00039_01281_0000_bg_112_jp.tga` | 512×512 | `2359fedbef46e6cea3a9292dd7c3f54f073e4e5d6c0087cc4c476c26fbee32a9` | Scenery or abstract card background; no readable writing. |
| 258 | `00039_01282_0000_bg_113_jp.tga` | 512×512 | `8aed5b3a9a8e717820cd7604d4526ffd3f51c66dc1dba2ee8a77ae52f4297f34` | Scenery or abstract card background; no readable writing. |
| 259 | `00039_01283_0000_bg_114_jp.tga` | 512×512 | `88b71117a63b632079058115a51f74140e397975e038e14010ffff01239f2da6` | Scenery or abstract card background; no readable writing. |
| 260 | `00039_01284_0000_bg_115_jp.tga` | 512×512 | `cfd5a241907fd48dc5d404aecbe30ea4910605d53ee628e91a5cb77a68a908a2` | Scenery or abstract card background; no readable writing. |
| 261 | `00039_01285_0000_bg_116_jp.tga` | 512×512 | `1536453dcad59511b0788f2d3e528d31f37c97caaa51a38306780ea034b13a57` | Scenery or abstract card background; no readable writing. |
| 262 | `00039_01286_0000_bg_117_jp.tga` | 512×512 | `a3f5f7268889b1ce1221fdb86d9fc2e7f7e2e3cc84420277957e69cb0ef9b49e` | Scenery or abstract card background; no readable writing. |
| 263 | `00039_01287_0000_bg_118_jp.tga` | 512×512 | `fd69857939448703b25e55518390e3738db3fdcf51ffe11ca74ac21b96090c72` | Scenery or abstract card background; no readable writing. |
| 264 | `00039_01288_0000_bg_119_jp.tga` | 512×512 | `1f017c36db8d543e569e3f7383d42dcbdac902537f2a4b034fdca49a4f5c2778` | Scenery or abstract card background; no readable writing. |
| 265 | `00039_01289_0000_bg_120_jp.tga` | 512×512 | `7ba6ab322f7495899b0a1e80bb065afab913dfb4783bc3251d798b8d969c371c` | Scenery or abstract card background; no readable writing. |
| 266 | `00039_01290_0000_bg_121_jp.tga` | 512×512 | `44531c32c3a6a4f371f64f928a04accf2f373c7ee5a8d030cf33eca38223970a` | Scenery or abstract card background; no readable writing. |
| 267 | `00039_01291_0000_bg_122_jp.tga` | 512×512 | `f02fa98fd3bfc87f9f49666124bc198c2320600596163bca686dd714a837f6fd` | Scenery or abstract card background; no readable writing. |
| 268 | `00039_01292_0000_bg_123_jp.tga` | 512×512 | `ffa51a9c3d97b97ead5ed6ca5b3b1ba5e9394a58829cdcc257d755d89fecdea0` | Scenery or abstract card background; no readable writing. |
| 269 | `00039_01293_0000_bg_124_jp.tga` | 512×512 | `70b0a51dd8d3d4d5f8adabf6c1549ee0e4a4914defc92f4173b5f146bc0d5d43` | Scenery or abstract card background; no readable writing. |
| 270 | `00039_01294_0000_bg_125_jp.tga` | 512×512 | `059113c6e730f44b7bad55329636a344d36deae387b1e2d31c8726e3f4bc9365` | Scenery or abstract card background; no readable writing. |
| 271 | `00039_01295_0000_bg_126_jp.tga` | 512×512 | `87a1022bdda8ee9ccd478e1ee02bb4dab033c58fa2d9b881ccf5de7396c6c59a` | Scenery or abstract card background; no readable writing. |
| 272 | `00039_01296_0000_bg_127_jp.tga` | 512×512 | `0f9424d89c59a9187c43041a8026e6df1aa6942e538c15b9690a86c9afc4f146` | Scenery or abstract card background; no readable writing. |
| 273 | `00039_01297_0000_bg_128_jp.tga` | 512×512 | `c4cf2356dd53c3641580e220082ebb19f72b9dcf774332d197e459631fdbcd29` | Scenery or abstract card background; no readable writing. |
| 274 | `00039_01298_0000_bg_129_jp.tga` | 512×512 | `9989bb929f9f7b5f0d31d7be029ec1ed29239a78e68a3508d0471294ad39ba15` | Scenery or abstract card background; no readable writing. |
| 275 | `00039_01299_0000_bg_130_jp.tga` | 512×512 | `a70763623541d39fde702cd8ba818cc1c88536c3f6943aa52a0789886a7aa4c3` | Scenery or abstract card background; no readable writing. |
| 276 | `00039_01300_0000_bg_131_jp.tga` | 512×512 | `3477cf9bdd202c4ff796f1d87d58819d96709b3ffb77fd4ae13c8959bc91e3d7` | Scenery or abstract card background; no readable writing. |
| 277 | `00039_01301_0000_bg_132_jp.tga` | 512×512 | `5be64673387e19b8a3186a42edaac97321b226ffda488e04c4e4036ccc5d490e` | Scenery or abstract card background; no readable writing. |
| 278 | `00039_01302_0000_bg_133_jp.tga` | 512×512 | `e441877e5eae6e979792801ba8a10659f605d304281b5ee599b4ac242f2614f2` | Scenery or abstract card background; no readable writing. |
| 279 | `00039_01303_0000_bg_134_jp.tga` | 512×512 | `aa88a07d4d3b5d67be89eeaaa4c139cb5131f095a16d04f8de0db79a034f8d95` | Scenery or abstract card background; no readable writing. |
| 280 | `00039_01304_0000_bg_135_jp.tga` | 512×512 | `f99f99e5d4221928e86ddfa1a248ddd50d3cbc4965c3e142ca8702b8e79fe570` | Scenery or abstract card background; no readable writing. |
| 281 | `00039_01305_0000_bg_136_jp.tga` | 512×512 | `5bb696ae16e5ba4f6b5857b353e06a988aea2a6fcaf248d5cbd2bf6a5909ee90` | Scenery or abstract card background; no readable writing. |
| 282 | `00039_01306_0000_bg_137_jp.tga` | 512×512 | `88baf1e956a840f93a51345cf9b926958282f4f9e07434dce190ac871f2cc6a1` | Scenery or abstract card background; no readable writing. |
| 283 | `00039_01307_0000_bg_138_jp.tga` | 512×512 | `8cc100d8e56a7b06e1bfbc2683a6b51e5312a3b22a26095cf4b24a2bd14fbc46` | Scenery or abstract card background; no readable writing. |
| 284 | `00039_01308_0000_bg_139_jp.tga` | 512×512 | `00b80dd610a3c11bf3e4ddab61b6922c90125744fad2d0ab6728cf5820fed46b` | Scenery or abstract card background; no readable writing. |
| 285 | `00039_01309_0000_bg_140_jp.tga` | 512×512 | `502be3dcf4e133888e9e008927c1cb51c8155c352b97470601f862e0767b7cb2` | Scenery or abstract card background; no readable writing. |
| 286 | `00039_01310_0000_bg_141_jp.tga` | 512×512 | `9870376a1022bc44fdb1f99c3ff22c286f907e89d6436df1c8565180e142b369` | Scenery or abstract card background; no readable writing. |
| 287 | `00039_01311_0000_bg_142_jp.tga` | 512×512 | `229abc86d9ebb584583b2fadd1d4f69cca737ccc37cc012db34215ea16e5f5ce` | Scenery or abstract card background; no readable writing. |
| 288 | `00039_01312_0000_bg_143_jp.tga` | 512×512 | `1827bf627812c91ad8a1a744e28b4bd7f4586d787b401254f8fc9b7ef34d4436` | Scenery or abstract card background; no readable writing. |
| 289 | `00039_01313_0000_bg_gba_jp.tga` | 512×512 | `00b80dd610a3c11bf3e4ddab61b6922c90125744fad2d0ab6728cf5820fed46b` | Scenery or abstract card background; no readable writing. Exact byte duplicate of #284 `00039_01308_0000_bg_139_jp.tga`. |
| 290 | `00039_01314_0000_bg_sunday_jp.tga` | 512×512 | `54abed9d73204c9fb141152f89ce84603922a6607b2dd2bdb4cc1a0f9c62c0af` | Scenery or abstract card background; no readable writing. |
| 291 | `00039_01315_0000_card_gba_jp.tga` | 512×512 | `7aeb1af20540f8ef7c9e6126f7d551061224b24c298656dc62ec2f1855e99146` | Framed card/character illustration; no readable writing. Exact byte duplicate of #139 `00039_01163_0000_card_139_jp.tga`. |
| 292 | `00039_01316_0000_plt_001_jp.tga` | 512×128 | `aa8dcb1488676cec5d03dade8e2abef70e5003ce450b5a929cfe71545a73a393` | Japanese kana/kanji name or caption; dark-ink core [170,343)×[58,74). |
| 293 | `00039_01317_0000_plt_002_jp.tga` | 512×128 | `445ef8ad7861474616c2ba3ffa01712fb3679d9e0a4abf29c3747aa36c829496` | Japanese kana/kanji name or caption; dark-ink core [193,312)×[57,73). |
| 294 | `00039_01318_0000_plt_003_jp.tga` | 512×128 | `4330c06bdd39c0d0ff1453de44e8421deec169bf0292345bed91d44f3af6172c` | Japanese kana/kanji name or caption; dark-ink core [169,336)×[57,73). |
| 295 | `00039_01319_0000_plt_004_jp.tga` | 512×128 | `bd7d884d604fa8ee58a01668025f41a85ca2d82e42f8c82a3566b022f1d61d1c` | Japanese kana/kanji name or caption; dark-ink core [153,352)×[57,73). |
| 296 | `00039_01320_0000_plt_005_jp.tga` | 512×128 | `448622dad28aaa709ba1c9d255ba43d155f76a07c663a3f0307b5fbb2ba6d470` | Japanese kana/kanji name or caption; dark-ink core [137,369)×[57,73). |
| 297 | `00039_01321_0000_plt_006_jp.tga` | 512×128 | `a24f2148637316c3a8d34be07f6beff7ccf0c98e47005bdcf31bee1fdf47e3c8` | Japanese kana/kanji name or caption; dark-ink core [178,328)×[57,73). |
| 298 | `00039_01322_0000_plt_007_jp.tga` | 512×128 | `2902e1744b40da58d0bad475478267dc738ac58ef7a1143e5e5be7e17203df80` | Japanese kana/kanji name or caption; dark-ink core [186,320)×[57,73). |
| 299 | `00039_01323_0000_plt_008_jp.tga` | 512×128 | `7b97cbb2dedd5bf6ac0d74485f29a41cea60e79e34118e405920506ebd79f08b` | Japanese kana/kanji name or caption; dark-ink core [178,328)×[57,73). |
| 300 | `00039_01324_0000_plt_009_jp.tga` | 512×128 | `02ad1b1baf8e316c16ad931172db31602c3005149563996a8cd6b4c7a4956993` | Japanese kana/kanji name or caption; dark-ink core [138,369)×[56,73). |
| 301 | `00039_01325_0000_plt_010_jp.tga` | 512×128 | `4075573d29a97d680397d18c5be03105c3b37ace2aa72df316973fe05829d1a6` | Japanese kana/kanji name or caption; dark-ink core [172,335)×[52,73). |
| 302 | `00039_01326_0000_plt_011_jp.tga` | 512×128 | `8cbcc824ef2fb63e91b76186f2c25a54e70074fba1509acd9f92f9f21cc74a50` | Japanese kana/kanji name or caption; dark-ink core [186,320)×[57,73). |
| 303 | `00039_01327_0000_plt_012_jp.tga` | 512×128 | `e4c77d9d7c493a891ecda7528c9263790353e7ed8afc615ef63af70a346d4c11` | Japanese kana/kanji name or caption; dark-ink core [154,352)×[57,73). |
| 304 | `00039_01328_0000_plt_013_jp.tga` | 512×128 | `01a4b979fb4948b6672891e31808a7a7e7c8707814880e18fd345ebd8e804a1f` | Japanese kana/kanji name or caption; dark-ink core [174,336)×[57,73). |
| 305 | `00039_01329_0000_plt_014_jp.tga` | 512×128 | `ffcddaaf1f96766a98686e85ac98624278f283169d2826076671ac9ddfa13221` | Japanese kana/kanji name or caption; dark-ink core [165,344)×[57,73). |
| 306 | `00039_01330_0000_plt_015_jp.tga` | 512×128 | `fa7014935e36c5b2829873f90dd38002f710089d7b8c595024d8f1ee7472796b` | Japanese kana/kanji name or caption; dark-ink core [153,352)×[57,73). |
| 307 | `00039_01331_0000_plt_016_jp.tga` | 512×128 | `2847e38e6ebbfdb3b478bb073dcd3a850a2b93a161ae5870595aabd49338ae1a` | Japanese kana/kanji name or caption; dark-ink core [161,344)×[57,73). |
| 308 | `00039_01332_0000_plt_017_jp.tga` | 512×128 | `2b6358266944b7bd3158405212e934c8c5f960dbc051f8d212862d56d67eebb2` | Japanese kana/kanji name or caption; dark-ink core [170,336)×[57,73). |
| 309 | `00039_01333_0000_plt_018_jp.tga` | 512×128 | `1d98241b704da0e7bd997c97fa6da6e3162aa5ddf621e6c9da7130c94849c39f` | Japanese kana/kanji name or caption; dark-ink core [170,336)×[57,73). |
| 310 | `00039_01334_0000_plt_019_jp.tga` | 512×128 | `5520e5f332b7ae662dd471d8732371298dd6dea6b2b465937511a6a1f203076e` | Japanese kana/kanji name or caption; dark-ink core [161,344)×[57,73). |
| 311 | `00039_01335_0000_plt_020_jp.tga` | 512×128 | `9ca7628eda5b43635d0f29d202aee0095e86c44e650dc1040df2aa1c7daae58c` | Japanese kana/kanji name or caption; dark-ink core [185,320)×[57,73). |
| 312 | `00039_01336_0000_plt_021_jp.tga` | 512×128 | `d7f1ebfb698e51c631c050d3af3cf65be3046f719bc532b5bb188a87fa081fde` | Japanese kana/kanji name or caption; dark-ink core [154,352)×[57,73). |
| 313 | `00039_01337_0000_plt_022_jp.tga` | 512×128 | `994452407b644c692aa1883932caeae1f93ae85f371e80382e8cc623a22e0259` | Japanese kana/kanji name or caption; dark-ink core [162,344)×[57,73). |
| 314 | `00039_01338_0000_plt_023_jp.tga` | 512×128 | `e0bffb20e454e46acc2b86355a3f44fa045eb116838e3944873bc990a2d03837` | Japanese kana/kanji name or caption; dark-ink core [190,320)×[57,73). |
| 315 | `00039_01339_0000_plt_024_jp.tga` | 512×128 | `ec32d9566babf7788781f28a586a95d1f2a840b37320c3b013f73e349f7a0c73` | Japanese kana/kanji name or caption; dark-ink core [159,347)×[57,73). |
| 316 | `00039_01340_0000_plt_025_jp.tga` | 512×128 | `48985a28a488ed1efdb9da1c156401de3d3068f7eb2886a335b8392c174538ac` | Japanese kana/kanji name or caption; dark-ink core [120,385)×[55,75). This visible caption includes Latin “ARM”. |
| 317 | `00039_01341_0000_plt_026_jp.tga` | 512×128 | `8bd6674a55683a5eca42dfa816f2df6aeccd675d2c0b729eff5b111ed27be7d6` | Japanese kana/kanji name or caption; dark-ink core [144,361)×[57,73). |
| 318 | `00039_01342_0000_plt_027_jp.tga` | 512×128 | `e5932c3a418de157dad98dfb28c08cf61c29c5794fd684472b29fccf17e0d8a0` | Japanese kana/kanji name or caption; dark-ink core [161,344)×[57,73). |
| 319 | `00039_01343_0000_plt_028_jp.tga` | 512×128 | `2b424f5b8093dab22b96c74e81d78f2f2dc42e7356f6ba43f318fac57f4637d5` | Japanese kana/kanji name or caption; dark-ink core [186,320)×[57,73). |
| 320 | `00039_01344_0000_plt_029_jp.tga` | 512×128 | `f698ce12e32b0e77e1eb83fc07e4981aff5f31bc4f40b0e6fc9ad35f0d9043f9` | Japanese kana/kanji name or caption; dark-ink core [138,369)×[57,73). |
| 321 | `00039_01345_0000_plt_030_jp.tga` | 512×128 | `de3c711631099b3eba26b09ab6dc3ddade5a24e4e3db948c4990c11a293e7135` | Japanese kana/kanji name or caption; dark-ink core [165,344)×[57,73). |
| 322 | `00039_01346_0000_plt_031_jp.tga` | 512×128 | `5ab87437faba57b6babc71e8f9c70ea355d04b307589a115df3ea45b0485cb0c` | Japanese kana/kanji name or caption; dark-ink core [174,336)×[57,73). |
| 323 | `00039_01347_0000_plt_032_jp.tga` | 512×128 | `cde1c1c163f1cb8b4c590dd3166aa485e4986bcdffaa42a2b087d7c40e8ff597` | Japanese kana/kanji name or caption; dark-ink core [145,361)×[57,73). |
| 324 | `00039_01348_0000_plt_033_jp.tga` | 512×128 | `af71848b67af6fcfd1d757c22a863f17f6adafd11927192fd3175569bf07cf38` | Japanese kana/kanji name or caption; dark-ink core [153,352)×[57,73). |
| 325 | `00039_01349_0000_plt_034_jp.tga` | 512×128 | `a6150516d17b294f1deaeae2a9c8c7b1b7baaa21e388b43d3cf49139fb90cef2` | Japanese kana/kanji name or caption; dark-ink core [194,312)×[57,73). |
| 326 | `00039_01350_0000_plt_035_jp.tga` | 512×128 | `5df43226ab500e122922d1359d609a1d232e562a2ade7c42a007eceb18cdbb53` | Japanese kana/kanji name or caption; dark-ink core [185,320)×[57,73). |
| 327 | `00039_01351_0000_plt_036_jp.tga` | 512×128 | `34e74ea2b0671d702544746363b6546e4a5ffa78c1b66ec42bc85cd7c6dd56e5` | Japanese kana/kanji name or caption; dark-ink core [170,336)×[57,73). |
| 328 | `00039_01352_0000_plt_037_jp.tga` | 512×128 | `86c393fb5cd457c7afe6be1a8dc144daa95cf78858f31153a72024510ebcf003` | Japanese kana/kanji name or caption; dark-ink core [194,312)×[57,74). |
| 329 | `00039_01353_0000_plt_038_jp.tga` | 512×128 | `dceb21a530f6f1e5cc893a19f3349f5061df69db5ad5d3d355870e15ffc96f43` | Japanese kana/kanji name or caption; dark-ink core [185,320)×[57,73). |
| 330 | `00039_01354_0000_plt_039_jp.tga` | 512×128 | `abe4123ad52dfde1bad3201929aab90c74ab6a106d90326986264c53bdeca26c` | Japanese kana/kanji name or caption; dark-ink core [185,320)×[57,73). |
| 331 | `00039_01355_0000_plt_040_jp.tga` | 512×128 | `332d947f490703b2b7ea805058d1cab4bf44549eb119cba513c0c0a6fc719315` | Japanese kana/kanji name or caption; dark-ink core [156,352)×[57,73). |
| 332 | `00039_01356_0000_plt_041_jp.tga` | 512×128 | `7879f86e0cbcdab02bd40448293e274567a280dab4bd12dc68909fdbe9e8fb64` | Japanese kana/kanji name or caption; dark-ink core [153,352)×[57,73). |
| 333 | `00039_01357_0000_plt_042_jp.tga` | 512×128 | `e7d45aa9a5d9989303859d9d8397668eb6872d5fbb79447ca146608c81eb1068` | Japanese kana/kanji name or caption; dark-ink core [145,361)×[57,73). |
| 334 | `00039_01358_0000_plt_043_jp.tga` | 512×128 | `477d573ba05419b90fed7c3b3080d278c0e6bcc3cf6511603ebacaf9627edfd3` | Japanese kana/kanji name or caption; dark-ink core [171,336)×[57,73). |
| 335 | `00039_01359_0000_plt_044_jp.tga` | 512×128 | `75a241453ab25dedce2a0cd51614af3a4a144c0cd60356a8afd0e9c23c8f559e` | Japanese kana/kanji name or caption; dark-ink core [146,361)×[57,73). |
| 336 | `00039_01360_0000_plt_045_jp.tga` | 512×128 | `3f554fa741baee9c6a140679836cf09afa6c336b3c5cb02824affc10cb04da5e` | Japanese kana/kanji name or caption; dark-ink core [234,280)×[57,73). |
| 337 | `00039_01361_0000_plt_046_jp.tga` | 512×128 | `3f554fa741baee9c6a140679836cf09afa6c336b3c5cb02824affc10cb04da5e` | Japanese kana/kanji name or caption; dark-ink core [234,280)×[57,73). Exact byte duplicate of #336 `00039_01360_0000_plt_045_jp.tga`. |
| 338 | `00039_01362_0000_plt_047_jp.tga` | 512×128 | `f9ef5b69a6b18a0d3c81ef8d110592290e1f62e70ad6b53c0f3337da1c19c215` | Japanese kana/kanji name or caption; dark-ink core [202,312)×[58,72). |
| 339 | `00039_01363_0000_plt_048_jp.tga` | 512×128 | `73bcb5c01d2a049b6c2ea3534ae278083365a1d6a491bdef962f2efc9a640284` | Japanese kana/kanji name or caption; dark-ink core [211,304)×[57,73). |
| 340 | `00039_01364_0000_plt_049_jp.tga` | 512×128 | `02b02b97a67a40eee8025195f505b332d8a583ce4982a97266f4e5ae7801e24d` | Japanese kana/kanji name or caption; dark-ink core [218,296)×[57,72). |
| 341 | `00039_01365_0000_plt_050_jp.tga` | 512×128 | `4ae58641b1f42f933065fb52e22e04e69701d904e9b02da180c2a603e74cf7db` | Japanese kana/kanji name or caption; dark-ink core [167,345)×[57,73). |
| 342 | `00039_01366_0000_plt_051_jp.tga` | 512×128 | `fb9da9309b455eb1c5f6fc960c4fe8f021fbac4edea32f1455bf5c03fb20095d` | Japanese kana/kanji name or caption; dark-ink core [218,296)×[59,72). |
| 343 | `00039_01367_0000_plt_052_jp.tga` | 512×128 | `fb9da9309b455eb1c5f6fc960c4fe8f021fbac4edea32f1455bf5c03fb20095d` | Japanese kana/kanji name or caption; dark-ink core [218,296)×[59,72). Exact byte duplicate of #342 `00039_01366_0000_plt_051_jp.tga`. |
| 344 | `00039_01368_0000_plt_053_jp.tga` | 512×128 | `8d1fdbe912d66f55ff7be25af4bfa5ae1851a84032ec333e19885e8683561e27` | Japanese kana/kanji name or caption; dark-ink core [218,296)×[57,73). |
| 345 | `00039_01369_0000_plt_054_jp.tga` | 512×128 | `cddc5008e05e237fa902cbba50fedcec040decc570a7a9cb09aca8ad794d3286` | Japanese kana/kanji name or caption; dark-ink core [167,345)×[57,73). |
| 346 | `00039_01370_0000_plt_055_jp.tga` | 512×128 | `5939efa7fac3bdc478901cf834072cc1d266dd8aaea636b327468e6296ff2a96` | Japanese kana/kanji name or caption; dark-ink core [202,313)×[56,72). |
| 347 | `00039_01371_0000_plt_056_jp.tga` | 512×128 | `5939efa7fac3bdc478901cf834072cc1d266dd8aaea636b327468e6296ff2a96` | Japanese kana/kanji name or caption; dark-ink core [202,313)×[56,72). Exact byte duplicate of #346 `00039_01370_0000_plt_055_jp.tga`. |
| 348 | `00039_01372_0000_plt_057_jp.tga` | 512×128 | `7349b9b0cab338eb86996335736942ab2da2b1a86248bf490393fe12d25e8ab6` | Japanese kana/kanji name or caption; dark-ink core [201,313)×[56,73). |
| 349 | `00039_01373_0000_plt_058_jp.tga` | 512×128 | `a20148604ea5eab2f98e2724d3d0359ff99f61b4c79d86a29d9afd8357185725` | Japanese kana/kanji name or caption; dark-ink core [202,313)×[57,73). |
| 350 | `00039_01374_0000_plt_059_jp.tga` | 512×128 | `af677f8290b5905afeb77ce4cbd4ffbfa796c03bd6ec8bb6028dc5676072e904` | Japanese kana/kanji name or caption; dark-ink core [204,313)×[57,73). |
| 351 | `00039_01375_0000_plt_060_jp.tga` | 512×128 | `3943d8f780c1732c21f6809f5fb2c732e4cdbeada5f6216d615ab78acfc29d66` | Japanese kana/kanji name or caption; dark-ink core [203,312)×[57,73). |
| 352 | `00039_01376_0000_plt_061_jp.tga` | 512×128 | `0dd7e9a8dd9826f8150db75d45f8d831671576ff720938a3cd82f6d9f08cc386` | Japanese kana/kanji name or caption; dark-ink core [165,349)×[57,73). |
| 353 | `00039_01377_0000_plt_062_jp.tga` | 512×128 | `7886f8e32d67cdbe6fe69c6f31dc6114e61273d877f69adcb176361d21eab597` | Japanese kana/kanji name or caption; dark-ink core [198,322)×[57,73). |
| 354 | `00039_01378_0000_plt_063_jp.tga` | 512×128 | `e51a6ed720449cd3a8e6266e19b2ccab55fee3143a8458404344c4d9b6724ea2` | Japanese kana/kanji name or caption; dark-ink core [177,337)×[57,73). |
| 355 | `00039_01379_0000_plt_064_jp.tga` | 512×128 | `000e6715ca350cd6782de971f80ce3dc98f2609ef2c2ee3b275173babd520a82` | Japanese kana/kanji name or caption; dark-ink core [227,288)×[57,73). |
| 356 | `00039_01380_0000_plt_065_jp.tga` | 512×128 | `acb8c9956ab6304b4eb9e94718aa4c2883e90285bebc02a0169a3b9aadeede0f` | Japanese kana/kanji name or caption; dark-ink core [218,294)×[57,73). |
| 357 | `00039_01381_0000_plt_066_jp.tga` | 512×128 | `d98ab5b4e736afef28ba7d890d069c4a84a1bc88e0bd467889e9f83d034f9559` | Japanese kana/kanji name or caption; dark-ink core [211,304)×[59,73). |
| 358 | `00039_01382_0000_plt_067_jp.tga` | 512×128 | `e190553a24a818f54235fe1191b52281b14488e6760befbfb5461a6f4faec4b3` | Japanese kana/kanji name or caption; dark-ink core [178,335)×[58,73). |
| 359 | `00039_01383_0000_plt_068_jp.tga` | 512×128 | `51e6d389d7204556b1ee4fcbe0779167bb57eb8dfa91c47a66289bcbe8807b7d` | Japanese kana/kanji name or caption; dark-ink core [187,329)×[57,73). |
| 360 | `00039_01384_0000_plt_069_jp.tga` | 512×128 | `50978e9a4adea72e2ccb004d9690034806db7674e07b664cc44d6958e2c2eae7` | Japanese kana/kanji name or caption; dark-ink core [194,321)×[56,73). |
| 361 | `00039_01385_0000_plt_070_jp.tga` | 512×128 | `6c179d523889e958ddfc8174b3e6cc97d6602d5e4e17be7331b7d135ee0e7e4a` | Japanese kana/kanji name or caption; dark-ink core [218,295)×[57,73). |
| 362 | `00039_01386_0000_plt_071_jp.tga` | 512×128 | `d36e04c2371e062e8bd0672a103186acd98d518909288b00ba050543a98f1460` | Japanese kana/kanji name or caption; dark-ink core [177,328)×[57,73). |
| 363 | `00039_01387_0000_plt_072_jp.tga` | 512×128 | `bab8bde90b94bd2133daec24faa280d223ef00bad70fa5f159a0d8dd524201b7` | Japanese kana/kanji name or caption; dark-ink core [218,296)×[57,73). |
| 364 | `00039_01388_0000_plt_073_jp.tga` | 512×128 | `5a2ea08194096b716feeb0affbcc80e0df0b041e8bc933a190e5caafa549b524` | Japanese kana/kanji name or caption; dark-ink core [186,327)×[57,73). |
| 365 | `00039_01389_0000_plt_074_jp.tga` | 512×128 | `c5bffad29502dc6d01b30dbd4580212e6a9c35859cfe8d958028f91c0c4b909c` | Japanese kana/kanji name or caption; dark-ink core [218,293)×[57,73). |
| 366 | `00039_01390_0000_plt_075_jp.tga` | 512×128 | `2e3c757452e1c93c4412399642d39050085e54400ee9a405ffc4b6052b8ac895` | Japanese kana/kanji name or caption; dark-ink core [186,328)×[57,73). |
| 367 | `00039_01391_0000_plt_076_jp.tga` | 512×128 | `3f554fa741baee9c6a140679836cf09afa6c336b3c5cb02824affc10cb04da5e` | Japanese kana/kanji name or caption; dark-ink core [234,280)×[57,73). Exact byte duplicate of #336 `00039_01360_0000_plt_045_jp.tga`. |
| 368 | `00039_01392_0000_plt_077_jp.tga` | 512×128 | `3f554fa741baee9c6a140679836cf09afa6c336b3c5cb02824affc10cb04da5e` | Japanese kana/kanji name or caption; dark-ink core [234,280)×[57,73). Exact byte duplicate of #336 `00039_01360_0000_plt_045_jp.tga`. |
| 369 | `00039_01393_0000_plt_078_jp.tga` | 512×128 | `02b02b97a67a40eee8025195f505b332d8a583ce4982a97266f4e5ae7801e24d` | Japanese kana/kanji name or caption; dark-ink core [218,296)×[57,72). Exact byte duplicate of #340 `00039_01364_0000_plt_049_jp.tga`. |
| 370 | `00039_01394_0000_plt_079_jp.tga` | 512×128 | `bab8bde90b94bd2133daec24faa280d223ef00bad70fa5f159a0d8dd524201b7` | Japanese kana/kanji name or caption; dark-ink core [218,296)×[57,73). Exact byte duplicate of #363 `00039_01387_0000_plt_072_jp.tga`. |
| 371 | `00039_01395_0000_plt_080_jp.tga` | 512×128 | `ac0cdbe889a7bd38df85fc7ddc881cccc01a33443f47ff9a7bd373d0f9364f04` | Japanese kana/kanji name or caption; dark-ink core [202,313)×[57,73). |
| 372 | `00039_01396_0000_plt_081_jp.tga` | 512×128 | `b18611dcb679e59bb14ca69df44980a5ec5e9c7aa66063e3dad4af73e41f279e` | Japanese kana/kanji name or caption; dark-ink core [227,288)×[57,73). |
| 373 | `00039_01397_0000_plt_082_jp.tga` | 512×128 | `d98ab5b4e736afef28ba7d890d069c4a84a1bc88e0bd467889e9f83d034f9559` | Japanese kana/kanji name or caption; dark-ink core [211,304)×[59,73). Exact byte duplicate of #357 `00039_01381_0000_plt_066_jp.tga`. |
| 374 | `00039_01398_0000_plt_083_jp.tga` | 512×128 | `cfc71a64d37e4e0315dd1d10db02b39e9389309392ef51e2d2ae20889e78af43` | Japanese kana/kanji name or caption; dark-ink core [235,277)×[57,72). |
| 375 | `00039_01399_0000_plt_084_jp.tga` | 512×128 | `e190553a24a818f54235fe1191b52281b14488e6760befbfb5461a6f4faec4b3` | Japanese kana/kanji name or caption; dark-ink core [178,335)×[58,73). Exact byte duplicate of #358 `00039_01382_0000_plt_067_jp.tga`. |
| 376 | `00039_01400_0000_plt_085_jp.tga` | 512×128 | `16d5c0f792f232e62debaaafe2f5f434a10bf3ecb09b7fe395b057e1bc870c29` | Japanese kana/kanji name or caption; dark-ink core [135,380)×[57,73). |
| 377 | `00039_01401_0000_plt_086_jp.tga` | 512×128 | `6ff0ab11b51173782fab87c1025944d733e4834aabcfb94eb57f880890b1307e` | Japanese kana/kanji name or caption; dark-ink core [198,322)×[57,73). |
| 378 | `00039_01402_0000_plt_087_jp.tga` | 512×128 | `5e194cfb694d0218f8141b88fde1cf24b6165540488fb80b7874f7d27afd00cd` | Japanese kana/kanji name or caption; dark-ink core [180,338)×[57,73). |
| 379 | `00039_01403_0000_plt_088_jp.tga` | 512×128 | `0bc7e2839116749c40e5983dbbd07e77bbd6f9be8bf4ec9d8574ed5129d4ce20` | Japanese kana/kanji name or caption; dark-ink core [196,324)×[56,73). |
| 380 | `00039_01404_0000_plt_089_jp.tga` | 512×128 | `6108b1e7a9c82ca3154fb17146fce74241f16344ed4aa95955171a4fadc284e5` | Japanese kana/kanji name or caption; dark-ink core [221,299)×[57,73). |
| 381 | `00039_01405_0000_plt_090_jp.tga` | 512×128 | `022be84fb0c0d93e0e15f0863062680d7e3a3173b91d313c967185ef2fd26da2` | Japanese kana/kanji name or caption; dark-ink core [168,350)×[57,73). |
| 382 | `00039_01406_0000_plt_091_jp.tga` | 512×128 | `8ed5148a0e4ff91b2b5208284aed314795e64880412d391e99abca5447759956` | Japanese kana/kanji name or caption; dark-ink core [204,314)×[57,73). |
| 383 | `00039_01407_0000_plt_092_jp.tga` | 512×128 | `b4c0ce63fa754955441791e83e83c3fb26a18e0488198bb00e7633b2a7aef575` | Japanese kana/kanji name or caption; dark-ink core [188,331)×[57,73). |
| 384 | `00039_01408_0000_plt_093_jp.tga` | 512×128 | `b6c35edebf53b4be6000c448a6a56abfa8772185d020a2b8ebd9bddfca5e3448` | Japanese kana/kanji name or caption; dark-ink core [222,298)×[57,73). |
| 385 | `00039_01409_0000_plt_094_jp.tga` | 512×128 | `e42486d80f1cfc56d6ed9ec4229b4cfe6810076535525312c9337e910c6217b5` | Japanese kana/kanji name or caption; dark-ink core [222,298)×[57,73). |
| 386 | `00039_01410_0000_plt_095_jp.tga` | 512×128 | `9b521bf2b5c15a60945520752b56543492db6be3d64603112b562e7cc142987a` | Japanese kana/kanji name or caption; dark-ink core [180,340)×[57,73). |
| 387 | `00039_01411_0000_plt_096_jp.tga` | 512×128 | `cf37d04b5f1d456eff571ca5d7c191e479dec6ec214627aa977f46a143cb82cc` | Japanese kana/kanji name or caption; dark-ink core [206,315)×[57,73). |
| 388 | `00039_01412_0000_plt_097_jp.tga` | 512×128 | `e788d31fff3c9056a65493531f8037ff1289ac7af8672b7630a0cca13c1bc0f4` | Japanese kana/kanji name or caption; dark-ink core [174,344)×[57,73). |
| 389 | `00039_01413_0000_plt_098_jp.tga` | 512×128 | `f22e7cde1c68162d2b9ee6cb4bf3894d5371025fa2a7fc279c3b2b16bfa4c3d2` | Japanese kana/kanji name or caption; dark-ink core [204,315)×[57,73). |
| 390 | `00039_01414_0000_plt_099_jp.tga` | 512×128 | `2fe4080edcff0abe5bc1b7748237a31a13c6d3e80b53986721bff733ede8193e` | Japanese kana/kanji name or caption; dark-ink core [164,356)×[57,73). |
| 391 | `00039_01415_0000_plt_100_jp.tga` | 512×128 | `7488c1e0869403956b3028708c21230e4a1dd1a19999995b2e356708f621ee12` | Japanese kana/kanji name or caption; dark-ink core [198,321)×[57,73). |
| 392 | `00039_01416_0000_plt_101_jp.tga` | 512×128 | `a0ea7d426b060a07800d8e5480b7903d83400d7da98f13984ffaafca4a65ff77` | Japanese kana/kanji name or caption; dark-ink core [198,321)×[57,73). |
| 393 | `00039_01417_0000_plt_102_jp.tga` | 512×128 | `4a2e637390bfd4843bce88b6ad56cb8831dcc85eb6fb3b56f5d002bb8f6ad7ac` | Japanese kana/kanji name or caption; dark-ink core [204,315)×[57,73). |
| 394 | `00039_01418_0000_plt_103_jp.tga` | 512×128 | `7b89b0deb2a920a5f1fbcdb33394c2b5cc44c627da683de6460002651bde8a8e` | Japanese kana/kanji name or caption; dark-ink core [229,289)×[57,73). |
| 395 | `00039_01419_0000_plt_104_jp.tga` | 512×128 | `1a45bd8e909cd0fc73304e12d3e18c0cd3f9afd0d4a6a9bc35d42cfffde7e5af` | Japanese kana/kanji name or caption; dark-ink core [215,307)×[57,73). |
| 396 | `00039_01420_0000_plt_105_jp.tga` | 512×128 | `f1b0c885dd4a88e28bf530560873b393bdbf5ec2e4f246584ff1a8b2e69f9d83` | Japanese kana/kanji name or caption; dark-ink core [156,355)×[57,73). |
| 397 | `00039_01421_0000_plt_106_jp.tga` | 512×128 | `4b27f8a20b2cbe2ff8fdd195bcf25da507fabd062b31c48a90b297f56c43982f` | Japanese kana/kanji name or caption; dark-ink core [212,306)×[57,73). |
| 398 | `00039_01422_0000_plt_107_jp.tga` | 512×128 | `8181574a38f7e5c3e45f8d79ee9c28d61a726fcfaf17285dfd0513fb514bab1b` | Japanese kana/kanji name or caption; dark-ink core [192,327)×[57,73). |
| 399 | `00039_01423_0000_plt_108_jp.tga` | 512×128 | `eca43db8efb56afa3335a06d84069193b9fc1c7bef725e9b6f591176f58fd464` | Japanese kana/kanji name or caption; dark-ink core [204,315)×[57,73). |
| 400 | `00039_01424_0000_plt_109_jp.tga` | 512×128 | `621662969b4aedd3b79eba1d9b41471291e850193a0b22c22bbe0b99970d4213` | Japanese kana/kanji name or caption; dark-ink core [229,291)×[57,73). |
| 401 | `00039_01425_0000_plt_110_jp.tga` | 512×128 | `621662969b4aedd3b79eba1d9b41471291e850193a0b22c22bbe0b99970d4213` | Japanese kana/kanji name or caption; dark-ink core [229,291)×[57,73). Exact byte duplicate of #400 `00039_01424_0000_plt_109_jp.tga`. |
| 402 | `00039_01426_0000_plt_111_jp.tga` | 512×128 | `21c170c5244fb2237f949b55de029b5175de5e2264ecb1aa4aa4543eac4e4b7b` | Japanese kana/kanji name or caption; dark-ink core [135,376)×[57,73). |
| 403 | `00039_01427_0000_plt_112_jp.tga` | 512×128 | `9f5d77cb8591f0635dcd3a836fb3f7a44c0411e17869bb7851805b2dac9a24cd` | Japanese kana/kanji name or caption; dark-ink core [196,324)×[57,73). |
| 404 | `00039_01428_0000_plt_113_jp.tga` | 512×128 | `9f5d77cb8591f0635dcd3a836fb3f7a44c0411e17869bb7851805b2dac9a24cd` | Japanese kana/kanji name or caption; dark-ink core [196,324)×[57,73). Exact byte duplicate of #403 `00039_01427_0000_plt_112_jp.tga`. |
| 405 | `00039_01429_0000_plt_114_jp.tga` | 512×128 | `a67192e95768de461b96d4aec6474b859fb70d2dcc2cc868b95548a215b58aa6` | Japanese kana/kanji name or caption; dark-ink core [228,290)×[57,73). |
| 406 | `00039_01430_0000_plt_115_jp.tga` | 512×128 | `a67192e95768de461b96d4aec6474b859fb70d2dcc2cc868b95548a215b58aa6` | Japanese kana/kanji name or caption; dark-ink core [228,290)×[57,73). Exact byte duplicate of #405 `00039_01429_0000_plt_114_jp.tga`. |
| 407 | `00039_01431_0000_plt_116_jp.tga` | 512×128 | `a03511c260ba6d445cf10802bf98985164ed3fabb47fe95317fcd8287efbe253` | Japanese kana/kanji name or caption; dark-ink core [204,314)×[57,73). |
| 408 | `00039_01432_0000_plt_117_jp.tga` | 512×128 | `cafebb27eb4f76e3e7cbd642d30dd0c8c1673520236729b5f874487d44535835` | Japanese kana/kanji name or caption; dark-ink core [213,305)×[58,73). |
| 409 | `00039_01433_0000_plt_118_jp.tga` | 512×128 | `da48c1be6bdce10725f8e7891d12956da6499150a92474540b04e175129cf36a` | Japanese kana/kanji name or caption; dark-ink core [220,298)×[57,73). |
| 410 | `00039_01434_0000_plt_119_jp.tga` | 512×128 | `8945ad3ecd6e449f4be00950baf30b4732e56623db1695355c1176b198767a56` | Japanese kana/kanji name or caption; dark-ink core [167,345)×[57,73). |
| 411 | `00039_01435_0000_plt_120_jp.tga` | 512×128 | `1f727dd2bb5355220a083035115450b4551b6d06d81f7f7cdc72697567524f17` | Japanese kana/kanji name or caption; dark-ink core [204,314)×[57,73). |
| 412 | `00039_01436_0000_plt_121_jp.tga` | 512×128 | `a11bf1828ae01b2b07014c9b7ec9efba7b650dc7f26eb3f3c98d8a5f534918b2` | Japanese kana/kanji name or caption; dark-ink core [172,348)×[56,73). |
| 413 | `00039_01437_0000_plt_122_jp.tga` | 512×128 | `4684bd99c52ea1624e69beff2b2fce92f9cb4084751135c11eab6f97c7e1830d` | Japanese kana/kanji name or caption; dark-ink core [245,274)×[57,73). |
| 414 | `00039_01438_0000_plt_123_jp.tga` | 512×128 | `a67192e95768de461b96d4aec6474b859fb70d2dcc2cc868b95548a215b58aa6` | Japanese kana/kanji name or caption; dark-ink core [228,290)×[57,73). Exact byte duplicate of #405 `00039_01429_0000_plt_114_jp.tga`. |
| 415 | `00039_01439_0000_plt_124_jp.tga` | 512×128 | `695e80ca23c3d3d5dab068329a7bff29cbe2c3bf2306e9c09560d6f7a0218e6d` | Japanese kana/kanji name or caption; dark-ink core [196,323)×[57,73). |
| 416 | `00039_01440_0000_plt_125_jp.tga` | 512×128 | `e9d18571fffbd2160596ddb0bd23c73f8b3481e60a4ad5b863e5c7f197c72196` | Japanese kana/kanji name or caption; dark-ink core [212,307)×[57,73). |
| 417 | `00039_01441_0000_plt_126_jp.tga` | 512×128 | `deb088a0773524765349f0dbc4805aff8d23866417e658a53d90b11f40256b6f` | Japanese kana/kanji name or caption; dark-ink core [212,305)×[57,73). |
| 418 | `00039_01442_0000_plt_127_jp.tga` | 512×128 | `d30cbb220da9b1bd6c8425d977570582b9c49fb567b45a43a096f258064d7910` | Japanese kana/kanji name or caption; dark-ink core [212,305)×[57,73). |
| 419 | `00039_01443_0000_plt_128_jp.tga` | 512×128 | `3c2f51555399a56c054c0f825f2e0e9ba5522e4a3bf908179ba1755c333938b1` | Japanese kana/kanji name or caption; dark-ink core [229,291)×[57,73). |
| 420 | `00039_01444_0000_plt_129_jp.tga` | 512×128 | `6944e3d0d1c8e50d75a3c9f8321f04629f1459c806c3832bb3b4ce1442ced9c7` | Japanese kana/kanji name or caption; dark-ink core [236,283)×[57,73). |
| 421 | `00039_01445_0000_plt_130_jp.tga` | 512×128 | `c769f7261316732ffee5827c9477fd85788850fc8b785b3651ef49061ad0e4d1` | Japanese kana/kanji name or caption; dark-ink core [212,306)×[57,73). |
| 422 | `00039_01446_0000_plt_131_jp.tga` | 512×128 | `a9ad0bdacc9a9cb52aadf77343ebd68eb2d3515d25dfb5b19a8287f657453d2d` | Japanese kana/kanji name or caption; dark-ink core [206,315)×[57,73). |
| 423 | `00039_01447_0000_plt_132_jp.tga` | 512×128 | `470230dab75ecfdb2fcd1e6f04d276e54bda70b594ba15be4358a38ce9dd6507` | Japanese kana/kanji name or caption; dark-ink core [220,299)×[57,73). |
| 424 | `00039_01448_0000_plt_133_jp.tga` | 512×128 | `8d4945781e335bf59224f39fe9e918f52cfce965e5a565b441ef1dad580211a8` | Japanese kana/kanji name or caption; dark-ink core [184,335)×[57,73). |
| 425 | `00039_01449_0000_plt_134_jp.tga` | 512×128 | `d1537eeddba802b3773d75a5cb880e1115b154fae4ca485654e9223b06c0c21d` | Japanese kana/kanji name or caption; dark-ink core [172,339)×[57,73). |
| 426 | `00039_01450_0000_plt_135_jp.tga` | 512×128 | `b3508abf4903161bb8db2e8c0142661a2700114cd23c1b6b5f6a90f22fd90577` | Japanese kana/kanji name or caption; dark-ink core [176,339)×[57,73). |
| 427 | `00039_01451_0000_plt_136_jp.tga` | 512×128 | `49b4c2e6eb399c7e31bc4f18045fc79d495a18a7f3ce9de734998b484f2587b0` | Japanese kana/kanji name or caption; dark-ink core [156,355)×[57,73). |
| 428 | `00039_01452_0000_plt_137_jp.tga` | 512×128 | `6f202695a1b64fc14fbafc0cecd7c52f671d5c4cfd57da92a57ae4393c76b8be` | Japanese kana/kanji name or caption; dark-ink core [157,355)×[57,73). |
| 429 | `00039_01453_0000_plt_138_jp.tga` | 512×128 | `839ac195a6995b68c0b8e997a549beaa818850d114182301f9e176c4614f12d7` | Japanese kana/kanji name or caption; dark-ink core [237,283)×[57,73). |
| 430 | `00039_01454_0000_plt_139_jp.tga` | 512×128 | `e690444423bcd0412493b03e76a88b9283094d52deadf95d8d5c89648dd77928` | Japanese kana/kanji name or caption; dark-ink core [180,331)×[57,73). |
| 431 | `00039_01455_0000_plt_140_jp.tga` | 512×128 | `0f4e1e8a8761c6d448e738328136a7245d7ba748c0e7c3fcd3d660c2b1849a6d` | Japanese kana/kanji name or caption; dark-ink core [172,339)×[57,73). |
| 432 | `00039_01456_0000_plt_141_jp.tga` | 512×128 | `91efd2636325c6dd299dd1922a2b6b1b9de475b640ace3559713f705eb7d2196` | Japanese kana/kanji name or caption; dark-ink core [172,339)×[57,73). |
| 433 | `00039_01457_0000_plt_142_jp.tga` | 512×128 | `839ac195a6995b68c0b8e997a549beaa818850d114182301f9e176c4614f12d7` | Japanese kana/kanji name or caption; dark-ink core [237,283)×[57,73). Exact byte duplicate of #429 `00039_01453_0000_plt_138_jp.tga`. |
| 434 | `00039_01458_0000_plt_143_jp.tga` | 512×128 | `e2f5121764fe4d3595865aa036df04ff601e07a278a121afd1f931a130ea966e` | Japanese kana/kanji name or caption; dark-ink core [212,401)×[57,81). Also small alphanumeric “01A-007” [357,401)×[72,81). |
| 435 | `00039_01459_0000_plt_144_jp.tga` | 512×128 | `e2f5121764fe4d3595865aa036df04ff601e07a278a121afd1f931a130ea966e` | Japanese kana/kanji name or caption; dark-ink core [212,401)×[57,81). Also small alphanumeric “01A-007” [357,401)×[72,81). Exact byte duplicate of #434 `00039_01458_0000_plt_143_jp.tga`. |
| 436 | `00039_01460_0000_plt_145_jp.tga` | 512×128 | `e2f5121764fe4d3595865aa036df04ff601e07a278a121afd1f931a130ea966e` | Japanese kana/kanji name or caption; dark-ink core [212,401)×[57,81). Also small alphanumeric “01A-007” [357,401)×[72,81). Exact byte duplicate of #434 `00039_01458_0000_plt_143_jp.tga`. |
| 437 | `00039_01461_0000_card_s001_jp.tga` | 64×64 | `52afe07bd825a35b0daf545448547e1f4eaf4eb08f8028a351664de74669e895` | Small card portrait/sprite artwork; no readable writing. |
| 438 | `00039_01461_0001_card_s002_jp.tga` | 64×64 | `644261cebfd4aa60191cdfdf69163c87764dba04110921339454b0062cffaf12` | Small card portrait/sprite artwork; no readable writing. |
| 439 | `00039_01461_0002_card_s003_jp.tga` | 64×64 | `20402e8dbcf36dd9423626221dcc577fe67da64cf7894dd33dc4ec10f05ddd7e` | Small card portrait/sprite artwork; no readable writing. |
| 440 | `00039_01461_0003_card_s004_jp.tga` | 64×64 | `bf9ed098cd3b1b199a3c2a81ecf9005ce68f6780512e57bab223559ab0886cb8` | Small card portrait/sprite artwork; no readable writing. |
| 441 | `00039_01461_0004_card_s005_jp.tga` | 64×64 | `e84b51f413bb9a57a2396996e1ae3890f3949f15d9401eda5f61fd254acf1f1d` | Small card portrait/sprite artwork; no readable writing. |
| 442 | `00039_01461_0005_card_s006_jp.tga` | 64×64 | `08c54f125c8bacf88504c0bbe4e87c16628c539164c81d789e28a2d1b9193f5f` | Small card portrait/sprite artwork; no readable writing. |
| 443 | `00039_01461_0006_card_s007_jp.tga` | 64×64 | `1a70edcda77ac695e32b376d1bc6b43c9d7419ae199bbcc390222f0fe14a4da9` | Small card portrait/sprite artwork; no readable writing. |
| 444 | `00039_01461_0007_card_s008_jp.tga` | 64×64 | `02aaf40829f3cfa5551158709acc6c7ea556047782fceb08e344abcc6ac1cbd2` | Small card portrait/sprite artwork; no readable writing. |
| 445 | `00039_01461_0008_card_s009_jp.tga` | 64×64 | `0544db6e431833b7b8ad8f1d31afced9b6025f288f449beeaca4048ea483c5e0` | Small card portrait/sprite artwork; no readable writing. |
| 446 | `00039_01461_0009_card_s010_jp.tga` | 64×64 | `d7f9e796333f5c5c7d7a97befabd031cc4a5833b45d3ee65899d24fbe3aeda8d` | Small card portrait/sprite artwork; no readable writing. |
| 447 | `00039_01461_0010_card_s011_jp.tga` | 64×64 | `ae7a0eddec4ae27ec4c2013590c741324db822772681cb8ec3e43c2dd03a090b` | Small card portrait/sprite artwork; no readable writing. |
| 448 | `00039_01461_0011_card_s012_jp.tga` | 64×64 | `302eee97e99d42c3aa64c43975b9960df713ce514591c2cc1de7860681f81049` | Small card portrait/sprite artwork; no readable writing. |
| 449 | `00039_01461_0012_card_s013_jp.tga` | 64×64 | `1c989b97f2e7aa8e110141a8a97779589dbc87d6fe1cdf500d9eb2d6f61805c2` | Small card portrait/sprite artwork; no readable writing. |
| 450 | `00039_01461_0013_card_s014_jp.tga` | 64×64 | `cd0ed1d6149c523c9f0ed5c97c9a8f1ba65b6ebc207c1a3325690280da51ac7f` | Small card portrait/sprite artwork; no readable writing. |
| 451 | `00039_01461_0014_card_s015_jp.tga` | 64×64 | `02448abf4b808342fc845e65ab11659e66543d4c199a50f55726be049589b9b3` | Small card portrait/sprite artwork; no readable writing. |
| 452 | `00039_01461_0015_card_s016_jp.tga` | 64×64 | `e624c8e7c5d1223e1f0126e331370fa9f6c3e28ff8b32012ed13632e07a84e79` | Small card portrait/sprite artwork; no readable writing. |
| 453 | `00039_01461_0016_card_s017_jp.tga` | 64×64 | `84488c25f2c0fddb8598db8f0287254ad8c623709fc379b6b6e8fb9974d5a6d8` | Small card portrait/sprite artwork; no readable writing. |
| 454 | `00039_01461_0017_card_s018_jp.tga` | 64×64 | `d9a7990802b5ed0c6e441f5a2481fef67835cd60c9ea3b3023d2864464d8f683` | Small card portrait/sprite artwork; no readable writing. |
| 455 | `00039_01461_0018_card_s019_jp.tga` | 64×64 | `497aa80ab58d675e9e09320403462816c27c54e82972eab7134711715f90e9a7` | Small card portrait/sprite artwork; no readable writing. |
| 456 | `00039_01461_0019_card_s020_jp.tga` | 64×64 | `63b97b516ad8d58f1010ea5c5984892a4f80e1fb19c5a702f752d7d72868f429` | Small card portrait/sprite artwork; no readable writing. |
| 457 | `00039_01461_0020_card_s021_jp.tga` | 64×64 | `b776ee49c441d49d32e222883df4dc5203d889cde2fdc09ee45585d8483bd181` | Small card portrait/sprite artwork; no readable writing. |
| 458 | `00039_01461_0021_card_s022_jp.tga` | 64×64 | `911906307ec105be48900c53453b45a5aa87545a46ee967260c022c04ba3595d` | Small card portrait/sprite artwork; no readable writing. |
| 459 | `00039_01461_0022_card_s023_jp.tga` | 64×64 | `5f1d657997e4c73ad5f90bbdabbfdb40c6fcfd44f214810851731f6a74d4c625` | Small card portrait/sprite artwork; no readable writing. |
| 460 | `00039_01461_0023_card_s024_jp.tga` | 64×64 | `4356efd696c9a69de4443e7af13670faf7c9c0cbbedecb44cc81b80abc0a76f7` | Small card portrait/sprite artwork; no readable writing. |
| 461 | `00039_01461_0024_card_s025_jp.tga` | 64×64 | `ac95a0e0bb17ceaed099fdbf6d31d644e2867bccf093e3eb9b7ba4235b8a8244` | Small card portrait/sprite artwork; no readable writing. |
| 462 | `00039_01461_0025_card_s026_jp.tga` | 64×64 | `e1d29bf00b9d43ae1566be5af079eeed3447ef95f071f1f13260dda6b41ede0c` | Small card portrait/sprite artwork; no readable writing. |
| 463 | `00039_01461_0026_card_s027_jp.tga` | 64×64 | `a04d56c1d5122a656922fffbf8e241a964b4adacba1d861bc258c79b17427db2` | Small card portrait/sprite artwork; no readable writing. |
| 464 | `00039_01461_0027_card_s028_jp.tga` | 64×64 | `c67802e7de690e59090fb7f2daa8321a2d7a678728a2a88022659b8ffbfd8d50` | Small card portrait/sprite artwork; no readable writing. |
| 465 | `00039_01461_0028_card_s029_jp.tga` | 64×64 | `57c7332ae71bbfca91f48849dbdb89ef1592c5e03cef2aeb780e884f95a9e490` | Small card portrait/sprite artwork; no readable writing. |
| 466 | `00039_01461_0029_card_s030_jp.tga` | 64×64 | `c5a5d2f2aa1763651b12323b6642c995501a9488adc383575281e75b561b20b6` | Small card portrait/sprite artwork; no readable writing. |
| 467 | `00039_01461_0030_card_s031_jp.tga` | 64×64 | `775b27b46cc9bb5329d2ac1c2f2df21b737d19c2b1bbe538aec133209e723050` | Small card portrait/sprite artwork; no readable writing. |
| 468 | `00039_01461_0031_card_s032_jp.tga` | 64×64 | `6fb94c53ee8dd107f883b800ba5f8a663304f5c1945572052b890de315728c4b` | Small card portrait/sprite artwork; no readable writing. |
| 469 | `00039_01461_0032_card_s033_jp.tga` | 64×64 | `df455415175b174292195c052bf26c45ab0ca504c07375aca12baac29f63ef32` | Small card portrait/sprite artwork; no readable writing. |
| 470 | `00039_01461_0033_card_s034_jp.tga` | 64×64 | `f020a389eb4dc2bcb922dd8afa757bb3dfb63a7ad3c77d3927a4ff62a6340661` | Small card portrait/sprite artwork; no readable writing. |
| 471 | `00039_01461_0034_card_s035_jp.tga` | 64×64 | `f977028fdd37fafff7de0f9905e577c68ee19cee3eb565819a7bb6c23690adef` | Small card portrait/sprite artwork; no readable writing. |
| 472 | `00039_01461_0035_card_s036_jp.tga` | 64×64 | `a15feea57de2bde1c9fe87aac68a36812ec613cb8dd9af945bc89a0596d994db` | Small card portrait/sprite artwork; no readable writing. |
| 473 | `00039_01461_0036_card_s037_jp.tga` | 64×64 | `ec450e88e4209db41f3995797a912ccec9b55cbffcce77b9e3b62989a9ae61ba` | Small card portrait/sprite artwork; no readable writing. |
| 474 | `00039_01461_0037_card_s038_jp.tga` | 64×64 | `c966080500e1aaa57133caabf70e52e07b158515c36750ff4c5495c2532bf707` | Small card portrait/sprite artwork; no readable writing. |
| 475 | `00039_01461_0038_card_s039_jp.tga` | 64×64 | `bb4e7c1c55e90014294197b210e99f178aa97d06c25865741460ae693f52bcdb` | Small card portrait/sprite artwork; no readable writing. |
| 476 | `00039_01461_0039_card_s040_jp.tga` | 64×64 | `f76581f4870110e619464aa5bbe1a82f29563c73fdef02dd4f7a32111a8128a6` | Small card portrait/sprite artwork; no readable writing. |
| 477 | `00039_01461_0040_card_s041_jp.tga` | 64×64 | `d5e7d6c6fb5f1988f54cd28971534956e74574362798339a84751f3525285e9c` | Small card portrait/sprite artwork; no readable writing. |
| 478 | `00039_01461_0041_card_s042_jp.tga` | 64×64 | `e48bbefdbe914e6641392c925cc98e727f7cadfbcf5a30bcb9c5909cd6b85c40` | Small card portrait/sprite artwork; no readable writing. |
| 479 | `00039_01461_0042_card_s043_jp.tga` | 64×64 | `7d80a122515188f71265d91561748e8e0a8daf9c3405a0ebf551518f4dcac903` | Small card portrait/sprite artwork; no readable writing. |
| 480 | `00039_01461_0043_card_s044_jp.tga` | 64×64 | `277a9036c64533e68ea7c5b87332c7e59ded00e96ea15652441ce5ceafdb0bd9` | Small card portrait/sprite artwork; no readable writing. |
| 481 | `00039_01461_0044_card_s045_jp.tga` | 64×64 | `b518615187fc03909760ee3dc81a3b3fe29dda597ed23b682595982db68cafe2` | Small card portrait/sprite artwork; no readable writing. |
| 482 | `00039_01461_0045_card_s046_jp.tga` | 64×64 | `78e17834c943e3d1ec26de668bb5ad8f5c3ae65c461d520b978dd8540e60dd78` | Small card portrait/sprite artwork; no readable writing. |
| 483 | `00039_01461_0046_card_s047_jp.tga` | 64×64 | `ef10247440074e4c53300a664a3b02d2607313ed765d9403194f2d99ad6e2a53` | Small card portrait/sprite artwork; no readable writing. |
| 484 | `00039_01461_0047_card_s048_jp.tga` | 64×64 | `ba527736c16eba3944d2663ecb31639980f68d6af535feb10968981532a67a7c` | Small card portrait/sprite artwork; no readable writing. |
| 485 | `00039_01461_0048_card_s049_jp.tga` | 64×64 | `253f485da72c9cb5e615a199981e7f3400f6e6684134b532815c0ef4d178d1c6` | Small card portrait/sprite artwork; no readable writing. |
| 486 | `00039_01461_0049_card_s050_jp.tga` | 64×64 | `20896d419a8fc8a0ad5d2e9fb7db3c5a882ceb86782b65b918c4ad0468460bee` | Small card portrait/sprite artwork; no readable writing. |
| 487 | `00039_01461_0050_card_s051_jp.tga` | 64×64 | `e01db27e37f86376d96270d17dc366994b268575270e3a59d2c87343edbb92f4` | Small card portrait/sprite artwork; no readable writing. |
| 488 | `00039_01461_0051_card_s052_jp.tga` | 64×64 | `eea07e3ee99cb3200bedc161052aa34cf954e5c9b5153f77f9a5d25c0f2d0ddd` | Small card portrait/sprite artwork; no readable writing. |
| 489 | `00039_01461_0052_card_s053_jp.tga` | 64×64 | `c2c4ea09b336992d0800660ff8d40fb063790799dbd0181764fc06c94bd8be57` | Small card portrait/sprite artwork; no readable writing. |
| 490 | `00039_01461_0053_card_s054_jp.tga` | 64×64 | `015c1c6ea322b322da9ea83a084e045014907896b3fe2ca9d78bcd3e096728f0` | Small card portrait/sprite artwork; no readable writing. |
| 491 | `00039_01461_0054_card_s055_jp.tga` | 64×64 | `a9a2f5c56df78ed82b785e7abeb2625399f6e2fa2de18547fbe9b571c17b2704` | Small card portrait/sprite artwork; no readable writing. |
| 492 | `00039_01461_0055_card_s056_jp.tga` | 64×64 | `b3e0b7bdc7f59d06d8d270a02dba038512f8956505678f1db9267c903d05ade7` | Small card portrait/sprite artwork; no readable writing. |
| 493 | `00039_01461_0056_card_s057_jp.tga` | 64×64 | `a066745cc90f83f4482cfb41d867e5ffea8122c5e84d3810b44dd4968c818d97` | Small card portrait/sprite artwork; no readable writing. |
| 494 | `00039_01461_0057_card_s058_jp.tga` | 64×64 | `f018bed94daa96295b8dea42b7b7f172f75cb7166a59490102aca85fbd921702` | Small card portrait/sprite artwork; no readable writing. |
| 495 | `00039_01461_0058_card_s059_jp.tga` | 64×64 | `5545918bc2878fcc187c5d75c9fdf1c3fb3f8b8e0a9ed4becd8add31dd4b532d` | Small card portrait/sprite artwork; no readable writing. |
| 496 | `00039_01461_0059_card_s060_jp.tga` | 64×64 | `1cf7c3f75db8094f52ce5889f106e8c2a4bd34bb3da6145b92837341aa553c6c` | Small card portrait/sprite artwork; no readable writing. |
| 497 | `00039_01461_0060_card_s061_jp.tga` | 64×64 | `604c99287aaebbfd73d8df70402f269840f1cf65958a2eba39acd62a4d81d52d` | Small card portrait/sprite artwork; no readable writing. |
| 498 | `00039_01461_0061_card_s062_jp.tga` | 64×64 | `52719f13fc96192aa7063d8b2fd6e3dac667dda2454d76e0444520038c736575` | Small card portrait/sprite artwork; no readable writing. |
| 499 | `00039_01461_0062_card_s063_jp.tga` | 64×64 | `e77e979dfd1f8f3a58f810731917b13a3f67b04226becd19321a9cacbbecad33` | Small card portrait/sprite artwork; no readable writing. |
| 500 | `00039_01461_0063_card_s064_jp.tga` | 64×64 | `7a21bbcbdc6e71b7e3ef7bd6975962b6b70f7959a16e3eb4895d857c4776a585` | Small card portrait/sprite artwork; no readable writing. |
| 501 | `00039_01461_0064_card_s065_jp.tga` | 64×64 | `73de0dceae3749961adb168dce12a41605aefbc9ff3b84cc56904a81075062aa` | Small card portrait/sprite artwork; no readable writing. |
| 502 | `00039_01461_0065_card_s066_jp.tga` | 64×64 | `43f203df71ad005081a7d156e7667ac994fee0a7f2761c4ae8572dc32ebf65a2` | Small card portrait/sprite artwork; no readable writing. |
| 503 | `00039_01461_0066_card_s067_jp.tga` | 64×64 | `a890703a0f79d6433aad698746c0cd0b2cbda7791b21e3596e4a87e19fdab0e2` | Small card portrait/sprite artwork; no readable writing. |
| 504 | `00039_01461_0067_card_s068_jp.tga` | 64×64 | `68e27d29e7705f3c89fb8240c9e29aa3de85e2bf6d78131499d5ce1b7c8d095a` | Small card portrait/sprite artwork; no readable writing. |
| 505 | `00039_01461_0068_card_s069_jp.tga` | 64×64 | `85b1547f9500b496b8de827d2c5ebdefa2abfb4a42ff46da38769d8a2911e092` | Small card portrait/sprite artwork; no readable writing. |
| 506 | `00039_01461_0069_card_s070_jp.tga` | 64×64 | `9407307747973b2b6c64c426b553f393190a46280c3bf32d795a683a82843193` | Small card portrait/sprite artwork; no readable writing. |
| 507 | `00039_01461_0070_card_s071_jp.tga` | 64×64 | `29195f0f0ff69f021f381055868bfd40708daf571200fa993466a78f48573987` | Small card portrait/sprite artwork; no readable writing. |
| 508 | `00039_01461_0071_card_s072_jp.tga` | 64×64 | `07b1b1c783617f06bb26dd9a9494d9f456d42c5097e1d851a60f285be5a1f9e7` | Small card portrait/sprite artwork; no readable writing. |
| 509 | `00039_01462_0000_card_s073_jp.tga` | 64×64 | `1acedd34a3941d8d0dc05898127b79fb55f2cb61e625a945e8a6000e69335d25` | Small card portrait/sprite artwork; no readable writing. |
| 510 | `00039_01462_0001_card_s074_jp.tga` | 64×64 | `4acfe98b82a9bec6a50fd7627f2eea5cb2aa09bf4c82de016a085f823193999e` | Small card portrait/sprite artwork; no readable writing. |
| 511 | `00039_01462_0002_card_s075_jp.tga` | 64×64 | `d9d69c51667a15f6c4a4930bf1c8636ee261f07a5f10f5728b7fabd31bf5d2f9` | Small card portrait/sprite artwork; no readable writing. |
| 512 | `00039_01462_0003_card_s076_jp.tga` | 64×64 | `99c0c694701c205a8546612ceae73174c3da7551c39840fa8b32b10f4e4a5b72` | Small card portrait/sprite artwork; no readable writing. |
| 513 | `00039_01462_0004_card_s077_jp.tga` | 64×64 | `4baef66ba4eef81a3dc718f89c188388fed055e28abdcde770857ea2b712b7a8` | Small card portrait/sprite artwork; no readable writing. |
| 514 | `00039_01462_0005_card_s078_jp.tga` | 64×64 | `a7e795d9e8d38cbac6c55a4250102c7b331c5c51e36e590cce40a663aff97f61` | Small card portrait/sprite artwork; no readable writing. |
| 515 | `00039_01462_0006_card_s079_jp.tga` | 64×64 | `0d1c61ba10ddfe643a18437de391b66d6f6930177f81520be460cc04c1c9a475` | Small card portrait/sprite artwork; no readable writing. |
| 516 | `00039_01462_0007_card_s080_jp.tga` | 64×64 | `b1694e1139f815e3481c361757b0edf6a071f37f5210173ae6d94920e213792e` | Small card portrait/sprite artwork; no readable writing. |
| 517 | `00039_01462_0008_card_s081_jp.tga` | 64×64 | `d1d8319a5f228542c3d6177672c9d49be637962128ba42f7c18993f8dac36323` | Small card portrait/sprite artwork; no readable writing. |
| 518 | `00039_01462_0009_card_s082_jp.tga` | 64×64 | `f56fda5836839824e475f4117031043ff1766a27f93952d49aca333c1d4e0f8d` | Small card portrait/sprite artwork; no readable writing. |
| 519 | `00039_01462_0010_card_s083_jp.tga` | 64×64 | `9e1a7d6d3f8d77b2726ad00386428afb9c36278b9b88e109e2af1ed27bc59733` | Small card portrait/sprite artwork; no readable writing. |
| 520 | `00039_01462_0011_card_s084_jp.tga` | 64×64 | `0ea2a8d3ff864bcdda06c0ff69de072085f5c57b253c7fe07c80bae5b90bcf51` | Small card portrait/sprite artwork; no readable writing. |
| 521 | `00039_01462_0012_card_s085_jp.tga` | 64×64 | `ddeb9f6713c0396147c747233aa631cca7fa7fc87639847ec66b68e78aa9cbfe` | Small card portrait/sprite artwork; no readable writing. |
| 522 | `00039_01462_0013_card_s086_jp.tga` | 64×64 | `e709b30602b64ffd742a7b87eb9a45c97ddf2cdbd1005d3cc4bc25d88d102457` | Small card portrait/sprite artwork; no readable writing. |
| 523 | `00039_01462_0014_card_s087_jp.tga` | 64×64 | `70a3781797c29b9a4a3ff6939bc7c2ff915eebc17bb3f05cb03075d7133356e3` | Small card portrait/sprite artwork; no readable writing. |
| 524 | `00039_01462_0015_card_s088_jp.tga` | 64×64 | `d85a51e98fe3cc2ece6613db3a5fcf3406a0a9ad87453d271e35c9a4f5c88444` | Small card portrait/sprite artwork; no readable writing. |
| 525 | `00039_01462_0016_card_s089_jp.tga` | 64×64 | `584f28ea48a3ec09df6f05cfe9cd50b3a79edb9862aa30b2f1a5df12c74be48a` | Small card portrait/sprite artwork; no readable writing. |
| 526 | `00039_01462_0017_card_s090_jp.tga` | 64×64 | `a9652cea2fde982bf1968a0de0c1782d6d33b450d2b599e57a1ef3c4b4333b75` | Small card portrait/sprite artwork; no readable writing. |
| 527 | `00039_01462_0018_card_s091_jp.tga` | 64×64 | `a303ad3e72eeb7c3a75cb4b975e589b9b625a6d8020f874d364ac7d9c3ecf367` | Small card portrait/sprite artwork; no readable writing. |
| 528 | `00039_01462_0019_card_s092_jp.tga` | 64×64 | `cb3b900b8b503a0f54ec95fc0a716964e6417cfd9de969e8315cecc369100ed1` | Small card portrait/sprite artwork; no readable writing. |
| 529 | `00039_01462_0020_card_s093_jp.tga` | 64×64 | `b32e82a9a2f39d2f3a0802885c2aed058368538491e8f633ad257fa4e7d64c66` | Small card portrait/sprite artwork; no readable writing. |
| 530 | `00039_01462_0021_card_s094_jp.tga` | 64×64 | `bea383e2fd12db0177a68b3806a839185f05a2e960127bf1228f9857c2c0d6dd` | Small card portrait/sprite artwork; no readable writing. |
| 531 | `00039_01462_0022_card_s095_jp.tga` | 64×64 | `5953499c0c6ae58f0f45b1b56b3cd063fddba7a80c5dbe09dbe43009b33f3111` | Small card portrait/sprite artwork; no readable writing. |
| 532 | `00039_01462_0023_card_s096_jp.tga` | 64×64 | `1dacc78d9e1859d85361941e584c79ab8adc1e81eb3bd51078863c05b4d6773a` | Small card portrait/sprite artwork; no readable writing. |
| 533 | `00039_01462_0024_card_s097_jp.tga` | 64×64 | `87522fbc6155380ce95abe14923d94f15d24484cdcb307f4568f17bddc87628c` | Small card portrait/sprite artwork; no readable writing. |
| 534 | `00039_01462_0025_card_s098_jp.tga` | 64×64 | `06313430f9013674662a6fa72533d250e049bb5bf27e5de9f983e9249a47428c` | Small card portrait/sprite artwork; no readable writing. |
| 535 | `00039_01462_0026_card_s099_jp.tga` | 64×64 | `099a9a92ab6b7ca426fb28ede8c782bfd07a56879ae6390a4b3545b2ff88c57f` | Small card portrait/sprite artwork; no readable writing. |
| 536 | `00039_01462_0027_card_s100_jp.tga` | 64×64 | `41e754b6a4e50283529d48d32fed5a4e86649271e17c49a4d51d9b75dea3d0a2` | Small card portrait/sprite artwork; no readable writing. |
| 537 | `00039_01462_0028_card_s101_jp.tga` | 64×64 | `d1d0c45906bf1180df276e71b019a971dffa7a86bb12e15ea46ab31a2cb05eac` | Small card portrait/sprite artwork; no readable writing. |
| 538 | `00039_01462_0029_card_s102_jp.tga` | 64×64 | `910d33c3bf1fd24214b4fd94a6b3d5f508981919d5623b342a4500fe4f7f5369` | Small card portrait/sprite artwork; no readable writing. |
| 539 | `00039_01462_0030_card_s103_jp.tga` | 64×64 | `87c91eb827cbb19064867527e9879ab6eefabc1287222a082e4cf943a95a326a` | Small card portrait/sprite artwork; no readable writing. |
| 540 | `00039_01462_0031_card_s104_jp.tga` | 64×64 | `28b842cd118d429c39ee230fbe44c35441345995ab1190549c84f34acb88268c` | Small card portrait/sprite artwork; no readable writing. |
| 541 | `00039_01462_0032_card_s105_jp.tga` | 64×64 | `8d5b8e627e6b15027f2dbafc6b093184f6e54a178c98cb32b85d4ce2a0e4055d` | Small card portrait/sprite artwork; no readable writing. |
| 542 | `00039_01462_0033_card_s106_jp.tga` | 64×64 | `73fe7b0fef76e4add363ed96f373fc359cd9f490edc0f82b213e04bf64af6d06` | Small card portrait/sprite artwork; no readable writing. |
| 543 | `00039_01462_0034_card_s107_jp.tga` | 64×64 | `17e24ad2fda8b259db133d881c5acebe53dc4deb145484c598f118b77719eef1` | Small card portrait/sprite artwork; no readable writing. |
| 544 | `00039_01462_0035_card_s108_jp.tga` | 64×64 | `c9ee71f76e134a90df7b94887cec7e57f1c06ad6fdff29bdd5581d51d5003330` | Small card portrait/sprite artwork; no readable writing. |
| 545 | `00039_01462_0036_card_s109_jp.tga` | 64×64 | `d6e7d3496bd8725d254d9169500589af009dec0ef4c5a6572e4f098e585df14a` | Small card portrait/sprite artwork; no readable writing. |
| 546 | `00039_01462_0037_card_s110_jp.tga` | 64×64 | `3088544df036213f8e26e4a7afcbb35daf3fb9f7080265f32abc640eb5061b0b` | Small card portrait/sprite artwork; no readable writing. |
| 547 | `00039_01462_0038_card_s111_jp.tga` | 64×64 | `5c93e183a650906a53d1563049179b8c8eafcd86978fa6526af02159ff227685` | Small card portrait/sprite artwork; no readable writing. |
| 548 | `00039_01462_0039_card_s112_jp.tga` | 64×64 | `66354a68af6ccdf78745a41433e6102a11a40728ad072abee1b80bb58ee53c9b` | Small card portrait/sprite artwork; no readable writing. |
| 549 | `00039_01462_0040_card_s113_jp.tga` | 64×64 | `b8932420195512088484a2d0370c14ed5edf79d3b9daa8f9a3fd62d026b5b503` | Small card portrait/sprite artwork; no readable writing. |
| 550 | `00039_01462_0041_card_s114_jp.tga` | 64×64 | `56746e3eedbcb9882d93cec9ccd295b60640a7059155b7f2df8b91b0b98c5b92` | Small card portrait/sprite artwork; no readable writing. |
| 551 | `00039_01462_0042_card_s115_jp.tga` | 64×64 | `b1427799c0d0caf51efa64bbe3799554b5843397536a9c4696ca0ebfed84fc79` | Small card portrait/sprite artwork; no readable writing. |
| 552 | `00039_01462_0043_card_s116_jp.tga` | 64×64 | `92567b978516c536d7710ea308b0cc0b403926bc245b475f014900586950f440` | Small card portrait/sprite artwork; no readable writing. |
| 553 | `00039_01462_0044_card_s117_jp.tga` | 64×64 | `a6e1051de6875c70818edecf252c1bedfe26765f8a8b54cb60ab72e68d02b9a4` | Small card portrait/sprite artwork; no readable writing. |
| 554 | `00039_01462_0045_card_s118_jp.tga` | 64×64 | `8789129d828a91b50f44a8f7e087f87d0f24cbc2a21d8f0b328591a47c84d45d` | Small card portrait/sprite artwork; no readable writing. |
| 555 | `00039_01462_0046_card_s119_jp.tga` | 64×64 | `6a75943c13258186a695f596a4c2c4ac0cca9d5a03964fe98785a828afc219ce` | Small card portrait/sprite artwork; no readable writing. |
| 556 | `00039_01462_0047_card_s120_jp.tga` | 64×64 | `c252dbc98dda5c5d64bf656d0d3f55ca9f3e61c89bb652de3ca31427d794dfe6` | Small card portrait/sprite artwork; no readable writing. |
| 557 | `00039_01462_0048_card_s121_jp.tga` | 64×64 | `ccf8b2720e75f80bd45c158ba518ce8f46008d873a0f6eb43793bfa26b6d6187` | Small card portrait/sprite artwork; no readable writing. |
| 558 | `00039_01462_0049_card_s122_jp.tga` | 64×64 | `5c4401be72cda174f9b35e27f9e89211d8d6f54e7d0c2d68b57a84446d663cec` | Small card portrait/sprite artwork; no readable writing. |
| 559 | `00039_01462_0050_card_s123_jp.tga` | 64×64 | `84fd99b9ea788fe79a9ee206146daba547729005a426cb3a8e493d64628e7464` | Small card portrait/sprite artwork; no readable writing. |
| 560 | `00039_01462_0051_card_s124_jp.tga` | 64×64 | `359dbe9f32fde9dba685ebc728f4c03ed6756b9f80c9ff6175de0f26c6264b20` | Small card portrait/sprite artwork; no readable writing. |
| 561 | `00039_01462_0052_card_s125_jp.tga` | 64×64 | `0f3447bcf44fadd72da728246db9098bd15140fc00b558b4281859f4c965026f` | Small card portrait/sprite artwork; no readable writing. |
| 562 | `00039_01462_0053_card_s126_jp.tga` | 64×64 | `e41ca908fb12998280d54f8dc41995e9bdc011f1c6ce0236319e9b02dff38ac1` | Small card portrait/sprite artwork; no readable writing. |
| 563 | `00039_01462_0054_card_s127_jp.tga` | 64×64 | `921c7f890ec70a338056734f688dcbeef681ed50288166a07e2395233d936751` | Small card portrait/sprite artwork; no readable writing. |
| 564 | `00039_01462_0055_card_s128_jp.tga` | 64×64 | `2b665cd7db5a972c3a242db002fd9215ce65d218c4d95c43a90baed3346fae48` | Small card portrait/sprite artwork; no readable writing. |
| 565 | `00039_01462_0056_card_s129_jp.tga` | 64×64 | `ec48b5e17a3fa4c7ba43b91fba5196a0aca31573e06deecac9812c8464418a52` | Small card portrait/sprite artwork; no readable writing. |
| 566 | `00039_01462_0057_card_s130_jp.tga` | 64×64 | `b3808dfa54c65e293f269b508b324de3572f01734c76b1a471aee387cf39ee43` | Small card portrait/sprite artwork; no readable writing. |
| 567 | `00039_01462_0058_card_s131_jp.tga` | 64×64 | `4000d3131f4a1f8e7fa522e1db910ac570d8cdab6707dd7b757c8f5f95767f56` | Small card portrait/sprite artwork; no readable writing. |
| 568 | `00039_01462_0059_card_s132_jp.tga` | 64×64 | `92e6c0dcef5038485d650c30f6ad234a284e2d208eda8110967ad1bde4ca7bdb` | Small card portrait/sprite artwork; no readable writing. |
| 569 | `00039_01462_0060_card_s133_jp.tga` | 64×64 | `f44c36a40ea33bbf85d7ec35c15beb71909e02208b7bb67cd6bb8d6f5b871ecc` | Small card portrait/sprite artwork; no readable writing. |
| 570 | `00039_01462_0061_card_s134_jp.tga` | 64×64 | `bad18c17231ebd74a40e9713f8adf5f24e51b8cc90d3a1b33be3a9287d4bf56a` | Small card portrait/sprite artwork; no readable writing. |
| 571 | `00039_01462_0062_card_s135_jp.tga` | 64×64 | `b18fad601d2a08171a322dfa6821fb9a6e9ba6088e3bb12c40ba787b183f0ef8` | Small card portrait/sprite artwork; no readable writing. |
| 572 | `00039_01462_0063_card_s136_jp.tga` | 64×64 | `94d5b28bb9771aed9996d70d5c065da8934bdbd243e9f62d339ed64a59d96e80` | Small card portrait/sprite artwork; no readable writing. |
| 573 | `00039_01462_0064_card_s137_jp.tga` | 64×64 | `b560ddcc66f6fcac9fdd2c9ebc1b5d45c489cbc887debb5c019dcaf3e6e03e27` | Small card portrait/sprite artwork; no readable writing. |
| 574 | `00039_01462_0065_card_s138_jp.tga` | 64×64 | `70c7923efe46232c132d861ca427da2f7429d14b503e6cf5d8b4731f57eaaaa6` | Small card portrait/sprite artwork; no readable writing. |
| 575 | `00039_01462_0066_card_s139_jp.tga` | 64×64 | `49955a1a31342c16e72c82f183836ad98d7631c030f58915d59760171decff5a` | Small card portrait/sprite artwork; no readable writing. |
| 576 | `00039_01462_0067_card_s140_jp.tga` | 64×64 | `5281c13621f661a71458d89e92ff31cee35ceb5219dbd5c9380edf3046d9bb1a` | Small card portrait/sprite artwork; no readable writing. |
| 577 | `00039_01462_0068_card_s141_jp.tga` | 64×64 | `3ca53b069a75c81eed2bef55c37a3eccc4c20d75e23b31a22012a41009034ff1` | Small card portrait/sprite artwork; no readable writing. |
| 578 | `00039_01462_0069_card_s142_jp.tga` | 64×64 | `5281c13621f661a71458d89e92ff31cee35ceb5219dbd5c9380edf3046d9bb1a` | Small card portrait/sprite artwork; no readable writing. Exact byte duplicate of #576 `00039_01462_0067_card_s140_jp.tga`. |
| 579 | `00039_01462_0070_card_s141_jp.tga` | 64×64 | `3ca53b069a75c81eed2bef55c37a3eccc4c20d75e23b31a22012a41009034ff1` | Small card portrait/sprite artwork; no readable writing. Exact byte duplicate of #577 `00039_01462_0068_card_s141_jp.tga`. |
| 580 | `00039_01462_0071_card_sgba_jp.tga` | 64×64 | `49955a1a31342c16e72c82f183836ad98d7631c030f58915d59760171decff5a` | Small card portrait/sprite artwork; no readable writing. Exact byte duplicate of #575 `00039_01462_0066_card_s139_jp.tga`. |
| 581 | `00039_01462_0072_card_ssunday_jp.tga` | 64×64 | `aa01846d0f3840b68855e1ece1513de9cc5a4a9fc4bf39f2ad16ebbaa5d5d6c5` | Small card portrait/sprite artwork; no readable writing. |
| 582 | `00039_01463_0000_card_sunday_jp.tga` | 512×512 | `6aa8809a321defec738e5ca6793306993482044c0a5e9c526d3efdae2d4d7843` | Small card portrait/sprite artwork; no readable writing. Exact byte duplicate of #145 `00039_01169_0000_card_sunday_jp.tga`. |
| 583 | `00039_01521_0005_card_001_jp.tga` | 512×512 | `b4021e45b204ba7fc5758001acced03d4b5afaa654d3f6b2b66d1440db95033f` | Framed card/character illustration; no readable writing. |
| 584 | `00039_01521_0006_card_s000_jp.tga` | 64×64 | `87c69a765b7c69a78b6f4966db1d25374a4c5428b73c88392330b1b56b84dbc5` | Small card portrait/sprite artwork; no readable writing. |
| 585 | `00039_01521_0007_card_s001_jp.tga` | 64×64 | `7e4a8364e416090a908d3a7afdc41f96626acee403e305893e2bebb95e92d4f1` | Small card portrait/sprite artwork; no readable writing. |
| 586 | `00039_01521_0008_card_s002_jp.tga` | 64×64 | `dcca398a5443150be99f3ab9769f88a3f8076afc211820373a8f7422dc9b9d80` | Small card portrait/sprite artwork; no readable writing. |
| 587 | `00039_01521_0009_card_s003_jp.tga` | 64×64 | `af864019f035b1a000df6ad29aedff253b0d896997457f09ed136fac1f7445a3` | Small card portrait/sprite artwork; no readable writing. |
| 588 | `00039_01521_0010_card_s004_jp.tga` | 64×64 | `aa5b75de232054d9feb1e8cd0780c3877e387a93aab7e481efbab2f9847c3aa6` | Small card portrait/sprite artwork; no readable writing. |
| 589 | `00039_01521_0011_card_s005_jp.tga` | 64×64 | `6fa8d69c6196b84a936c6dbe07b8c7284661d66c5d8bf4d7651ce2ec21d2c7ed` | Small card portrait/sprite artwork; no readable writing. |
| 590 | `00039_01521_0012_card_s006_jp.tga` | 64×64 | `f77529aaf9bc7bee90f71198befc06dd9a8422c25ce06146d5e091dc0a3b2ef7` | Small card portrait/sprite artwork; no readable writing. |
| 591 | `00039_01521_0013_card_s007_jp.tga` | 64×64 | `ff148a467c1a8c5acba5ea04b2558d9bee38de607c6962970320305b36caf676` | Small card portrait/sprite artwork; no readable writing. |
| 592 | `00039_01521_0014_card_s008_jp.tga` | 64×64 | `162c64a7c376c3db288d473e3aeb3154d69babe6df1b41c03b161ff0cd33a600` | Small card portrait/sprite artwork; no readable writing. |
| 593 | `00039_01521_0015_card_s009_jp.tga` | 64×64 | `8651693ce785ad2bedc1116a8c91bc25b1c708f493442ac2270b26c3c9efd9e8` | Small card portrait/sprite artwork; no readable writing. |
| 594 | `00039_01521_0016_card_s010_jp.tga` | 64×64 | `f324d88265e906b72e8c7c2821f2c2aff914a2671af65596e11dd0ada8dc109e` | Small card portrait/sprite artwork; no readable writing. |
| 595 | `00039_01521_0017_card_s011_jp.tga` | 64×64 | `6530966a49cf4e3a17fe1ec8fcb01182dd17d5976e7a10ee02b11cf201475e33` | Small card portrait/sprite artwork; no readable writing. |
| 596 | `00039_01521_0018_card_s012_jp.tga` | 64×64 | `916a4fece7c13fa244347c39056354f0ebded9b72be85424f363c1884418088b` | Small card portrait/sprite artwork; no readable writing. |
| 597 | `00039_01521_0019_card_s013_jp.tga` | 64×64 | `7a1a29e88484aa66616210abd73fc9c1213d7839961ce8e9209b25044d498571` | Small card portrait/sprite artwork; no readable writing. |
| 598 | `00039_01521_0020_card_s014_jp.tga` | 64×64 | `53d7944ebfc72b80596497d1f7c250ad92ca5ebc0bb578ab88c3fb4d6481b7cb` | Small card portrait/sprite artwork; no readable writing. |
| 599 | `00039_01597_0000_00card_jp.tga` | 128×128 | `0f2bf472a4a2e8a7c66142f3380ddc4aa9b0e503683369841b1cf37a60a27243` | Character-card portrait/crop; no readable writing. |
| 600 | `00039_01597_0001_01card_jp.tga` | 128×128 | `5bf039d2467950e9044d15f80920353978af8a8916782069d87bd747c05b8593` | Character-card portrait/crop; no readable writing. |
| 601 | `00039_01597_0002_02card_jp.tga` | 128×128 | `0f93f90a589d4ad2fabd71c928a84813bb3f4ddfd0e26f17c021cb4bbb876748` | Character-card portrait/crop; no readable writing. |
| 602 | `00039_01597_0003_03card_jp.tga` | 128×128 | `b5caabe05e606e9bcc1c848c0cac67a9d29e567a076e828fedaa8c9495a50ba0` | Character-card portrait/crop; no readable writing. |
| 603 | `00039_01597_0004_04card_jp.tga` | 128×128 | `1dcb4baed4c7f070f976907863d6d47ccf545e1bfe8d1ea6c93b52d7d235fcc3` | Character-card portrait/crop; no readable writing. |
| 604 | `00039_01597_0005_05card_jp.tga` | 128×128 | `2c250aafc7a891f5eecb42d2e94b42b78c2b33075367a6f99c66d8ecf038ad3c` | Character-card portrait/crop; no readable writing. |
| 605 | `00039_01597_0006_06card_jp.tga` | 128×128 | `f954704123364a39ebc0108666e576bd08e019d1748621c71b3ae2f384cf1d49` | Character-card portrait/crop; no readable writing. |
| 606 | `00039_01597_0007_07card_jp.tga` | 128×128 | `26edfc1b328ff13ff44288c1ba6f9ca6f5ce6f5e38b8db3109e816910432238d` | Character-card portrait/crop; no readable writing. |
| 607 | `00039_01597_0008_08card_jp.tga` | 128×128 | `ec2acc389d26687213428796e5a0b66da072511c7bac40ea19bc16c3f2a0d0a4` | Character-card portrait/crop; no readable writing. |
| 608 | `00039_01597_0009_09card_jp.tga` | 128×128 | `0994b81f21d1561ea1560270a8dfb3dc7cb7fa239baf8c55b52ef2e8396916b5` | Character-card portrait/crop; no readable writing. |
| 609 | `00039_01597_0010_10card_jp.tga` | 128×128 | `1f0facac9d7b14dad62cd27babc8116542f3d12adf1bf0b36f88ffd66653623f` | Character-card portrait/crop; no readable writing. |
| 610 | `00039_01597_0011_11card_jp.tga` | 128×128 | `4be7a451b3309849282a93ca6a76ff86b94b9f1494d39508fb35f831b29a1d6d` | Character-card portrait/crop; no readable writing. |
| 611 | `00039_01597_0012_12card_jp.tga` | 128×128 | `2a093e1f9e07c197872f21f30577cbc5e552a624a22b64dbf3e80abe21912ffc` | Character-card portrait/crop; no readable writing. |
| 612 | `00039_01597_0013_13card_jp.tga` | 128×128 | `fa94b06fdf0e2f00789e40442d4297daeb977fe85ff74d271ec7cbcb5a3bb453` | Character-card portrait/crop; no readable writing. |
| 613 | `00039_01597_0014_14card_jp.tga` | 128×128 | `9d06c8ccb10c820393e9830bab3513e9789349a2bdf3578f5faac5977b95cac9` | Character-card portrait/crop; no readable writing. |
| 614 | `00039_01597_0015_15card_jp.tga` | 128×128 | `92f29b69f402403b057625d9f9a205009dbe107a991fc51bc2508215ce434bb2` | Character-card portrait/crop; no readable writing. |
| 615 | `00039_01597_0016_16card_jp.tga` | 128×128 | `279655699ebebe99aa97e641737e32898e248a4ff6ef3b7cff5baf8b1e80c979` | Character-card portrait/crop; no readable writing. |
| 616 | `00039_01600_0000_00card_jp.tga` | 128×128 | `7cb838207aacb26ce517a4259e935b439e95c9f5ee2bb8b2ecb6dcdd2792f540` | Character-card portrait/crop; no readable writing. |
| 617 | `00039_01600_0001_01card_jp.tga` | 128×128 | `6307d32bd4a5fa275eb229ad4e4bb54323b9203371a95c8e39d91c749ac8a922` | Character-card portrait/crop; no readable writing. |
| 618 | `00039_01600_0002_02card_jp.tga` | 128×128 | `524e9b53414f33bdd3e33c2fbee037092b809c227bf027f7f5db35b4123505a8` | Character-card portrait/crop; no readable writing. |
| 619 | `00039_01600_0003_03card_jp.tga` | 128×128 | `05700b57c5a651d74d34bd6831d81dd0ce3426484fe06c1871d8ea06899707c7` | Character-card portrait/crop; no readable writing. |
| 620 | `00039_01600_0004_04card_jp.tga` | 128×128 | `0f3cd66376597bbe9b97e3ba812a231491027908a816321c97e632fe753b2fd2` | Character-card portrait/crop; no readable writing. |
| 621 | `00039_01600_0005_05card_jp.tga` | 128×128 | `2750dadd27bdb0610a0f3d0f96620f5ed8651274a12d5448a924af0f63c74260` | Character-card portrait/crop; no readable writing. |
| 622 | `00039_01600_0006_06card_jp.tga` | 128×128 | `d8fef8a680811c2652793724e0dd6b25dc3da3a134cdd0749f79c336d1a6274d` | Character-card portrait/crop; no readable writing. |
| 623 | `00039_01600_0007_07card_jp.tga` | 128×128 | `830023a11de0752fb41887ffdad0108d087bba8518a1e4e114b8fecc9637136c` | Character-card portrait/crop; no readable writing. |
| 624 | `00039_01600_0008_08card_jp.tga` | 128×128 | `c4a2bc46183161af52950de3d05e0c4018a5d4f939df3f531ddeafa5e724c094` | Character-card portrait/crop; no readable writing. |
| 625 | `00039_01600_0009_09card_jp.tga` | 128×128 | `2ff79707aa35bc045d2914297dcfd6d5bd3a6391f162104cb24a937ecf49822b` | Character-card portrait/crop; no readable writing. |
| 626 | `00039_01600_0010_10card_jp.tga` | 128×128 | `9c02bf17f7a96a2d9ed70593bb1db090233a916cf1c82a2a23710bb0825eff19` | Character-card portrait/crop; no readable writing. |
| 627 | `00039_01600_0011_11card_jp.tga` | 128×128 | `a1d9f7811703bad3b4475def2e92eb5594aad6e5db9731a9691157eafc7f1340` | Character-card portrait/crop; no readable writing. |
| 628 | `00039_01600_0012_12card_jp.tga` | 128×128 | `c776bb7dd0492afb7674e45c176b31f4feaa2e2328a0e8b5ed8f3f9b41386129` | Character-card portrait/crop; no readable writing. |
| 629 | `00039_01600_0013_13card_jp.tga` | 128×128 | `6132016e25f7b90d99726b7de5510fb757944837318372a7fece6337d58beff3` | Character-card portrait/crop; no readable writing. |
| 630 | `00039_01600_0014_14card_jp.tga` | 128×128 | `41c0e3fd5f202eb3ca9aea6feb5d0dfdddb587eb0321811581fae0b0aa9bf9d6` | Character-card portrait/crop; no readable writing. |
| 631 | `00039_01600_0015_15card_jp.tga` | 128×128 | `1f7ae68967b97325eb0770239b51c71a3e75e2c70168d1bd5f13fca5fee7a848` | Character-card portrait/crop; no readable writing. |
| 632 | `00039_01600_0016_center_bar_jp.tga` | 128×64 | `f9f558f0d2ea2e4e3c122f46d0775118c5c5c11153911e988cca74adaa9eb574` | Dark patterned center strip; contrast-stretched preview has block-like marks, but no script/words can be read confidently. Unresolved candidate; no text bounds assigned. |
| 633 | `00039_01600_0017_hurry_jp.tga` | 128×32 | `f969e59b3b15e9379655a218e068c5e25f5d6af6fdb562208ec6398b087ff0b8` | English “HURRY UP!”; visible glyphs approx. [6,121)×[6,26). |
| 634 | `00039_01600_0018_wait_jp.tga` | 128×32 | `7d0950a9d99ab67b76f469a43c7204a264afa1fe41460f262485aa98a0c3c10a` | English “Please Wait...”; visible glyphs approx. [5,125)×[6,25). |
| 635 | `00039_01600_0020_safe_flame_jp.tga` | 64×64 | `f93f4987bb9f1fd1bf281ddc0c0ec29fb539f697c21db4cd05a20c77fcfe0e93` | Flame/effect pictogram; no readable lettering. |
| 636 | `00039_01600_0021_draw_jp.tga` | 128×32 | `93710cb36d5099411faaef6a4eee727c602be21218d2ef080b3cb95cfd1e723d` | English “DRAW”; visible glyphs approx. [6,122)×[3,28). |
| 637 | `00039_01600_0022_extb_jp.tga` | 256×64 | `09bbfd87ccfdbea462022d5b028c05cba9c4fd6f79c819e558941b0f773532c1` | English “EXTRA TITLE” / “EXTRA BATTLE”; visible glyphs approx. [9,250)×[6,60). |
| 638 | `00039_01600_0023_wld_jp.tga` | 64×64 | `424a5c8599441b2844eede6d05619716eb802a1a8af74cee90c25b573a950e21` | English “Win / Lose / Draw”: Win [13,52)×[3,18); Lose [13,51)×[24,38); Draw [8,58)×[45,59). |
| 639 | `00039_01629_0000_00card_jp.tga` | 128×128 | `0f2bf472a4a2e8a7c66142f3380ddc4aa9b0e503683369841b1cf37a60a27243` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #599 `00039_01597_0000_00card_jp.tga`. |
| 640 | `00039_01629_0001_01card_jp.tga` | 128×128 | `5bf039d2467950e9044d15f80920353978af8a8916782069d87bd747c05b8593` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #600 `00039_01597_0001_01card_jp.tga`. |
| 641 | `00039_01629_0002_02card_jp.tga` | 128×128 | `0f93f90a589d4ad2fabd71c928a84813bb3f4ddfd0e26f17c021cb4bbb876748` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #601 `00039_01597_0002_02card_jp.tga`. |
| 642 | `00039_01629_0003_03card_jp.tga` | 128×128 | `b5caabe05e606e9bcc1c848c0cac67a9d29e567a076e828fedaa8c9495a50ba0` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #602 `00039_01597_0003_03card_jp.tga`. |
| 643 | `00039_01629_0004_04card_jp.tga` | 128×128 | `1dcb4baed4c7f070f976907863d6d47ccf545e1bfe8d1ea6c93b52d7d235fcc3` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #603 `00039_01597_0004_04card_jp.tga`. |
| 644 | `00039_01629_0005_05card_jp.tga` | 128×128 | `2c250aafc7a891f5eecb42d2e94b42b78c2b33075367a6f99c66d8ecf038ad3c` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #604 `00039_01597_0005_05card_jp.tga`. |
| 645 | `00039_01629_0006_06card_jp.tga` | 128×128 | `f954704123364a39ebc0108666e576bd08e019d1748621c71b3ae2f384cf1d49` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #605 `00039_01597_0006_06card_jp.tga`. |
| 646 | `00039_01629_0007_07card_jp.tga` | 128×128 | `26edfc1b328ff13ff44288c1ba6f9ca6f5ce6f5e38b8db3109e816910432238d` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #606 `00039_01597_0007_07card_jp.tga`. |
| 647 | `00039_01629_0008_08card_jp.tga` | 128×128 | `ec2acc389d26687213428796e5a0b66da072511c7bac40ea19bc16c3f2a0d0a4` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #607 `00039_01597_0008_08card_jp.tga`. |
| 648 | `00039_01629_0009_09card_jp.tga` | 128×128 | `0994b81f21d1561ea1560270a8dfb3dc7cb7fa239baf8c55b52ef2e8396916b5` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #608 `00039_01597_0009_09card_jp.tga`. |
| 649 | `00039_01629_0010_10card_jp.tga` | 128×128 | `1f0facac9d7b14dad62cd27babc8116542f3d12adf1bf0b36f88ffd66653623f` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #609 `00039_01597_0010_10card_jp.tga`. |
| 650 | `00039_01629_0011_11card_jp.tga` | 128×128 | `4be7a451b3309849282a93ca6a76ff86b94b9f1494d39508fb35f831b29a1d6d` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #610 `00039_01597_0011_11card_jp.tga`. |
| 651 | `00039_01629_0012_12card_jp.tga` | 128×128 | `2a093e1f9e07c197872f21f30577cbc5e552a624a22b64dbf3e80abe21912ffc` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #611 `00039_01597_0012_12card_jp.tga`. |
| 652 | `00039_01629_0013_13card_jp.tga` | 128×128 | `fa94b06fdf0e2f00789e40442d4297daeb977fe85ff74d271ec7cbcb5a3bb453` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #612 `00039_01597_0013_13card_jp.tga`. |
| 653 | `00039_01629_0014_14card_jp.tga` | 128×128 | `9d06c8ccb10c820393e9830bab3513e9789349a2bdf3578f5faac5977b95cac9` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #613 `00039_01597_0014_14card_jp.tga`. |
| 654 | `00039_01629_0015_15card_jp.tga` | 128×128 | `92f29b69f402403b057625d9f9a205009dbe107a991fc51bc2508215ce434bb2` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #614 `00039_01597_0015_15card_jp.tga`. |
| 655 | `00039_01629_0016_16card_jp.tga` | 128×128 | `279655699ebebe99aa97e641737e32898e248a4ff6ef3b7cff5baf8b1e80c979` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #615 `00039_01597_0016_16card_jp.tga`. |
| 656 | `00039_01635_0000_00card_jp.tga` | 128×128 | `7cb838207aacb26ce517a4259e935b439e95c9f5ee2bb8b2ecb6dcdd2792f540` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #616 `00039_01600_0000_00card_jp.tga`. |
| 657 | `00039_01635_0001_01card_jp.tga` | 128×128 | `6307d32bd4a5fa275eb229ad4e4bb54323b9203371a95c8e39d91c749ac8a922` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #617 `00039_01600_0001_01card_jp.tga`. |
| 658 | `00039_01635_0002_02card_jp.tga` | 128×128 | `524e9b53414f33bdd3e33c2fbee037092b809c227bf027f7f5db35b4123505a8` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #618 `00039_01600_0002_02card_jp.tga`. |
| 659 | `00039_01635_0003_03card_jp.tga` | 128×128 | `05700b57c5a651d74d34bd6831d81dd0ce3426484fe06c1871d8ea06899707c7` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #619 `00039_01600_0003_03card_jp.tga`. |
| 660 | `00039_01635_0004_04card_jp.tga` | 128×128 | `0f3cd66376597bbe9b97e3ba812a231491027908a816321c97e632fe753b2fd2` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #620 `00039_01600_0004_04card_jp.tga`. |
| 661 | `00039_01635_0005_05card_jp.tga` | 128×128 | `2750dadd27bdb0610a0f3d0f96620f5ed8651274a12d5448a924af0f63c74260` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #621 `00039_01600_0005_05card_jp.tga`. |
| 662 | `00039_01635_0006_06card_jp.tga` | 128×128 | `d8fef8a680811c2652793724e0dd6b25dc3da3a134cdd0749f79c336d1a6274d` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #622 `00039_01600_0006_06card_jp.tga`. |
| 663 | `00039_01635_0007_07card_jp.tga` | 128×128 | `830023a11de0752fb41887ffdad0108d087bba8518a1e4e114b8fecc9637136c` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #623 `00039_01600_0007_07card_jp.tga`. |
| 664 | `00039_01635_0008_08card_jp.tga` | 128×128 | `c4a2bc46183161af52950de3d05e0c4018a5d4f939df3f531ddeafa5e724c094` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #624 `00039_01600_0008_08card_jp.tga`. |
| 665 | `00039_01635_0009_09card_jp.tga` | 128×128 | `2ff79707aa35bc045d2914297dcfd6d5bd3a6391f162104cb24a937ecf49822b` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #625 `00039_01600_0009_09card_jp.tga`. |
| 666 | `00039_01635_0010_10card_jp.tga` | 128×128 | `9c02bf17f7a96a2d9ed70593bb1db090233a916cf1c82a2a23710bb0825eff19` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #626 `00039_01600_0010_10card_jp.tga`. |
| 667 | `00039_01635_0011_11card_jp.tga` | 128×128 | `a1d9f7811703bad3b4475def2e92eb5594aad6e5db9731a9691157eafc7f1340` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #627 `00039_01600_0011_11card_jp.tga`. |
| 668 | `00039_01635_0012_12card_jp.tga` | 128×128 | `c776bb7dd0492afb7674e45c176b31f4feaa2e2328a0e8b5ed8f3f9b41386129` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #628 `00039_01600_0012_12card_jp.tga`. |
| 669 | `00039_01635_0013_13card_jp.tga` | 128×128 | `6132016e25f7b90d99726b7de5510fb757944837318372a7fece6337d58beff3` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #629 `00039_01600_0013_13card_jp.tga`. |
| 670 | `00039_01635_0014_14card_jp.tga` | 128×128 | `41c0e3fd5f202eb3ca9aea6feb5d0dfdddb587eb0321811581fae0b0aa9bf9d6` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #630 `00039_01600_0014_14card_jp.tga`. |
| 671 | `00039_01635_0015_15card_jp.tga` | 128×128 | `1f7ae68967b97325eb0770239b51c71a3e75e2c70168d1bd5f13fca5fee7a848` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #631 `00039_01600_0015_15card_jp.tga`. |
| 672 | `00039_01635_0016_16card_jp.tga` | 128×128 | `279655699ebebe99aa97e641737e32898e248a4ff6ef3b7cff5baf8b1e80c979` | Character-card portrait/crop; no readable writing. Exact byte duplicate of #615 `00039_01597_0016_16card_jp.tga`. |

## Dimension distribution

| Canvas | Paths |
|---:|---:|
| 64×64 | 162 |
| 128×32 | 3 |
| 128×64 | 1 |
| 128×128 | 67 |
| 256×64 | 1 |
| 512×128 | 145 |
| 512×512 | 292 |
| 1024×512 | 1 |

**Integrity result:** 672/672 paths match the index names, dimensions, and full SHA-256 values; all 672 have the validated TGA layout above. There are 615 unique complete-file hashes and 57 repeated paths. No asset bytes or index rows were edited.
