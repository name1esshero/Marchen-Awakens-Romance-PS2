# `TGS_menu_tex.b` coming-soon texture text audit

## Scope and method

This read-only audit covers the sole `user_interface` row in
`graphics/index.json` whose `asset_path` is exactly
`disc!/_DATA.YFS;1!/data/menu/TGS_menu_tex.b`. The exported Japanese baseline
was alpha-composited against light and dark temporary backgrounds and reviewed
at native and nearest-neighbor enlarged scales. Text bounds below use pixels
with alpha at least 128 and source RGB above 10; they use upper-left origin and
half-open intervals. They describe visible image content, not UVs or screen
placement.

The row maps to `graphics/user_interface/00039_01559_0002_comingsoon_jp.tga`,
512×256, full-file SHA-256
`e02c451473e618a962910c8eded66c9851d8f0cba67b8180f01da53ac5268ae8`. It is an
uncompressed true-color TGA (image type 2), with no color map, 32 bits per
pixel, top-origin descriptor `0x28`, and an exact 524,306-byte extent
(`18 + 512 × 256 × 4`). These values match the index row and file header.

## Visual finding

The transparent texture contains two clear, pale lime-green Japanese message
lines with dark edging:

| Source text | Approximate English sense | Visible bounds |
| --- | --- | --- |
| `1月3日まで!!` | “Until January 3!!” | `[97,416) × [9,50)` |
| `あと3日間!!` | “3 days remaining!!” | `[128,376) × [67,108)` |

Two much softer, diffuse repetitions appear below the crisp lettering, around
`[92,421) × [130,182)` and `[123,381) × [188,240)` when measured at alpha 16.
They resemble low-opacity echoes or shadows of the same two lines rather than
additional legible messages; their exact display role is unknown. The source
is therefore a confirmed Japanese text-bearing promo surface, with the lower
soft copies retained as a localization consideration rather than separate
transcriptions.

## Findings and limits

This one-row audit confirms that `comingsoon` needs an English counterpart if
the game’s localized menu is intended to replace Japanese promo lettering.
The baseline was not edited and no override was created. Static raster review
does not establish whether the dated message is still relevant, which UI state
uses it, its UVs or draw order, or how the low-opacity repeats appear in-game.
No ISO build, emulator, or runtime validation was performed.

References: `graphics/index.json`,
[`localization methodology`](../docs/LOCALIZATION_METHODOLOGY.md), and
[`TGA export/import methodology`](../docs/TASK_ASSET_WORKSPACE_METHODOLOGY.md).
