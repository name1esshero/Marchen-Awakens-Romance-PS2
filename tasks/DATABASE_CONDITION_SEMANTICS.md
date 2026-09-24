# DataBase column-5 condition text

Authority: [localization methodology](../docs/LOCALIZATION_METHODOLOGY.md),
[message-table evidence](MESSAGE_TABLE.md), and the source-hash-anchored
catalogue at [`localization/database.json`](../localization/database.json).
Evidence date: 2026-09-23.

## Scope and source integrity

Reviewed all populated column-5 cells in the 71-row `DataBase.txt` catalogue.
The catalogue remains anchored to source SHA-256
`b775dfa84567336cce820b5923f424ccea1f52e69e13e1075b45cb7f74f19f1f`.
The 39 previously untranslated cells in rows `row-0021`–`row-0066` contain
four distinct Japanese phrases. Their adjacent rows identify character voice,
movie, and sound entries; the same column already contains ten translated
`パスワード` (`Password`) markers. This supports translating the four natural-
language descriptions while preserving uncertainty about exactly where the
field is shown and how the Labyrinth visibility rule is implemented.

## Draft readings

| Source phrase | Rows | English draft |
| --- | ---: | --- |
| `ラビリンスで隠しOFF／試合前後ボイス変わる（バリエーション）` | 7 | `Labyrinth: hidden flag OFF; alternate pre/post-match voices.` |
| `ラビリンスで隠しOFF／試合前後ボイス聞ける` | 9 | `Labyrinth: hidden flag OFF; pre/post-match voices available.` |
| `ラビリンスで隠しOFF` | 22 | `Labyrinth: hidden flag OFF.` |
| `ラビリンスをクリアしたら隠しOFF` | 1 | `Hidden flag OFF after clearing Labyrinth.` |

The drafts preserve `隠しOFF` as a hidden-flag state rather than converting it
to “visible” or “unlocked.” This is a cautious literal rendering, not proof of
an unlock condition, menu behavior, or code-level flag meaning. Retain these as
English drafts and verify the displayed text and progression behavior in the
running game before editorially tightening the wording.

## Verification and limits

`text_catalog.validate` accepts the catalogue, and applying it to the exact
source produces a CP932-encodable 71-row table of 3,684 bytes (source: 3,413;
growth: 271). All 39 cells now have English drafts; together with the existing
87 translated fields, this gives 126/126 draft translations. The catalogue's
Japanese `original_cells` and source hash are unchanged. This proves catalogue
application and encoding only: no runtime rendering, unlock semantics, or
emulator acceptance is established here.
