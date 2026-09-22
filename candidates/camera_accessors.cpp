// Semantic candidate only: original compiler, class inheritance, virtual table
// placement and complete object size remain unknown. Not part of a game build.
// Evidence: docs/tasks/BOOTSTRAP.md, LINKONCE_CLUSTER.md and original named
// ELF sections. Mangled names (`__7CCamera`, `__8CCamera2`, `__9CCameraMv`)
// show these are three distinct classes; no relationship between them is
// established here.
#include <cstddef>
#include <cstdint>

struct CameraLayoutCandidate {
    std::uint8_t unknown000[0x16c];
    float nearClipPlane;
    float farClipPlane;
    std::uint8_t unknown174[0x4];
    float viewAngle;
    float viewScaleX;
    float viewScaleY;
    std::int32_t fogMode;
    float fogDistance;
    float fogConcentration;
};

struct Camera2LayoutCandidate {
    std::uint8_t unknown000[0x15c];
    float angleY;
    float angleX;
};

struct CameraMvLayoutCandidate {
    std::uint8_t unknown000[0x234];
    std::int32_t camType;
    std::uint8_t unknown238[0x294 - 0x238];
    std::int32_t tgtChr;
};

static_assert(sizeof(float) == 4, "requires 32-bit float storage");
static_assert(offsetof(CameraLayoutCandidate, nearClipPlane) == 0x16c);
static_assert(offsetof(CameraLayoutCandidate, farClipPlane) == 0x170);
static_assert(offsetof(CameraLayoutCandidate, viewAngle) == 0x178);
static_assert(offsetof(CameraLayoutCandidate, viewScaleX) == 0x17c);
static_assert(offsetof(CameraLayoutCandidate, viewScaleY) == 0x180);
static_assert(offsetof(CameraLayoutCandidate, fogMode) == 0x184);
static_assert(offsetof(CameraLayoutCandidate, fogDistance) == 0x188);
static_assert(offsetof(CameraLayoutCandidate, fogConcentration) == 0x18c);
static_assert(offsetof(Camera2LayoutCandidate, angleY) == 0x15c);
static_assert(offsetof(Camera2LayoutCandidate, angleX) == 0x160);
static_assert(offsetof(CameraMvLayoutCandidate, camType) == 0x234);
static_assert(offsetof(CameraMvLayoutCandidate, tgtChr) == 0x294);

// Free functions express the observed operations, not the original C++ ABI.
float GetNearClipPlane(const CameraLayoutCandidate *camera)
{
    return camera->nearClipPlane;
}

float GetFarClipPlane(const CameraLayoutCandidate *camera)
{
    return camera->farClipPlane;
}

void SetFogMode(CameraLayoutCandidate *camera, std::int32_t mode)
{
    camera->fogMode = mode;
}

std::int32_t GetFogMode(const CameraLayoutCandidate *camera)
{
    return camera->fogMode;
}

void SetFogDistance(CameraLayoutCandidate *camera, float distance)
{
    camera->fogDistance = distance;
}

float GetFogDistance(const CameraLayoutCandidate *camera)
{
    return camera->fogDistance;
}

void SetFogConcentration(CameraLayoutCandidate *camera, float concentration)
{
    camera->fogConcentration = concentration;
}

float GetFogConcentration(const CameraLayoutCandidate *camera)
{
    return camera->fogConcentration;
}

float GetViewScaleX(const CameraLayoutCandidate *camera)
{
    return camera->viewScaleX;
}

float GetViewScaleY(const CameraLayoutCandidate *camera)
{
    return camera->viewScaleY;
}

// GetViewAngle and GetViewAngleDir read the identical offset (0x178) in the
// original binary; modeled as one field with two accessor names.
float GetViewAngle(const CameraLayoutCandidate *camera)
{
    return camera->viewAngle;
}

float GetViewAngleDir(const CameraLayoutCandidate *camera)
{
    return camera->viewAngle;
}

// Evidenced body ignores its CRender* argument and unconditionally returns 1.
std::int32_t Draw(CameraLayoutCandidate *camera, void *render)
{
    (void)camera;
    (void)render;
    return 1;
}

float GetAngleY(const Camera2LayoutCandidate *camera)
{
    return camera->angleY;
}

float GetAngleX(const Camera2LayoutCandidate *camera)
{
    return camera->angleX;
}

// Evidenced bodies are empty; both ignore their arguments and return void.
void CameraControl(Camera2LayoutCandidate *camera, float value)
{
    (void)camera;
    (void)value;
}

void DebugCamera(Camera2LayoutCandidate *camera, std::int32_t a, std::int32_t b)
{
    (void)camera;
    (void)a;
    (void)b;
}

std::int32_t GetCamType(const CameraMvLayoutCandidate *camera)
{
    return camera->camType;
}

std::int32_t GetTgtChr(const CameraMvLayoutCandidate *camera)
{
    return camera->tgtChr;
}
