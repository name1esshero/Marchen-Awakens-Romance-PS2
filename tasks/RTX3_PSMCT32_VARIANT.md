# RTX3 PSMCT32 length variant investigation

Updated: 2026-09-23. Scope: the 43 PSM=0 RTX3 records indexed from the pinned
disc. This investigation is read-only; it changes no parser behavior and emits
no guessed images.

## Corpus measurements

Every indexed source hash was checked against its extracted bytes. All 43
records agree with the RTX3 header's own declared file size (`file_size - 8`),
and their PSM and power-of-two dimensions agree with the observed GS TEX0 PSM,
TW and TH fields. The header's `pixel_size` is `width * height * 4` in each
case, while the file contains eight fewer bytes after its 64-byte header.
There is no palette for PSMCT32.

| Records | Dimensions | File bytes | Header pixel bytes | Stored bytes after 64-byte header | Shortfall | Unique payload SHA-256 |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 28 | 8×8 | 312 | 256 | 248 | 8 | `e55ac2ced9c9bf64a2ea81e0d09d80c2e5ff2b1f0684953e859132adf3c626b8` |
| 14 | 32×64 | 8,248 | 8,192 | 8,184 | 8 | `400e44ad12bc16897868f2a97ac93d0fd080676ecdf6a2ce203811d54730baab` |
| 1 | 64×64 | 16,440 | 16,384 | 16,376 | 8 | `ece9dd384bf8e289e991c24b7dc191743c3192245e8675dfd673b01d6d2f3016` |

The three sample logical paths are:

- `disc!/_DATA.YFS;1!/data/chara/snw_1g_de_1.pac!/tex.pac!/arm.txc` (8×8)
- `disc!/_DATA.YFS;1!/data/chara/alv_3g_de_1.pac!/tex.pac!/hana.txc` (32×64)
- `disc!/_DATA.YFS;1!/data/bg/ic.pac!/tex.pac!/smoke2.txc` (64×64)

The 43 references account for 140,648 bytes including repeats; the three
distinct payloads account for 25,000 bytes. `tools/rtx3.parse` rejects all
three with `RTX3 length does not match header, palette and pixel extents`.
The source index and format survey also identify all 43 as unresolved and emit
no TGA; see `graphics/index.json` and `reports/rtx3_format_survey.json`.

## What the evidence supports

The repeated deficit is present across three distinct payloads and three
dimensions, so it is a stable corpus observation rather than one isolated
length anomaly. It does not identify why eight bytes are absent. The declared
size field is internally consistent with each actual file, which rules out a
stale declared-size value as the explanation. The header's pixel-byte count,
however, describes a larger extent than the bytes available after the header.

The existing `_unswizzle32` implementation further limits what can be tested
with its current geometry: 8×8 and 32×64 do not meet its 64-pixel width and
32-row page predicates; 64×64 meets those geometry predicates but still lacks
eight bytes and fails strict parsing first. Those implementation constraints
are not proof that the source records are malformed or that the game uses that
swizzle for all three sizes.

Plausible explanations such as an RTX3 variant, an omitted/truncated tail, or
a representation whose declared allocation differs from stored payload remain
unresolved. The bytes provide no independent boundary or marker that would
justify identifying a particular eight-byte trailer or restoring pixel data.
No image was padded, trimmed, shifted, or decoded, and no Japanese baseline was
modified. Do not promote these records to editable rasters from this evidence.

## Next evidence needed

Resolution requires an independent PSMCT32 RTX3 sample accepted by a known
producer/decoder, a trace of the game's loader or texture upload showing the
actual data extent and transfer dimensions, or another independent parser
that explains the same header/body relationship. Until then preserve all 43
payloads raw and keep them outside editable-TGA coverage.
