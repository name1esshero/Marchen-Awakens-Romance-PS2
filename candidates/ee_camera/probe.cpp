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
