# Preserved lower-level implementations. Section names come from the input ELF.
# Only these standard MIPS instructions have been validated with this assembler.
.set noreorder
.set noat

.section .gnu.linkonce.t.GetNearClipPlane__7CCamera,"ax",@progbits
jr $31
lwc1 $f0, 0x16c($4)
.section .gnu.linkonce.t.GetFarClipPlane__7CCamera,"ax",@progbits
jr $31
lwc1 $f0, 0x170($4)
.section .gnu.linkonce.t.SetFogMode__7CCamerai,"ax",@progbits
jr $31
sw $5, 0x184($4)
.section .gnu.linkonce.t.GetFogMode__7CCamera,"ax",@progbits
jr $31
lw $2, 0x184($4)
.section .gnu.linkonce.t.SetFogDistance__7CCameraf,"ax",@progbits
jr $31
swc1 $f12, 0x188($4)
.section .gnu.linkonce.t.GetFogDistance__7CCamera,"ax",@progbits
jr $31
lwc1 $f0, 0x188($4)
.section .gnu.linkonce.t.SetFogConcentration__7CCameraf,"ax",@progbits
jr $31
swc1 $f12, 0x18c($4)
.section .gnu.linkonce.t.GetFogConcentration__7CCamera,"ax",@progbits
jr $31
lwc1 $f0, 0x18c($4)
