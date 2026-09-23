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
.section .gnu.linkonce.t.ClearFrameBuffer__8CRender2i,"ax",@progbits
jr $31
sw $5, 0x600($4)
.section .gnu.linkonce.t.GetBgCol__8CRender2,"ax",@progbits
jr $31
addiu $2, $4, 0x548
.section .gnu.linkonce.t.GetWipeCnt__8CRender2,"ax",@progbits
jr $31
lw $2, 0x610($4)
.section .gnu.linkonce.t.SetWipeCnt__8CRender2i,"ax",@progbits
jr $31
sw $5, 0x610($4)
.section .gnu.linkonce.t.GetFlickerFree__C8CRender2,"ax",@progbits
jr $31
lw $2, 0x578($4)
.section .gnu.linkonce.t.GetPacketCount__8CRender2,"ax",@progbits
jr $31
lw $2, 0x4c4($4)
.section .gnu.linkonce.t.GetDBuffDc__8CRender2,"ax",@progbits
jr $31
addiu $2, $4, 0x30
.section .gnu.linkonce.t.GetLightTmp__8CRender2,"ax",@progbits
jr $31
addiu $2, $4, 0x460
.section .gnu.linkonce.t.GetLightMat__8CRender2,"ax",@progbits
jr $31
addiu $2, $4, 0x3e0
.section .gnu.linkonce.t.GetLightCol__8CRender2,"ax",@progbits
jr $31
addiu $2, $4, 0x420
.section .gnu.linkonce.t.GetProjectionMatrix__8CRender2,"ax",@progbits
jr $31
addiu $2, $4, 0x360
.section .gnu.linkonce.t.GetNearClipMode__8CRender2,"ax",@progbits
jr $31
lw $2, 0x534($4)
.section .gnu.linkonce.t.GetRegState__8CRender2,"ax",@progbits
jr $31
lw $2, 0x740($4)
.section .gnu.linkonce.t.IsNearClipMode__8CRender2,"ax",@progbits
jr $31
lw $2, 0x534($4)
.section .gnu.linkonce.t.GetViewScaleX__11CGameCamera,"ax",@progbits
jr $31
lwc1 $f0, 0x17c($4)
.section .gnu.linkonce.t.GetViewScaleY__11CGameCamera,"ax",@progbits
jr $31
lwc1 $f0, 0x180($4)
.section .gnu.linkonce.t.GetSelectedChara__11CGameCamera,"ax",@progbits
jr $31
lw $2, 0x3fc($4)
.section .gnu.linkonce.t.SetCharaOfsY__11CGameCameraf,"ax",@progbits
jr $31
swc1 $f12, 0x408($4)
.section .gnu.linkonce.t.GetCamDistFuncNo__11CGameCamera,"ax",@progbits
jr $31
lw $2, 0x1a0($4)
.section .gnu.linkonce.t.GetViewAngleDir__C11CGameCamera,"ax",@progbits
jr $31
lwc1 $f0, 0x404($4)
.section .gnu.linkonce.t.GetParent__9C3dObject,"ax",@progbits
jr $31
lw $2, 0($4)
.section .gnu.linkonce.t.GetFirstChild__9C3dObject,"ax",@progbits
jr $31
lw $2, 4($4)
.section .gnu.linkonce.t.GetNextChild__9C3dObjectP9C3dObject,"ax",@progbits
jr $31
lw $2, 8($5)
.section .gnu.linkonce.t.SetLinkBoneMat__9C3dObjectP9objMatrix,"ax",@progbits
jr $31
sw $5, 0x10($4)
.section .gnu.linkonce.t.GetLinkBoneMat__9C3dObject,"ax",@progbits
jr $31
lw $2, 0x10($4)
.section .gnu.linkonce.t._GetLocalMat__C9C3dObjecti,"ax",@progbits
jr $31
addiu $2, $4, 0x20
.section .gnu.linkonce.t._GetWorldMat__C9C3dObjecti,"ax",@progbits
jr $31
addiu $2, $4, 0x60
.section .gnu.linkonce.t.DirectWorldMatrix__9C3dObject,"ax",@progbits
jr $31
addiu $2, $4, 0x60
.section .gnu.linkonce.t.DirectWorldMatrix__C9C3dObject,"ax",@progbits
jr $31
addiu $2, $4, 0x60
.section .gnu.linkonce.t.GetRootMatrix__9C3dObject,"ax",@progbits
jr $31
addiu $2, $4, 0x20
.section .gnu.linkonce.t.GetRootMatrix__C9C3dObject,"ax",@progbits
jr $31
addiu $2, $4, 0x20
.section .gnu.linkonce.t.GetLocalMatrix__9C3dObjecti,"ax",@progbits
jr $31
addiu $2, $4, 0x20
.section .gnu.linkonce.t.Draw__9C3dObjectP7CRender,"ax",@progbits
jr $31
addiu $2, $0, 1
.section .gnu.linkonce.t.GetNowGmPadCheck__6CCharaUl,"ax",@progbits
jr $31
daddu $2, $5, $0
.section .gnu.linkonce.t.SetNextAction__6CCharai,"ax",@progbits
jr $31
sw $5, 0xfc4($4)
.section .gnu.linkonce.t.IsSyncroSeChk__6CChara,"ax",@progbits
jr $31
lw $2, 0x1090($4)
.section .gnu.linkonce.t.SetSyncroSeChk__6CCharai,"ax",@progbits
jr $31
sw $5, 0x1090($4)
.section .gnu.linkonce.t.StartActPmv__6CChara,"ax",@progbits
jr $31
lw $2, 0xfa8($4)
.section .gnu.linkonce.t.GetActPmvTgt__6CChara,"ax",@progbits
jr $31
lw $2, 0xfac($4)
.section .gnu.linkonce.t.SetHpDamageBlock__6CCharai,"ax",@progbits
jr $31
sw $5, 0x1088($4)
.section .gnu.linkonce.t.SetCurrentMove__6CCharaiii,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.GetLocate__6CChara,"ax",@progbits
jr $31
addiu $2, $4, 0x600
.section .gnu.linkonce.t.GetLocateV__6CChara,"ax",@progbits
jr $31
addiu $2, $4, 0x600
.section .gnu.linkonce.t.GetLocateV_Btm__6CChara,"ax",@progbits
jr $31
addiu $2, $4, 0x610
.section .gnu.linkonce.t.GetLocateV_Null__6CChara,"ax",@progbits
jr $31
addiu $2, $4, 0x620
.section .gnu.linkonce.t.GetNowLocate__6CChara,"ax",@progbits
jr $31
addiu $2, $4, 0x50
.section .gnu.linkonce.t.GetRotateY__6CChara,"ax",@progbits
jr $31
lwc1 $f0, 0x35c($4)
.section .gnu.linkonce.t.GetTargetAngle__6CChara,"ax",@progbits
jr $31
lwc1 $f0, 0xfb8($4)
.section .gnu.linkonce.t.GetCharSts__6CChara,"ax",@progbits
jr $31
lw $2, 0x394($4)
.section .gnu.linkonce.t.GetMyPause__6CChara,"ax",@progbits
jr $31
lw $2, 0xcd8($4)
.section .gnu.linkonce.t.GetPadDisable__6CChara,"ax",@progbits
jr $31
lw $2, 0xce4($4)
.section .gnu.linkonce.t.GetPadCnfig__6CChara,"ax",@progbits
jr $31
addiu $2, $4, 0xa28
.section .gnu.linkonce.t.GetPadChk__6CChara,"ax",@progbits
jr $31
lw $2, 0xcdc($4)
.section .gnu.linkonce.t.GetPadChk2__6CChara,"ax",@progbits
jr $31
lw $2, 0xce0($4)
.section .gnu.linkonce.t.GetPlayerType__6CChara,"ax",@progbits
jr $31
lw $2, 0xfcc($4)
.section .gnu.linkonce.t.GetActTblC__6CChara,"ax",@progbits
jr $31
lw $2, 0xcfc($4)
.section .gnu.linkonce.t.GetActTblBase__6CChara,"ax",@progbits
jr $31
lw $2, 0xcf8($4)
.section .gnu.linkonce.t.GetPadOffMask__6CChara,"ax",@progbits
jr $31
lw $2, 0xce8($4)
.section .gnu.linkonce.t.GetTarget__6CChara,"ax",@progbits
jr $31
lw $2, 0xcf4($4)
.section .gnu.linkonce.t.GetTargetModel__6CChara,"ax",@progbits
jr $31
lw $2, 0xcf4($4)
.section .gnu.linkonce.t.GetCurrentArmNo__6CChara,"ax",@progbits
jr $31
lw $2, 0xf74($4)
.section .gnu.linkonce.t.GetPadNo__6CChara,"ax",@progbits
jr $31
lw $2, 0xd40($4)
.section .gnu.linkonce.t.GetPadNoReal__6CChara,"ax",@progbits
jr $31
lw $2, 0xd44($4)
.section .gnu.linkonce.t.GetBonusFlg__6CChara,"ax",@progbits
jr $31
lw $2, 0xd1c($4)
.section .gnu.linkonce.t.GetArmUseCnt__6CChara,"ax",@progbits
jr $31
lw $2, 0xcec($4)
.section .gnu.linkonce.t.GetPadType__6CChara,"ax",@progbits
jr $31
lw $2, 0xcd0($4)
.section .gnu.linkonce.t.GetLastSyncRate__6CChara,"ax",@progbits
jr $31
lwc1 $f0, 0xf78($4)
.section .gnu.linkonce.t.GetLastSyncRateMax__6CChara,"ax",@progbits
jr $31
lwc1 $f0, 0xf7c($4)
.section .gnu.linkonce.t.GetChrParam__C6CChara,"ax",@progbits
jr $31
lw $2, 0xf50($4)
.section .gnu.linkonce.t.SetPadOffMask__6CCharai,"ax",@progbits
jr $31
sw $5, 0xce8($4)
.section .gnu.linkonce.t.SetAutoGuard__6CCharai,"ax",@progbits
jr $31
sw $5, 0xfc8($4)
.section .gnu.linkonce.t.GetCharCol__10CCharaBase,"ax",@progbits
jr $31
lw $2, 0x430($4)
.section .gnu.linkonce.t.GetCharColG__10CCharaBase,"ax",@progbits
jr $31
lw $2, 0x434($4)
.section .gnu.linkonce.t.GetCharColK__10CCharaBase,"ax",@progbits
jr $31
lw $2, 0x438($4)
.section .gnu.linkonce.t.GetCharSe__10CCharaBase,"ax",@progbits
jr $31
addiu $2, $4, 0x504
.section .gnu.linkonce.t.GetIndex__10CCharaBase,"ax",@progbits
jr $31
lw $2, 0x368($4)
.section .gnu.linkonce.t.GetDataIdx__10CCharaBase,"ax",@progbits
jr $31
lw $2, 0x36c($4)
.section .gnu.linkonce.t.GetCharNo__10CCharaBase,"ax",@progbits
jr $31
lw $2, 0x370($4)
.section .gnu.linkonce.t.GetColorNo__10CCharaBase,"ax",@progbits
jr $31
lw $2, 0x374($4)
.section .gnu.linkonce.t.GetCharDataSts__10CCharaBase,"ax",@progbits
jr $31
lw $2, 0x394($4)
.section .gnu.linkonce.t.GetShadow__10CCharaBase,"ax",@progbits
jr $31
lw $2, 0x3a0($4)
.section .gnu.linkonce.t.GetCastIndex__10CCharaBase,"ax",@progbits
jr $31
lw $2, 0x384($4)
.section .gnu.linkonce.t.SetCastIndex__10CCharaBasei,"ax",@progbits
jr $31
sw $5, 0x384($4)
.section .gnu.linkonce.t.SetMotionSpeed__10CCharaBasef,"ax",@progbits
jr $31
swc1 $f12, 0x440($4)
.section .gnu.linkonce.t.GetCurrentWeapon__10CCharaBase,"ax",@progbits
jr $31
lw $2, 0x40c($4)
.section .gnu.linkonce.t.GetCurrentWeaponTmp__10CCharaBase,"ax",@progbits
jr $31
lw $2, 0x410($4)
.section .gnu.linkonce.t.GetCurWeaponSnd__10CCharaBase,"ax",@progbits
jr $31
lw $2, 0x414($4)
.section .gnu.linkonce.t.GetDoukiParent__10CCharaBase,"ax",@progbits
jr $31
lw $2, 0x310($4)
.section .gnu.linkonce.t.SetCurrentAct__10CCharaBaseiii,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.SetCurrentStatus__10CCharaBaseiiP12TypeArmParami,"ax",@progbits
jr $31
daddu $2, $0, $0
.section .gnu.linkonce.t.SetCurrentOwnCtrl__10CCharaBasei,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.SetCurrentMove__10CCharaBaseiii,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.GetActTblC__10CCharaBase,"ax",@progbits
jr $31
daddu $2, $0, $0
.section .gnu.linkonce.t.GetActTblBase__10CCharaBase,"ax",@progbits
jr $31
daddu $2, $0, $0
.section .gnu.linkonce.t.GetTargetModel__10CCharaBase,"ax",@progbits
jr $31
daddu $2, $0, $0
.section .gnu.linkonce.t.CalcDamage__10CCharaBasefi,"ax",@progbits
jr $31
mov.s $f0, $f12
.section .gnu.linkonce.t.CheckPadPress__10CCharaBaseUi,"ax",@progbits
jr $31
daddu $2, $0, $0
.section .gnu.linkonce.t.CheckPadOn__10CCharaBaseUi,"ax",@progbits
jr $31
daddu $2, $0, $0
.section .gnu.linkonce.t.GetRotY__10CCharaBase,"ax",@progbits
jr $31
lwc1 $f0, 0x35c($4)
.section .gnu.linkonce.t.GetBipRotY__10CCharaBase,"ax",@progbits
jr $31
lwc1 $f0, 0x360($4)
.section .gnu.linkonce.t.GetBaseModel__10CCharaBase,"ax",@progbits
jr $31
lw $2, 0x340($4)
.section .gnu.linkonce.t.GetNowMotion__10CCharaBase,"ax",@progbits
jr $31
lw $2, 0x1bc($4)
.section .gnu.linkonce.t.PreNutralMotionJump__10CCharaBase,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.PreAction2__10CCharaBase,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.HitCheckAll__10CCharaBase,"ax",@progbits
jr $31
daddu $2, $0, $0
.section .gnu.linkonce.t.ActionCntrl__10CCharaBase,"ax",@progbits
jr $31
daddu $2, $0, $0
.section .gnu.linkonce.t.IsDoukiAct__10CCharaBasei,"ax",@progbits
jr $31
daddu $2, $0, $0
.section .gnu.linkonce.t.ActionCntrlExcute__10CCharaBasei,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.PreUpdatePmv__10CCharaBasef,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.SetYhoseiOffPmv__10CCharaBasei,"ax",@progbits
jr $31
sw $5, 0x5f0($4)
.section .gnu.linkonce.t.SetYbaseSetPmv__10CCharaBasei,"ax",@progbits
jr $31
sw $5, 0x5f4($4)
.section .gnu.linkonce.t.GetCharCom__10CCharaBase,"ax",@progbits
jr $31
lw $2, 0x5ec($4)
.section .gnu.linkonce.t.GetChara__7CWeapon,"ax",@progbits
jr $31
lw $2, 0x8($4)
.section .gnu.linkonce.t.GetArmParam__7CWeapon,"ax",@progbits
jr $31
lw $2, 0x0($4)
.section .gnu.linkonce.t.GetLinkBoneType__7CWeapon,"ax",@progbits
jr $31
lw $2, 0xc($4)
.section .gnu.linkonce.t.IsSubWeapon__7CWeapon,"ax",@progbits
jr $31
lw $2, 0x1c($4)
.section .gnu.linkonce.t.GetArmType__7CWeapon,"ax",@progbits
jr $31
lw $2, 0x14($4)
.section .gnu.linkonce.t.GetTblNo__7CWeapon,"ax",@progbits
jr $31
lw $2, 0x18($4)
.section .gnu.linkonce.t.SetPmv__7CWeaponi,"ax",@progbits
jr $31
sw $5, 0x20($4)
.section .gnu.linkonce.t.InitWeapon__7CWeapon,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.InitColFlag__7CWeapon,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.SetAttackFlag__7CWeaponi,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.SetCatchFlag__7CWeaponi,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.GetCol__7CWeaponi,"ax",@progbits
jr $31
daddu $2, $0, $0
.section .gnu.linkonce.t.SetSubMotion__7CWeaponG8MotionNoif,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.SetWeapon__7CWeaponi,"ax",@progbits
jr $31
daddu $2, $0, $0
.section .gnu.linkonce.t.ResetWeapon__7CWeapon,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.IsAirAction__7CWeapon,"ax",@progbits
jr $31
daddu $2, $0, $0
.section .gnu.linkonce.t.SetEffect__7CWeaponii,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.SetWeponCng__7CWeapon,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.ReSetWeponCng__7CWeapon,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.ActionUpdate__7CWeapon,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.DebRender__7CWeapon,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.RenderN__7CWeapon,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.RenderA__7CWeapon,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.RenderE__7CWeapon,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.GetModel__7CWeapon,"ax",@progbits
jr $31
daddu $2, $0, $0
.section .gnu.linkonce.t.GetSubModelNum__7CWeaponi,"ax",@progbits
jr $31
daddu $2, $0, $0
.section .gnu.linkonce.t.SetCurrentSubModel__7CWeaponii,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.OnOpenNewMotion__8CMotion3,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.GetLoopCount__8CMotion3,"ax",@progbits
jr $31
lw $2, 0xe4($4)
.section .gnu.linkonce.t.IsLoop__8CMotion3,"ax",@progbits
jr $31
lw $2, 0xec($4)
.section .gnu.linkonce.t.GetDataBase__8CMotion3,"ax",@progbits
jr $31
lw $2, 0xa4($4)
.section .gnu.linkonce.t.GetMotionNo__8CMotion3,"ax",@progbits
jr $31
lw $2, 0xbc($4)
.section .gnu.linkonce.t.GetSubMotionNo__8CMotion3,"ax",@progbits
jr $31
lw $2, 0xc0($4)
.section .gnu.linkonce.t.GetMotionIndex__8CMotion3,"ax",@progbits
jr $31
lw $2, 0xc4($4)
.section .gnu.linkonce.t.GetNextMotionNo__8CMotion3,"ax",@progbits
jr $31
lw $2, 0xc8($4)
.section .gnu.linkonce.t.GetNextSubMotionNo__8CMotion3,"ax",@progbits
jr $31
lw $2, 0xcc($4)
.section .gnu.linkonce.t.GetNextIndex__8CMotion3,"ax",@progbits
jr $31
lw $2, 0xd0($4)
.section .gnu.linkonce.t.GetNextMotionNoS__8CMotion3,"ax",@progbits
jr $31
lw $2, 0xd4($4)
.section .gnu.linkonce.t.GetNextSubMotionNoS__8CMotion3,"ax",@progbits
jr $31
lw $2, 0xd8($4)
.section .gnu.linkonce.t.GetNextIndexS__8CMotion3,"ax",@progbits
jr $31
lw $2, 0xdc($4)
.section .gnu.linkonce.t.SetNextJumpDC__8CMotion3P8CMotion3,"ax",@progbits
jr $31
sw $5, 0xb8($4)
.section .gnu.linkonce.t.GetNextFrame__8CMotion3,"ax",@progbits
jr $31
lwc1 $f0, 0xb0($4)
.section .gnu.linkonce.t.GetNextLabel__8CMotion3,"ax",@progbits
jr $31
lw $2, 0xb4($4)
.section .gnu.linkonce.t.GetJumpMode__8CMotion3,"ax",@progbits
jr $31
lw $2, 0xe0($4)
.section .gnu.linkonce.t.IsError__8CMotion3,"ax",@progbits
jr $31
lw $2, 0xf0($4)
.section .gnu.linkonce.t.GetModel__7CMotion,"ax",@progbits
jr $31
lw $2, 0x8($4)
.section .gnu.linkonce.t.SetInterpolateType__7CMotion10InterpType,"ax",@progbits
jr $31
sw $5, 0x0($4)
.section .gnu.linkonce.t.SetScaleEnable__7CMotioni,"ax",@progbits
jr $31
sw $5, 0x4($4)
.section .gnu.linkonce.t.EnableColorMotion__7CMotioni,"ax",@progbits
jr $31
sw $5, 0x60($4)
.section .gnu.linkonce.t.IsEnableColorMotion__7CMotion,"ax",@progbits
jr $31
lw $2, 0x60($4)
.section .gnu.linkonce.t.GetTargetType__7CMotion,"ax",@progbits
jr $31
lw $2, 0x58($4)
.section .gnu.linkonce.t.SetTargetType__7CMotion16MotionTargetType,"ax",@progbits
jr $31
sw $5, 0x58($4)
.section .gnu.linkonce.t.GetFrame__7CMotion,"ax",@progbits
jr $31
lwc1 $f0, 0x18($4)
.section .gnu.linkonce.t.GetAddFrame__7CMotion,"ax",@progbits
jr $31
lwc1 $f0, 0x1c($4)
.section .gnu.linkonce.t.GetMotion__7CMotion,"ax",@progbits
jr $31
lw $2, 0x24($4)
.section .gnu.linkonce.t.GetAttribute__7CMotion,"ax",@progbits
jr $31
lw $2, 0xc($4)
.section .gnu.linkonce.t.GetNowAttributeClass__7CMotion,"ax",@progbits
jr $31
addiu $2, $4, 0xc
.section .gnu.linkonce.t.IsEndMotion__7CMotion,"ax",@progbits
jr $31
lw $2, 0x50($4)
.section .gnu.linkonce.t.GetLinkBone__7CMotion,"ax",@progbits
jr $31
lw $2, 0x48($4)
.section .gnu.linkonce.t.GetStartCntrlMode__10CGameCntrl,"ax",@progbits
jr $31
addiu $2, $0, 0xa
.section .gnu.linkonce.t.StartDataInitialize__10CGameCntrl,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.StartDataInitializeAfter__10CGameCntrl,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.DataInitalizeEx__10CGameCntrl,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.CheckActCntrl__10CGameCntrl,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.PreActionCntrlFr__10CGameCntrl,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.AfterActionCntrlFr__10CGameCntrl,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.CheckThrowPause__10CGameCntrl,"ax",@progbits
jr $31
daddu $2, $0, $0
.section .gnu.linkonce.t.SetReturnStatus__10CGameCntrl,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.GetActBoyake__10CGameCntrl,"ax",@progbits
jr $31
lw $2, 0x40($4)
.section .gnu.linkonce.t.IsGameOver__10CGameCntrl,"ax",@progbits
jr $31
daddu $2, $0, $0
.section .gnu.linkonce.t.ActionCntrl__10CGameCntrl,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.GetPauseMenu__10CGameCntrl,"ax",@progbits
jr $31
daddu $2, $0, $0
.section .gnu.linkonce.t.PauseMenuAction__10CGameCntrl,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.GetPMovie__8CPAppear,"ax",@progbits
jr $31
lw $2, 0x90($4)
.section .gnu.linkonce.t.GetParent__8CPAppear,"ax",@progbits
jr $31
lw $2, 0x9c($4)
.section .gnu.linkonce.t.GetYpcHead__8CPAppear,"ax",@progbits
jr $31
lw $2, 0x94($4)
.section .gnu.linkonce.t.GetNodeData__8CPAppear,"ax",@progbits
jr $31
lw $2, 0x98($4)
.section .gnu.linkonce.t.GetLocalMatrix__8CPAppear,"ax",@progbits
jr $31
addiu $2, $4, 0x10
.section .gnu.linkonce.t.GetWorldMatrix__8CPAppear,"ax",@progbits
jr $31
addiu $2, $4, 0x50
.section .gnu.linkonce.t.GetSceneTargetLink__8CPAppear,"ax",@progbits
jr $31
addiu $2, $4, 0x26c
.section .gnu.linkonce.t.GetActionLink__8CPAppear,"ax",@progbits
jr $31
addiu $2, $4, 0x260
.section .gnu.linkonce.t.GetFrame__8CPAppear,"ax",@progbits
jr $31
lwc1 $f0, 0x25c($4)
.section .gnu.linkonce.t.IsDisplay__8CPAppear,"ax",@progbits
jr $31
lw $2, 0x258($4)
.section .gnu.linkonce.t.IsMotionEnd__8CPAppear,"ax",@progbits
jr $31
lw $2, 0x254($4)
.section .gnu.linkonce.t.OnMotionJumpPre__8CPAppearP9AprMotionT1,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.OnMotionJumpAfter__8CPAppearP9AprMotionT1,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.StatusCngAttrCheck__13CCharaDataSts,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.StatusCheck__13CCharaDataSts,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.StatusCheckPmv__13CCharaDataSts,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.StatusJmpParam__13CCharaDataSts,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.OnJmpMotion__13CCharaDataSts,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.InitializeStatDataEx__13CCharaDataSts,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.InitializeDataEx__13CCharaDataSts,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.CheckGatyaStsArm__13CCharaDataSts9SArmTypeD,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.GetPrgSts__13CCharaDataSts,"ax",@progbits
jr $31
addiu $2, $4, 0x180
.section .gnu.linkonce.t.SetNowMotNo__13CCharaDataStsi,"ax",@progbits
jr $31
sw $5, 0xad0($4)
.section .gnu.linkonce.t.PreNutralJump__13CCharaDataSts,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.ReturnArmObj__13CCharaDataSts,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.SetMotSts__8CMotionCP10CMotionSts,"ax",@progbits
jr $31
sw $5, 0xf4($4)
.section .gnu.linkonce.t.SetActTbl__8CMotionCP7CActTbl,"ax",@progbits
jr $31
sw $5, 0xf8($4)
.section .gnu.linkonce.t.SetParent__8CMotionCP8CMotionC,"ax",@progbits
jr $31
sw $5, 0x100($4)
.section .gnu.linkonce.t.SetChild__8CMotionCP8CMotionC,"ax",@progbits
jr $31
sw $5, 0x104($4)
.section .gnu.linkonce.t.SetSubChild__8CMotionCP8CMotionC,"ax",@progbits
jr $31
sw $5, 0x108($4)
.section .gnu.linkonce.t.SetParentAddFr__8CMotionCP8CMotionC,"ax",@progbits
jr $31
sw $5, 0x10c($4)
.section .gnu.linkonce.t.SetChildAddFr__8CMotionCP8CMotionC,"ax",@progbits
jr $31
sw $5, 0x110($4)
.section .gnu.linkonce.t.SetSubChildAddFr__8CMotionCP8CMotionC,"ax",@progbits
jr $31
sw $5, 0x114($4)
.section .gnu.linkonce.t.PreAction__12ActionObject,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.Action__12ActionObject,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.ActionM__12ActionObject,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.ReAction__12ActionObject,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.GetDispPosE__12ActionObject,"ax",@progbits
jr $31
lw $2, 0x10($4)
.section .gnu.linkonce.t.GetDispPosZ__12ActionObject,"ax",@progbits
jr $31
lwc1 $f0, 0x14($4)
.section .gnu.linkonce.t.Display__12ActionObject,"ax",@progbits
jr $31
daddu $2, $0, $0
.section .gnu.linkonce.t.Reset__12ActionObject,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.SetMaterialCol__12ActionObjectf,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.GetHitSE__12ActionObject,"ax",@progbits
jr $31
addiu $2, $0, -0x1
.section .gnu.linkonce.t.GetOwner__4CCol,"ax",@progbits
jr $31
lw $2, 0x24($4)
.section .gnu.linkonce.t.GetKind__4CCol,"ax",@progbits
jr $31
lw $2, 0x50($4)
.section .gnu.linkonce.t.GetColNum__4CCol,"ax",@progbits
jr $31
lw $2, 0xc($4)
.section .gnu.linkonce.t.GetBoundingSphere__4CCol,"ax",@progbits
jr $31
addiu $2, $4, 0x14
.section .gnu.linkonce.t.GetUpper__4CCol,"ax",@progbits
jr $31
lwc1 $f0, 0x44($4)
.section .gnu.linkonce.t.GetLower__4CCol,"ax",@progbits
jr $31
lwc1 $f0, 0x34($4)
.section .gnu.linkonce.t.GetMin__4CCol,"ax",@progbits
jr $31
addiu $2, $4, 0x30
.section .gnu.linkonce.t.GetMax__4CCol,"ax",@progbits
jr $31
addiu $2, $4, 0x40
.section .gnu.linkonce.t.CallBack__4CColP4CColiiP14ColCheckResultT4,"ax",@progbits
jr $31
daddu $2, $0, $0
.section .gnu.linkonce.t.Draw2D__13ArmEffectBase,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.HitAfter__13ArmEffectBase,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.GetChara__13ArmEffectBase,"ax",@progbits
jr $31
lw $2, 0x7c($4)
.section .gnu.linkonce.t.GetType__13ArmEffectBase,"ax",@progbits
jr $31
lw $2, 0x88($4)
.section .gnu.linkonce.t.ActionSameType__13ArmEffectBase,"ax",@progbits
jr $31
nop
.section .gnu.linkonce.t.SetType__13ArmEffectBase13ArmEffectType,"ax",@progbits
jr $31
sw $5, 0x88($4)
.section .gnu.linkonce.t.GetPos__13ArmEffectBase,"ax",@progbits
jr $31
daddu $2, $4, $0
.section .gnu.linkonce.t.GetArmParam__13ArmEffectBase,"ax",@progbits
jr $31
lw $2, 0x84($4)
.section .gnu.linkonce.t.GetBody__10CSubObject,"ax",@progbits
jr $31
addiu $2, $4, 0x10
.section .gnu.linkonce.t.GetOriginal__10CSubObject,"ax",@progbits
jr $31
lw $2, 0xc($4)
.section .gnu.linkonce.t.GetFlags__10CSubObject,"ax",@progbits
jr $31
lw $2, 0x90($4)
.section .gnu.linkonce.t.GetVertexListNum__10CSubObject,"ax",@progbits
jr $31
lw $2, 0x10($4)
.section .gnu.linkonce.t.GetPrimListNum__10CSubObject,"ax",@progbits
jr $31
lw $2, 0x14($4)
.section .gnu.linkonce.t.GetObjType__12CPDataArmObj,"ax",@progbits
jr $31
lw $2, 0x10c($4)
.section .gnu.linkonce.t.GetObjIdx__12CPDataArmObj,"ax",@progbits
jr $31
lw $2, 0x110($4)
.section .gnu.linkonce.t.GetArmNo__12CPDataArmObj,"ax",@progbits
jr $31
lw $2, 0x118($4)
.section .gnu.linkonce.t.GetArmMdlNo__12CPDataArmObj,"ax",@progbits
jr $31
lw $2, 0x11c($4)
.section .gnu.linkonce.t.GetCharNo__12CPDataArmObj,"ax",@progbits
jr $31
lw $2, 0x114($4)
.section .gnu.linkonce.t.GetSclBoneNo__12CPDataArmObj,"ax",@progbits
jr $31
lw $2, 0x124($4)
.section .gnu.linkonce.t.GetHitTgt__7CActTgt,"ax",@progbits
jr $31
lw $2, 0x318($4)
.section .gnu.linkonce.t.GetTgtArmNo__7CActTgt,"ax",@progbits
jr $31
lw $2, 0x2d8($4)
.section .gnu.linkonce.t.CheckEndType__7CActTgt,"ax",@progbits
jr $31
lw $2, 0x30c($4)
.section .gnu.linkonce.t.GetActTgtParam__7CActTgt,"ax",@progbits
jr $31
addiu $2, $4, 0x2d0
.section .gnu.linkonce.t.IsExtraDmg__7CActTgt,"ax",@progbits
jr $31
lw $2, 0x334($4)
.section .gnu.linkonce.t.GetTgtNo__7CActTgt,"ax",@progbits
jr $31
lw $2, 0x2d4($4)
.section .gnu.linkonce.t.GetGetArm__16Labyrinth_ArmGet,"ax",@progbits
jr $31
addiu $2, $4, 0xe8
.section .gnu.linkonce.t.GetDelArm__16Labyrinth_ArmGet,"ax",@progbits
jr $31
lw $2, 0xfc($4)
.section .gnu.linkonce.t.SetDelArm__16Labyrinth_ArmGeti,"ax",@progbits
jr $31
sw $5, 0xfc($4)
.section .gnu.linkonce.t.GetMoney__16Labyrinth_ArmGet,"ax",@progbits
jr $31
lw $2, 0x100($4)
.section .gnu.linkonce.t.IsFullBag__16Labyrinth_ArmGet,"ax",@progbits
jr $31
lw $2, 0xf8($4)
.section .gnu.linkonce.t.GetCheckChar__16Labyrinth_ArmGet,"ax",@progbits
jr $31
lh $2, 0x11c($4)
.section .gnu.linkonce.t.GetRoutine__16Labyrinth_ArmGet,"ax",@progbits
jr $31
lw $2, 0xdc($4)
