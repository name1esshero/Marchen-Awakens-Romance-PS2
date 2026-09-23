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

## Validated coordinate editing

`tools/yobj_geometry.py` adds a deliberately narrow, source-hash-bound JSON
representation for same-count mesh coordinate edits. Across all 913 direct and
nested resources, it validates 9,976 mesh records and 1,399,314 vertices. Each
mesh's vertex pointer is present in POF0; its target points to a VIF buffer whose
Vector4f `0x6c` command and count match the mesh descriptor. A second adjacent
Vector4f buffer has the same count. Every vector component is finite throughout
the corpus, and the fourth position/normal components consistently equal 1.0
and 0.0. These checks support treating the first three components of the paired
buffers as editable position and normal coordinates; the labels remain a local
format interpretation, not runtime-confirmed game semantics.

The editor exposes exactly 33,583,536 source bytes: six XYZ float components per
vertex (24 bytes). It preserves both W components and every other byte, requires
the original file hash and size, and rejects changed mesh/vertex counts or
non-finite/out-of-range floats. All 899 direct and 14 nested resources export
and rebuild to byte-identical no-ops. A synthetic edited model also passed
through UI bundle, BPE and PAC rebuilding and reparsed with its changed
coordinate. This is a fixed-size edit; it does not change vertex counts or
support model growth.

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
python3 tools/yobj_geometry.py SOURCE.ymp --output-json GEOMETRY.json
python3 tools/yobj_geometry.py SOURCE.ymp --build-json GEOMETRY.json --output EDITED.ymp
```

The JSON separates prefix, fixed header, opaque model body, and POF0 bytes. The
envelope builder accepts same-size edits when the header, POF0 bounds, decoded
slots and targets remain valid. The geometry builder patches only validated XYZ
components and likewise rejects growth. To insert a geometry edit, replace the
matching extracted `.ymp` member sidecar with the geometry builder output, then
run the usual asset build; the member rebuilds through its UI bundle/BPE/PAC
parents. The container builder may relocate or grow those parents, but no model
body growth or runtime pointer-fixup behavior is established.

## Limits and next work

The coordinate arrays are now editable, but topology/face indices, UVs, object
data, skinning, materials, animation, and most mesh/bone records remain opaque.
A POF0 pointer-slot list alone does not prove the engine's load-time fixup
behavior or identify every field that must change when a model grows. Do not
claim safe internal growth, shiftability, visual correctness or runtime
acceptance. The 333 YPC candidates (3,539,860 bytes) are a separate unresolved
format.

Next, validate coordinate interpretation against the model draw path or a
runtime render, then recover topology/UVs and determine which POF0 references
the loader rebases. Extend the same-count editor only when each new field has
bounded corpus evidence, and test internal growth separately through POF0,
PAC, YFS and the full ISO.

A community [YOBJ POF0 generator](https://github.com/rumblerosesxx/yobj_pof0_generator/blob/main/pof0gen.c)
provided a cross-format lead for delta coding. The local parser derives and
validates the variant used here directly against this game's YMP corpus; the
community source is not evidence of game provenance or runtime compatibility.
