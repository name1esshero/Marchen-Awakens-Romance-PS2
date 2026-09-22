# Negative knowledge

Authority: [STANDARDS.md](STANDARDS.md).

## Host GNU objdump is not a target disassembler

Hypothesis: the installed `objdump` could inspect the MIPS code because `readelf`
could read its ELF headers. `objdump -i` instead lists only x86/iamcu architectures.
ELF metadata inspection and instruction decoding have different target requirements.
Use the installed `llvm-objdump-21` for the evidenced accessor instructions.
This does not establish complete R5900 decoding support in LLVM, nor prevent use
of a separately installed R5900-aware GNU toolchain later.

No original-compiler matching experiment has yet been run. An unresolved compiler
identity is not evidence that natural source cannot match.
