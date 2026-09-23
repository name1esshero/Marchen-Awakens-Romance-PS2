# English title-parts texture draft

Updated: 2026-09-23.

`graphics/title/00039_01565_0000_ttlprts_jp.tga` remains the immutable
recovered baseline (512×512, 32-bit TGA, 1,048,594 bytes; SHA-256
`a528447c14929d7d16fc62254d6fdca90ff6d3f336c8b3a27b53f303d646542c`). Its
English sibling, `graphics/title/00039_01565_0000_ttlprts_eng.tga`, is a
same-size draft (SHA-256
`eb3d226ace0f02b70eec514b993d027adf1e5a74bbc9b5bf15ad99914114ae88`). The
baseline hash also matches `graphics/index.json`.

The atlas has three Japanese wordmark placements in gray, color, and gray
treatments. These were replaced with the already localized native `MÄR HEAVEN`
wordmark from `00039_01566_0002_title_marh_eng.tga`; its gray and color
lettering was scaled into the corresponding slots. The Japanese creator and
publisher credit strip was replaced with the established line
`© Nobuyuki Anzai / Shogakukan • ShoPro • TV Tokyo`, reused from
`00039_01566_0003_title_parts_eng.tga` and rotated into the source strip's
vertical atlas orientation. Existing `MÄRCHEN AWAKENS ROMANCE`, `PRESS START
BUTTON`, and `© 2005 KONAMI` lettering remains. All edits are limited to the
three logo regions and the credit strip; every TGA pixel outside those regions
is byte-identical to the Japanese baseline.

## Palette and local checks

The graphics index identifies the source as PSMT8 in
`disc!/_DATA.YFS;1!/data/menu/title_new_tex.b`. Its 263,232-byte TXC has
SHA-256 `55b24160b8c3c56db4e02f8f2cd945594c5347c43685842d986a985427b556bb`.
`tools/rtx3.py import` mapped the English draft through that source's existing
PSMT8 palette without changing the TXC dimensions or palette. The imported TXC
is still 263,232 bytes (SHA-256
`531af0d45dd58cf327ff7d43549d5abdaf7b7752d79bc6faea970fbf6164367f`). Exporting
it again with `tools/rtx3.py export` produced a 512×512 TGA (SHA-256
`f117db14a888846cabe2bfcec020791245888187982faf58ef3c0d0daf849c8e`). Both the
authored image and palette-mapped re-export were inspected at native texture
scale; the title lettering and rotated credit line remain legible.

The local checks confirmed the source TGA hash and header are unchanged, the
English TGA retains the same 512×512 dimensions and header, and none of its
188,068 changed pixels are outside the four scoped edit regions. The TXC
import/export check demonstrates same-size PSMT8 palette compatibility only.
No shared graphics audit, graphics staging, ISO build/reparse, emulator test,
or in-game UV/display validation was run for this asset. The three title marks
could be alternate animation states or separate displayed layers; the texture
preview does not establish the final draw sequence or rule out repeated
branding. This is a localization draft, not runtime-validated artwork. See
[`TITLE_TEXTURE_RENDERING.md`](TITLE_TEXTURE_RENDERING.md) and
[`GRAPHIC_TEXT_LOCALIZATION.md`](GRAPHIC_TEXT_LOCALIZATION.md) for related title
and atlas evidence.
