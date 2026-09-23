# Explicit bootstrap preservation

Authority: [standards](../../docs/STANDARDS.md).

`layout.json` covers every byte of the 3,445,204-byte boot ELF exactly once.
323 object sections contribute 2,584 bytes, assembled from
`asm/camera_accessors.s` in the normal build. The optional EE compiler probe can
supply those same sections. The remaining **3,442,620 bytes** are raw
hexadecimal source intervals (one per gap between recovered sections). They
preserve code, data, ELF metadata, section names and gaps without claiming
their semantics have been recovered. This is explicit technical debt.

The raw intervals omit the selected methods entirely. The builder cannot fall
back to their original bytes when the supplied object differs. It rejects missing
or ambiguous selected sections, relocations targeting them, size changes, gaps,
overlaps and incomplete coverage. File offsets remain fixed at this bootstrap stage.

Provenance: explicit export from the pinned boot ELF using:

```sh
python3 tools/reconstruct_elf.py export 'extracted/SLPM_661.56;1' \
  config/camera_sections.txt preserved/boot --hash-file config/boot.sha256
```

The exporter refuses existing destinations. For reproducibility experiments, use
a new temporary directory and compare its generated files; do not overwrite
source work or change expected hashes. The normal build never invokes export.

Section classifications/addresses remain in `reports/SLPM_661.56;1.elf.json`.
A broader census of the 1,694-section, 71,932-byte `.gnu.linkonce.t.*` cluster
that these sections belong to is in `reports/linkonce_text_inventory.json`; see
[the linkonce cluster task](../../docs/tasks/LINKONCE_CLUSTER.md) for how it was
built and what remains unrecovered. The raw intervals are not individually
classified by semantic content beyond that census. Replace them progressively
with evidenced source, preserving the full ELF equality gate.
