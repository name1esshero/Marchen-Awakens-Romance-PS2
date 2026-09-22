// Partial C++ declaration for the EE GCC research probe, not a recovered class.
// Unknown bytes may contain bases, virtual tables or other members. No instances
// are constructed, and sizeof(CCamera) is not a recovered object-size claim.
// Names/offsets: docs/tasks/BOOTSTRAP.md; compiler evidence: COMPILER_PROBE.md.
#ifndef CANDIDATES_EE_CAMERA_CCAMERA_H
#define CANDIDATES_EE_CAMERA_CCAMERA_H

class CCamera {
public:
    unsigned char unknown000[0x16c];
    float nearClipPlane;
    float farClipPlane;
    unsigned char unknown174[0x10];
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
};

#endif
