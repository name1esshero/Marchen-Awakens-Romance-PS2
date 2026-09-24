# War-close texture text audit

## Scope and method

This read-only audit covers the single `user_interface` row in
`graphics/index.json` whose `asset_path` is exactly
`disc!/_DATA.YFS;1!/data/menu/war_close_tex.b`. I reviewed the exported
Japanese-baseline TGA visually at native size and with a nearest-neighbor
alpha-composited enlargement. No Japanese baseline, English override, index,
queue, or status file was changed.

| Bundle | Resource | Japanese-baseline TGA | PSM | Dimensions | Indexed source SHA-256 | TGA full-file SHA-256 |
| --- | --- | --- | --- | ---: | --- | --- |
| `war_close_tex.b` | `0000_sel_frame.txc.bin` (`sel_frame`) | `00039_01602_0000_sel_frame_jp.tga` | PSMT4 (`20`) | 32×32 | `76af114b8e9f89a5e2c91a689f534c3c6901fdcd26c8d14d59deb0ddd91a466d` | `0591f3cd7ce8612b6e27ee2da5174a869f034653ef00a580515dddd39178803f` |

The source digest above is the value recorded in `graphics/index.json`; the
source TXC is not present at its extracted resource path in this worktree, so
that digest was not independently recomputed. The TGA digest was recomputed
from the tracked image and matches the index.

## TGA structure and visual finding

The TGA is 4,114 bytes. Its complete 18-byte header is
`000002000000000000000000200020002028`: no image ID or color map, uncompressed
true-color image type 2, 32×32 pixels, 32 bits per pixel, top-left origin and
descriptor `0x28`. The expected extent is `18 + 32 × 32 × 4 = 4,114` bytes,
exactly the observed file length.

The image is a pale, thin square frame/border with a transparent center. Its
nonzero-alpha artwork spans `[0,32) × [0,32)`; 664 of 1,024 pixels have zero
alpha. I found no visible Japanese or Latin wording, symbols that read as
text, or other translation-bearing marks, so there are no text bounds to
record. The name `sel_frame` is consistent with the visible frame shape but
does not establish where or how the game displays it.

## Verification and limits

The exact path/category filter returned one index row. The indexed dimensions,
source and image hashes, and PSM agree with that row; the TGA SHA-256 was
recomputed, and the header and exact extent were checked. The image was
visually reviewed at native size and in an enlarged alpha-composited preview.
No bundle rebuild, UV inspection, runtime test, ISO build, or emulator test was
performed. The source TXC digest remains an index-recorded value rather than a
locally rehashed source-file result.

References: `graphics/index.json`,
[`localization methodology`](../docs/LOCALIZATION_METHODOLOGY.md), and the
war-selection frame findings in
[`GRAPHIC_TEXT_REMAINING_MENU_TEX.md`](GRAPHIC_TEXT_REMAINING_MENU_TEX.md).
