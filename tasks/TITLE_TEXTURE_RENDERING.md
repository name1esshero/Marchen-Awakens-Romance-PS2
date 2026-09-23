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

## Renderer observations

The `MarTitleMenu` vtable is at ELF address `0x003ddc48`; its Display override
at `0x00249b5c` calls `0x00248e90` when its state field at object offset `0x5c`
is nonzero. This override alone does not expose title texture UVs. The
`MarRectDrawTex` vtable at `0x003de080` points to methods including
`0x00247260`, `0x00247314`, and `0x002473a0`. Disassembly of these routines
shows rectangle coordinates converted to four corners and passed to the GS
draw path; coordinates are scaled by 16 (`0x41800000`) in one conversion.
Interpreting all object fields and their source animation records remains open.

The companion `title_at.b` has an `AT  ` member with four `.tga` references,
including `title_marh_jp.tga`. Its entry-field semantics and the mapping from
those references to RTX3 UV rectangles have not yet been proven. Next, correlate
the AT records with the `MarRectDrawTex` call sites and the matching TXC atlas,
then compare the composed result with an in-game capture before editing art.

## Evidence limits

- Exact extraction and hash identity do not prove correct PSM decode or visual
  equivalence in the game.
- A recognizable stored-order preview does not prove the game samples bytes in
  that order; it only rules against accidental corruption before the TXC member.
- Disassembly evidence identifies a rectangle-to-GS draw path, but the register
  arguments, object fields, AT record fields, and title draw sequence are not
  fully named or recovered.
- No runtime capture has been made from this workspace.
