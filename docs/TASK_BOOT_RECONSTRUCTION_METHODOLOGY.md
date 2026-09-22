# Boot reconstruction and compiler probes

Authority: [STANDARDS.md](STANDARDS.md), [AGENT_ENVIRONMENT.md](AGENT_ENVIRONMENT.md).
Objective: replace explicitly preserved regions with evidenced source while
retaining full boot ELF equality and honest recovery status.

## Preconditions and inputs

Read [status](STATUS.md), [work queue](WORK_QUEUE.md), successes/failures and the
relevant task notes. Require Python 3.12+, Make, Clang, sha256sum and cmp.
Comparison requires the hash-pinned extracted boot ELF; normal building does not.
Do not change `config/boot.sha256` or `config/reference.sha256` to accept new output.

## Procedure and gates

1. Inspect `preserved/boot/layout.json`, named section reports and source provenance.
   Unrecovered hex is bootstrap debt, never recovered high-level source.
2. `make build-boot` rebuilds the entire ELF using text artifacts and assembly.
   No reference or extraction command may enter this dependency graph.
3. Use known section boundaries, callers and target ABI evidence for candidates.
   Keep incomplete class layouts in `candidates/`, even when individual methods match.
4. For the EE probe, run `make setup-ee` once. Download hash and version are pinned
   in `config/ee_compiler.json`. The current `-O2` is an experimental common setting,
   not a recovered original flag. Do not tune flags separately per method.
5. `make verify-ee` stages compiler and candidate files in a native temporary
   directory, compiles, compares selected sections, reconstructs a separate full
   probe ELF and runs `cmp`. Only named methods enter that file; harness pointers
   and other object metadata are excluded by the explicit layout.
6. Run `make test verify-boot verify-source-only`; additionally run `make verify-ee`
   when touching the probe or compiler setup. Changed instructions must propagate
   into output; regression tests deliberately check that no original-byte fallback exists.
7. Update status, queue, task evidence and shared knowledge. Review source authenticity
   independently of byte matching. Commit with all five required evidence trailers.

## Tool contracts

`reconstruct_elf.py export REFERENCE SELECTION DESTINATION --hash-file HASH_FILE`
authenticates a reference and explicitly writes text source intervals plus a layout.
The destination must not exist. It preserves all unselected bytes and excludes the
selected methods from the raw sources. Use a temporary destination when checking
reproducibility; no normal build calls export. Failure may leave partial files.

`reconstruct_elf.py build SOURCES OBJECT OUTPUT` reads only the layout, its hex files
and a compiled MIPS ELF object. The layout must cover the complete output exactly
once, in order. Selected executable sections must have unique names, expected
sizes and no REL/RELA entries targeting them. Unsupported input fails nonzero.
Only after validation does it write output. This is fixed-placement reconstruction,
not a linker; address relocation, branch relaxation and arbitrary references are
not supported. The original 64-byte accessors are position-independent within this
experiment because they only return and access fields through the object argument.

`check_source_only.py` copies only Makefile, preserved text, assembly and the two
needed Python tools to a temporary tree. It builds there and compares the result
hash with the parent process's pinned baseline. It performs no network calls and
copies no reference files, existing objects or reports. It is a dependency-isolation
check, not an OS security sandbox or a claim of fully recovered source.

`setup_ee_compiler.py` downloads the pinned archive and validates exact size/SHA-256
before filtered extraction. It refuses existing destinations. Network or integrity
errors fail; extraction failure may leave a partial install. Do not retry over that
directory or change the hash. Use a fresh explicit `--destination` for diagnosis.

`run_ee_probe.py` copies the compiler and probe source directory to a temporary
filesystem, executes the configured common flags and writes the object only on
success. No ABI/source tweaks are made for host compatibility. `TMPDIR` must point
to a native filesystem suitable for the legacy 32-bit tools, not the Windows mount.
The host needs i386 runtime support; this environment already has it. Setup does
not install host packages. Installed compiler bytes are expected to remain unmodified
after verified extraction; local tampering is not separately checked on each invocation.

`compiler_evidence.py ELF` emits JSON to stdout with literal build banners, byte
offsets, preceding library strings and section membership. It makes no claim that
the library compiler was used throughout the game. Parser and staging behavior
have synthetic regression tests; the real probe provides the target integration check.

## Failure handling and completion

Preserve the verified assembly whenever a candidate fails or authenticity remains
unclear. Record mismatch, flags, evidence and attempted pathways. Legacy tool failures
on a Windows-mounted filesystem call for host-side staging, not target flag changes.
Do not insert unresolved relocatable bytes into the fixed-layout builder.

A bootstrap change is complete after full boot equality, isolated rebuild, relevant
regression tests and documented limitations. Full game completion additionally
requires the standards' authentic source/assets, full-disc and provenance gates.
