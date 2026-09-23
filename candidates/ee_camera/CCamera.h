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

class CCamera;

class CRender {
public:
    unsigned char unknown000[0x4a0];
    unsigned int prmode;
    unsigned char unknown4a4[0x4c8 - 0x4a4];
    int frame;
    unsigned char unknown4cc[0x4e0 - 0x4cc];
    CCamera *camera;
    int frameBufferMode;
    int zBufferMode;
    unsigned char unknown4ec[0x4f4 - 0x4ec];
    int frameField;
    int screenWidth;
    int screenHeight;
    unsigned char unknown500[0x554 - 0x500];
    void *freeList;
    unsigned char unknown558[0x55c - 0x558];
    int oldOddEven;

    void *GetPRMODE() { return &prmode; }
    int GetFrame() const { return frame; }
    CCamera *GetCamera() { return camera; }
    int GetFrameBufferMode() const { return frameBufferMode; }
    int GetZBufferMode() const { return zBufferMode; }
    int GetFrameField() const { return frameField; }
    int GetScreenWidth() const { return screenWidth; }
    int GetScreenHeight() const { return screenHeight; }
    void *GetFreeList() { return freeList; }
    int GetOldOddEven() const { return oldOddEven; }
};

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

class CRender2 {
public:
    unsigned char unknown000[0x30];
    unsigned int dBuffDc;
    unsigned char unknown034[0x360 - 0x34];
    unsigned int projectionMatrix;
    unsigned char unknown364[0x3e0 - 0x364];
    unsigned int lightMat;
    unsigned char unknown3e4[0x420 - 0x3e4];
    unsigned int lightCol;
    unsigned char unknown424[0x460 - 0x424];
    unsigned int lightTmp;
    unsigned char unknown464[0x4c4 - 0x464];
    int packetCount;
    unsigned char unknown4c8[0x534 - 0x4c8];
    int nearClipMode;
    unsigned char unknown538[0x548 - 0x538];
    unsigned int bgCol;
    unsigned char unknown54c[0x578 - 0x54c];
    int flickerFree;
    unsigned char unknown57c[0x600 - 0x57c];
    int clearFrameBuffer;
    unsigned char unknown604[0x610 - 0x604];
    int wipeCnt;
    unsigned char unknown614[0x740 - 0x614];
    int regState;

    void *GetDBuffDc() { return &dBuffDc; }
    void *GetProjectionMatrix() { return &projectionMatrix; }
    void *GetLightMat() { return &lightMat; }
    void *GetLightCol() { return &lightCol; }
    void *GetLightTmp() { return &lightTmp; }
    int GetPacketCount() { return packetCount; }
    int GetNearClipMode() { return nearClipMode; }
    int IsNearClipMode() { return nearClipMode; }
    void *GetBgCol() { return &bgCol; }
    int GetFlickerFree() const { return flickerFree; }
    void ClearFrameBuffer(int value) { clearFrameBuffer = value; }
    int GetWipeCnt() { return wipeCnt; }
    void SetWipeCnt(int value) { wipeCnt = value; }
    int GetRegState() { return regState; }
};

#endif
