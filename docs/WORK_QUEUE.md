# Work queue

Authority: [STANDARDS.md](STANDARDS.md). Updated: 2026-09-22.
Manager maintains this page and [status](STATUS.md) at each verified milestone.

| Priority | Task | State / next evidence | Completion gate |
| --- | --- | --- | --- |
| P0 | Full boot ELF reconstruction | Bootstrap baseline implemented; 152 object bytes plus 3,445,052 raw bytes | Full `cmp`, isolated source-only rebuild, regression tests |
| P1 | Recover trivial linkonce accessor cluster | Census done (`reports/linkonce_text_inventory.json`): 1,694 named sections/71,932 bytes/497 classes; 19 sections/3 classes recovered so far, ~733 same-shape trivial 8-byte sections remain candidates | Same method per section: disassemble, natural one-line accessor, `compare_sections.py`, full `cmp` |
| P1 | Broaden compiler identification | EE GCC 2.96 now matches 19 sections across 3 classes (const methods, a pointer-arg stub, two no-op methods), unmodified `-O2` | Representative nontrivial C++ methods/callers (struct-return, matrix copies), defensible common ABI/flags; no per-function steering |
| P1 | Recover CCamera/CCamera2/CCameraMv class evidence | Partial layout candidates for 3 classes exist; [GetViewRect probe](tasks/VIEW_RECT_PROBE.md) differs (40 vs 24 bytes, unaligned vs aligned copies). Next inspect callers/writes for member type/alignment evidence; matrix pairs and RTTI remain open | Justified layout/signatures plus authentic-source review and complete ELF comparison |
| P1 | Reduce main ELF raw regions | Five explicit preserved intervals remain (was two); split further by evidenced sections as recovery proceeds | Full byte equality and provenance for each replacement |
| P2 | Inventory DVP overlays and IOP modules | Headers known, internal semantics not yet researched | Tested format/ISA inventory; round trips before replacement |
| P2 | Inventory AFS/YFS/IOPRP internals | Top-level extents known, internal entries unresolved | Evidence-based parsers, malformed-input tests, lossless round trips |
| P2 | Full-disc reconstruction | Not implemented | Source-artifact rebuild, all metadata/gaps preserved, complete image comparison |
| P3 | Independent provenance / runtime checks | Not performed | External dump provenance and recorded runtime validation |

Completed enabling work: ISO/ELF inventory, selected assembly preservation,
historical compiler probe, explicit boot reconstruction, isolated rebuild check,
mandatory commit attribution trailers, and a linkonce-cluster census tool.

Any source promotion must satisfy authenticity independently of byte equality.
Do not treat P0 bootstrap completion as recovered-code or whole-game completion.
