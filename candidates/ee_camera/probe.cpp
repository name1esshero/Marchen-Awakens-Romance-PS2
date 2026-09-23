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
