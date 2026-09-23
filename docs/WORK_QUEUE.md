# Work queue

Authority: [STANDARDS.md](STANDARDS.md). Updated: 2026-09-22.
Manager maintains this page and [status](STATUS.md) at each verified milestone.

| Priority | Task | State / next evidence | Completion gate |
| --- | --- | --- | --- |
| P0 | Full boot ELF reconstruction | Bootstrap baseline implemented; 496 object bytes plus 3,444,708 raw bytes | Full `cmp`, isolated source-only rebuild, regression tests |
| P1 | Recover trivial linkonce accessor cluster | Census done (`reports/linkonce_text_inventory.json`): 1,694 named sections/71,932 bytes/497 classes; 62 sections/7 classes recovered so far, ~690 same-shape trivial 8-byte sections remain candidates | Same method per section: disassemble, natural one-line accessor, `compare_sections.py`, full `cmp` |
| P1 | Broaden compiler identification | EE GCC 2.96 now matches 62 sections across 7 classes (const methods, pointer-return and pointer-argument stubs, fixed return and no-op methods), unmodified `-O2` | Representative nontrivial C++ methods/callers (struct-return, matrix copies), defensible common ABI/flags; no per-function steering |
| P1 | Recover CCamera/CCamera2/CCameraMv class evidence | Partial layout candidates for 3 classes exist; [GetViewRect probe](tasks/VIEW_RECT_PROBE.md) differs (40 vs 24 bytes, unaligned vs aligned copies). Next inspect callers/writes for member type/alignment evidence; matrix pairs and RTTI remain open | Justified layout/signatures plus authentic-source review and complete ELF comparison |
| P1 | Reduce main ELF raw regions | Five explicit preserved intervals remain (was two); split further by evidenced sections as recovery proceeds | Full byte equality and provenance for each replacement |
| P1 | Decode and localize UI graphics | All 724 menu `.b` leaves now decode through the 16-byte BPE wrapper to the exact declared output length; edited decoded payloads can be rewrapped and relocated through the archive chain. Decoded payloads have 32-byte resource tables with `at3` animation records and `txc` texture records. `AT  ` animation data references `.tga` authoring images, while sampled runtime texture payloads begin `RTX3`. Next parse/extract these nested resources and recover RTX3-to-TGA import/export, then make one English UI graphic and reinsert/reparse it. | All nested entry ranges/tables validated, texture export/import round-trips pixel data and untouched source bytes, controlled edit/reinsert/relocation passes and visual/runtime validation where supported; keep unsupported TXC fields explicitly unresolved |
| P2 | Inventory DVP overlays and IOP modules | Headers known, internal semantics not yet researched | Tested format/ISA inventory; round trips before replacement |
| P2 | Inventory AFS/YFS/IOPRP internals | Top-level extents known, internal entries unresolved | Evidence-based parsers, malformed-input tests, lossless round trips |
| P1 | Asset workspace and translation surfaces | Full-disc unchanged rebuild matches; tracked, source-hash-anchored catalogues now cover `_msg.dat`, `CardList.txt`, and `DataBase.txt`. All 229 messages have English drafts; CardList names/titles/categories are drafted but its captions remain Japanese; 87/126 database fields are translated. UI `.b` wrappers have a tested decoded/reinsertable BPE layer; nested AT/TXC resources and their graphic editability remain open. | Translate CardList captions and investigate database condition metadata; next checkpoint: extract nested AT/TXC records, create English TGA variants from texture data, and reinsert. Review drafts, validate in runtime, and improve append placement; see [method](TASK_ASSET_WORKSPACE_METHODOLOGY.md) |
| P2 | Full-disc reconstruction and relocation | Untouched image matches exactly. A tracked 15-byte `_msg.dat` growth built a 5.016 GB ISO, passed ISO inventory and nested YFS/PAC message reparse, and produced an authenticated expected baseline mismatch. Current append path adds the full 428,967,936-byte YFS. | Runtime acceptance, broader relocation cases and a more space-efficient placement strategy |
| P3 | Independent provenance / runtime checks | Not performed | External dump provenance and recorded runtime validation |

Completed enabling work: ISO/ELF inventory, lossless asset export/rebuild and
streaming whole-disc comparison, selected assembly preservation,
historical compiler probe, explicit boot reconstruction, isolated rebuild check,
mandatory commit attribution trailers, and a linkonce-cluster census tool.

Any source promotion must satisfy authenticity independently of byte equality.
Do not treat P0 bootstrap completion as recovered-code or whole-game completion.
