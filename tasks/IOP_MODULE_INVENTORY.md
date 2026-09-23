# IOP module and IOPRP inventory

Updated: 2026-09-23.

## Scope and limits

This is a bounded first pass on the P2 queue item “Inventory DVP overlays and
IOP modules.” It covers the 14 standalone `MODULES/*.IRX;1` files and the
`MODULES/IOPRP300.IMG;1` image. It does not inspect DVP overlays, modify any
module, recover module source, or establish runtime loader behavior. Detailed
byte ranges, section records, hashes, relocation counts, ROMDIR entries, and
extinfo envelopes are in [`iop_module_inventory.json`](../reports/iop_module_inventory.json).

Each standalone module was compared directly with its pinned ISO extent, its
extracted leaf, and the SHA-256 in `reports/disc.json`. ELF section headers were
read from the module bytes and checked against the existing per-module ELF JSON
reports; file-backed section hashes were recomputed. This authenticates the
inventory inputs within this checkout, but is not an independent retail-dump
provenance claim.

## Standalone module profile

All 14 files (381,321 bytes combined) are ELF32, little-endian, MIPS ELF with
processor-specific type `0xff80`, `e_machine=8` (`EM_MIPS`), `e_flags=0x1`, and
two program headers. Host `readelf` describes the flag as MIPS-I. Each contains
a processor-specific `.iopmod` section (`0x70000080`) with one readable ASCII
label. This is observed metadata, not proof that the label fully describes the
module. Section counts range from 11 to 13. Relocation records reported by
`readelf -rW` total 10,765: 4,610 `R_MIPS_26`, 2,667 each `R_MIPS_HI16` and
`R_MIPS_LO16`, and 821 `R_MIPS_32`. All 14 have `.rel.text` and `.rel.data`;
eight also have `.rel.rodata`. The `.bss` and `.sbss` sections are NOBITS and
are not file-backed bytes.

| Disc file | Bytes | ELF entry field | Sections | `.iopmod` printable label |
| --- | ---: | ---: | ---: | --- |
| `CRI_ADXI.IRX` | 68,893 | `0x57c` | 13 | `CRI_ADX_Driver` |
| `DBCMAN.IRX` | 15,653 | `0x0` | 12 | `Dbc_Manager` |
| `DS1O.IRX` | 9,509 | `0x0` | 12 | `ds1o` |
| `LIBSD.IRX` | 30,085 | `0xb0` | 12 | `Sound_Device_Library` |
| `MC2_D.IRX` | 20,269 | `0x0` | 13 | `mc2_d` |
| `MCMAN.IRX` | 96,181 | `0x178` | 12 | `mcman` |
| `MCSERV.IRX` | 7,385 | `0x40` | 11 | `mcserv` |
| `MODHSYN.IRX` | 63,037 | `0x0` | 12 | `SPU2_Synthesizer_Module` |
| `MODSEIN.IRX` | 9,393 | `0x0` | 11 | `SE_Sequence_Input_Module` |
| `MODSESQ2.IRX` | 19,069 | `0x0` | 12 | `SE_Sequencer_Module2` |
| `SDRDRV.IRX` | 9,161 | `0x3a0` | 11 | `sdr_driver` |
| `SE_PLAY.IRX` | 14,756 | `0xe50` | 12 | `se_play_driver` |
| `SIO2D.IRX` | 11,289 | `0xe14` | 11 | `sio2d` |
| `SIO2MAN.IRX` | 6,641 | `0x634` | 11 | `sio2man` |

A zero ELF entry field is preserved as observed; it does not establish that a
module is unloadable or lacks a runtime entry mechanism. Most symbol tables are
minimal, so the relocation records do not by themselves recover named imports,
exports, or dependencies. The files remain unchanged. No standalone-module
rewrite or in-game load test was performed.

## `IOPRP300.IMG;1` container evidence

The 275,345-byte image has SHA-256
`02d314464c17c715d7e809297b0aba184173a98616b1fafeac27fe33fc480c82`. Its
initial table matches the 16-byte `romdir_t` record documented by the
[PS2SDK IOP reboot implementation](https://github.com/ps2dev/ps2sdk/blob/master/ee/iopreboot/src/SifIopRebootBuffer.c):
10-byte name, little-endian extinfo length, and little-endian data size. The
observed table contains 19 named records and one empty terminator. Its `ROMDIR`
record declares exactly 320 bytes, matching all 20 records. `EXTINFO` occupies
596 bytes at offset 320; its records consume that full extent. The extinfo
record types are 17 `DATE`, 16 `VERSION`, and 17 `COMMENT` entries, using the
PS2SDK-declared type values. Comment payloads are retained by hash only in the
machine report, not rendered in this note.

The 16 embedded module payloads all begin with ELF magic and have ELF32
little-endian MIPS headers (`type=0xff80`, `e_machine=8`, `e_flags=0x1`). Their
starts are 16-byte aligned. Their complete extents are:

| IOPRP member | Offset | Bytes |
| --- | ---: | ---: |
| `SYSMEM` | 928 | 6,041 |
| `LOADCORE` | 6,976 | 10,433 |
| `SIFCMD` | 17,424 | 10,529 |
| `SIFMAN` | 27,968 | 5,969 |
| `THREADMAN` | 33,952 | 39,405 |
| `IOMAN` | 73,360 | 12,545 |
| `MODLOAD` | 85,920 | 18,565 |
| `FILEIO` | 104,496 | 19,661 |
| `CDVDMAN` | 124,160 | 83,053 |
| `CDVDFSV` | 207,216 | 32,653 |
| `LOADFILE` | 239,872 | 10,505 |
| `TIMEMANI` | 250,384 | 6,085 |
| `ROMDRV` | 256,480 | 3,881 |
| `EESYNC` | 260,368 | 1,545 |
| `SYSCLIB` | 261,920 | 10,045 |
| `STDIO` | 271,968 | 3,377 |

A no-op reconstruction from the 320-byte table, the 596-byte extinfo pool, the
16 payload extents, and zero-filled inter-member alignment gaps reproduced all
275,345 bytes exactly. The final member ends at EOF; the image has no trailing
16-byte pad. This validates one extraction/reassembly layout. It does not test
edited member growth, changes to metadata, another IOPRP variant, module
relocation application, loader behavior, or runtime execution. The ROMDIR shape
is corroborated by PS2SDK source and direct byte boundaries, but that does not
prove the game's image was generated by PS2SDK.

## Verification record

- The inventory procedure read all 15 disc members from their `reports/disc.json` LBA/size extents in `baserom.iso`; each matched its extracted leaf and catalog SHA-256.
- ELF32 identity, header extents, section headers, program-header extents, and all file-backed section hashes passed for the 14 standalone modules. Existing per-module JSON section records matched decoded headers.
- `readelf -rW` relocation records were counted across all standalone modules; no relocation was applied or rewritten.
- IOPRP ROMDIR/EXTINFO sizes, records, module extents, aligned starts, zero gaps, embedded ELF header bounds, and a no-op full-byte reconstruction passed.
- `python3 -m json.tool reports/iop_module_inventory.json` accepted the machine-readable report.

The analysis used a temporary local script, not a checked-in parser. The P2 queue
item remains open for a reusable, malformed-input-tested parser and safe edited
rebuilds; the DVP-overlay half remains untouched.
