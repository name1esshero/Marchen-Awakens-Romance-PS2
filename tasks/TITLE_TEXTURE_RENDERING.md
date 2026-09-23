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
These hashes pin the evidence sample without claiming meanings for the opaque
animation records.

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
The remaining animation body and mapping from the references to RTX3 UV
rectangles have not yet been decoded. A first English title-parts draft is now
inserted into the existing title atlas; it changes only language-bearing regions
and preserves the canvas and palette. Correlate the AT records with the
`MarRectDrawTex` call sites and compare the composition with an in-game capture
before treating the wording or presentation as final.

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
one English override. The title bundle was rebuilt through BPE and the four-entry
UI resource table. The final `mar_eng.iso` reparses through ISO/YFS/BPE/UI-table
layers and contains the exact staged English TXC bytes.

The unchanged bundle decoded size is 922,000 bytes, but the observed BPE writer
uses a literal identity table: the rebuilt `title_tex.b` grows from 301,071 to
922,091 bytes. Relocation succeeds, but this is a substantial compression loss.
The final mod ISO is 5,017,673,728 bytes (SHA-256
`4853c7a12799f52074a698ae5483a2def15178df741d81081d171e0d59be7c63`), inventories
as 42 files, and all four edited resources (`_msg.dat`, `CardList.txt`,
`DataBase.txt`, and `title_parts`) reparse exactly. The pinned-reference
comparison authenticates the baserom and records 752,229,873 differing bytes in
[`reports/title_graphics_mod_compare.json`](../reports/title_graphics_mod_compare.json).
These are static packaging checks; the title has not been rendered in an
emulator, and the typography remains a draft pending visual review. This only
localizes the title-parts atlas; the prominent `title_marh_jp` Japanese wordmark
is still untranslated, so the title screen is not yet fully localized.

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
