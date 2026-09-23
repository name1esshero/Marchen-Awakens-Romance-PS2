# Title-screen `title000` English texture

Updated: 2026-09-23.

## Surface and translation

The standalone TXC is `standalone:/00039.asset/00985.asset/00000.bin`, at
`disc!/_DATA.YFS;1!/data/menu/esy_menu.tex!/title000.txc`. It is PSMT8, 512x512,
and 263,232 bytes. Its SHA-256 is
`cfc91c5f6539f0240790c4ed2086d77ec4c853b309227461be5699e7dfadd15b`.
The recovered Japanese TGA baseline is 1,048,594 bytes, SHA-256
`19b66cfa3f6c69717e0250cca8c0cd89e5e195dfb2ecd3279d9f3ff4b34365e6`; it remains
unchanged.

The title mark is rendered as `MÄR HEAVEN` using the existing English lettering
from `graphics/title/00039_01566_0002_title_marh_eng.tga`. The tagline
`MÄRCHEN AWAKENS ROMANCE`, the `PRESS START BUTTON` prompt, and `© 2005 KONAMI`
were already English and remain. The Japanese author/publisher line was changed
to `© Nobuyuki Anzai / Shogakukan • ShoPro • TV Tokyo`, reusing lettering from
`graphics/title/00039_01566_0003_title_parts_eng.tga`.

The title-mark area `[88,0)-[403,123)` was cleared and filled with the existing
English title-mark crop `[32,263)-[478,421)`, resized to 306x108 at `(93,6)`.
The credit lettering crop `[44,203)-[469,219)` was resized to 344x16, colored to
the source line's light gray while retaining antialiasing, and placed at `(8,433)`.
The canvas and source PSMT8 palette are retained. The `_jp.tga` remains the
recovered baseline; localization is only in the `_eng.tga` sibling.

## Verification and limits

The English TGA is 512x512, 1,048,594 bytes, SHA-256
`6851419b7b8db356435faa80dc7fba3536a695e9d2d2a51acc9dab11a3efa5bc`. Static
preview review confirms the reused English wordmark and translated credit are
legible in their texture regions. Comparing decoded source and output rasters
found 32,701 changed pixels, all inside the two edit rectangles above. RTX3
import preserves the original 64-byte header and all 1,024 palette bytes; the
resulting TXC remains 263,232 bytes and has SHA-256
`fbe2ee68108ba7bd4455f415c6bb86ace5b2988b401793c57679319abb658911`. Importing
the final TGA again produces byte-identical TXC output, and exporting that TXC
reproduces the English TGA byte-for-byte.

This verifies static texture editing and same-palette conversion. The texture's
runtime UV rectangle, on-screen placement, composition, and in-game readability
have not been validated. No ISO build or emulator test was performed for this
isolated asset task.

References: `tools/rtx3.py`,
[`LOCALIZATION_METHODOLOGY.md`](../docs/LOCALIZATION_METHODOLOGY.md),
[`TITLE_TEXTURE_RENDERING.md`](TITLE_TEXTURE_RENDERING.md),
[`GRAPHIC_TEXT_LOCALIZATION.md`](GRAPHIC_TEXT_LOCALIZATION.md).
