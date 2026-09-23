# Byte-weighted asset recovery census

Evidence date: 2026-09-23

Pinned reference SHA-256: `cc059a3acf818dfbd0a782a9d20ee67e020d167866cd1c4dca77e6eb9224e3ec`

## Physical disc accounting

**Disc image:** 4.59 GB (4,587,749,376 bytes).

These disjoint physical spans sum to the image size:

| Physical span | Bytes | Share of image |
| --- | ---: | ---: |
| All-zero named members | 3,324,768,000 | 72.4706% |
| All-zero gaps | 2,527,881 | 0.0551% |
| Information-bearing terminal members | 1,237,522,725 | 26.9745% |
| Nonzero unassigned gaps/structure | 22,930,770 | 0.4998% |

Measured all-zero bytes total 3.33 GB (3,327,295,881 bytes) (72.5257% of the image). **Intentional zero/padding: not established.** Zero contents alone do not prove the spans were padding or placeholders.

## Recovery levels

**Expanded information-bearing payload Y:** 1.30 GB (1,303,947,016 bytes) (28.4224% of the physical image). Compressed BPE wrappers are replaced by their decoded member payloads once; bundle control and gap bytes are excluded.

| Measure | Covered bytes / denominator | Coverage | Evidence represented |
| --- | ---: | ---: | --- |
| Container hierarchy addressed | 1,237,522,725 / 1,237,522,725 physical member bytes | 100.0000% | Named path and validated parent extent; separate from Y |
| Structurally classified Z/Y | 1,132,030,822 / 1,303,947,016 | 86.8157% | Parser-backed records or bounded extents |
| Losslessly rebuildable A/Y | 1,303,947,016 / 1,303,947,016 | 100.0000% | Authenticated unchanged-input rebuild |
| Semantically editable B/Y | 888,328,887 / 1,303,947,016 | 68.1261% | Editable source representation and insertion path |
| Runtime-validated editable C/Y | 0 / 1,303,947,016 | 0.0000% | Edited payload passed in-game runtime validation |

These are independent evidence levels, not a combined decompilation or translation percentage. In particular, B measures available editable representations, not how much content has been translated.

### Editable source bytes counted in B

| Editable source surface | Source bytes | Share of Y |
| --- | ---: | ---: |
| Editable texture source bytes | 239,444,320 | 18.3630% |
| Reversible text companions | 68,042 | 0.0052% |
| Structured message catalog | 20,452 | 0.0016% |
| YOBJ position/normal XYZ fields | 33,583,536 | 2.5755% |
| MPEG-2 video elementary streams | 615,212,537 | 47.1808% |

## Remaining payload, with denominators kept separate

**Full non-editable queue Y-B:** 0.42 GB (415,618,129 bytes) (31.8739% of Y). It includes both structurally classified but non-editable bytes and structurally unclassified bytes.

Structurally classified but not semantically editable Z-B: 243,701,935 bytes (18.6896% of Y).

| Y-B inventory class | Bytes | Share of Y-B | Share of Y | Catalog records |
| --- | ---: | ---: | ---: | ---: |
| Audio/sound candidates | 216,096,336 | 51.9940% | 16.5725% | 153 |
| Model/geometry candidates | 168,048,912 | 40.4335% | 12.8877% | 1,246 |
| Animation/motion candidates | 12,552,248 | 3.0201% | 0.9626% | 2,430 |
| Video container/packetization | 10,256,065 | 2.4677% | 0.7865% | 13 |
| Executables/modules | 4,101,870 | 0.9869% | 0.3146% | 16 |
| Other unclassified | 2,644,996 | 0.6364% | 0.2028% | 2,253 |
| Font assets | 896,928 | 0.2158% | 0.0688% | 2 |
| Scripts/event/data candidates | 880,126 | 0.2118% | 0.0675% | 319 |
| Unresolved graphics | 140,648 | 0.0338% | 0.0108% | 43 |

**Strictly structurally unclassified queue Y-Z:** 0.17 GB (171,916,194 bytes) (13.1843% of Y). This is not a measure of every opaque field: a structurally bounded record may still contain uninterpreted data.

| Y-Z inventory class | Bytes | Share of Y-Z | Share of Y | Catalog records |
| --- | ---: | ---: | ---: | ---: |
| Audio/sound candidates | 156,453,642 | 91.0058% | 11.9985% | 140 |
| Executables/modules | 4,101,870 | 2.3860% | 0.3146% | 16 |
| Animation/motion candidates | 3,731,880 | 2.1708% | 0.2862% | 102 |
| Model/geometry candidates | 3,539,860 | 2.0591% | 0.2715% | 333 |
| Other unclassified | 2,184,740 | 1.2708% | 0.1675% | 2,246 |
| Font assets | 896,928 | 0.5217% | 0.0688% | 2 |
| Scripts/event/data candidates | 866,626 | 0.5041% | 0.0665% | 318 |
| Unresolved graphics | 140,648 | 0.0818% | 0.0108% | 43 |

Category names are evidence-led inventory labels based on parsed signatures, member types, extensions, or paths. They do not claim semantic decoding of every listed payload.
