// Partial C++ declarations for the EE GCC research probe, not recovered classes.
// Unknown bytes may contain bases, virtual tables or other members. No instances
// are constructed, and none of these sizeof() values are recovered object-size
// claims. Names/offsets: docs/tasks/BOOTSTRAP.md and LINKONCE_CLUSTER.md;
// compiler evidence: COMPILER_PROBE.md.
//
// Mangled section names (`__7CCamera`, `__8CCamera2`, `__9CCameraMv`) show these
// are three distinct classes, not one class with overloads. No inheritance or
// relationship between them is established here.
#ifndef CANDIDATES_EE_CAMERA_CCAMERA_H
#define CANDIDATES_EE_CAMERA_CCAMERA_H

// Only forward-declared: Draw()'s evidenced body never dereferences its
// argument, so no members of CRender are required by this probe.
class CRender;

class CCamera {
public:
    unsigned char unknown000[0x16c];
    float nearClipPlane;
    float farClipPlane;
    unsigned char unknown174[0x4];
    float viewAngle;
    float viewScaleX;
    float viewScaleY;
    int fogMode;
    float fogDistance;
    float fogConcentration;

    float GetNearClipPlane() { return nearClipPlane; }
    float GetFarClipPlane() { return farClipPlane; }
    void SetFogMode(int mode) { fogMode = mode; }
    int GetFogMode() { return fogMode; }
    void SetFogDistance(float distance) { fogDistance = distance; }
    float GetFogDistance() { return fogDistance; }
    void SetFogConcentration(float concentration) { fogConcentration = concentration; }
    float GetFogConcentration() { return fogConcentration; }
    float GetViewScaleX() { return viewScaleX; }
    float GetViewScaleY() { return viewScaleY; }
    // GetViewAngle and GetViewAngleDir read the identical offset (0x178) in the
    // original binary. Modeled as one field with two accessor names; whether the
    // original source used one field or two aliased ones is not established.
    float GetViewAngle() const { return viewAngle; }
    float GetViewAngleDir() const { return viewAngle; }
    // Evidenced body ignores the CRender* argument and unconditionally returns 1.
    int Draw(CRender *) { return 1; }
};

class CCamera2 {
public:
    unsigned char unknown000[0x15c];
    float angleY;
    float angleX;

    float GetAngleY() { return angleY; }
    float GetAngleX() { return angleX; }
    // Evidenced bodies are empty; both ignore their arguments and return void.
    void CameraControl(float) {}
    void DebugCamera(int, int) {}
};

class CCameraMv {
public:
    unsigned char unknown000[0x234];
    int camType;
    unsigned char unknown238[0x294 - 0x238];
    int tgtChr;

    int GetCamType() { return camType; }
    int GetTgtChr() { return tgtChr; }
};

#endif
