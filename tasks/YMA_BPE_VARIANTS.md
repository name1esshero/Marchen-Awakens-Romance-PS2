# BPE-decoded YMA payload comparison

## Scope and method

This read-only comparison covers the three BPE-decoded menu resources
`top_yma.b`, `war_common_yma.b`, and `war_stage_yma.b`. The queue's
`reports/ui_bundle_survey.json` lists these as the only three of 724 menu
`.b` payloads that the common UI resource-table parser does not accept, with
reason `unknown UI bundle header variant`.

For each catalogued `.b` source, I ran the existing `tools.bpe.decode()` in
memory and compared the result with its generated `.decoded.bin` and
same-directory sibling `.pac` source listed in the extracted catalog. No
decoded source, `.pac`, parser, bundle, or ISO was modified.

## Byte identity

| Resource | Extracted BPE source | BPE bytes / SHA-256 | Decoded and sibling `.pac` bytes / SHA-256 | Exact equality |
| --- | --- | ---: | ---: | ---: |
| `top_yma.b` | `00039.asset/01571.bin` → `01571.decoded.bin` = `01572.bin` (`top_yma.pac`) | 1,295 / `eb98a4e415c2ef9f4e1bde5d1efc00a895382e88ed5c88694ee9e191d74d78dc` | 4,576 / `f41047b6931224b0050bf0d6d233e697b2ea09def31d25fe10d938a2f26a467b` | yes |
| `war_common_yma.b` | `00039.asset/01607.bin` → `01607.decoded.bin` = `01608.bin` (`war_common_yma.pac`) | 56 / `2eedc04273aa0062f161710c1a1bd165611d10d28c6757310a718ac5ff8cfa47` | 64 / `6e23c13fd6bc934576e93f72404eb620ef917cc9aaf035859aef82e5840f1afa` | yes |
| `war_stage_yma.b` | `00039.asset/01625.bin` → `01625.decoded.bin` = `01626.bin` (`war_stage_yma.pac`) | 166 / `59c98987508a93681083b85ea3f5fe183436297ccc0dc0f91d2f28816da7ceae` | 256 / `2ed86377d9516facfe831e18dbc1a7c100f5dfad6063f864bc1f1957a21c9a96` | yes |

Each `.b` starts with the BPE signature, declares a 256-byte translation table,
a packed extent equal to source size minus the 16-byte wrapper, and the decoded
size shown above. The in-memory decoder output matches both the stored decoded
sidecar and the sibling `.pac` byte-for-byte.

## Observed decoded structure

The first four little-endian 32-bit words differ as follows:

| Payload | `u32le@0x00` | `u32le@0x04` | `u32le@0x08` | `u32le@0x0c` | `root` string |
| --- | ---: | ---: | ---: | ---: | ---: |
| `top_yma` | `0x000000fc` | `0x000010c0` | `0x00000020` | `0x00000120` | offset `0x24` |
| `war_common_yma` | `0x00000018` | `0x00000000` | `0x00000020` | `0x00000040` | offset `0x24` |
| `war_stage_yma` | `0x00000024` | `0x000000a0` | `0x00000020` | `0x00000060` | offset `0x24` |

The shared `0x20` value at `0x08` coincides with a byte sequence beginning
at `0x20`; the ASCII word `root` begins four bytes later, at `0x24`. The
value at `0x0c` coincides with the first `YANM` tag in `top_yma` (`0x120`)
and `war_stage_yma` (`0x60`); in `war_common_yma` it equals EOF (`0x40`),
where no `YANM` or `POF0` tags were found. This makes
[0x20, u32le@0x0c) a candidate root/metadata region in these samples, not a
decoded table definition. The first two header words have no established
meanings.

`top_yma` contains 19 visible `YANM` tags; `war_stage_yma` contains one;
`war_common_yma` contains none. In both files with `YANM` tags, the following
little-endian size field gives an extent whose end (tag offset + 8 + size)
lands exactly on a `POF0` tag:

- `top_yma`: `0x120` size `0x68`; 15 starts from `0x1c0` through `0xc40`
  at `0xc0` intervals, each size `0x80`; then `0xd00` size `0x1e0`,
  `0xf40` size `0xd0`, and `0x1080` size `0x100`.
- `war_stage_yma`: `0x60` size `0x68`, ending at `0xd0`.

Direct tag counts are `YANM/POF0/ACFB/YATR = 19/38/19/19` for `top_yma`,
`0/0/0/0` for `war_common_yma`, and `1/2/1/1` for `war_stage_yma`. These are
observed signatures and extents, not a complete parser for these chunks.

## Conclusion and next evidence

The BPE wrapper is not the obstacle: all three decoded payloads are exactly
recovered again from catalogued sibling `.pac` members. They fail the common UI
resource-table prefix and do not establish an alternate table layout. The cross-file
`root`/`YANM` boundary correlations are useful for further investigation.
However, three examples do not establish the meanings of the first header
fields, entry counts/widths, pointer/fixup semantics, or a general YMA grammar.
Keep all three files as raw payloads and continue to reject them from the common
UI parser unless independent evidence establishes a separate layout.

Next useful evidence is another independently sourced `.yma` payload or the
producer/loader code that consumes these `YANM`, `POF0`, `ACFB`, and `YATR`
regions. No growth/rebuild experiment or runtime test was performed.

## Reproduction

From the repository root, rerun `tools.bpe.decode()` against the three
extracted `.b` files in memory, then compare each output with both its
`.decoded.bin` sidecar and mapped sibling `.pac` file. The extraction paths,
expected hashes, tag offsets, and candidate boundaries above are sufficient to
repeat this audit.
