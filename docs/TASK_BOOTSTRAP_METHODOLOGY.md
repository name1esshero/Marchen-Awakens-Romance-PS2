# Bootstrap methodology

Authority: [STANDARDS.md](STANDARDS.md), [AGENT_ENVIRONMENT.md](AGENT_ENVIRONMENT.md).
Objective: turn supplied media into reproducible evidence and bounded recovery tasks.

1. Read standards, status, successes and failures before changing tools or source.
2. Pin input size and SHA-256. Never regenerate expected hashes to accept a mismatch.
   Our pinned hashes identify the supplied image, not external release provenance.
3. Run `make inventory`. Preserve ISO file versions in output paths. Inventory
   reports are generated evidence; explicit extraction is research, never a build.
4. Inspect ELF headers and named sections with independent tools (`readelf -h`,
   `llvm-objdump-21 -d` with a bounded address range). Do not infer ISA from filename.
5. Select a bounded region using evidenced names/boundaries. Preserve instruction
   source, record offsets and uncertainty, and place high-level hypotheses under
   `candidates/` until the original compiler/ABI and matching gates are established.
6. Run `make test` and the relevant scoped comparison. Check negative fixtures as
   well as success. Never describe a section match as a full executable match.
7. Record evidence and blockers in task notes; promote reusable mechanisms to memory.

## Tool contracts and limits

`tools/bootstrap.py IMAGE --reports DIR [--extract DIR]` reads ISO descriptors and
directories, hashes the complete image, and writes deterministic JSON. The explicit
extraction option writes files no larger than 16 MiB; it never modifies the input.
Use dedicated output directories: existing report/extraction paths are overwritten.
Malformed/unsupported inputs raise an exception and exit nonzero; output may be
partial on failure. It supports 2048-byte blocks, one volume, contiguous extents,
ASCII identifiers, and ELF32 little-endian section tables. No archive recursion,
Rock Ridge/Joliet interpretation, generic ELF extended numbering, or disc repacking.

`tools/compare_sections.py REFERENCE OBJECT SELECTION` requires nonempty, explicitly
listed PROGBITS sections and compares their complete bytes. Missing names or unequal
bytes fail. It does not apply relocations or verify executable headers, placement,
unselected sections, or semantics. Only use it for relocation-free local experiments.
Full reconstruction must add a separate whole-file byte comparison before integration.

If a pinned hash fails, stop dependent matching and investigate the input; do not
edit the baseline. If an unsupported format is encountered, retain the original
and add a tested parser extension only after evidence. If compiler identity is
unknown, preserve assembly and document candidate semantics without promoting them.

Bootstrap handoff requires reproducible reports, tested tools, bounded comparison
evidence and an explicit queue. Project completion still requires the full standards
gates, including source-only full reconstruction and authentic source/assets.

## Format references

- [ECMA-119](https://ecma-international.org/publications-and-standards/standards/ecma-119/)
  defines the ISO volume and directory record fields used by the inventory parser.
- [System V ABI ELF header](https://www.sco.com/developers/gabi/latest/ch4.eheader.html)
  defines ELF identification, machine and section-table header fields.

These references describe formats; observed image bytes and independent tools
remain the evidence for this particular executable.
