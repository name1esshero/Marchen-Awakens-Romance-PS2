# AFS filename-TOC 16-byte suffix audit

Updated: 2026-09-23.

## Scope and source authentication

This read-only audit compares the opaque 16-byte suffix in every filename-TOC
row of `MOVIE.AFS;1` and `BGM.AFS;1` (13 + 25 = 38 records). The repository
parser, inventory and both source archives were left unchanged.

The pinned source image is 4,587,749,376 bytes with SHA-256
`cc059a3acf818dfbd0a782a9d20ee67e020d167866cd1c4dca77e6eb9224e3ec`; a fresh
`sha256sum` matched this value in `reports/disc.json`. A fresh read-only run of
`tools/afs.py` against the image wrote only `/tmp/afs_suffix_recheck.json`; its
JSON matched `reports/afs_inventory.json` exactly. The scan rechecked both full
archive hashes and their TOCs:

| Archive | Members | Archive bytes | Archive SHA-256 | TOC bytes | TOC SHA-256 |
| --- | ---: | ---: | --- | ---: | --- |
| `MOVIE.AFS;1` | 13 | 685,115,392 | `26153fa4577fa47698cdfaccd8b85e99429b3966ef73f3ff3aa078bbe932327a` | 624 | `31632bc9af889e2dbf1c3c4733afe02cf4a02ee0184f384c6ac6f0c7aa677e96` |
| `BGM.AFS;1` | 25 | 123,400,192 | `6ba7809145b613e14cb03125a2f42662912f7720f6f4fd4ed2bb5709fe50d33c` | 1,200 | `2582c9c742798d1015250579dd68faa0a7396a6a4ff3019b60b3d5f5aa0df7ae` |

## Measured correlations

The 38 suffix byte strings are all distinct. Each full 16-byte suffix and its
SHA-256 are listed below; the SHA-256 values also match
`reports/afs_inventory.json`'s per-record entries.

Two byte patterns stand out:

1. The first 12 suffix bytes, when read as six little-endian 16-bit values,
   form a valid calendar tuple under the candidate grouping
   `year, month, day, hour, minute, second` in all 38 records. All candidate
   years are 2005; the range is 2005-07-11 11:46:52 through 2005-08-12
   16:08:28. There are 34 distinct tuples; four BGM rows repeat a tuple.
   This is consistent with timestamp-like data, but calendar validity alone
   does not establish the field names, timezone, or purpose.
2. The suffix's final four bytes exactly equal the four-byte word at relative
   archive offset `4 + 4*row_index` for every row in both archives (38/38).
   At row 0 that word is the member count. For rows 1 onward, odd rows match
   the offset and even rows match the size of member `floor((row_index-1)/2)`.
   Thus, across the suffixes in row order, these words reproduce the member
   count followed by the offset/size pairs of the first half of the member
   table. This is an exact byte correlation, not an explanation of why the
   values occur in each filename record.

The names remain associated with the same-index member rows in the observed
inventory. Payload prefixes remain consistent with the prior archive findings:
all 13 movie members begin with `00 00 01 BA`, and all 25 BGM members begin with
`80 00`. No additional mapping from the first 12 suffix bytes to these payload
prefixes, filename extensions, or same-index member offsets/sizes was established.

## Per-record suffix evidence

Coordinates/indices below are zero-based TOC row numbers. The date/time strings
are explicitly candidate readings, while `Raw 16-byte suffix` preserves the
observed bytes. `Final u32le` is merely the little-endian numeric display of the
last four bytes; the separate correlation above describes what those bytes
match mechanically.

### MOVIE.AFS;1 (13 rows)
| TOC row | Name | First 12 bytes, candidate calendar tuple | Final u32le / exact table-word match | Raw 16-byte suffix | Suffix SHA-256 |
| ---: | --- | --- | --- | --- | --- |
| 0 | `opening.sfd` | `2005-07-29 11:36:22` | 13 (`member_count = 13`) | `d50707001d000b00240016000d000000` | `431140198d0c9f2042ecd1761682801e963218c7bb4cc8c36229cc5a525c8215` |
| 1 | `prolog(ginta).sfd` | `2005-07-29 12:30:14` | 2,048 (`member[0].offset`) | `d50707001d000c001e000e0000080000` | `cc299fa6f2651abc8d3e10b90a0ee336f35ae29c5f58a5344c75e8edefa920bd` |
| 2 | `prolog(dorothy).sfd` | `2005-07-29 13:44:48` | 57,427,968 (`member[0].size`) | `d50707001d000d002c00300000486c03` | `ee6f81953b2a556025ed90df0b45598ec47a7223bf49f92cebf209e60b3b0ab4` |
| 3 | `prolog(jack).sfd` | `2005-07-29 12:38:50` | 57,430,016 (`member[1].offset`) | `d50707001d000c002600320000506c03` | `8017c6284f17c2e2bd43e021634543648a654730b050e2d106bcfe46bb0f4ada` |
| 4 | `prolog(snow).sfd` | `2005-07-29 12:48:26` | 58,388,480 (`member[1].size`) | `d50707001d000c0030001a0000f07a03` | `75781a91a1161fa3a9940ea34ed360576fd28ba6ea4136e0c2bcefe774aa3589` |
| 5 | `prolog(aran).sfd` | `2005-07-29 12:02:10` | 115,818,496 (`member[2].offset`) | `d50707001d000c0002000a000040e706` | `087af7dc834e96662e6558414f0fc3b5cac1208508bd4b6d9d08d8d7db4b7436` |
| 6 | `prolog(nanashi).sfd` | `2005-07-29 14:08:02` | 58,687,488 (`member[2].size`) | `d50707001d000e000800020000807f03` | `d9ea8aebac0d70f725257eaea5026f4ce140b859fa7a39f97f41fbd736e1b9c4` |
| 7 | `prolog(alviss).sfd` | `2005-07-29 12:22:20` | 174,505,984 (`member[3].offset`) | `d50707001d000c001600140000c0660a` | `ff0ed4e4b0f341029d7027f3459191ed08a751d142d2e56c000817e77a207fef` |
| 8 | `epilog.sfd` | `2005-08-02 16:10:34` | 59,033,600 (`member[3].size`) | `d5070800020010000a00220000c88403` | `0f13f96acecf8bedca873c5a2658bfa6112aec0886781ddb81038ee87f5b038e` |
| 9 | `mirror.sfd` | `2005-07-11 11:50:16` | 233,539,584 (`member[4].offset`) | `d50707000b000b00320010000088eb0d` | `5727d7fac8fbaea5a5e5f621560dbad9c5c704ce813b3301fb219c2fe4cc72a1` |
| 10 | `door_open.sfd` | `2005-07-11 11:46:52` | 59,072,512 (`member[4].size`) | `d50707000b000b002e00340000608503` | `bd370dbfa431f04270006f47b3d59e2ca4b2bbbd9455b9ff11da84b0e342e71f` |
| 11 | `door_close.sfd` | `2005-07-11 11:48:00` | 292,612,096 (`member[5].offset`) | `d50707000b000b003000000000e87011` | `43deecfbeafa192fa02a49f0b8affb84e3b575cd55b6f90c4a74b9c6a1025bcc` |
| 12 | `ending.sfd` | `2005-08-12 16:08:28` | 58,785,792 (`member[5].size`) | `d50708000c00100008001c0000008103` | `8debbcf0d41e7b71df5adbafb31f4f04987f5f315febf6fdd9d0d76180a6f692` |

### BGM.AFS;1 (25 rows)
| TOC row | Name | First 12 bytes, candidate calendar tuple | Final u32le / exact table-word match | Raw 16-byte suffix | Suffix SHA-256 |
| ---: | --- | --- | --- | --- | --- |
| 0 | `bgm_menu_tit001.adx` | `2005-07-23 21:10:38` | 25 (`member_count = 25`) | `d5070700170015000a00260019000000` | `fa0c7dadeb7adace1bac9085910934240b56b587c38d82ef3fcf933664fda113` |
| 1 | `bgm_menu_man001.adx` | `2005-07-23 21:10:44` | 2,048 (`member[0].offset`) | `d5070700170015000a002c0000080000` | `e906ef5ba166416a7a144fdb511cf5d668266b607f975f7bc00a576e95564133` |
| 2 | `bgm_menu_exb001.adx` | `2005-07-30 13:30:10` | 1,650,688 (`member[0].size`) | `d50707001e000d001e000a0000301900` | `be73d5fd7636b2b86e9e13db36cd335f715486810fd6d5291fe837917c7a73f4` |
| 3 | `bgm_menu_shp001.adx` | `2005-07-23 21:10:40` | 1,652,736 (`member[1].offset`) | `d5070700170015000a00280000381900` | `4e2d669c9f24165568fe7477827be6cb016f14958caaeda06bd919af00e409ed` |
| 4 | `bgm_menu_dat001.adx` | `2005-07-23 21:10:12` | 6,213,632 (`member[1].size`) | `d5070700170015000a000c0000d05e00` | `b10b134336227590c7b001c424159306bf820c6fe34ab7c4dbd851585c830760` |
| 5 | `bgm_menu_win001.adx` | `2005-07-23 21:10:36` | 7,866,368 (`member[2].offset`) | `d5070700170015000a00240000087800` | `300b70c3296cf90c563eeef7bb49c277e534eb6af9e82b6aaf278f3f6fe7ae69` |
| 6 | `bgm_menu_win002.adx` | `2005-07-23 21:10:34` | 6,354,944 (`member[2].size`) | `d5070700170015000a00220000f86000` | `edc1c159b92341a30df66e1da305a5e9d48e5e9166dfde2393d4de79ad601eb5` |
| 7 | `bgm_menu_get001.adx` | `2005-07-23 21:10:04` | 14,221,312 (`member[3].offset`) | `d5070700170015000a0004000000d900` | `906a31ed2442a788be74cf3315f75cefb6e6e977cda787e079fb242d093422f6` |
| 8 | `bgm_menu_lab000.adx` | `2005-07-23 21:10:02` | 3,194,880 (`member[3].size`) | `d5070700170015000a00020000c03000` | `860c12b89f69969a1257e9609354f4d426090dc8edf3845fbdbddb549fd37d11` |
| 9 | `bgm_menu_lab001.adx` | `2005-07-23 21:10:58` | 17,416,192 (`member[4].offset`) | `d5070700170015000a003a0000c00901` | `0ed6d639b0841d79fd1a0c23e96192511686ea31695b52f0cc0949fc52e9cd70` |
| 10 | `bgm_menu_lab100.adx` | `2005-07-23 21:10:54` | 4,380,672 (`member[4].size`) | `d5070700170015000a00360000d84200` | `40b84f95cd83c6f4868207bceaa9e4840244bf0b0af1448d0b915062dd9e04e0` |
| 11 | `bgm_menu_lab200.adx` | `2005-07-23 21:10:52` | 21,796,864 (`member[5].offset`) | `d5070700170015000a00340000984c01` | `f671905b09b09eedf0e7f8963fe65474580893d990f7d35359ecf9efba8e3192` |
| 12 | `bgm_menu_lab210.adx` | `2005-07-23 21:10:50` | 1,064,960 (`member[5].size`) | `d5070700170015000a00320000401000` | `a7d8b27a4a315159b641b7228b7c21a3dc2b851772f4d868392490f6cc2b695b` |
| 13 | `bgm_menu_ovr001.adx` | `2005-07-23 21:10:40` | 22,861,824 (`member[6].offset`) | `d5070700170015000a00280000d85c01` | `02df4bd6b5dc4281e481597fe2ce597f5aa115a88dc369d75c03a67716f695c7` |
| 14 | `bgm_btl_001.adx` | `2005-07-25 21:42:16` | 1,351,680 (`member[6].size`) | `d5070700190015002a00100000a01400` | `77c3b30ab2a9e6e2b7df3759de18a2eb5e7605917ca63000080f521e50f1074a` |
| 15 | `bgm_btl_002.adx` | `2005-07-23 21:10:50` | 24,213,504 (`member[7].offset`) | `d5070700170015000a00320000787101` | `2c698d4a98997e1b46e333ac045ab7851f57a8fbed03ee13bbc6159b30c85658` |
| 16 | `bgm_btl_003.adx` | `2005-07-23 21:10:42` | 3,526,656 (`member[7].size`) | `d5070700170015000a002a0000d03500` | `4b5291c9a29868b7d520574e1f0f80adb14457c7f69c2f863e5b5df054312a34` |
| 17 | `bgm_btl_004.adx` | `2005-07-23 21:10:36` | 27,740,160 (`member[8].offset`) | `d5070700170015000a0024000048a701` | `3788451ea3665fbbc3483184d2413d51bce66afbc5ce973b017e934396944b88` |
| 18 | `bgm_btl_005.adx` | `2005-07-23 21:10:30` | 4,057,088 (`member[8].size`) | `d5070700170015000a001e0000e83d00` | `c6d4430d86fc846cfb119f89c5da573f1fb556a5d182efee0fac820000aebdc0` |
| 19 | `bgm_btl_006.adx` | `2005-07-23 21:10:24` | 31,797,248 (`member[9].offset`) | `d5070700170015000a0018000030e501` | `71607ade75a9ee9d319c204fff0726b00f05c8e75cac63cdde48fa8f5e3060ca` |
| 20 | `bgm_btl_007.adx` | `2005-07-23 21:10:18` | 7,290,880 (`member[9].size`) | `d5070700170015000a00120000406f00` | `9ad86090661444ba4d8d531bbaf03c3754c242ff3599c3614559ed2803f3e776` |
| 21 | `AEF_105_001.adx` | `2005-07-25 19:52:22` | 39,088,128 (`member[10].offset`) | `d5070700190013003400160000705402` | `748b503426d2e4cad4b35814905c545a8e61965872bf5fc19f21e1dd93be3216` |
| 22 | `AEF_101_001.adx` | `2005-07-25 19:52:22` | 1,353,728 (`member[10].size`) | `d5070700190013003400160000a81400` | `806dbaf757b5813a3b83ae6793b3e3878ff089c36aceae0503cb05bad09c694c` |
| 23 | `ram_op.adx` | `2005-07-28 18:20:16` | 40,441,856 (`member[11].offset`) | `d50707001c0012001400100000186902` | `f168c71aa3c430d6534b6f83bc6f877c04dcc2a82d5c12a8af4089d549acd9e9` |
| 24 | `ram_ed_s.adx` | `2005-07-28 18:20:20` | 3,891,200 (`member[11].size`) | `d50707001c0012001400140000603b00` | `ea03ece4f8013fb01010f6427e8989d2c1b055323a0ca6867774b8b5be60f6bd` |

## Limits and disposition

No source-side CRI specification or independent build-time metadata was
available in this task to confirm the calendar interpretation or explain why
the final dword sequence is embedded across suffix rows. The exact mirror of
the archive count/table words may be a deliberate repeated representation or a
format/layout artifact; the byte match alone cannot choose between those
explanations. The row-to-member correlation and matching media signatures do
not establish that the AFS loader reads or cares about these bytes.

Keep all 16 suffix bytes opaque in `tools/afs.py` and preserve them unchanged.
This audit made no archive edits, assigned no field names in the parser, and
performed no AFS rebuild, relocation, or runtime test.

References: `reports/afs_inventory.json`, `tools/afs.py`,
[`AFS internal inventory`](AFS_INTERNALS.md),
[`asset workspace methodology`](../docs/TASK_ASSET_WORKSPACE_METHODOLOGY.md).
