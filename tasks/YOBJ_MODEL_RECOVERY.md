# YOBJ/YMP model format recovery

## Current result

The prepared archive catalog contains 899 direct `.ymp` resources totaling
197,085,308 bytes. Fourteen additional YMP members (1,007,280 bytes) occur
inside parsed UI bundles. `tools/yobj.py` parses all 913 resources and rebuilds
each byte-for-byte. The census counts the complete direct YMP envelopes in Z;
nested members remain counted once through their bounded UI-bundle extents.

The parser finds two prefix variants:

| Variant | Count | Observed prefix |
| --- | ---: | --- |
| Direct YOBJ | 912 | `YOBJ` at offset 0, including 14 nested members |
| DUMY-prefixed YOBJ | 1 | `DUMY\0\0\0\0YOBJ` |

The YOBJ header is a bounded 0x40-byte range after the four-byte magic and
length prefix. Its duplicate POF0 offset resolves to a `POF0` signature and
little-endian length whose extent ends exactly at EOF. The parser reads four
numeric count fields and four numeric offsets without assigning unverified
semantic labels. POF0 payload entries decode as increasing four-byte-aligned
pointer-slot offsets. Every slot lies before POF0, and each nonzero value points
inside the model envelope or exactly to the POF0 boundary. Across the corpus,
the parser audited 807,439 pointer slots: 803,754 direct and 3,685 nested.

One direct `basebone.ymp` uses the DUMY-prefixed header. Its POF0 payload has a
23-byte all-zero tail beyond the canonical encoded slot stream; the parser
preserves those bytes. The corpus total is 1,474 preserved POF0 zero-tail bytes
(1,449 direct plus 25 nested).

Representative pinned workspace samples:

| Logical path | Size | SHA-256 | Variant |
| --- | ---: | --- | --- |
| `disc!/_DATA.YFS;1!/data/bg/00.pac!/model.ymp` | 101,488 | `c558947bcd437bf90e6c5d865b489716aa8e1796b79c6c9a19c6b286d66a4943` | YOBJ |
| `disc!/_DATA.YFS;1!/data/common.dat!/basebone.ymp` | 6,592 | `ea2f1abe2bc8b1f6c193434ee06530df778ac2163fc33070996fb31c41f854f7` | DUMY/YOBJ |
| `disc!/_DATA.YFS;1!/data/chara/gnt_3g_de_1.pac!/model.ymp` | 468,864 | `947da7e07bf55ddbbad398f451ed9b130ddc88e3cc3e43233b6a55d616a2d7b0` | YOBJ |

## Use

```sh
python3 tools/yobj.py SOURCE.ymp --output-json EDITABLE.json
python3 tools/yobj.py --build-json EDITABLE.json --output REBUILT.ymp
```

The JSON separates prefix, fixed header, opaque model body, and POF0 bytes. The
builder accepts same-size edits when the header, POF0 bounds, decoded slots and
targets remain valid. It rejects growth. It does not regenerate POF0 or update
relocation fields after a shifted body.

## Limits and next work

The fixed record sizes or names for mesh, bone, texture/material, and object
structures have not been established from this game's executable or runtime.
Geometry, skinning, UVs, materials, and animation remain opaque. A POF0 pointer
slot list alone does not prove the engine's load-time fixup behavior or identify
every field that must change when a model grows. Do not treat the same-size raw
writer as a semantic model editor or claim safe internal relocation.

Next, correlate header counts, body records, and POF0 slot patterns with the
game's model-loading code; then produce a semantic model export/import path and
test growth through POF0, PAC, YFS, and the full ISO. The 333 YPC candidates
(3,539,860 bytes) are a separate unresolved format.

A community [YOBJ POF0 generator](https://github.com/rumblerosesxx/yobj_pof0_generator/blob/main/pof0gen.c)
provided a cross-format lead for delta coding. The local parser derives and
validates the variant used here directly against this game's YMP corpus; the
community source is not evidence of game provenance or runtime compatibility.
