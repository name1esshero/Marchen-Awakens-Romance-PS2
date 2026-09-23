# DVP overlay section inventory

## Result

The main executable `SLPM_661.56;1` contains 42 sections named `.DVP.*`:
40 `.DVP.overlay.*` payload sections, `.DVP.ovlytab`, and `.DVP.ovlystrtab`.
The 40 raw overlay section bodies total 32,232 bytes. The two metadata section
bodies add 1,987 bytes, for 34,219 bytes across all `.DVP.*` sections. The
sections occupy one contiguous, non-overlapping file range `[3,231,844,
3,266,063)` in the extracted 3,445,204-byte ELF.

`reports/dvp_overlay_inventory.json` is the row-level inventory. It records the
source ELF hash, each section's ELF index/type/flags/address/alignment, file
extent, byte count, and SHA-256, plus each corresponding overlay-table row.
The executable has ELF32 little-endian `ET_EXEC` headers and machine value 8
(MIPS); the ELF flags are retained as the raw value `0x20924001`. The overlay
sections have processor-specific section type `0x7ffff421`, flags `0x5`, zero
ELF section address, and byte alignment. This establishes section boundaries
and executable/write flags, not how the DVP loader maps or runs them.

## Table correlation

`.DVP.ovlytab` is 480 bytes and divides exactly into 40 records of 12 bytes.
Reading each record as three little-endian `u32` values, the first value points
to a NUL-terminated ASCII name in `.DVP.ovlystrtab`; every row resolves to one
unique `.DVP.overlay.*` section name, and all 40 overlay sections are covered
once. The second and third words are preserved as raw values without assigning
runtime meanings. The third word agrees with the first numeric suffix token in
38 names; the other two names contain the literal `unknvma`, so their name text
does not expose that token as a number. Six distinct values appear as the second
name token; the JSON reports their counts and payload byte totals as opaque
labels, not decoded module identifiers.

The ELF contains no standard `SHT_REL` or `SHT_RELA` sections, and `readelf -rW`
reports no relocations. This says nothing about possible DVP-specific relocation,
load-address, or fixup behavior encoded outside conventional ELF relocation
sections.

## Evidence and limits

The extracted ELF SHA-256 is
`9f562361510b2d82bc99bbc02306f63efc3c61d2ae3d1c484401eb60a46af672`; it matches
the hash in `reports/SLPM_661.56;1.elf.json`. Direct source-byte checks recompute
every `.DVP.*` section hash and validate all extents are in-bounds, disjoint,
and contiguous. `readelf -h`, `readelf -SW`, `readelf -x .DVP.ovlytab`,
`readelf -p .DVP.ovlystrtab`, and `readelf -rW` were used for independent ELF
header, section, table, string, and conventional relocation inspection.

This is a structural inventory only. Overlay payload instructions, table word
semantics beyond the verified string references, loader logic, runtime pointers,
inter-overlay references, safe growth/relocation, and game acceptance remain
unresolved. The source executable was not modified. No overlays were rebuilt,
translated, or tested in an emulator.
