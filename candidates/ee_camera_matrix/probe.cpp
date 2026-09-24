// Non-matching size/type experiment, excluded from boot reconstruction.
// The size match (achieved only with the aligned(8) attribute) is real
// evidence about the type's alignment; the exact byte sequence still does
// not match under the pinned, otherwise-unmodified -O2 flag. Evidence and
// exact mismatch: docs/tasks/CAMERA_MATRIX_PROBE.md.
class __attribute__((aligned(8))) objMatrix {
public:
    float m[16];
};
class CCamera {
public:
    unsigned char unknown000[0xb0];
    objMatrix projectionMatrix;
    objMatrix viewMatrix;

    objMatrix GetViewMatrix() { return viewMatrix; }
    void SetViewMatrix(objMatrix value) { viewMatrix = value; }
    objMatrix GetProjectionMatrix() { return projectionMatrix; }
    void SetProjectionMatrix(objMatrix value) { projectionMatrix = value; }
};
// Harness only; these pointers are not recovered game data.
objMatrix (CCamera::*gGetViewMatrixAddress)() = &CCamera::GetViewMatrix;
void (CCamera::*gSetViewMatrixAddress)(objMatrix) = &CCamera::SetViewMatrix;
objMatrix (CCamera::*gGetProjectionMatrixAddress)() = &CCamera::GetProjectionMatrix;
void (CCamera::*gSetProjectionMatrixAddress)(objMatrix) = &CCamera::SetProjectionMatrix;
