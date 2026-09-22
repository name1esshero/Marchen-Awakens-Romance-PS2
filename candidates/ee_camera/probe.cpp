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
