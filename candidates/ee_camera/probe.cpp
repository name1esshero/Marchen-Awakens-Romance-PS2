// Harness only: taking member addresses requires out-of-line definitions of the
// inline functions. These pointers are not recovered game data and are never
// inserted into the reconstructed executable. No codegen attributes or assembly.
#include "CCamera.h"

float (CCamera::*gGetNearClipPlaneAddress)() = &CCamera::GetNearClipPlane;
float (CCamera::*gGetFarClipPlaneAddress)() = &CCamera::GetFarClipPlane;
int (CCamera::*gGetFogModeAddress)() = &CCamera::GetFogMode;
void (CCamera::*gSetFogModeAddress)(int) = &CCamera::SetFogMode;
float (CCamera::*gGetFogDistanceAddress)() = &CCamera::GetFogDistance;
void (CCamera::*gSetFogDistanceAddress)(float) = &CCamera::SetFogDistance;
float (CCamera::*gGetFogConcentrationAddress)() = &CCamera::GetFogConcentration;
void (CCamera::*gSetFogConcentrationAddress)(float) = &CCamera::SetFogConcentration;
float (CCamera::*gGetViewScaleXAddress)() = &CCamera::GetViewScaleX;
float (CCamera::*gGetViewScaleYAddress)() = &CCamera::GetViewScaleY;
float (CCamera::*gGetViewAngleAddress)() const = &CCamera::GetViewAngle;
float (CCamera::*gGetViewAngleDirAddress)() const = &CCamera::GetViewAngleDir;
int (CCamera::*gDrawAddress)(CRender *) = &CCamera::Draw;

void (CCamera2::*gCameraControlAddress)(float) = &CCamera2::CameraControl;
float (CCamera2::*gGetAngleYAddress)() = &CCamera2::GetAngleY;
float (CCamera2::*gGetAngleXAddress)() = &CCamera2::GetAngleX;
void (CCamera2::*gDebugCameraAddress)(int, int) = &CCamera2::DebugCamera;

int (CCameraMv::*gGetTgtChrAddress)() = &CCameraMv::GetTgtChr;
int (CCameraMv::*gGetCamTypeAddress)() = &CCameraMv::GetCamType;

void *(CRender::*gGetPRMODEAddress)() = &CRender::GetPRMODE;
int (CRender::*gGetFrameAddress)() const = &CRender::GetFrame;
CCamera *(CRender::*gGetCameraAddress)() = &CRender::GetCamera;
int (CRender::*gGetFrameBufferModeAddress)() const = &CRender::GetFrameBufferMode;
int (CRender::*gGetZBufferModeAddress)() const = &CRender::GetZBufferMode;
int (CRender::*gGetFrameFieldAddress)() const = &CRender::GetFrameField;
int (CRender::*gGetScreenWidthAddress)() const = &CRender::GetScreenWidth;
int (CRender::*gGetScreenHeightAddress)() const = &CRender::GetScreenHeight;
void *(CRender::*gGetFreeListAddress)() = &CRender::GetFreeList;
int (CRender::*gGetOldOddEvenAddress)() const = &CRender::GetOldOddEven;

void *(CRender2::*gGetDBuffDcAddress)() = &CRender2::GetDBuffDc;
void *(CRender2::*gGetProjectionMatrixAddress)() = &CRender2::GetProjectionMatrix;
void *(CRender2::*gGetLightMatAddress)() = &CRender2::GetLightMat;
void *(CRender2::*gGetLightColAddress)() = &CRender2::GetLightCol;
void *(CRender2::*gGetLightTmpAddress)() = &CRender2::GetLightTmp;
int (CRender2::*gGetPacketCountAddress)() = &CRender2::GetPacketCount;
int (CRender2::*gGetNearClipModeAddress)() = &CRender2::GetNearClipMode;
int (CRender2::*gIsNearClipModeAddress)() = &CRender2::IsNearClipMode;
void *(CRender2::*gGetBgColAddress)() = &CRender2::GetBgCol;
int (CRender2::*gGetFlickerFreeAddress)() const = &CRender2::GetFlickerFree;
void (CRender2::*gClearFrameBufferAddress)(int) = &CRender2::ClearFrameBuffer;
int (CRender2::*gGetWipeCntAddress)() = &CRender2::GetWipeCnt;
void (CRender2::*gSetWipeCntAddress)(int) = &CRender2::SetWipeCnt;
int (CRender2::*gGetRegStateAddress)() = &CRender2::GetRegState;

float (CGameCamera::*gGameCameraGetViewScaleXAddress)() = &CGameCamera::GetViewScaleX;
float (CGameCamera::*gGameCameraGetViewScaleYAddress)() = &CGameCamera::GetViewScaleY;
int (CGameCamera::*gGameCameraGetCamDistFuncNoAddress)() = &CGameCamera::GetCamDistFuncNo;
void *(CGameCamera::*gGameCameraGetSelectedCharaAddress)() = &CGameCamera::GetSelectedChara;
float (CGameCamera::*gGameCameraGetViewAngleDirAddress)() const = &CGameCamera::GetViewAngleDir;
void (CGameCamera::*gGameCameraSetCharaOfsYAddress)(float) = &CGameCamera::SetCharaOfsY;

C3dObject *(C3dObject::*g3dGetParentAddress)() = &C3dObject::GetParent;
C3dObject *(C3dObject::*g3dGetFirstChildAddress)() = &C3dObject::GetFirstChild;
C3dObject *(C3dObject::*g3dGetNextChildAddress)(C3dObject *) = &C3dObject::GetNextChild;
void (C3dObject::*g3dSetLinkBoneMatAddress)(objMatrix *) = &C3dObject::SetLinkBoneMat;
objMatrix *(C3dObject::*g3dGetLinkBoneMatAddress)() = &C3dObject::GetLinkBoneMat;
const void *(C3dObject::*g3dGetLocalMatAddress)(int) const = &C3dObject::_GetLocalMat;
const void *(C3dObject::*g3dGetWorldMatAddress)(int) const = &C3dObject::_GetWorldMat;
void *(C3dObject::*g3dDirectWorldMatrixAddress)() = &C3dObject::DirectWorldMatrix;
const void *(C3dObject::*g3dDirectWorldMatrixConstAddress)() const = &C3dObject::DirectWorldMatrix;
void *(C3dObject::*g3dGetRootMatrixAddress)() = &C3dObject::GetRootMatrix;
const void *(C3dObject::*g3dGetRootMatrixConstAddress)() const = &C3dObject::GetRootMatrix;
void *(C3dObject::*g3dGetLocalMatrixAddress)(int) = &C3dObject::GetLocalMatrix;
int (C3dObject::*g3dDrawAddress)(CRender *) = &C3dObject::Draw;

unsigned long (CChara::*gCharaGetNowGmPadCheckAddress)(unsigned long) = &CChara::GetNowGmPadCheck;
void (CChara::*gCharaSetNextActionAddress)(int) = &CChara::SetNextAction;
int (CChara::*gCharaIsSyncroSeChkAddress)() = &CChara::IsSyncroSeChk;
void (CChara::*gCharaSetSyncroSeChkAddress)(int) = &CChara::SetSyncroSeChk;
void *(CChara::*gCharaStartActPmvAddress)() = &CChara::StartActPmv;
void *(CChara::*gCharaGetActPmvTgtAddress)() = &CChara::GetActPmvTgt;
void (CChara::*gCharaSetHpDamageBlockAddress)(int) = &CChara::SetHpDamageBlock;
void (CChara::*gCharaSetCurrentMoveAddress)(int, int, int) = &CChara::SetCurrentMove;
void *(CChara::*gCharaGetLocateAddress)() = &CChara::GetLocate;
void *(CChara::*gCharaGetLocateVAddress)() = &CChara::GetLocateV;
void *(CChara::*gCharaGetLocateV_BtmAddress)() = &CChara::GetLocateV_Btm;
void *(CChara::*gCharaGetLocateV_NullAddress)() = &CChara::GetLocateV_Null;
void *(CChara::*gCharaGetNowLocateAddress)() = &CChara::GetNowLocate;
float (CChara::*gCharaGetRotateYAddress)() = &CChara::GetRotateY;
float (CChara::*gCharaGetTargetAngleAddress)() = &CChara::GetTargetAngle;
int (CChara::*gCharaGetCharStsAddress)() = &CChara::GetCharSts;
int (CChara::*gCharaGetMyPauseAddress)() = &CChara::GetMyPause;
int (CChara::*gCharaGetPadDisableAddress)() = &CChara::GetPadDisable;
void *(CChara::*gCharaGetPadCnfigAddress)() = &CChara::GetPadCnfig;
int (CChara::*gCharaGetPadChkAddress)() = &CChara::GetPadChk;
int (CChara::*gCharaGetPadChk2Address)() = &CChara::GetPadChk2;
int (CChara::*gCharaGetPlayerTypeAddress)() = &CChara::GetPlayerType;
void *(CChara::*gCharaGetActTblCAddress)() = &CChara::GetActTblC;
void *(CChara::*gCharaGetActTblBaseAddress)() = &CChara::GetActTblBase;
int (CChara::*gCharaGetPadOffMaskAddress)() = &CChara::GetPadOffMask;
void *(CChara::*gCharaGetTargetAddress)() = &CChara::GetTarget;
void *(CChara::*gCharaGetTargetModelAddress)() = &CChara::GetTargetModel;
int (CChara::*gCharaGetCurrentArmNoAddress)() = &CChara::GetCurrentArmNo;
int (CChara::*gCharaGetPadNoAddress)() = &CChara::GetPadNo;
int (CChara::*gCharaGetPadNoRealAddress)() = &CChara::GetPadNoReal;
int (CChara::*gCharaGetBonusFlgAddress)() = &CChara::GetBonusFlg;
int (CChara::*gCharaGetArmUseCntAddress)() = &CChara::GetArmUseCnt;
int (CChara::*gCharaGetPadTypeAddress)() = &CChara::GetPadType;
float (CChara::*gCharaGetLastSyncRateAddress)() = &CChara::GetLastSyncRate;
float (CChara::*gCharaGetLastSyncRateMaxAddress)() = &CChara::GetLastSyncRateMax;
void *(CChara::*gCharaGetChrParamAddress)() const = &CChara::GetChrParam;
void (CChara::*gCharaSetPadOffMaskAddress)(int) = &CChara::SetPadOffMask;
void (CChara::*gCharaSetAutoGuardAddress)(int) = &CChara::SetAutoGuard;

void *(CCharaBase::*gCBaseGetCharColAddress)() = &CCharaBase::GetCharCol;
int (CCharaBase::*gCBaseGetCharColGAddress)() = &CCharaBase::GetCharColG;
int (CCharaBase::*gCBaseGetCharColKAddress)() = &CCharaBase::GetCharColK;
void *(CCharaBase::*gCBaseGetCharSeAddress)() = &CCharaBase::GetCharSe;
int (CCharaBase::*gCBaseGetIndexAddress)() = &CCharaBase::GetIndex;
int (CCharaBase::*gCBaseGetDataIdxAddress)() = &CCharaBase::GetDataIdx;
int (CCharaBase::*gCBaseGetCharNoAddress)() = &CCharaBase::GetCharNo;
int (CCharaBase::*gCBaseGetColorNoAddress)() = &CCharaBase::GetColorNo;
int (CCharaBase::*gCBaseGetCharDataStsAddress)() = &CCharaBase::GetCharDataSts;
int (CCharaBase::*gCBaseGetShadowAddress)() = &CCharaBase::GetShadow;
int (CCharaBase::*gCBaseGetCastIndexAddress)() = &CCharaBase::GetCastIndex;
void (CCharaBase::*gCBaseSetCastIndexAddress)(int) = &CCharaBase::SetCastIndex;
void (CCharaBase::*gCBaseSetMotionSpeedAddress)(float) = &CCharaBase::SetMotionSpeed;
void *(CCharaBase::*gCBaseGetCurrentWeaponAddress)() = &CCharaBase::GetCurrentWeapon;
void *(CCharaBase::*gCBaseGetCurrentWeaponTmpAddress)() = &CCharaBase::GetCurrentWeaponTmp;
void *(CCharaBase::*gCBaseGetCurWeaponSndAddress)() = &CCharaBase::GetCurWeaponSnd;
void *(CCharaBase::*gCBaseGetDoukiParentAddress)() = &CCharaBase::GetDoukiParent;
void (CCharaBase::*gCBaseSetCurrentActAddress)(int, int, int) = &CCharaBase::SetCurrentAct;
int (CCharaBase::*gCBaseSetCurrentStatusAddress)(int, int, TypeArmParam *, int) = &CCharaBase::SetCurrentStatus;
void (CCharaBase::*gCBaseSetCurrentOwnCtrlAddress)(int) = &CCharaBase::SetCurrentOwnCtrl;
void (CCharaBase::*gCBaseSetCurrentMoveAddress)(int, int, int) = &CCharaBase::SetCurrentMove;
void *(CCharaBase::*gCBaseGetActTblCAddress)() = &CCharaBase::GetActTblC;
void *(CCharaBase::*gCBaseGetActTblBaseAddress)() = &CCharaBase::GetActTblBase;
void *(CCharaBase::*gCBaseGetTargetModelAddress)() = &CCharaBase::GetTargetModel;
float (CCharaBase::*gCBaseCalcDamageAddress)(float, int) = &CCharaBase::CalcDamage;
int (CCharaBase::*gCBaseCheckPadPressAddress)(unsigned int) = &CCharaBase::CheckPadPress;
int (CCharaBase::*gCBaseCheckPadOnAddress)(unsigned int) = &CCharaBase::CheckPadOn;
float (CCharaBase::*gCBaseGetRotYAddress)() = &CCharaBase::GetRotY;
float (CCharaBase::*gCBaseGetBipRotYAddress)() = &CCharaBase::GetBipRotY;
void *(CCharaBase::*gCBaseGetBaseModelAddress)() = &CCharaBase::GetBaseModel;
int (CCharaBase::*gCBaseGetNowMotionAddress)() = &CCharaBase::GetNowMotion;
void (CCharaBase::*gCBasePreNutralMotionJumpAddress)() = &CCharaBase::PreNutralMotionJump;
void (CCharaBase::*gCBasePreAction2Address)() = &CCharaBase::PreAction2;
int (CCharaBase::*gCBaseHitCheckAllAddress)() = &CCharaBase::HitCheckAll;
int (CCharaBase::*gCBaseActionCntrlAddress)() = &CCharaBase::ActionCntrl;
int (CCharaBase::*gCBaseIsDoukiActAddress)(int) = &CCharaBase::IsDoukiAct;
void (CCharaBase::*gCBaseActionCntrlExcuteAddress)(int) = &CCharaBase::ActionCntrlExcute;
void (CCharaBase::*gCBasePreUpdatePmvAddress)(float) = &CCharaBase::PreUpdatePmv;
void (CCharaBase::*gCBaseSetYhoseiOffPmvAddress)(int) = &CCharaBase::SetYhoseiOffPmv;
void (CCharaBase::*gCBaseSetYbaseSetPmvAddress)(int) = &CCharaBase::SetYbaseSetPmv;
int (CCharaBase::*gCBaseGetCharComAddress)() = &CCharaBase::GetCharCom;

void *(CWeapon::*gWeaponGetArmParamAddress)() = &CWeapon::GetArmParam;
void *(CWeapon::*gWeaponGetCharaAddress)() = &CWeapon::GetChara;
int (CWeapon::*gWeaponGetLinkBoneTypeAddress)() = &CWeapon::GetLinkBoneType;
int (CWeapon::*gWeaponIsSubWeaponAddress)() = &CWeapon::IsSubWeapon;
int (CWeapon::*gWeaponGetArmTypeAddress)() = &CWeapon::GetArmType;
int (CWeapon::*gWeaponGetTblNoAddress)() = &CWeapon::GetTblNo;
void (CWeapon::*gWeaponSetPmvAddress)(int) = &CWeapon::SetPmv;
void (CWeapon::*gWeaponInitWeaponAddress)() = &CWeapon::InitWeapon;
void (CWeapon::*gWeaponInitColFlagAddress)() = &CWeapon::InitColFlag;
void (CWeapon::*gWeaponSetAttackFlagAddress)(int) = &CWeapon::SetAttackFlag;
void (CWeapon::*gWeaponSetCatchFlagAddress)(int) = &CWeapon::SetCatchFlag;
int (CWeapon::*gWeaponGetColAddress)(int) = &CWeapon::GetCol;
void (CWeapon::*gWeaponSetSubMotionAddress)(MotionNo, int, float) = &CWeapon::SetSubMotion;
int (CWeapon::*gWeaponSetWeaponAddress)(int) = &CWeapon::SetWeapon;
void (CWeapon::*gWeaponResetWeaponAddress)() = &CWeapon::ResetWeapon;
int (CWeapon::*gWeaponIsAirActionAddress)() = &CWeapon::IsAirAction;
void (CWeapon::*gWeaponSetEffectAddress)(int, int) = &CWeapon::SetEffect;
void (CWeapon::*gWeaponSetWeponCngAddress)() = &CWeapon::SetWeponCng;
void (CWeapon::*gWeaponReSetWeponCngAddress)() = &CWeapon::ReSetWeponCng;
void (CWeapon::*gWeaponActionUpdateAddress)() = &CWeapon::ActionUpdate;
void (CWeapon::*gWeaponDebRenderAddress)() = &CWeapon::DebRender;
void (CWeapon::*gWeaponRenderNAddress)() = &CWeapon::RenderN;
void (CWeapon::*gWeaponRenderAAddress)() = &CWeapon::RenderA;
void (CWeapon::*gWeaponRenderEAddress)() = &CWeapon::RenderE;
int (CWeapon::*gWeaponGetModelAddress)() = &CWeapon::GetModel;
int (CWeapon::*gWeaponGetSubModelNumAddress)(int) = &CWeapon::GetSubModelNum;
void (CWeapon::*gWeaponSetCurrentSubModelAddress)(int, int) = &CWeapon::SetCurrentSubModel;

void (CMotion3::*gMotion3OnOpenNewMotionAddress)() = &CMotion3::OnOpenNewMotion;
int (CMotion3::*gMotion3GetLoopCountAddress)() = &CMotion3::GetLoopCount;
int (CMotion3::*gMotion3IsLoopAddress)() = &CMotion3::IsLoop;
void *(CMotion3::*gMotion3GetDataBaseAddress)() = &CMotion3::GetDataBase;
int (CMotion3::*gMotion3GetMotionNoAddress)() = &CMotion3::GetMotionNo;
int (CMotion3::*gMotion3GetSubMotionNoAddress)() = &CMotion3::GetSubMotionNo;
int (CMotion3::*gMotion3GetMotionIndexAddress)() = &CMotion3::GetMotionIndex;
int (CMotion3::*gMotion3GetNextMotionNoAddress)() = &CMotion3::GetNextMotionNo;
int (CMotion3::*gMotion3GetNextSubMotionNoAddress)() = &CMotion3::GetNextSubMotionNo;
int (CMotion3::*gMotion3GetNextIndexAddress)() = &CMotion3::GetNextIndex;
int (CMotion3::*gMotion3GetNextMotionNoSAddress)() = &CMotion3::GetNextMotionNoS;
int (CMotion3::*gMotion3GetNextSubMotionNoSAddress)() = &CMotion3::GetNextSubMotionNoS;
int (CMotion3::*gMotion3GetNextIndexSAddress)() = &CMotion3::GetNextIndexS;
void (CMotion3::*gMotion3SetNextJumpDCAddress)(CMotion3 *) = &CMotion3::SetNextJumpDC;
float (CMotion3::*gMotion3GetNextFrameAddress)() = &CMotion3::GetNextFrame;
int (CMotion3::*gMotion3GetNextLabelAddress)() = &CMotion3::GetNextLabel;
int (CMotion3::*gMotion3GetJumpModeAddress)() = &CMotion3::GetJumpMode;
int (CMotion3::*gMotion3IsErrorAddress)() = &CMotion3::IsError;

void *(CMotion::*gMotionGetModelAddress)() = &CMotion::GetModel;
void (CMotion::*gMotionSetInterpolateTypeAddress)(InterpType) = &CMotion::SetInterpolateType;
void (CMotion::*gMotionSetScaleEnableAddress)(int) = &CMotion::SetScaleEnable;
void (CMotion::*gMotionEnableColorMotionAddress)(int) = &CMotion::EnableColorMotion;
int (CMotion::*gMotionIsEnableColorMotionAddress)() = &CMotion::IsEnableColorMotion;
MotionTargetType (CMotion::*gMotionGetTargetTypeAddress)() = &CMotion::GetTargetType;
void (CMotion::*gMotionSetTargetTypeAddress)(MotionTargetType) = &CMotion::SetTargetType;
float (CMotion::*gMotionGetFrameAddress)() = &CMotion::GetFrame;
float (CMotion::*gMotionGetAddFrameAddress)() = &CMotion::GetAddFrame;
int (CMotion::*gMotionGetMotionAddress)() = &CMotion::GetMotion;
int (CMotion::*gMotionGetAttributeAddress)() = &CMotion::GetAttribute;
void *(CMotion::*gMotionGetNowAttributeClassAddress)() = &CMotion::GetNowAttributeClass;
int (CMotion::*gMotionIsEndMotionAddress)() = &CMotion::IsEndMotion;
int (CMotion::*gMotionGetLinkBoneAddress)() = &CMotion::GetLinkBone;

int (CGameCntrl::*gGameCntrlGetStartCntrlModeAddress)() = &CGameCntrl::GetStartCntrlMode;
void (CGameCntrl::*gGameCntrlStartDataInitializeAddress)() = &CGameCntrl::StartDataInitialize;
void (CGameCntrl::*gGameCntrlStartDataInitializeAfterAddress)() = &CGameCntrl::StartDataInitializeAfter;
void (CGameCntrl::*gGameCntrlDataInitalizeExAddress)() = &CGameCntrl::DataInitalizeEx;
void (CGameCntrl::*gGameCntrlCheckActCntrlAddress)() = &CGameCntrl::CheckActCntrl;
void (CGameCntrl::*gGameCntrlPreActionCntrlFrAddress)() = &CGameCntrl::PreActionCntrlFr;
void (CGameCntrl::*gGameCntrlAfterActionCntrlFrAddress)() = &CGameCntrl::AfterActionCntrlFr;
int (CGameCntrl::*gGameCntrlCheckThrowPauseAddress)() = &CGameCntrl::CheckThrowPause;
void (CGameCntrl::*gGameCntrlSetReturnStatusAddress)() = &CGameCntrl::SetReturnStatus;
int (CGameCntrl::*gGameCntrlGetActBoyakeAddress)() = &CGameCntrl::GetActBoyake;
int (CGameCntrl::*gGameCntrlIsGameOverAddress)() = &CGameCntrl::IsGameOver;
void (CGameCntrl::*gGameCntrlActionCntrlAddress)() = &CGameCntrl::ActionCntrl;
int (CGameCntrl::*gGameCntrlGetPauseMenuAddress)() = &CGameCntrl::GetPauseMenu;
void (CGameCntrl::*gGameCntrlPauseMenuActionAddress)() = &CGameCntrl::PauseMenuAction;

void *(CPAppear::*gPAppearGetPMovieAddress)() = &CPAppear::GetPMovie;
void *(CPAppear::*gPAppearGetParentAddress)() = &CPAppear::GetParent;
void *(CPAppear::*gPAppearGetYpcHeadAddress)() = &CPAppear::GetYpcHead;
void *(CPAppear::*gPAppearGetNodeDataAddress)() = &CPAppear::GetNodeData;
void *(CPAppear::*gPAppearGetLocalMatrixAddress)() = &CPAppear::GetLocalMatrix;
void *(CPAppear::*gPAppearGetWorldMatrixAddress)() = &CPAppear::GetWorldMatrix;
void *(CPAppear::*gPAppearGetSceneTargetLinkAddress)() = &CPAppear::GetSceneTargetLink;
void *(CPAppear::*gPAppearGetActionLinkAddress)() = &CPAppear::GetActionLink;
float (CPAppear::*gPAppearGetFrameAddress)() = &CPAppear::GetFrame;
int (CPAppear::*gPAppearIsDisplayAddress)() = &CPAppear::IsDisplay;
int (CPAppear::*gPAppearIsMotionEndAddress)() = &CPAppear::IsMotionEnd;
void (CPAppear::*gPAppearOnMotionJumpPreAddress)(AprMotion *, AprMotion *) = &CPAppear::OnMotionJumpPre;
void (CPAppear::*gPAppearOnMotionJumpAfterAddress)(AprMotion *, AprMotion *) = &CPAppear::OnMotionJumpAfter;

void (CCharaDataSts::*gCDSStatusCngAttrCheckAddress)() = &CCharaDataSts::StatusCngAttrCheck;
void (CCharaDataSts::*gCDSStatusCheckAddress)() = &CCharaDataSts::StatusCheck;
void (CCharaDataSts::*gCDSStatusCheckPmvAddress)() = &CCharaDataSts::StatusCheckPmv;
void (CCharaDataSts::*gCDSStatusJmpParamAddress)() = &CCharaDataSts::StatusJmpParam;
void (CCharaDataSts::*gCDSOnJmpMotionAddress)() = &CCharaDataSts::OnJmpMotion;
void (CCharaDataSts::*gCDSInitializeStatDataExAddress)() = &CCharaDataSts::InitializeStatDataEx;
void (CCharaDataSts::*gCDSInitializeDataExAddress)() = &CCharaDataSts::InitializeDataEx;
void (CCharaDataSts::*gCDSCheckGatyaStsArmAddress)(SArmTypeD) = &CCharaDataSts::CheckGatyaStsArm;
void *(CCharaDataSts::*gCDSGetPrgStsAddress)() = &CCharaDataSts::GetPrgSts;
void (CCharaDataSts::*gCDSSetNowMotNoAddress)(int) = &CCharaDataSts::SetNowMotNo;
void (CCharaDataSts::*gCDSPreNutralJumpAddress)() = &CCharaDataSts::PreNutralJump;
void (CCharaDataSts::*gCDSReturnArmObjAddress)() = &CCharaDataSts::ReturnArmObj;

void (CMotionC::*gMotionCSetMotStsAddress)(CMotionSts *) = &CMotionC::SetMotSts;
void (CMotionC::*gMotionCSetActTblAddress)(CActTbl *) = &CMotionC::SetActTbl;
void (CMotionC::*gMotionCSetParentAddress)(CMotionC *) = &CMotionC::SetParent;
void (CMotionC::*gMotionCSetChildAddress)(CMotionC *) = &CMotionC::SetChild;
void (CMotionC::*gMotionCSetSubChildAddress)(CMotionC *) = &CMotionC::SetSubChild;
void (CMotionC::*gMotionCSetParentAddFrAddress)(CMotionC *) = &CMotionC::SetParentAddFr;
void (CMotionC::*gMotionCSetChildAddFrAddress)(CMotionC *) = &CMotionC::SetChildAddFr;
void (CMotionC::*gMotionCSetSubChildAddFrAddress)(CMotionC *) = &CMotionC::SetSubChildAddFr;

void (ActionObject::*gAOPreActionAddress)() = &ActionObject::PreAction;
void (ActionObject::*gAOActionAddress)() = &ActionObject::Action;
void (ActionObject::*gAOActionMAddress)() = &ActionObject::ActionM;
void (ActionObject::*gAOReActionAddress)() = &ActionObject::ReAction;
int (ActionObject::*gAOGetDispPosEAddress)() = &ActionObject::GetDispPosE;
float (ActionObject::*gAOGetDispPosZAddress)() = &ActionObject::GetDispPosZ;
int (ActionObject::*gAODisplayAddress)() = &ActionObject::Display;
void (ActionObject::*gAOResetAddress)() = &ActionObject::Reset;
void (ActionObject::*gAOSetMaterialColAddress)(float) = &ActionObject::SetMaterialCol;
int (ActionObject::*gAOGetHitSEAddress)() = &ActionObject::GetHitSE;

void *(CCol::*gCColGetOwnerAddress)() = &CCol::GetOwner;
int (CCol::*gCColGetKindAddress)() = &CCol::GetKind;
int (CCol::*gCColGetColNumAddress)() = &CCol::GetColNum;
void *(CCol::*gCColGetBoundingSphereAddress)() = &CCol::GetBoundingSphere;
float (CCol::*gCColGetUpperAddress)() = &CCol::GetUpper;
float (CCol::*gCColGetLowerAddress)() = &CCol::GetLower;
void *(CCol::*gCColGetMinAddress)() = &CCol::GetMin;
void *(CCol::*gCColGetMaxAddress)() = &CCol::GetMax;
int (CCol::*gCColCallBackAddress)(CCol *, int, int, ColCheckResult *, ColCheckResult *) = &CCol::CallBack;

void (ArmEffectBase::*gAEBDraw2DAddress)() = &ArmEffectBase::Draw2D;
void (ArmEffectBase::*gAEBHitAfterAddress)() = &ArmEffectBase::HitAfter;
void *(ArmEffectBase::*gAEBGetCharaAddress)() = &ArmEffectBase::GetChara;
ArmEffectType (ArmEffectBase::*gAEBGetTypeAddress)() = &ArmEffectBase::GetType;
void (ArmEffectBase::*gAEBActionSameTypeAddress)() = &ArmEffectBase::ActionSameType;
void (ArmEffectBase::*gAEBSetTypeAddress)(ArmEffectType) = &ArmEffectBase::SetType;
void *(ArmEffectBase::*gAEBGetPosAddress)() = &ArmEffectBase::GetPos;
void *(ArmEffectBase::*gAEBGetArmParamAddress)() = &ArmEffectBase::GetArmParam;

void *(CSubObject::*gSubObjGetBodyAddress)() = &CSubObject::GetBody;
int (CSubObject::*gSubObjGetOriginalAddress)() = &CSubObject::GetOriginal;
int (CSubObject::*gSubObjGetFlagsAddress)() = &CSubObject::GetFlags;
int (CSubObject::*gSubObjGetVertexListNumAddress)() = &CSubObject::GetVertexListNum;
int (CSubObject::*gSubObjGetPrimListNumAddress)() = &CSubObject::GetPrimListNum;

int (CPDataArmObj::*gPDAOGetObjTypeAddress)() = &CPDataArmObj::GetObjType;
int (CPDataArmObj::*gPDAOGetObjIdxAddress)() = &CPDataArmObj::GetObjIdx;
int (CPDataArmObj::*gPDAOGetArmNoAddress)() = &CPDataArmObj::GetArmNo;
int (CPDataArmObj::*gPDAOGetArmMdlNoAddress)() = &CPDataArmObj::GetArmMdlNo;
int (CPDataArmObj::*gPDAOGetCharNoAddress)() = &CPDataArmObj::GetCharNo;
int (CPDataArmObj::*gPDAOGetSclBoneNoAddress)() = &CPDataArmObj::GetSclBoneNo;

int (CActTgt::*gActTgtGetHitTgtAddress)() = &CActTgt::GetHitTgt;
int (CActTgt::*gActTgtGetTgtArmNoAddress)() = &CActTgt::GetTgtArmNo;
int (CActTgt::*gActTgtCheckEndTypeAddress)() = &CActTgt::CheckEndType;
void *(CActTgt::*gActTgtGetActTgtParamAddress)() = &CActTgt::GetActTgtParam;
int (CActTgt::*gActTgtIsExtraDmgAddress)() = &CActTgt::IsExtraDmg;
int (CActTgt::*gActTgtGetTgtNoAddress)() = &CActTgt::GetTgtNo;

void *(Labyrinth_ArmGet::*gLAGGetGetArmAddress)() = &Labyrinth_ArmGet::GetGetArm;
int (Labyrinth_ArmGet::*gLAGGetDelArmAddress)() = &Labyrinth_ArmGet::GetDelArm;
void (Labyrinth_ArmGet::*gLAGSetDelArmAddress)(int) = &Labyrinth_ArmGet::SetDelArm;
int (Labyrinth_ArmGet::*gLAGGetMoneyAddress)() = &Labyrinth_ArmGet::GetMoney;
int (Labyrinth_ArmGet::*gLAGIsFullBagAddress)() = &Labyrinth_ArmGet::IsFullBag;
short (Labyrinth_ArmGet::*gLAGGetCheckCharAddress)() = &Labyrinth_ArmGet::GetCheckChar;
int (Labyrinth_ArmGet::*gLAGGetRoutineAddress)() = &Labyrinth_ArmGet::GetRoutine;

int (CMotion2::*gMotion2IsHokanDisableAddress)() = &CMotion2::IsHokanDisable;
void (CMotion2::*gMotion2SetHokanFrameAddress)(float) = &CMotion2::SetHokanFrame;
float (CMotion2::*gMotion2GetHokanFrameNextAddress)() = &CMotion2::GetHokanFrameNext;
void (CMotion2::*gMotion2SetHokanFrameNextAddress)(float) = &CMotion2::SetHokanFrameNext;
void (CMotion2::*gMotion2SetDefaultHokanFrameAddress)(float) = &CMotion2::SetDefaultHokanFrame;

void (CEffObject::*gEffObjSetHitEffAddress)(int) = &CEffObject::SetHitEff;
int (CEffObject::*gEffObjChkHitEffAddress)() = &CEffObject::ChkHitEff;
void *(CEffObject::*gEffObjGetEffStsAddress)() = &CEffObject::GetEffSts;
int (CEffObject::*gEffObjGetEffOwnerAddress)() = &CEffObject::GetEffOwner;
int (CEffObject::*gEffObjGetArmTgtAddress)() = &CEffObject::GetArmTgt;

int (CPAppear_PS2::*gPAppearPS2CalcObjectWorldMatrixAddress)(objMatrix *) = &CPAppear_PS2::CalcObjectWorldMatrix;
int (CPAppear_PS2::*gPAppearPS2GetChildNodeNoAddress)(const char *) = &CPAppear_PS2::GetChildNodeNo;
int (CPAppear_PS2::*gPAppearPS2VibAddress)(int) = &CPAppear_PS2::Vib;
void (CPAppear_PS2::*gPAppearPS2HokanAddress)(int) = &CPAppear_PS2::Hokan;
void (CPAppear_PS2::*gPAppearPS2DrawAddress)() = &CPAppear_PS2::Draw;

void (CCharaCntrl::*gCharaCntrlSetCamCheckAddress)(int) = &CCharaCntrl::SetCamCheck;
void (CCharaCntrl::*gCharaCntrlSetActiveDrawAddress)(int) = &CCharaCntrl::SetActiveDraw;
int (CCharaCntrl::*gCharaCntrlIsActiveDrawAddress)() const = &CCharaCntrl::IsActiveDraw;
void (CCharaCntrl::*gCharaCntrlSetActiveActionChAddress)(int) = &CCharaCntrl::SetActiveActionCh;
int (CCharaCntrl::*gCharaCntrlIsActiveActionChAddress)() const = &CCharaCntrl::IsActiveActionCh;

int (CPrim::*gPrimGetNumVertexAddress)() = &CPrim::GetNumVertex;
unsigned long (CPrim::*gPrimGetPrimAddress)() = &CPrim::GetPrim;
void (CPrim::*gPrimSetTex0Address)(unsigned long) = &CPrim::SetTex0;
unsigned long (CPrim::*gPrimGetTex0Address)() = &CPrim::GetTex0;
void *(CPrim::*gPrimGetTex0AddrAddress)() = &CPrim::GetTex0Addr;

int (CStageSk::*gStageSkGetBgPosAddress)() = &CStageSk::GetBgPos;
int (CStageSk::*gStageSkGetBgPosAlf0Address)() = &CStageSk::GetBgPosAlf0;
int (CStageSk::*gStageSkGetBgPosAlf1Address)() = &CStageSk::GetBgPosAlf1;
int (CStageSk::*gStageSkGetBgPosTopAddress)() = &CStageSk::GetBgPosTop;

void *(CWeaponPmv::*gWeaponPmvGetModelAddress)() = &CWeaponPmv::GetModel;
void (CWeaponPmv::*gWeaponPmvSetChildAddress)(CWeaponPmv *) = &CWeaponPmv::SetChild;
void (CWeaponPmv::*gWeaponPmvSetParentAddress)(CWeaponPmv *) = &CWeaponPmv::SetParent;
void (CWeaponPmv::*gWeaponPmvCheckParentOffsetPmvAddress)(int) = &CWeaponPmv::CheckParentOffsetPmv;

int (CAlpha::*gAlphaGetFadeFrameAddress)() = &CAlpha::GetFadeFrame;
float (CAlpha::*gAlphaGetAlphaAddress)() = &CAlpha::GetAlpha;
float (CAlpha::*gAlphaGetMaxAlphaAddress)() = &CAlpha::GetMaxAlpha;
float (CAlpha::*gAlphaGetMinAlphaAddress)() = &CAlpha::GetMinAlpha;

int (CGameEffect_Base::*gGEBIsActiveActionAddress)() const = &CGameEffect_Base::IsActiveAction;
int (CGameEffect_Base::*gGEBIsActiveDrawAddress)() const = &CGameEffect_Base::IsActiveDraw;
void (CGameEffect_Base::*gGEBSetActiveActionAddress)(int) = &CGameEffect_Base::SetActiveAction;
void (CGameEffect_Base::*gGEBSetActiveDrawAddress)(int) = &CGameEffect_Base::SetActiveDraw;

int (CMCard2::*gMCard2GetActNoAddress)() = &CMCard2::GetActNo;
void *(CMCard2::*gMCard2GetActionParamAddress)() = &CMCard2::GetActionParam;
int (CMCard2::*gMCard2GetDataCapaAddress)() = &CMCard2::GetDataCapa;
int (CMCard2::*gMCard2GetTotalDataCapaAddress)() = &CMCard2::GetTotalDataCapa;

int (CFade::*gFadeIsFadeExcuteAddress)() = &CFade::isFadeExcute;
int (CFade::*gFadeIsFadeOutAddress)() = &CFade::isFadeOut;
void (CFade::*gFadeSetDispModeAddress)(ACTOBJ_TYPE) = &CFade::SetDispMode;

int (CBgCtrl::*gBgCtrlGetBgAddress)() = &CBgCtrl::GetBg;
void *(CBgCtrl::*gBgCtrlGetNowBgAddress)() = &CBgCtrl::GetNowBg;
void (CBgCtrl::*gBgCtrlSetDispAddress)(int) = &CBgCtrl::SetDisp;

float (CGameCntrlGm::*gGameCntrlGmGetGameCtrlTimerAddress)() const = &CGameCntrlGm::GetGameCtrlTimer;
float (CGameCntrlGm::*gGameCntrlGmGetGameCtrlTimeOverAddress)() const = &CGameCntrlGm::GetGameCtrlTimeOver;
int (CGameCntrlGm::*gGameCntrlGmGetPauseMenuAddress)() = &CGameCntrlGm::GetPauseMenu;

void *(CMotionPMS::*gMotionPMSGetPmvMotStsAddress)() = &CMotionPMS::GetPmvMotSts;
void (CMotionPMS::*gMotionPMSSetHumanAddress)(int) = &CMotionPMS::SetHuman;
int (CMotionPMS::*gMotionPMSGetDirectFlagAddress)() = &CMotionPMS::GetDirectFlag;

void *(CPDataGef::*gPDataGefGetDataAddress)() = &CPDataGef::GetData;
int (CPDataGef::*gPDataGefGetGefNoAddress)() = &CPDataGef::GetGefNo;
int (CPDataGef::*gPDataGefGetScnNoAddress)() = &CPDataGef::GetScnNo;

void (CWeaponArm::*gWeaponArmActionUpdate_ArmAddress)() = &CWeaponArm::ActionUpdate_Arm;
int (CWeaponArm::*gWeaponArmActionUpdate_Arm3Address)() = &CWeaponArm::ActionUpdate_Arm3;
int (CWeaponArm::*gWeaponArmGetSubNoAddress)(int, int, int) = &CWeaponArm::GetSubNo;

void *(CEffectArm::*gEffectArmGetModelAddress)() = &CEffectArm::GetModel;
int (CEffectArm::*gEffectArmGetArmModelNumAddress)() = &CEffectArm::GetArmModelNum;
int (CEffectArm::*gEffectArmIsAirAddress)() = &CEffectArm::IsAir;

void *(CCharCom::*gCharComGetComPadAddress)() = &CCharCom::GetComPad;
void (CCharCom::*gCharComSetManualGuardFlagAddress)(int) = &CCharCom::SetManualGuardFlag;
void (CCharCom::*gCharComSetTrainingStatusAddress)(CCharCom::ComTrainingStatus) = &CCharCom::SetTrainingStatus;

int (CObjList::*gObjListGetNumObjectAddress)() = &CObjList::GetNumObject;
void *(CObjList::*gObjListGetFirstObjectAddress)() = &CObjList::GetFirstObject;
void *(CObjList::*gObjListGetLastObjectAddress)() = &CObjList::GetLastObject;

int (CGefBirth::*gGefBirthGetParentSceneAddress)() = &CGefBirth::GetParentScene;
int (CGefBirth::*gGefBirthIsEnableAddress)() = &CGefBirth::IsEnable;
float (CGefBirth::*gGefBirthGetRateAddress)() = &CGefBirth::GetRate;

int (CHitEff::*gHitEffIsEndAddress)() = &CHitEff::IsEnd;
int (CHitEff::*gHitEffGetCharNoAddress)() = &CHitEff::GetCharNo;
void (CHitEff::*gHitEffDrawHitAddress)() = &CHitEff::DrawHit;

void (CArmEffect::*gArmEffectGameEffectOnAddress)(const objMatrix &) = &CArmEffect::GameEffectOn;

float (CEffPrimObj::*gEffPrimObjGetAlphaAddress)() = &CEffPrimObj::GetAlpha;
void *(CEffPrimObj::*gEffPrimObjGetCenterAddress)() = &CEffPrimObj::GetCenter;

void (CActBoyake::*gActBoyakeSetDestroyAddress)(int) = &CActBoyake::SetDestroy;
void (CActBoyake::*gActBoyakeSetActionSwAddress)(int) = &CActBoyake::SetActionSw;

void (CStage::*gStageSetBgTypeAddress)(DispBgType) = &CStage::SetBgType;
DispBgType (CStage::*gStageGetBgTypeAddress)() = &CStage::GetBgType;

void (CStageWall::*gStageWallSetBgTypeAddress)(DispBgType) = &CStageWall::SetBgType;
DispBgType (CStageWall::*gStageWallGetBgTypeAddress)() = &CStageWall::GetBgType;

int (CPArm_PS2::*gPArmPS2GetClassArmObjAddress)() = &CPArm_PS2::GetClassArmObj;
int (CPArm_PS2::*gPArmPS2GetWeaponClassAddress)() = &CPArm_PS2::GetWeaponClass;

void *(CBabGun::*gBabGunGetPosAddress)() = &CBabGun::GetPos;
int (CBabGun::*gBabGunGetColAddress)() = &CBabGun::GetCol;

void *(CCharCol::*gCharColGetColHitDataAddress)() = &CCharCol::GetColHitData;
void (CCharCol::*gCharColSetPropAddress)(int) = &CCharCol::SetProp;

float (CCharaMotion::*gCharaMotionGetRotAngleAddress)() = &CCharaMotion::GetRotAngle;
void (CCharaMotion::*gCharaMotionSetRotAngleAddress)(float) = &CCharaMotion::SetRotAngle;

void (CGefScene::*gGefSceneSetLoopCntAddress)(int) = &CGefScene::SetLoopCnt;
void *(CGefScene::*gGefSceneGetBillBoardAngleAddress)() = &CGefScene::GetBillBoardAngle;

int (CGameEffect_Ctrl::*gGameEffectCtrlGetDispPosEAddress)() = &CGameEffect_Ctrl::GetDispPosE;

void (FireWall_Seed::*gFireWallSeedDraw3DAddress)() = &FireWall_Seed::Draw3D;
int (FireWall_Seed::*gFireWallSeedIsActiveAddress)() = &FireWall_Seed::IsActive;

void (FireStorm_Ptcl::*gFireStormPtclDraw2DAddress)() = &FireStorm_Ptcl::Draw2D;
void (FireStorm_Ptcl::*gFireStormPtclSetAlphaAddress)(float) = &FireStorm_Ptcl::SetAlpha;

void (FireStorm_Seed::*gFireStormSeedDraw2DAddress)() = &FireStorm_Seed::Draw2D;
void (FireStorm_Seed::*gFireStormSeedSetAlphaAddress)(float) = &FireStorm_Seed::SetAlpha;

void (CRenderCallBack::*gRenderCallBackSynchCallBackAddress)(CRender *) = &CRenderCallBack::SynchCallBack;
void (CActFilter::*gActFilterSetDispFilterAddress)(int) = &CActFilter::SetDispFilter;
int (CEventAct::*gEventActGetDispPosEAddress)() = &CEventAct::GetDispPosE;
void (CActReversal::*gActReversalSetCountAddress)(float) = &CActReversal::SetCount;
int (CStageObj::*gStageObjGetMotStsAddress)() = &CStageObj::GetMotSts;
int (CPBG_PS2::*gPBGPS2GetBgAddress)() = &CPBG_PS2::GetBg;
void *(CPObject_PS2::*gPObjectPS2GetObjDispLinkAddress)() = &CPObject_PS2::GetObjDispLink;
void *(CPGef_PS2::*gPGefPS2GetGefDispLinkAddress)() = &CPGef_PS2::GetGefDispLink;
void *(CPDataGefDt::*gPDataGefDtGetDataAddress)() = &CPDataGefDt::GetData;
void *(CPDataSeDt::*gPDataSeDtGetDataAddress)() = &CPDataSeDt::GetData;
int (CPClassBG::*gPClassBGGetBGAddress)() = &CPClassBG::GetBG;
int (CPClassEventObj::*gPClassEventObjGetObjAddress)() = &CPClassEventObj::GetObj;
int (CPClassArmObj::*gPClassArmObjGetObjAddress)() = &CPClassArmObj::GetObj;
int (CPClassGef::*gPClassGefGetObjAddress)() = &CPClassGef::GetObj;
void (CCharaPmv::*gCharaPmvRestartConvertStoneAddress)() = &CCharaPmv::RestartConvertStone;
void *(CCharaSts::*gCharaStsGetCharaAddress)() = &CCharaSts::GetChara;
void (CActTblC::*gActTblCDisableReversalAddress)() = &CActTblC::DisableReversal;
void *(CMotionSts::*gMotionStsGetAtrStsAddress)() = &CMotionSts::GetAtrSts;
void *(CActTbl::*gActTblGetActDataAddress)() = &CActTbl::GetActData;
int (CEffectArmActTbl::*gEffectArmActTblGetModelAddress)() = &CEffectArmActTbl::GetModel;
int (CEffectArmActTbl::*gEffectArmActTblGetArmModelNumAddress)() = &CEffectArmActTbl::GetArmModelNum;
int (CEffectWeaponArm::*gEffectWeaponArmGetModelAddress)() = &CEffectWeaponArm::GetModel;
void *(CGefFactor::*gGefFactorGetParentAddress)() = &CGefFactor::GetParent;
void *(CGef::*gGefGetDataAddress)() = &CGef::GetData;
int (CActFootStmp::*gActFootStmpGetDispPosEAddress)() = &CActFootStmp::GetDispPosE;
void *(ArmEffectCtrl::*gArmEffectCtrlGetHeadAddress)() = &ArmEffectCtrl::GetHead;
void (FireBall::*gFireBallDraw3DAddress)() = &FireBall::Draw3D;
void (FireWall_Ctrl::*gFireWallCtrlSetEraseFlagAddress)(int) = &FireWall_Ctrl::SetEraseFlag;
void (FireStorm::*gFireStormDraw2DAddress)() = &FireStorm::Draw2D;
void (Thunder::*gThunderDraw3DAddress)() = &Thunder::Draw3D;
void (ThunderStorm::*gThunderStormDraw3DAddress)() = &ThunderStorm::Draw3D;
void (IcedEarthCircle::*gIcedEarthCircleDraw2DAddress)() = &IcedEarthCircle::Draw2D;
int (Aura_Effect::*gAuraEffectGetCharNoAddress)() = &Aura_Effect::GetCharNo;
void (CGameEffect_FootStamp::*gGameEffectFootStampGameEffectOnAddress)(const objMatrix &) = &CGameEffect_FootStamp::GameEffectOn;
void (FootStamp_Base::*gFootStampBaseInitAddress)(const objVector &, const float &, const int &) = &FootStamp_Base::Init;
void (CGameEffect_Dammy::*gGameEffectDammyGameEffectActionAddress)() = &CGameEffect_Dammy::GameEffectAction;
void (CGameEffect_Dammy::*gGameEffectDammyGameEffectDrawAddress)() = &CGameEffect_Dammy::GameEffectDraw;
void *(ClsSpring::*gClsSpringGetChainSettingAddress)() = &ClsSpring::GetChainSetting;
void (CMcFunc::*gMcFuncSetFileSizeAddress)(int) = &CMcFunc::SetFileSize;

int (CRender2::*gCRender2IsCulModeAddress)() = &CRender2::IsCulMode;
int (CRender2::*gCRender2IsUpdateLightMatrixAddress)() = &CRender2::isUpdateLightMatrix;
int (CMotionC::*gMotionCIsFrameJumpAddress)() = &CMotionC::IsFrameJump;
int (CMotionC::*gMotionCIsFrameJumpNextAddress)() = &CMotionC::IsFrameJumpNext;
void (CMotionC::*gMotionCSetEndOfMotionAddress)() = &CMotionC::SetEndOfMotion;
float (CEventAct::*gEventActGetDispPosZAddress)() = &CEventAct::GetDispPosZ;
void (CActBoyake::*gActBoyakeDispOffAddress)() = &CActBoyake::DispOff;
void (CActReversal::*gActReversalSetRevMaxAddress)(float, float) = &CActReversal::SetRevMax;
int (CGameCntrlGm::*gGameCntrlGmIsGameOverAddress)() = &CGameCntrlGm::IsGameOver;
int (CChara::*gCharaCheckPadPressAddress)(unsigned int) = &CChara::CheckPadPress;
int (CChara::*gCharaCheckPadOnAddress)(unsigned int) = &CChara::CheckPadOn;
void *(CChara::*gCharaGetNowRootLocateAddress)() = &CChara::GetNowRootLocate;
void *(CChara::*gCharaGetNowNullLocateAddress)() = &CChara::GetNowNullLocate;
void *(CChara::*gCharaGetNowBipLocateAddress)() = &CChara::GetNowBipLocate;
int (CChara::*gCharaIsHitDmgCntChkAddress)() = &CChara::IsHitDmgCntChk;
void (CChara::*gCharaSetPadChkAddress)(int, int) = &CChara::SetPadChk;
void (CCharaPmv::*gCharaPmvStopConvertStoneAddress)() = &CCharaPmv::StopConvertStone;
void *(CCharaBase::*gCBaseGetColHitDataAddress)() = &CCharaBase::GetColHitData;
float (CCharaBase::*gCBaseGetGroundHeightAddress)() = &CCharaBase::GetGroundHeight;
float (CCharaBase::*gCBaseGetLastSyncRateAddress)() = &CCharaBase::GetLastSyncRate;
float (CCharaBase::*gCBaseGetLastSyncRateMaxAddress)() = &CCharaBase::GetLastSyncRateMax;
MOTNO_TBL *(CActTbl::*gActTblSetActTblAddress)(MOTNO_TBL *) = &CActTbl::SetActTbl;
void (CWeapon::*gWeaponSetTgtPosAddress)(objVector, int) = &CWeapon::SetTgtPos;
void (CWeapon::*gWeaponPositionInitAddress)(objVector) = &CWeapon::PositionInit;
void (CWeapon::*gWeaponAddOffsetAddress)(objVector) = &CWeapon::AddOffset;
void (CCol::*gColResetPositionAddress)() = &CCol::ResetPosition;
unsigned long (CPrim::*gPrimGetPrimPRIMAddress)() = &CPrim::GetPrimPRIM;
PRIMINF *(CPrim::*gPrimArgFilterAddress)(PRIMINF *) = &CPrim::ArgFilter;
void (CGefScene::*gGefSceneEnableEndAddress)() = &CGefScene::EnableEnd;
float (CGameEffect_Ctrl::*gGameEffectCtrlGetDispPosZAddress)() = &CGameEffect_Ctrl::GetDispPosZ;
void (FireStorm::*gFireStormActionSameTypeAddress)() = &FireStorm::ActionSameType;
float (ClsSpring::*gClsSpringGetGroundHeightAddress)() = &ClsSpring::GetGroundHeight;
void (ClsSpring::*gClsSpringSkFollowInitAddress)() = &ClsSpring::SkFollowInit;
void (CMCard2::*gMCard2SelectSaveDataAddress)(const MAR_SAVEDATA &) = &CMCard2::SelectSaveData;

int (CRender::*gRenderGetVUEntryCVAddress)(int) = &CRender::GetVUEntryCV;
int (CRender::*gRenderGetVUEntryPrimAddress)(YMP_PRIM_TYPE) = &CRender::GetVUEntryPrim;
void (CMotion::*gMotionSetMaskAddress)(int, int) = &CMotion::SetMask;
int (CMotion3::*gMotion3IsChangeMotionNoAddress)() = &CMotion3::IsChangeMotionNo;
int (CMotion3::*gMotion3IsChangeMotionNoSAddress)() = &CMotion3::IsChangeMotionNoS;
void (CFade::*gFadeSetFadeColorAddress)(unsigned char, unsigned char, unsigned char) = &CFade::SetFadeColor;
int (CBgCtrl::*gBgCtrlGetFilterAddress)(int) = &CBgCtrl::GetFilter;
void (CCharaCntrl::*gCharaCntrlSetNowCharaAddress)(int, CCharaBase *) = &CCharaCntrl::SetNowChara;
int (CChara::*gCharaIsStartActPmvAddress)() = &CChara::IsStartActPmv;
int (CCharaDataSts::*gCBaseDataStsGetStatusBufAddress)(int) = &CCharaDataSts::GetStatusBuf;
void (CCharaBase::*gCBaseSetPartsMdlSwAddress)(int, int) = &CCharaBase::SetPartsMdlSw;
CWeapon *(CCharaBase::*gCBaseGetWeaponCAddress)(int) = &CCharaBase::GetWeaponC;
void (CCharaBase::*gCBaseSetCurrentSubWeaponPmvAddress)(CWeapon *, int) = &CCharaBase::SetCurrentSubWeaponPmv;
CWeapon *(CCharaBase::*gCBaseGetWeaponPmvAddress)(int) = &CCharaBase::GetWeaponPmv;
int (CMotionSts::*gMotionStsGetStatusAddress)(int) = &CMotionSts::GetStatus;
int (CMotionSts::*gMotionStsGetStatusPreAddress)(int) = &CMotionSts::GetStatusPre;
void (CMotionSts::*gMotionStsSetStatusAddress)(int, int) = &CMotionSts::SetStatus;
void (CMotionSts::*gMotionStsSetStatusPreAddress)(int, int) = &CMotionSts::SetStatusPre;
void (CWeapon::*gWeaponCreateModelsAddress)(CCharaBase *, CHR_PARAM *, ARM_PARAM *, int) = &CWeapon::CreateModels;
void (CCharCom::*gCharComSetActTblAddress)(CheckActList *, int *, int) = &CCharCom::SetActTbl;
int (CAlpha::*gAlphaIsFadeInDoneAddress)() = &CAlpha::IsFadeInDone;
int (CAlpha::*gAlphaIsFadeOutDoneAddress)() = &CAlpha::IsFadeOutDone;
int (CGameEffect_Ctrl::*gGameEffectCtrlGetGameEffectBaseAddress)(int) = &CGameEffect_Ctrl::GetGameEffectBase;
FootPosEntry *(CGameEffect_FootStamp::*gGameEffectFootStampGetFootPosAddress)(int) = &CGameEffect_FootStamp::GetFootPos;
FootPosEntry *(CGameEffect_FootStamp::*gGameEffectFootStampGetOldFootPosAddress)(int) = &CGameEffect_FootStamp::GetOldFootPos;
int (Labyrinth_ArmGet::*gLabyArmGetGetAnimAddress)(int) = &Labyrinth_ArmGet::GetAnim;
int (Labyrinth_ArmGet::*gLabyArmGetGetBrokenArmNoAddress)(int) = &Labyrinth_ArmGet::GetBrokenArmNo;
int (Labyrinth_ArmGet::*gLabyArmGetGetShopArmNoAddress)(int) = &Labyrinth_ArmGet::GetShopArmNo;
int (Labyrinth_ArmGet::*gLabyArmGetGetDBNoAddress)(int) = &Labyrinth_ArmGet::GetDBNo;
int (Labyrinth_ArmGet::*gLabyArmGetGetDBTypeAddress)(int) = &Labyrinth_ArmGet::GetDBType;
