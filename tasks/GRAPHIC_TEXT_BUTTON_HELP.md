# Button-help graphics localization evidence

Updated: 2026-09-23.

## Source and wording

`graphics/backgrounds/00039_00991_0030_btnhlptxt_jp.tga` is the 128×64
button-help texture from `disc!/_DATA.YFS;1!/data/menu/Laby_BG_tex.b`. Its
source member is
`00039.asset/00991.resources/0030_btnhlptxt.txc.bin`, a 4,224-byte PSMT4 RTX3
texture. The TXC SHA-256 is
`c450833f1f1dcc3f80d204da27fbf8af078b8fe5f019b44ed8da34783c599d8b`. The
Japanese baseline TGA remains unchanged at SHA-256
`f8ce181acf8a5e3bab090c564f5cc5e50d36075c0f85014387c27cf02d69ce3f`.

The three visible labels read `十字キー` → `D-PAD`, `右スティック` →
`RIGHT STICK`, and `左スティック` → `LEFT STICK`. The message catalogue's
movement tutorials translate `方向キー` as “D-pad” and use “left stick” for
`左スティック`; the short `十字キー` label is rendered as the same control
name. The right-stick reading is visually confirmed in the texture. The
separate button-like pictogram at approximately `[82,102)×[23,43)` is retained
without assigning it a more specific identity.

Direct alpha inspection gives lettering bounds `[3,62)×[0,20)`,
`[2,80)×[23,42)`, and `[1,80)×[45,63)`. The separate middle pictogram occupies
`[82,103)×[23,43)` and is left unchanged. The earlier background-corpus row
lists the first label as `[2,20)`, which does not match the measured source
pixels; this task uses the measured `[3,62)` extent. No texture runtime or UV
mapping is inferred from these flat-image bounds.

## English artwork

The English sibling is
`graphics/backgrounds/00039_00991_0030_btnhlptxt_eng.tga`, SHA-256
`182bca89c71042ea46b75292379ebdeecdcf38ca20f0bb34f2f884b56f70f3fa`. It
keeps the 128×64 canvas and TGA header. The short Latin labels use glyphs from
the game's 128×128, 8×16 ASCII atlas
`graphics/text/00039_00825_font_jp.tga` (SHA-256
`069387c9d76ca200b576cdb59e095960cf717378a13c56016b7bf4e1bebbebb8`). The
atlas tint was converted to neutral grayscale and mapped through colors already
present in the target texture palette. `RIGHT STICK` fits in the horizontal
lane immediately before the preserved pictogram: its changed-pixel extent ends
at x=82, where the unchanged pictogram begins. The other labels are centered in
their measured bands. The Japanese TGA remains the source baseline.
The 0-based 8×16 glyph cells are A–P on atlas row 1, Q–Z on row 2, and hyphen
at row 5, column 6; each output character was visually checked against its
source cell before placement.

The English TGA is 32,786 bytes; importing it produced a 4,224-byte TXC with
SHA-256 `2affe5aa6690f2de0884e0ffac7892e2ef01829a22fc2566f5a9b360f4c212b7`.

One image-generation edit was rejected: it returned a 1774×887 composition,
redrew the full texture rather than preserving its small layout, and omitted
the separate pictogram. That output was not imported. The final English sibling
uses native atlas glyphs and the existing RTX3 palette importer instead.

## Verification and limits

`python3 tools/rtx3.py export` reproduced the Japanese TGA byte-for-byte from
the source TXC. `python3 tools/rtx3.py import` accepted the English TGA and
produced a 4,224-byte PSMT4 TXC with the source's 64-byte header and 64-byte
palette unchanged; exporting that TXC reproduced the English TGA byte-for-byte.
The final raster was reviewed at native and 4× nearest-neighbor scale. A pixel
comparison found changes only in the three lettering bands, with the middle
pictogram unchanged; the English middle label's changed pixels end at x=82,
and none overlap the pictogram. The Japanese source hash still matches the
catalogue.

No enclosing BPE/UI bundle was rebuilt, and no ISO build, ISO reparse, emulator,
or runtime/UV validation was performed. The successful evidence here is limited
to same-size TGA editing and standalone PSMT4 import/export.
