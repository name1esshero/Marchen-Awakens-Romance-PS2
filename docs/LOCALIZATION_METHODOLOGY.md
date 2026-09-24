# LOCALIZATION_METHODOLOGY.md

## Purpose

This document defines a **system-agnostic methodology for turning an
untranslated game into a reproducible, editable, verifiable localization
project**.

The objective is not merely to replace Japanese strings with English
text. The objective is to establish a reusable localization pipeline in
which language-bearing content can be discovered, extracted without
loss, represented in editable source form, translated while preserving
semantics and presentation, rebuilt and reinserted safely, relocated or
expanded when translated content grows, verified mechanically, validated
in the running game where practical, and inherited by future workers
without repeating prior reverse engineering.

Apply `STANDARDS.md` and `AGENT_ENVIRONMENT.md` throughout.

------------------------------------------------------------------------

## 1. Localization Objective

Aim for an experience that looks and behaves as though an official
localization could have existed.

Translation-bearing surfaces may include dialogue, menus,
item/skill/character/enemy/location names, descriptions, tutorials,
system messages, save/load UI, subtitles, credits, scripts, fonts, text
rendered into textures, logos, title screens, button prompts, map
labels, UI atlases, videos, executable data, dynamically generated
strings, and compressed/encoded text tables.

The first major milestone is:

> **A repeatable path from original game to playable localized build.**

Complete decompilation is not a prerequisite.

------------------------------------------------------------------------

## 2. Non-Negotiable Principles

### Preserve the original

Never modify the only reference copy. Authenticate original inputs where
possible and preserve hashes.

### Extraction must be reversible

For every recovered container or asset format, seek:

`original -> extract -> rebuild -> equivalent/original`

Prefer byte-identical round trips for deterministic formats. If byte
identity is impossible, define and test the strongest meaningful
equivalence contract.

### Translation must survive growth

English frequently requires more space than Japanese. Do not build a
localization pipeline that works only while translations fit original
slots.

Investigate and support, where permitted: relocation, pointer/reference
updates, archive repacking, table growth, filesystem relocation,
alignment updates, length/count fields, checksums, compression-size
changes, section/container growth, and expansion regions.

### Preserve uncertainty

Unknown bytes, fields, flags, references, and metadata remain unknown
until evidence establishes their meaning. Preserve unknown data
losslessly where practical.

### Separate claims

A byte-identical rebuild proves reconstruction, not complete recovery.
Extraction does not prove editability. Translation does not prove safe
reinsertion. Rebuilding does not prove runtime correctness.

------------------------------------------------------------------------

## 3. General Pipeline

`authenticate -> inventory -> containers -> lossless extraction -> lossless reconstruction -> catalogue -> classify -> translation surfaces -> editable forms -> translate -> growth/relocation -> reinsert -> rebuild -> verify -> runtime validate`

Do not wait for every asset format to be understood before pursuing the
first playable translation. Prioritize translation-bearing surfaces.

------------------------------------------------------------------------

## 4. Acclimation

Before investigating formats:

1.  Read `STANDARDS.md` and `AGENT_ENVIRONMENT.md`.
2.  Read `STATUS.md` and `WORK_QUEUE.md`.
3.  Read relevant `SUCCESSES.md`, `FAILURES.md`, task evidence, and
    methodologies.
4.  Inspect current extraction/rebuild tools.
5.  Run documented verification gates when practical.

Do not repay reverse-engineering costs already paid by prior workers.

------------------------------------------------------------------------

## 5. Authenticate and Inventory

Record reference hashes, image size, filesystem/container type,
executables, file count, directories, archives, large opaque regions,
compression indicators, middleware, filenames/extensions, duplicates,
and likely language-bearing files.

Maintain a machine-readable catalogue where practical with fields such
as:

`path, offset, size, hash, container, compression, format hypothesis, translation relevance, extraction status, rebuild status, editability status, relocation status, verification status`

The catalogue is living project state.

------------------------------------------------------------------------

## 6. Lossless Container Reconstruction

For each filesystem/archive/container:

1.  identify structural metadata;
2.  extract members without altering them;
3.  preserve unknown metadata;
4.  rebuild;
5.  compare against the original;
6.  test nested containers recursively;
7.  document ordering/alignment rules;
8.  add regression tests.

The normal reconstructed build must not secretly copy reference bytes
except through explicit preserved source artifacts allowed by project
standards.

For large images, prefer a streaming whole-image comparator reporting
expected/actual size, differing-byte count, first mismatch
offsets/ranges, and hashes.

------------------------------------------------------------------------

## 7. Prove Growth and Relocation

Create a controlled fixture in which one contained file grows. Verify
all required offsets, archive tables, filesystem entries, volume sizes,
alignment, lengths, checksums, pointers, and relocation metadata update
correctly.

Prefer a synthetic fixture first, then a real-game fixture.

Target invariant:

> **An unchanged game rebuilds identically, and a deliberately enlarged
> resource relocates correctly without corrupting unrelated content.**

Do not generalize shiftability beyond the tested scope.

------------------------------------------------------------------------

## 8. Build the Asset Catalogue

Recursively classify extracted content by extension, magic, headers,
size patterns, hashes, archive membership, directory, strings,
entropy/compression, and middleware signatures.

High-volume formats are valuable because one recovery can unlock many
assets, but distinguish **high-volume** from **translation-bearing**.

The catalogue should answer:

-   What exists?
-   What is understood?
-   What is editable?
-   What rebuilds?
-   What can grow/relocate?
-   What contains language?

------------------------------------------------------------------------

## 9. Identify Translation-Bearing Surfaces

Search systematically across text-like files, scripts, executable
strings, archive members, string/pointer tables, fonts, UI textures,
menu atlases, map labels, title graphics, help images, subtitles, and
video overlays.

Distinguish user-facing content from debug strings, metadata, symbols,
source fragments, middleware labels, and format descriptors.

Create a translation-surface report with evidence and confidence.
Prioritize the shortest path to a playable localized build.

------------------------------------------------------------------------

## 10. Recover Text Encoding and Structure

For each text-bearing format establish:

-   source encoding;
-   terminators;
-   lengths;
-   pointers/references;
-   control codes;
-   line breaks;
-   variables/placeholders;
-   color/style codes;
-   speaker metadata;
-   message IDs;
-   ordering;
-   compression;
-   checksums;
-   display constraints.

Do not assume UTF-8 internally. Editable localization source should
preferably be Unicode/UTF-8, with deterministic conversion back to the
game's encoding.

Conceptual path:

`game bytes -> decoder -> UTF-8 source -> translation -> encoder/compiler -> game representation`

Preserve control codes explicitly.

------------------------------------------------------------------------

## 11. Prove the Translation Loop Early

Do not wait for complete text recovery. Select one real
translation-bearing resource and prove:

`extract -> decode -> translate/edit -> encode -> grow -> relocate/repoint -> rebuild container -> rebuild game image -> structural verify -> runtime test`

Prefer a deliberately longer English replacement.

Once this succeeds, the format has moved from open reverse-engineering
into repeatable production.

Add a dedicated mod/localization build target where appropriate,
e.g. `make build-mod-disc`.

------------------------------------------------------------------------

## 12. Translation Source Design

Keep translation source reviewable and version-controlled. Prefer UTF-8
text, CSV/TSV, JSON/YAML, PO-like catalogues, readable script languages,
or per-resource text files.

Useful entry metadata:

`stable ID, original text, translated text, context, speaker, resource, constraints, notes, status`

Avoid raw offsets as the only long-term identity when resources can
move.

------------------------------------------------------------------------

## 13. Graphical Text Localization

Graphical language is part of localization.

Preferred objective:

> **Change only the language-bearing content while preserving the
> original artwork and visual identity.**

Do not regenerate an entire image when only text needs changing unless
necessary.

For text atlases and compact UI labels, measure each original label's pixel
bounds and keep independent labels inside their source rows. A generative edit
that changes the canvas, logo, arrows, background, or layout is not a usable
replacement. If its text is still legible and correct, reviewed lettering crops
may be composited over the unchanged source artwork; discard the generated
composition, preserve the original transparent regions and palette, and center
translated wording within the evidenced source label area. Reinspect the final
source-sized, palette-mapped texture before staging it. The generated image is
only a lettering source, not evidence of translation accuracy or runtime UV
placement.

Keep any approved generated PNG layer in the repository beside its target art;
a path under a user's model cache is not a reproducible source. Use the
deterministic `tools/graphics_compose.py` / `make graphics-compose` step to
alpha-crop, apply a documented low-alpha threshold if needed, fit to measured
source bounds, clear only the old lettering rectangle, and composite onto the
immutable Japanese TGA canvas. The tool preserves exact dimensions and reports
its source bounds, fit, threshold, and output hash. Reopen and inspect that final
raster at native size, then stage it through the original RTX3 palette importer.
Keep the input layer, exact command parameters, final TGA, and palette-mapped
TXC evidence together; this makes model artwork an editable input and the
postprocessing deterministic. A successful static import says nothing about
runtime UV placement or screen composition.

Preserve composition, non-text artwork, decorative/spinning effects,
gradients, outlines, shadows, highlights, transparency, dimensions,
palette constraints, texture layout, animation frames, and surrounding
UI geometry.

English lettering should approximate the original color family, outline,
shadow, weight, perspective/skew, capitalization, spacing, and pixel-art
character where applicable.

Workflow:

`original -> identify text region -> preserve non-text content -> translate -> style-match English -> composite -> restore format/palette -> validate dimensions/alpha -> rebuild -> reinsert -> runtime inspect`

Keep original and localized assets side by side. For the extracted RTX3
graphics workspace, the exported `*_jp.tga` is the immutable recovered-game
baseline: never edit it for localization. Copy it to a sibling `*_eng.tga` and
edit or regenerate only that English variant. This preserves the Japanese image
for visual comparison, translation revision, and rebuilding English artwork
without re-extracting the ISO. The mod-disc build selects the `_eng` sibling
when present and keeps the `_jp` baseline unchanged. Keep both in the same
human-readable category folder and preserve the indexed source mapping. Generated
Japanese `_jp.tga` baselines, `graphics/index.json`, and authored `_eng.tga`
variants are all version-controlled so the repository contains both recovered
source artwork and localized replacements. Keep the larger extracted container
workspace separate; `/extracted/` remains a reproducible generated workspace.

------------------------------------------------------------------------

## 14. Fonts and Glyph Coverage

Investigate font textures, glyph maps, character lookup tables,
variable/fixed width behavior, kerning, line height, fallback behavior,
punctuation, and case support.

Prefer adapting the existing visual style. Test uppercase, lowercase,
digits, punctuation, apostrophes, quotation marks, and required symbols.

------------------------------------------------------------------------

## 15. UI and Layout Validation

English often occupies more horizontal space. Test menus, dialog boxes,
descriptions, multiline text, prompts, lists, status screens, map names,
and save/load screens.

Watch for clipping, overlap, bad wrapping, alignment drift, buffer
limits, fixed-width assumptions, and hardcoded character counts.

If layout behavior requires code changes, document and queue the
dependency rather than hiding it with poor translation.

------------------------------------------------------------------------

## 16. Scripts and Event Languages

If dialogue lives in bytecode/scripts, recover a readable representation
where practical:

`native script <-> readable script source`

Seek byte-exact unchanged round trips. Expose dialogue, control flow,
commands, labels, arguments, resource references, and control codes.

When translated scripts grow, integrate with relocation/expansion rather
than imposing artificial original-size limits.

------------------------------------------------------------------------

## 17. Translation Quality and Terminology

Machine translation can bootstrap coverage, but context matters.
Preserve terminology, character voice, names, recurring
items/skills/locations, UI consistency, and narrative continuity.

Maintain a glossary when useful:

`Japanese, romanization, preferred English, category, context, notes`

Do not silently change established terminology.

------------------------------------------------------------------------

## 18. Verification Layers

Localization needs independent gates:

-   **Reference reconstruction:** unchanged source artifacts reproduce
    the authenticated original where supported.
-   **Extraction round trip:** unchanged asset/container rebuild
    preserves required equivalence.
-   **Growth/relocation:** deliberately enlarged resource relocates
    correctly.
-   **Encoding:** deterministic Unicode \<-\> game encoding conversion.
-   **Structural validation:** offsets, pointers, lengths, counts,
    alignment, checksums, metadata.
-   **Build validation:** localized image builds reproducibly.
-   **Runtime validation:** game boots and modified resources
    render/function correctly where emulator/hardware testing is
    available.

Never substitute one layer for another.

------------------------------------------------------------------------

## 19. Separate Reference and Localized Builds

Maintain a strict distinction between reference reconstruction and
localized/modded builds.

The reference build proves recovery accuracy. The localized build
intentionally differs.

Conceptually:

`make compare` `make build-reference` `make build-mod`
`make build-english`

Exact names are project-specific. Translation overrides must not
contaminate authoritative reference reconstruction.

------------------------------------------------------------------------

## 20. Asset Editors and Modding Tools

Once a format is reversible, evaluate dedicated tooling.

Progression:

`binary -> parser/rebuilder -> canonical editable representation -> CLI conversion/editing -> specialized editor -> integrated authoring environment`

Potential tools include text/script editors, map editors, texture tools,
model import/export, animation editors, archive browsers, and
localization dashboards.

GUIs should use the same tested format libraries as command-line tools.

------------------------------------------------------------------------

## 21. 3D Model and Scene Tooling

For 3D games, long-term modding may require geometry, submeshes,
materials, textures, UVs, normals, skeletons, bones, skin weights,
animations, attachment points, bounding volumes, LODs, scene hierarchy,
and engine metadata.

Prefer a verified import/export library first. A Blender-like or
dedicated GUI can then sit on top.

An unchanged `import -> export` should preserve the strongest achievable
equivalence before arbitrary editing is trusted.

------------------------------------------------------------------------

## 22. Tool Creation Rule

Repeated deterministic localization work should become tooling.

Examples: archive inventory, pointer-table decoding, encoding
conversion, text extraction, graphical-text census, texture conversion,
relocation updates, image comparison, untranslated-string detection, and
coverage reports.

Do not make future workers repeatedly perform mechanical work through
reasoning.

------------------------------------------------------------------------

## 23. Test Creation Rule

Evaluate every discovered invariant for a regression test.

High-value fixtures include unchanged round trips, longer translations,
archive growth, alignment-boundary crossings, nested archives, invalid
encoding, malformed pointers, graphical dimensions/alpha, palette
preservation, script growth, and full-image reconstruction.

Use synthetic fixtures for edge cases where useful.

------------------------------------------------------------------------

## 24. Institutional Knowledge Capture

Every significant discovery should be evaluated for `SUCCESSES.md`,
`FAILURES.md`, format docs, task evidence, methodology updates, tools,
tests, status, and work queue.

A success entry should capture:

`symptom/opportunity -> mechanism -> evidence -> procedure -> verification -> scope -> limits -> references`

A failure entry should capture:

`hypothesis -> why plausible -> experiment -> observed failure -> mechanism -> lesson -> reconsideration conditions -> what it does NOT prove`

The next worker should begin at the current localization frontier.

------------------------------------------------------------------------

## 25. Prioritization for a Playable English Build

When the owner's immediate objective is to play the game in English, a
useful default order is:

1.  reversible filesystem/container pipeline;
2.  growth/relocation support;
3.  main dialogue/story text;
4.  menus and UI text;
5.  fonts/glyph coverage;
6.  graphical UI text;
7.  item/skill/location/name tables;
8.  scripts/event text;
9.  remaining graphical language;
10. secondary/nonessential text;
11. polish and terminology consistency.

Adapt to evidence. Do not let an interesting but non-blocking format
displace a direct translation bottleneck.

------------------------------------------------------------------------

## 26. Definition of an Initial Playable Translation

An initial localization milestone is reached when:

-   the game image rebuilds reproducibly;
-   translation-bearing containers can be rebuilt safely;
-   translated content can grow/relocate where required;
-   primary text is editable and reinsertable;
-   required English glyphs render;
-   critical menus/UI are understandable;
-   major graphical text required for navigation is localized;
-   the game boots and representative translated content works in
    runtime testing;
-   remaining untranslated surfaces are inventoried rather than silently
    ignored.

This is **not** the same as a polished final localization.

------------------------------------------------------------------------

## 27. Definition of a Mature Localization Pipeline

A mature pipeline should allow a future worker to:

1.  clone/acclimate;
2.  obtain the legally supplied reference input;
3.  verify it;
4.  extract/rebuild assets reproducibly;
5.  edit translation source rather than binary offsets;
6.  rebuild a localized image with one documented workflow;
7.  run automated validation;
8.  identify untranslated or unresolved surfaces;
9.  continue improving the localization without repeating format
    research.

The project should become easier to localize and mod as institutional
knowledge accumulates.

------------------------------------------------------------------------

## 28. AI Worker Directive

When assigned a broad objective such as **"make this game playable in
English"**:

> Do not interpret the request as merely translating strings. Acclimate
> to the repository, establish the shortest verified path to an editable
> and reproducible localization loop, prioritize translation-bearing
> surfaces, preserve original presentation, support growth and
> relocation where evidence permits, create tools/tests for repeated
> work, distinguish reference reconstruction from localized output,
> document uncertainty and blockers, update institutional knowledge, and
> continue autonomously through bounded verified milestones. When a
> prerequisite becomes solved infrastructure, return focus to the
> localization objective rather than treating the prerequisite as the
> endpoint.

------------------------------------------------------------------------

## 29. Core Principle

> **The localization pipeline should convert one-time
> reverse-engineering effort into reusable infrastructure, so later
> workers spend their reasoning on untranslated content and genuinely
> new formats rather than rediscovering how the game stores its
> language.**

The final product is not only an English build.

It is a workplace capable of continuing to translate, edit, mod, verify,
and understand the game.
