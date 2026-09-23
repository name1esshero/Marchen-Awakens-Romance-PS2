# Title texture and renderer evidence

Updated: 2026-09-23. This note records candidates and measurements; it does not
claim an in-game render reconstruction.

## Texture extraction and views

The `title_tex.b` asset is BPE-compressed. Its decoded resource bundle has a
32-byte resource table and a `title_marh_jp` TXC member at offset 526,608, size
263,232. The span in `extracted/assets/00039.asset/01566.decoded.bin` hashes to
`b67db2f3a834c05de583c3dbd360da3208384c4234072f0ed66b58711dcfc375`, matching
`01566.bundle.json`. This establishes exact wrapper and member extraction for
this texture.

The TXC has RTX3 magic, PSMT8 mode, 512x512 dimensions, 262,144 pixel bytes at
offset 64 and a 1,024-byte CLUT at offset 262,208. The current export leaves
pixel indices linear, applies the PSMT8 CLUT index permutation, and expands
palette alpha from the PS2 GS 0..128 range to TGA's 0..255 range. The owner
selected this mapped-linear view, which displays gray and colorful Japanese
logo variants vertically stacked and matches the supplied reference image.
`--stored-order` remains a diagnostic that leaves the CLUT in raw order and
does not expand alpha. A controlled matrix across ten PSMT8 and ten PSMT4
resources favored linear pixel indexing over the old pixel-unswizzle output;
the selected title image provides the CLUT-order reference. See
`reports/rtx3_layout_diagnostics.json` for the sample paths and hashes. The
editable baseline is `graphics/title/00039_01566_0002_title_marh_jp.tga`; its
localized sibling is `graphics/title/00039_01566_0002_title_marh_eng.tga`. Keep the
Japanese baseline unchanged and put localization edits in the English sibling.

The initial exported TGA alpha was wrong for display: it copied the PS2's
0..128 alpha values into an 8-bit image channel unchanged, making opaque pixels
look half transparent. The corrected conversion doubles those values, keeping
0 transparent and mapping 128 to 255. This preserves antialiased intermediate
alpha values. The texture is still an atlas surface; this choice does not
establish how the game crops or samples it. The old GS pixel-unswizzle result
was visibly tiled/garbled and is not the current output.

The `title_00.at3` source is 4,548 bytes with SHA-256
`b9d5f2e26e57f51e6b936f55763de5b9618b47d652b2577c94d2812e5f1cb263`. Its
observed header fields are `3`, reference count `4`, and name-slot width `64`;
the reference table ends at `0x120`. The post-table region is 4,260 bytes with
SHA-256 `518d61e203eb5e87c18acbff6ca87cd81742d0655ecad8977872462c419af71f`.
It contains a 16-byte preamble and nine validated node envelopes ending at EOF.
Each node is a 64-byte name slot followed by 192 fixed opaque bytes and zero or
more 112-byte opaque blocks. The envelope and raw regions round-trip exactly;
the hashes pin the evidence sample without claiming meanings for its animation
properties.

## Renderer observations

The `MarTitleMenu` vtable is at ELF address `0x003ddc48`; its Display override
at `0x00249b5c` calls `0x00248e90` when its state field at object offset `0x5c`
is nonzero. This override alone does not expose title texture UVs. The
`MarRectDrawTex` vtable at `0x003de080` points to methods including
`0x00247260`, `0x00247314`, and `0x002473a0`. Disassembly of these routines
shows rectangle coordinates converted to four corners and passed to the GS
draw path; coordinates are scaled by 16 (`0x41800000`) in one conversion.
Interpreting all object fields and their source animation records remains open.

The companion `title_at.b` has an `AT  ` member with four `.tga` references.
`tools/at3.py` reads its 16-byte header as observed fields and validates four
64-byte CP932 name slots, each followed by a 4-byte uninterpreted value. The
names begin at offsets `0x10`, `0x54`, `0x98`, and `0xdc`; following values are
`64`, `64`, `64`, and `0`. All four name stems (`title_parts`, `title_mar`,
`title_marh_jp`, `title_bg`) match TXC member names in the sibling bundle
manifest. This proves reference-to-texture name linkage, not that `.tga` files
exist as separate image files or how the animation samples those textures.
The title node record starts and sizes are: `BG` (`0x130`, 484 bytes), `MAR`
(`0x314`, 372), `Layer02` (`0x488`, 708), `Layer03` (`0x74c`, 484), `Layer04`
(`0x930`, 484), `Layer05` (`0xb14`, 484), `Scene01` (`0xcf8`, 484), `Layer07`
(`0xedc`, 484), and `Scene00` (`0x10c0`, 260). Their sizes follow
`260 + 112*n`; the fixed and repeated data remain raw.

Several 32-bit floats in the title body are exact 1/512 multiples near atlas
alpha-region boundaries: `0.443359375` (`227/512`) repeats at `0x67c` through
`0x6ac`; `0.4453125` (`228/512`) at `0x888` through `0x8a0`; `0.888671875`
(`455/512`) at `0x8b0` through `0x8c8`; and `0.890625` (`456/512`) at `0xa6c`
through `0xa84`. These are UV candidates, not decoded field meanings. The
reusable parser now segments all 723 direct AT3 leaves and 1,605 nested UI-bundle
AT3 members (26,798 node envelopes), and its bounded writer round-trips all of
them byte-exactly. It rejects node growth and does not claim relocation safety.

A first English title-parts draft is inserted into the existing title atlas; it
changes only language-bearing regions and preserves the canvas and palette.
Correlate the candidate values with the `MarRectDrawTex` call sites and compare
the composition with an in-game capture before treating the wording or
presentation as final.

## English title-parts draft and insertion evidence

`graphics/title/00039_01566_0003_title_parts_jp.tga` remains the immutable
Japanese source (SHA-256
`b835f80dca0628a81645defa2dc91359c462d6113f6ef514741328a3a294253f`). Its
same-size English sibling,
`graphics/title/00039_01566_0003_title_parts_eng.tga` (SHA-256
`f80b19f2d596f75b82701ee62451312c3ea1da7df6f021fa6bfe142accd138cb`), is a
reviewable draft. It renders `メルヘヴン アームファイトドリーム` as “MÄR Heaven
ÄRM Fight Dream” and `© 安西信行 / 小学館 ・ ShoPro ・ TV Tokyo` as “© Nobuyuki
Anzai / Shogakukan • ShoPro • TV Tokyo.” Existing “PRESS START BUTTON,”
“MÄRCHEN AWAKENS ROMANCE,” and “© KONAMI” artwork is preserved. The title
wording is a draft translation of
the Japanese product title listed by [Famitsu](https://www.famitsu.com/game/title/6849/page/1),
using the accented MÄR/ÄRM spelling from [VIZ's MÄR series](https://www.viz.com/mar);
it is not presented as an official English release title. The raster uses DejaVu
Sans bold/italic lettering, antialiased and mapped into the original palette. No
Japanese baseline pixels were changed.

The source TXC hash is
`f18d908d8201b2433973fb03937748706f3504a80d2d573846ac1f02bfb54f2a`; the
same-size imported TXC hash is
`dacbf57c36ab281eb1ebc2fd1a205421fdeee2dea77bb703aa11343d3a8e42a0` (132,160
bytes). The graphics audit passed across all 30,397 indexed resources: 30,354
editable exports, 43 unresolved records, zero changed Japanese baselines, and
two English overrides. The title bundle was rebuilt through BPE and the four-entry
UI resource table. The mod ISO reparse contains the exact staged English
title-parts TXC bytes.

The unchanged bundle decoded size is 922,000 bytes, but the observed BPE writer
uses a literal identity table: the rebuilt `title_tex.b` grows from 301,071 to
922,091 bytes. Relocation succeeds, but this is a substantial compression loss.
The current combined mod ISO is 5,017,673,728 bytes (SHA-256
`baa8c68a3b4e27d359d0692947239e1a6b4261a8a69f83801f9259db56d2a89e`). The three
catalog-applied text resources and both English title TXCs reparse byte-exactly
from a fresh ISO export. Their text sizes are 20,700 bytes (`_msg.dat`), 14,152
bytes (`CardList.txt`) and 3,319 bytes (`DataBase.txt`). The pinned-reference
comparison authenticates the baserom and records 752,229,873 differing bytes in
[`reports/title_graphics_mod_compare.json`](../reports/title_graphics_mod_compare.json).
These are static packaging checks. Neither title atlas has passed emulator
review; the main wordmark may repeat the existing “MÄR HEAVEN” mark elsewhere
on-screen, and the AT/UV draw composition has not been reconstructed.

## English main-wordmark draft and insertion evidence

`graphics/title/00039_01566_0002_title_marh_jp.tga` remains the unchanged
Japanese baseline (SHA-256
`e72a760fccf45ba7ab71d18e2b5f3c865a74cf9e827e6a93d37a619d2625052c`). Its
same-size English sibling
`graphics/title/00039_01566_0002_title_marh_eng.tga` (SHA-256
`528d758732c3bffa9f5aad5c97d1a0bc556039afdf499b263cd90e155ed55f85`) is a draft.
It reuses the native “MÄR HEAVEN” lettering from
`00039_01565_0003_sbttl_jp.tga` (SHA-256
`0f0f115297c76f02407e1ae0f2b299b6190e775ea021c633e58ee07de74bcc89`), removes
the Japanese subtitle embedded beneath that lettering, places a grayscale copy
in the upper logo region and a color copy in the lower region, and preserves
the separate registered-mark artwork. The 512x512 canvas and original palette
remain unchanged.

The original main-logo TXC remains SHA-256
`b67db2f3a834c05de583c3dbd360da3208384c4234072f0ed66b58711dcfc375`; the
palette-mapped English TXC is 263,232 bytes with SHA-256
`e974f1ee39f60732fc500ad8ee663f837b98866e0e141127f06332784aa81e66`. A fresh
export of `mar_eng.iso` reparsed this exact TXC through ISO/YFS/BPE/UI-table
layers and matched the staged override byte-for-byte. The full graphics audit
reported 30,397 indexed resources, 30,354 editable images, 43 unresolved
records, zero changed Japanese baselines and two English overrides. The full
mod image comparison authenticated the pinned Japanese reference and recorded
the current output hash above.

This is a reusable-art draft, not runtime evidence of placement or scale. The
existing title screen already draws English “MÄR HEAVEN” artwork from a sibling
texture, so repeated branding is possible. The title animation body and UV
rectangles still need decoding, and no emulator capture has been reviewed.

## Evidence limits

- Exact extraction and hash identity do not prove correct PSM decode or visual
  equivalence in the game.
- A human-selected mapped-linear preview supports a candidate texture
  representation, but does not prove runtime UV selection or final composition.
- Disassembly evidence identifies a rectangle-to-GS draw path, but the register
  arguments, object fields, AT record fields, and title draw sequence are not
  fully named or recovered.
- The 20-resource visual sample is not the entire RTX3 corpus. The current
  workspace has 30,354 editable TGA exports across standalone and nested TXCs;
  43 malformed-length PSMCT32 candidates remain raw. Corpus-wide visual/runtime
  correctness is not established by the audit.
- No runtime capture has been made from this workspace.
