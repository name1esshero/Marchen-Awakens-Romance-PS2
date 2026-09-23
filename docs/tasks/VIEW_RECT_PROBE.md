# GetViewRect aggregate-return probe — 2026-09-22

Authority: [standards](../STANDARDS.md). Contributor: GPT-6, R&D.
State: non-matching candidate; all 24 original bytes remain preserved hex.

## Evidence and hypothesis

The pinned boot ELF section `.gnu.linkonce.t.GetViewRect__7CCamera` at
`0x33afe0` contains:

```text
move $2, $4
ld   $3, 0x140($5)
sd   $3, 0($2)
ld   $3, 0x148($5)
jr   $ra
sd   $3, 8($2)
```

The method copies 16 bytes from `$5 + 0x140` to the address passed in `$4`,
and returns that destination in `$2`. A hidden aggregate-return destination
preceding `this` is consistent with this sequence and the experiment below.
The transfer widths do not establish the source fields' types, original type
name, or full class layout.

A rectangle of four floats was tested as a plausible hypothesis suggested by
the method name and 16-byte copy. The candidate uses a partial class with
unknown bytes through `0x13f`, a four-float aggregate, and the natural method
body `return viewRect;`. It uses the existing pinned EE GCC
`2.96-ee-001003-1` and unchanged common `-O2` flag. No alignment attributes,
register assignments, pointer/integer casts or assembly were introduced.

## Observed mismatch

The compiler emits the expected named section and the same destination/`this`
register roles, but **40 bytes rather than 24**:

```text
move $2, $4
ldl  $3, 0x147($5)
ldr  $3, 0x140($5)
ldl  $4, 0x14f($5)
ldr  $4, 0x148($5)
sdl  $3, 7($2)
sdr  $3, 0($2)
sdl  $4, 15($2)
jr   $ra
sdr  $4, 8($2)
```

The first differing instruction is at section offset `0x4`. The candidate
uses unaligned merge operations instead of aligned `ld`/`sd`, and schedules
the two loads before the stores. Insufficient aggregate alignment is a
mechanism hypothesis; the experiment does not prove the original type or
which declaration/compiler difference explains the original code.

Do not add alignment or wider component types solely to reproduce the bytes.
Next inspect callers and writes to the `0x140`–`0x14f` member region for
independent evidence of type, alignment and construction. A different compiler
or aggregate definition remains possible. This result does not reject EE GCC
2.96 for the game or aggregate returns generally.

## Reproduction and verification

```sh
python3 tools/run_ee_probe.py --sources candidates/ee_view_rect --output build/view_rect.o
python3 tools/compare_sections.py 'extracted/SLPM_661.56;1' build/view_rect.o candidates/ee_view_rect/sections.txt
llvm-objdump-21 -d --section=.gnu.linkonce.t.GetViewRect__7CCamera build/view_rect.o
llvm-objdump-21 -d --section=.gnu.linkonce.t.GetViewRect__7CCamera 'extracted/SLPM_661.56;1'
```

The comparison is expected to fail with `byte mismatch (24 vs 40 bytes)`;
this research candidate is excluded from the passing reconstruction gates.
Existing section comparison already mechanically detects this mismatch. No
new parser invariant or repeatedly performed manual analysis was discovered,
so no additional test or tool is needed for this single experiment.

Executed outcomes:

- Historical compilation of the checked-in candidate: PASS; selected comparison:
  expected FAIL, 24 versus 40 bytes.
- `clang++ -std=c++98 -fsyntax-only candidates/ee_view_rect/probe.cpp`: PASS.
- `make test verify-boot verify-source-only verify-ee`: PASS (27 unit tests,
  existing candidate syntax checks, 19 matching sections / 152 bytes, full boot
  comparison, isolated pinned-hash rebuild, and existing EE probe comparison).
- `git diff --check`: PASS.

The existing EE probe gate used its up-to-date build artifacts; the new research
probe was freshly compiled. No reference hash, selected reconstruction section,
or preserved byte was changed. Shared negative knowledge and methodology were
updated; no new successful recovery mechanism warrants a `SUCCESSES.md` entry.
