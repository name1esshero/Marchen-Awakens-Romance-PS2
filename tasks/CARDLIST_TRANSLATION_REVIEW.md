# CardList translation review

Authority: [STANDARDS.md](../docs/STANDARDS.md),
[localization methodology](../docs/LOCALIZATION_METHODOLOGY.md),
[asset workspace methodology](../docs/TASK_ASSET_WORKSPACE_METHODOLOGY.md).
Evidence date: 2026-09-23.

## Scope and review method

This pass compared the Japanese caption cell and English caption translation for
all 142 rows in `localization/card_list.json`, using each row's character/ARM name
and title as local context. It also reviewed repeated terminology where the same
concept appears in the message, database, and card catalogues. The stable row ID
is retained; only English source values change. The JSON catalogue continues to
anchor every row to the recovered `CardList.txt` source hash.

The pass makes editorial corrections where the Japanese wording or nearby
catalogue entries resolve the intended sense. It does not promote provisional
ARM spellings or assert that a line has been checked against the game's full
script. `localization/GLOSSARY.md` remains the authority for current draft
terminology. VIZ's English edition uses the plural name “War Games” for the
team competition, so that spelling is now consistent in translated catalogue
surfaces ([VIZ, MÄR Vol. 10](https://www.viz.com/manga-books/manga/mar-volume-10/product/622)).

## Reviewed corrections

| Stable ID / surface | Source or former draft | Reviewed English | Reason |
| --- | --- | --- | --- |
| `key-01C-015`, caption | `ARMよ誘え ―そして、応えよ異界の住人!!!!` | `O ARM, summon him! And you, visitor from another world, answer!` | Makes the ARM invocation and the addressed visitor distinct in natural English. |
| `key-01C-023`, caption | “I'm not suspicious. I'm just...” | “I'm not a bad guy. I'm...” | Uses the English idiom for `怪しい者じゃない` and retains the interrupted introduction. |
| `key-02C-010`, caption | “We need to settle this. I can't let it go.” | “I've got to settle the score.” | Keeps the speaker singular and renders `ケジメをつける` as settling the score. |
| `key-02A-021`, title | “Flame, Clothe My Blade!!!” | “Flame, Cloak My Blade!” | Replaces the literal but unnatural “clothe” with the idiomatic spell image “cloak.” |
| `key-01E-001`, caption | “There's something exciting waiting beyond this door!” | “Excitement awaits beyond this door!” | Preserves `ワクワク` while tightening the line. |
| `key-02E-006`, title | “A Strange Irritation” | “A Strange Queasy Feeling” | Distinguishes `ムカムカ` from the adjacent irritation entry; its caption explicitly refers to feeling sick. |
| `key-02E-007`, title | “A Strange Annoyance” | “A Strange Irritation” | Uses the more direct English sense for `イライラ`, distinct from nausea/queasiness. |
| `key-02E-013`, title | “The War Game Begins!!” | “The War Games Begin!!” | Applies the glossary's publisher-backed plural name and matching verb agreement. |
| Message `msg-k00000001-i0000000a-o001` | “It's a team-versus-team War Game!” | “The War Games are a team-versus-team tournament!” | Uses the established competition name and makes the sentence idiomatic. |
| Message `msg-k00000004-i00000002-o000` | “He lived with his mother and grew crops. He joins the War Game alongside Ginta.” | “He lived with his mother and grew crops, then joined the War Games with Ginta.” | Restores consistent past tense and the established competition name. |
| Database `row-0053` | “Member Select (War Game Theme)” | “Member Select (War Games Theme)” | Aligns the soundtrack label with the named competition. |

## Verification and limits

All 142 caption translations are present. The asset builder validates catalogue
source hashes, stable IDs, CP932 encoding, and actual application to the unique
matching tables. The updated English ISO must still be structurally reparsed;
successful packaging does not establish on-screen phrasing, line wrapping, or
runtime behavior. Names, most character titles, all remaining catalogue strings,
and the provisional ARM terminology still need further editorial/contextual
review. No claim of native-speaker or in-game proofread acceptance is made.
