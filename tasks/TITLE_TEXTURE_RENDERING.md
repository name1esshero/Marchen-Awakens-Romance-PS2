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
offset 64 and a 1,024-byte CLUT at offset 262,208. The stored-order diagnostic
(`tools/rtx3.py export --stored-order`) treats the pixel byte stream as linear
indices and reads the CLUT in stored order. It shows two vertically stacked
Japanese logo variants. This is direct evidence about byte interpretation, not
the texture's spatial layout in game. The normal legacy decode shows a repeated
atlas-like surface. The attempted generic GS page/block mapping produced a
more corrupted, striped image and was discarded; raw GS VRAM address layout is
therefore not established as the RTX3 payload layout.

The `title_00.at3` source is 4,548 bytes with SHA-256
`b9d5f2e26e57f51e6b936f55763de5b9618b47d652b2577c94d2812e5f1cb263`. Its
observed header fields are `3`, reference count `4`, and name-slot width `64`;
the reference table ends at `0x120`. The post-table region is 4,260 bytes with
SHA-256 `518d61e203eb5e87c18acbff6c1ae49377202e4e661e91be5fc5601bd3cd921a`.
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
rectangles have not yet been decoded. Next, correlate the AT records with the
`MarRectDrawTex` call sites, then compare the composition with an in-game capture
before editing art.

## Evidence limits

- Exact extraction and hash identity do not prove correct PSM decode or visual
  equivalence in the game.
- A recognizable stored-order preview does not prove the game samples bytes in
  that order; it only rules against accidental corruption before the TXC member.
- Disassembly evidence identifies a rectangle-to-GS draw path, but the register
  arguments, object fields, AT record fields, and title draw sequence are not
  fully named or recovered.
- No runtime capture has been made from this workspace.
