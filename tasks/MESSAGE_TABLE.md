# `_msg.dat` message-table evidence

Authority: [STANDARDS.md](../docs/STANDARDS.md),
[asset workspace methodology](../docs/TASK_ASSET_WORKSPACE_METHODOLOGY.md).
Evidence date: 2026-09-22.

## Candidate and observed layout

Logical path: `disc!/_DATA.YFS;1!/data/common.pac!/_msg.dat`.
Workspace raw leaf: `extracted/assets/00039.asset/00001.asset/00015.bin`.
Size: 20,452 bytes. Exported member SHA-256:
`0a9f5da3da31ce313523ab3f0591583669a9cb48146a3e4a91b04e3a5edd85cb`.

Direct parsing found 229 monotonically ordered records. Each record contains
three little-endian 32-bit values at byte 8 plus `12 * index`: `kind`, `key`,
and a string offset relative to byte 8. The first string begins immediately after
the record table. Each string is CP932 and ends at its single NUL terminator;
the next record offset marks the next string. The observed file has no gap between
the table and strings or between strings. All observed strings decode strictly as
CP932, and offsets stay inside the 20,452-byte member.

These are field-shape names, not recovered semantic types. One `_msg.dat` sample
proves only that this parser contract applies to that file. Other `.dat` files
must not be routed through the format based on extension alone.

## Editable and reinsertable path

`make prepare-assets` emits `00015.messages.json` next to the raw leaf and stores
its relative path in the layout/catalog. Each JSON entry exposes `kind`, `key`,
and UTF-8 `text`. The builder re-encodes text as CP932 and recalculates each
relative string offset. Invalid pointers, embedded NULs, unsupported CP932 text,
and unsupported JSON records fail closed.

Verified outcomes:

- `messages.build(messages.parse(raw)) == raw` for the exact 20,452-byte sample.
- Rebuilding the containing 274,592-byte PAC with no edits reproduced every one
  of its 30 recorded member/gap hashes, including the `_msg.dat` member hash.
- In a temporary workspace copy, prepending `An English translation: ` to the
  first message grew `_msg.dat` by 24 bytes. The PAC relocation path moved and
  repointed the changed member; reparsing the result recovered the edited message
  and preserved the second record key. The rebuilt PAC was 295,072 bytes.
- The same temporary edit was passed through `make build-mod-disc`. The resulting
  5,016,717,312-byte ISO inventories as 42 entries; following its relocated YFS
  and PAC records recovers the edited first message and all 229 entries.
  `compare_disc.py` authenticates the pinned 4,587,749,376-byte reference and
  reports the expected mismatch: 751,273,457 differing bytes. The output SHA-256
  is `76d12d74b0926af5a3a054233e043ca6ac6e64f2d6db2c4b6672ecff4dda837b`.
  This append strategy copies the grown 428,967,936-byte YFS to the end of the
  ISO for a 24-byte text increase, so current relocation is correct but space-
  inefficient.
- After restoring the temporary test edit, `make verify-disc`
  passed unchanged with the structured message source integrated: both images
  were 4,587,749,376 bytes with SHA-256
  `cc059a3acf818dfbd0a782a9d20ee67e020d167866cd1c4dca77e6eb9224e3ec` and zero
  differing bytes.
- `make test` passed all 42 repository tests. `make verify-disc` passed with
  zero differing bytes after the structured source was integrated. The changed
  image's ISO inventory passed with 42 entries, and nested YFS/PAC parsing
  recovered all 229 messages including the edited first entry. The changed-image
  comparator authenticated the baseline and returned its expected mismatch.
- Synthetic tests cover exact message round trip, growth and pointer updates,
  malformed data, CP932 encoding failure, workspace preparation, and PAC
  relocation. `python3 -m json.tool reports/translation_surfaces.json` and
  `git diff --check` passed.

## Tracked translation catalogue and full growth loop

`localization/messages.json` is the version-controlled source catalogue for this
one table. Its 229 entries preserve the exact original Japanese text and expose
nullable `translation`, stable ID, context, notes and status. IDs combine the
observed `kind`/`key` pair with an occurrence index so the single duplicate pair
remains distinct. The catalogue is anchored to original table SHA-256
`0a9f5da3da31ce313523ab3f0591583669a9cb48146a3e4a91b04e3a5edd85cb`.
`make build-mod-disc` applies this catalogue; the builder rejects a stale source
or failure to apply it to exactly one table. Untranslated entries emit their
original strings. One initial English rendering is present; 228 rows remain
untranslated.

The first prompt is a save/start question. Its CP932 original is 178 bytes; the
English rendering is 193 bytes (+15), including explicit newlines. The changed
catalogue-driven build produced a 5,016,717,312-byte ISO with SHA-256
`b0cb3764533e9c958babd56e5d1819832be93703f21259e6232e2c8d17f14dc7`. Its ISO
inventory passed with 42 entries. Following the moved `_DATA.YFS;1`,
`data/common.pac`, and `_msg.dat` records recovered all 229 messages, the full
English prompt, and the unchanged second entry. The message table grew from
20,452 to 20,467 bytes; the PAC is 295,072 bytes and the enclosing YFS remains
428,967,936 bytes but is appended at the ISO end. The authenticated comparator
reported the expected mismatch: 751,273,457 differing bytes against the pinned
4,587,749,376-byte original. The generated ISO was removed after verification.

The canonical catalogue with all translations empty was also passed through
`make build-mod-disc`; its 4,587,749,376-byte output matched the pinned reference
with zero differing bytes. This confirms catalog integration leaves reference
reconstruction uncontaminated. The English build proves encoding, table growth,
container relocation and ISO packaging, not legibility or gameplay: runtime
line wrapping, glyph behavior, prompt timing, and save/load interaction remain
unverified.

Runtime loading, on-screen line breaks, glyph support, controller/message
parameter substitution, and growth relocation acceptance have not been tested.
A fuller translation and runtime validation, additional translation-bearing
surface recovery, and a more space-efficient placement strategy remain open.
The generated editable message JSON remains in the ignored extraction workspace;
the tracked localization catalogue is the source for translated builds.
