# DQ-37 `ｗ.b` Japanese UI-text audit

## Scope and method

This is a read-only visual audit of exactly the `user_interface` rows in
`graphics/index.json` whose `asset_path` is the fullwidth-w path
`disc!/_DATA.YFS;1!/data/menu/ｗ.b`. The selection contains 30 rows. Each
Japanese TGA was viewed at native or nearest-neighbor enlargement with its
stored alpha composited over a checkerboard; close-ups were made for the
candidate text surfaces. No Japanese baseline, index, override, bundle, or ISO
was edited or built.

Every listed filename, dimension, and complete TGA SHA-256 matches its index
row and was recomputed from the file. All 30 files are uncompressed type-2,
32-bit TGAs with descriptor `0x28` (top-origin and 8 alpha bits), zero ID and
color-map fields, and zero x/y origin. Each file has the exact extent
`18 + width * height * 4`; extents are listed below. The 30 TGA hashes are
unique and the files total 2,048,540 bytes.

## Inventory and visual findings

| Japanese baseline | Dimensions | TGA extent | SHA-256 | Visual finding |
| --- | ---: | ---: | --- | --- |
| `00039_01635_0017_center_bar_jp.tga` | 128×64 | 32,786 bytes | `f9f558f0d2ea2e4e3c122f46d0775118c5c5c11153911e988cca74adaa9eb574` | Dark central-bar/UI frame with repeated very low-contrast block forms; white-, black-, and magenta-composited previews still yielded no confidently readable words. Keep the faint forms unclassified. |
| `00039_01635_0018_draw_jp.tga` | 128×32 | 16,402 bytes | `93710cb36d5099411faaef6a4eee727c602be21218d2ef080b3cb95cfd1e723d` | English `DRAW` label (alpha-content bounds x=[3,124), y=[1,31)); no Japanese wording. |
| `00039_01635_0019_extb_jp.tga` | 256×64 | 65,554 bytes | `2487b923ab690ca578a97f7d8066433860df1e939ed58e7417e8985a334b7d9c` | English `SUDDEN` / `DEATH` lettering on two lines (approximate alpha bounds x=[5,250), y=[5,28) and x=[1,256), y=[33,64)); no Japanese wording. |
| `00039_01635_0021_fgr_00_jp.tga` | 128×128 | 65,554 bytes | `f09268cdfadf3518a75aae86aca0b28c5b58c228eefd0b59907ecf0a7b40a290` | Small scene/art tile; no legible writing found. |
| `00039_01635_0022_fgr_01_jp.tga` | 128×128 | 65,554 bytes | `b7f924eaf6214f10f5755f2a5611461f037fa57418d1972937d3392d224aae22` | Small scene/art tile; no legible writing found. |
| `00039_01635_0023_fgr_02_jp.tga` | 128×128 | 65,554 bytes | `f166b5427846c62e17fd5bd86c7537cd4f53f10b2a2081e3f65af2e9a79ccb0c` | Small scene/art tile; no legible writing found. |
| `00039_01635_0024_fgr_03_jp.tga` | 128×128 | 65,554 bytes | `36bcc8864395cfb6b0d18de453050df663287f68cd41546da1d6607726f43f1f` | Small scene/art tile; no legible writing found. |
| `00039_01635_0025_fgr_04_jp.tga` | 128×128 | 65,554 bytes | `719cee0b9f5bb582581e7610461c482e40052ee7bdaf7716b575254a97f054b1` | Small scene/art tile; no legible writing found. |
| `00039_01635_0026_fgr_05_jp.tga` | 128×128 | 65,554 bytes | `b4efffe6f371a9ba0cee98c4542d86500c557778b9e5475ab5844b8009302f2c` | Small scene/art tile; no legible writing found. |
| `00039_01635_0027_fgr_06_jp.tga` | 128×128 | 65,554 bytes | `9c39a07f48234f06f2ba001ce1cf485bcd9f87b866803ce245335ba534cfd37a` | Small scene/art tile; no legible writing found. |
| `00039_01635_0028_field_name_jp.tga` | 256×128 | 131,090 bytes | `5703632ecde398c352c36bbaf0ab4a449178d793e0e003ddea9048600d9abed4` | Japanese field-name atlas: three paired rows of labels ending `のフィールド`, plus centered `サイコロ操作` (dice operation/control). Exact leading names remain too small/contextless to transcribe confidently. Alpha-row bounds: x=[5,252), y=[2,23), [26,47), [50,71); final centered row x=[33,225), y=[73,95). |
| `00039_01635_0029_gl_00_jp.tga` | 128×128 | 65,554 bytes | `ead3eddfb552c433aebeb06ef14fd889610ed96b6dc5e74c932cd56fff10276e` | Terrain/material texture; no legible writing found. |
| `00039_01635_0030_gl_01_jp.tga` | 64×128 | 32,786 bytes | `b3b2b7f180ac772504f1e83e44e45a7a36a59b3e681c983ebd1e4df07a24be44` | Narrow terrain/material texture; no legible writing found. |
| `00039_01635_0031_gl_02_jp.tga` | 128×32 | 16,402 bytes | `8102a2bbd55a83eac448ebc6b14193497c1b07ecb42131b7a3d0ccdc2944df31` | Short band-like texture; no legible writing found. |
| `00039_01635_0032_hurry_jp.tga` | 128×32 | 16,402 bytes | `f969e59b3b15e9379655a218e068c5e25f5d6af6fdb562208ec6398b087ff0b8` | English `HURRY UP!` label; no Japanese wording. |
| `00039_01635_0037_nof_00_jp.tga` | 128×128 | 65,554 bytes | `7583c88a8f10fa18d629f1c2e3631c052da33efed4edd6acdc967db2a4f1a927` | Monochrome human-silhouette artwork; no visible wording. |
| `00039_01635_0038_nof_01_jp.tga` | 128×128 | 65,554 bytes | `7d5136bd03f1edd10b20210006571e45295dfe5fc64e3783fe9d4bf47af4c263` | Monochrome human-silhouette artwork; no visible wording. |
| `00039_01635_0039_nof_02_jp.tga` | 128×128 | 65,554 bytes | `360c096be191ab681e8b2343f175024f8c002938d537e771113b159e064658fe` | Monochrome human-silhouette artwork; no visible wording. |
| `00039_01635_0040_nof_03_jp.tga` | 128×128 | 65,554 bytes | `5dba5ff5d5b021ef8cc4498f87d6127a8b891ec0a33a296063a86d2aa93eccbb` | Monochrome human-silhouette artwork; no visible wording. |
| `00039_01635_0041_nof_04_jp.tga` | 128×128 | 65,554 bytes | `d00c6638f9b8b749a8168e9b4038f00da4743a2cd22b920175c9ea120bb46411` | Monochrome human-silhouette artwork; no visible wording. |
| `00039_01635_0042_nof_05_jp.tga` | 128×128 | 65,554 bytes | `c1f5d589718d7c4c761aad279ccf2a46a1515c6d8d7e92deb03b1fcf84e003f9` | Monochrome human-silhouette artwork; no visible wording. |
| `00039_01635_0051_sel_pl_com_jp.tga` | 256×64 | 65,554 bytes | `7bbee25926e8f69bd131b50a39b10f6f6f90762b00355fa579b4db2e704729b3` | English matchup labels: `PLAYER 1 VS COM`, `PLAYER 1 VS PLAYER 2`, and `COM VS COM`. Row bounds: x=[25,179), [26,230), [76,180); y=[2,19), [22,39), [42,59). No Japanese wording. |
| `00039_01635_0052_selend_jp.tga` | 64×64 | 16,402 bytes | `5308abb63838858eeb6d4c23d96e329b25a6c4aae500a86e597d0ff4311c1c36` | English `Select` / `END` controls; no Japanese wording. |
| `00039_01635_0053_silver_dice_jp.tga` | 512×256 | 524,306 bytes | `4fcc81a1b95a7ddc6eeeb738e549716e8de6f8da787073eba3939c5489e5a88d` | Mixed icon/lettering atlas. Its lower-right panel has two blue and two magenta text-like rows at x/y=[388,507)×[136,152), [403,489)×[168,184), [396,510)×[200,216), and [385,507)×[232,250). The script/words are unresolved; other cells contain repeated monochrome symbols or mark-like forms that are not confidently text. |
| `00039_01635_0056_trns_jp.tga` | 64×64 | 16,402 bytes | `2eda80d4f411d76cef992dd5d8429ffec5c7f82b07452605a9a33fd34af11c76` | Color/alpha transition strip; no visible wording. |
| `00039_01635_0057_vs_number_jp.tga` | 128×64 | 32,786 bytes | `9bfd43284c93ab8818b7a6bd3303ac77060e520f7546c1843a29171cc0adcd77` | Numeric/symbol atlas; no Japanese wording found. |
| `00039_01635_0058_wait_jp.tga` | 128×32 | 16,402 bytes | `7d0950a9d99ab67b76f469a43c7204a264afa1fe41460f262485aa98a0c3c10a` | English `Please Wait...` lettering; no Japanese wording. |
| `00039_01635_0075_window_jp.tga` | 128×128 | 65,554 bytes | `3fbd5203048a1dcfbca7046992ee3a07bc7bebb85e3338006dc9797b3519f1fb` | Three outlined Japanese-looking label rows, readings unresolved. Alpha bounds x/y=[1,101)×[1,27), [1,100)×[45,71), and [5,123)×[76,99). A separate full-width lower band at y=[110,124) appears decorative/frame-like at this view, not confidently readable text. |
| `00039_01635_0076_wld_jp.tga` | 64×64 | 16,402 bytes | `424a5c8599441b2844eede6d05619716eb802a1a8af74cee90c25b573a950e21` | English three-label set: `Win`, `Lose`, and `Draw`; row bounds x=[11,54), [11,53), [6,60); y=[2,20), [23,39), [44,60). No Japanese wording. |
| `00039_01635_0077_wrgm_jp.tga` | 256×64 | 65,554 bytes | `bac1356323bb8aa21659d7715b51f40cedbbcbeac658ff0360b6d71a92b85017` | Extruded multicolor Japanese/katakana-like wordmark; content bounds x=[1,202), y=[14,59). Exact reading remains unresolved; do not substitute a nearby similarly named logo's reading. |

## Result and limits

The `field_name` export is a confirmed Japanese-bearing surface: three paired
field-label rows end in `のフィールド`, and a centered row reads
`サイコロ操作`. The first three labels need contextual translation before an
English sibling is drafted. The `silver_dice` lower-right lettering and the
three outlined `window` rows are additional text-like candidates, but their
script/reading was not confirmed from isolated pixels. The colorful `wrgm`
mark also appears Japanese/katakana-like, but its reading remains unresolved.
The faint central-bar forms were reviewed with adjusted contrast and are not a
confirmed text surface. Other rows contain English UI labels or artwork,
silhouettes, symbols, and material/effect textures without visible Japanese
wording.

These are image-content observations only. Flat TGAs do not establish UVs,
atlas-to-screen mapping, draw order, animation, or runtime visibility. Bounds
are raster-space half-open pixel rectangles, not game UVs. No translation,
palette import, rebuild, ISO, or emulator validation was performed.
All Japanese baselines remain unchanged; no English override was created.

References: [`graphics/index.json`](../graphics/index.json),
[`LOCALIZATION_METHODOLOGY.md`](../docs/LOCALIZATION_METHODOLOGY.md), and the
indexed source bundle `disc!/_DATA.YFS;1!/data/menu/ｗ.b`.
