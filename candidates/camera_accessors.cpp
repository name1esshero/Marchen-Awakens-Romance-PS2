// Semantic candidate only: original compiler, class inheritance, virtual table
// placement and complete object size remain unknown. Not part of a game build.
// Evidence: docs/tasks/BOOTSTRAP.md and original named ELF sections.
#include <cstddef>
#include <cstdint>

struct CameraLayoutCandidate {
    std::uint8_t unknown000[0x16c];
    float nearClipPlane;
    float farClipPlane;
    std::uint8_t unknown174[0x10];
    std::int32_t fogMode;
    float fogDistance;
    float fogConcentration;
};

static_assert(sizeof(float) == 4, "requires 32-bit float storage");
static_assert(offsetof(CameraLayoutCandidate, nearClipPlane) == 0x16c);
static_assert(offsetof(CameraLayoutCandidate, farClipPlane) == 0x170);
static_assert(offsetof(CameraLayoutCandidate, fogMode) == 0x184);
static_assert(offsetof(CameraLayoutCandidate, fogDistance) == 0x188);
static_assert(offsetof(CameraLayoutCandidate, fogConcentration) == 0x18c);

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
