// Non-matching ABI experiment, excluded from boot reconstruction.
// Four float components are a hypothesis, not recovered field types or names.
// Evidence and exact mismatch: docs/tasks/VIEW_RECT_PROBE.md.
struct ViewRectCandidate { float unknown00, unknown04, unknown08, unknown0c; };
class CCamera {
public:
    unsigned char unknown000[0x140];
    ViewRectCandidate viewRect;
    ViewRectCandidate GetViewRect() { return viewRect; }
};
// Harness only; this pointer is not recovered game data.
ViewRectCandidate (CCamera::*gGetViewRectAddress)() = &CCamera::GetViewRect;
