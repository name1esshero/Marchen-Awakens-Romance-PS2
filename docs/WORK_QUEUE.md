# Work queue

Authority: [STANDARDS.md](STANDARDS.md). Updated: 2026-09-22.
Manager maintains this page and [status](STATUS.md) at each verified milestone.

| Priority | Task | State / next evidence | Completion gate |
| --- | --- | --- | --- |
| P0 | Full boot ELF reconstruction | Bootstrap baseline implemented; 64 object bytes plus 3,445,140 raw bytes | Full `cmp`, isolated source-only rebuild, regression tests |
| P1 | Broaden compiler identification | EE GCC 2.96 matches eight trivial accessors; middleware labels found | Representative nontrivial C++ methods/callers, defensible common ABI/flags; no per-function steering |
| P1 | Recover CCamera class evidence | Partial layout candidate; inspect constructors, virtual tables, callers and larger named methods | Justified layout/signatures plus authentic-source review and complete ELF comparison |
| P1 | Reduce main ELF raw regions | Two explicit preserved intervals remain; split by evidenced sections as recovery proceeds | Full byte equality and provenance for each replacement |
| P2 | Inventory DVP overlays and IOP modules | Headers known, internal semantics not yet researched | Tested format/ISA inventory; round trips before replacement |
| P2 | Inventory AFS/YFS/IOPRP internals | Top-level extents known, internal entries unresolved | Evidence-based parsers, malformed-input tests, lossless round trips |
| P2 | Full-disc reconstruction | Not implemented | Source-artifact rebuild, all metadata/gaps preserved, complete image comparison |
| P3 | Independent provenance / runtime checks | Not performed | External dump provenance and recorded runtime validation |

Completed enabling work: ISO/ELF inventory, selected assembly preservation,
historical compiler probe, explicit boot reconstruction, isolated rebuild check,
and mandatory commit attribution trailers.

Any source promotion must satisfy authenticity independently of byte equality.
Do not treat P0 bootstrap completion as recovered-code or whole-game completion.
