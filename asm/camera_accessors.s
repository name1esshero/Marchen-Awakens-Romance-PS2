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
.section .gnu.linkonce.t.GetViewScaleX__7CCamera,"ax",@progbits
jr $31
lwc1 $f0, 0x17c($4)
.section .gnu.linkonce.t.GetViewScaleY__7CCamera,"ax",@progbits
jr $31
lwc1 $f0, 0x180($4)
.section .gnu.linkonce.t.GetViewAngle__C7CCamera,"ax",@progbits
jr $31
lwc1 $f0, 0x178($4)
.section .gnu.linkonce.t.GetViewAngleDir__C7CCamera,"ax",@progbits
jr $31
lwc1 $f0, 0x178($4)
.section .gnu.linkonce.t.Draw__7CCameraP7CRender,"ax",@progbits
jr $31
addiu $2, $0, 1
.section .gnu.linkonce.t.CameraControl__8CCamera2f,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.GetAngleY__8CCamera2,"ax",@progbits
jr $31
lwc1 $f0, 0x15c($4)
.section .gnu.linkonce.t.GetAngleX__8CCamera2,"ax",@progbits
jr $31
lwc1 $f0, 0x160($4)
.section .gnu.linkonce.t.DebugCamera__8CCamera2ii,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.GetTgtChr__9CCameraMv,"ax",@progbits
jr $31
lw $2, 0x294($4)
.section .gnu.linkonce.t.GetCamType__9CCameraMv,"ax",@progbits
jr $31
lw $2, 0x234($4)
.section .gnu.linkonce.t.GetFrameBufferMode__C7CRender,"ax",@progbits
jr $31
lw $2, 0x4e4($4)
.section .gnu.linkonce.t.GetZBufferMode__C7CRender,"ax",@progbits
jr $31
lw $2, 0x4e8($4)
.section .gnu.linkonce.t.GetFrameField__C7CRender,"ax",@progbits
jr $31
lw $2, 0x4f4($4)
.section .gnu.linkonce.t.GetScreenWidth__C7CRender,"ax",@progbits
jr $31
lw $2, 0x4f8($4)
.section .gnu.linkonce.t.GetScreenHeight__C7CRender,"ax",@progbits
jr $31
lw $2, 0x4fc($4)
.section .gnu.linkonce.t.GetOldOddEven__C7CRender,"ax",@progbits
jr $31
lw $2, 0x55c($4)
.section .gnu.linkonce.t.GetFrame__C7CRender,"ax",@progbits
jr $31
lw $2, 0x4c8($4)
.section .gnu.linkonce.t.GetCamera__7CRender,"ax",@progbits
jr $31
lw $2, 0x4e0($4)
.section .gnu.linkonce.t.GetPRMODE__7CRender,"ax",@progbits
jr $31
addiu $2, $4, 0x4a0
.section .gnu.linkonce.t.GetFreeList__7CRender,"ax",@progbits
jr $31
lw $2, 0x554($4)
