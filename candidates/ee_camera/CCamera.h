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
// Named only to reproduce the mangled parameter type in
// SetCurrentStatus__10CCharaBaseiiP12TypeArmParami; no members are evidenced.
class TypeArmParam;
// Named only to reproduce SetSubMotion__7CWeaponG8MotionNoif's mangled
// parameter: 'G' is this old ABI's encoding for a class passed BY VALUE
// (any class type, trivial or not — an earlier belief that this required a
// non-trivial constructor was tested and disproved; see SUCCESSES.md),
// distinct from 'P' (pointer) and 'R' (genuine C++ reference) seen
// elsewhere. No members are evidenced.
class MotionNo {};

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

class CGameCamera {
public:
    unsigned char unknown000[0x17c];
    float viewScaleX;
    float viewScaleY;
    unsigned char unknown184[0x1a0 - 0x184];
    int camDistFuncNo;
    unsigned char unknown1a4[0x3fc - 0x1a4];
    void *selectedChara;
    unsigned char unknown400[0x4];
    float viewAngleDir;
    float charaOfsY;

    float GetViewScaleX() { return viewScaleX; }
    float GetViewScaleY() { return viewScaleY; }
    int GetCamDistFuncNo() { return camDistFuncNo; }
    void *GetSelectedChara() { return selectedChara; }
    float GetViewAngleDir() const { return viewAngleDir; }
    void SetCharaOfsY(float value) { charaOfsY = value; }
};

class objMatrix;

class C3dObject {
public:
    C3dObject *parent;
    C3dObject *firstChild;
    C3dObject *nextChild;
    unsigned char unknown00c[0x10 - 0xc];
    objMatrix *linkBoneMat;
    unsigned char unknown014[0x20 - 0x14];
    unsigned int localMat;
    unsigned char unknown024[0x60 - 0x24];
    unsigned int worldMat;

    C3dObject *GetParent() { return parent; }
    C3dObject *GetFirstChild() { return firstChild; }
    C3dObject *GetNextChild(C3dObject *object) { return object->nextChild; }
    void SetLinkBoneMat(objMatrix *value) { linkBoneMat = value; }
    objMatrix *GetLinkBoneMat() { return linkBoneMat; }
    const void *_GetLocalMat(int) const { return &localMat; }
    const void *_GetWorldMat(int) const { return &worldMat; }
    void *DirectWorldMatrix() { return &worldMat; }
    const void *DirectWorldMatrix() const { return &worldMat; }
    void *GetRootMatrix() { return &localMat; }
    const void *GetRootMatrix() const { return &localMat; }
    void *GetLocalMatrix(int) { return &localMat; }
    int Draw(CRender *) { return 1; }
};

class CChara {
public:
    unsigned char unknown000[0x50];
    unsigned int nowLocate;
    unsigned char unknown054[0x308];
    float rotateY;
    unsigned char unknown360[0x34];
    int charSts;
    unsigned char unknown398[0x268];
    unsigned int locate;
    unsigned char unknown604[0xc];
    unsigned int locateBtm;
    unsigned char unknown614[0xc];
    unsigned int locateNull;
    unsigned char unknown624[0x404];
    unsigned int padCnfig;
    unsigned char unknowna2c[0x2a4];
    int padType;
    unsigned char unknowncd4[0x4];
    int myPause;
    int padChk;
    int padChk2;
    int padDisable;
    int padOffMask;
    int armUseCnt;
    unsigned char unknowncf0[0x4];
    void *target;
    void *actTblBase;
    void *actTblC;
    unsigned char unknownd00[0x1c];
    int bonusFlg;
    unsigned char unknownd20[0x20];
    int padNo;
    int padNoReal;
    unsigned char unknownd48[0x208];
    void *chrParam;
    unsigned char unknownf54[0x20];
    int currentArmNo;
    float lastSyncRate;
    float lastSyncRateMax;
    unsigned char unknownf80[0x28];
    void *actPmv;
    void *actPmvTgt;
    unsigned char unknownfb0[0x8];
    float targetAngle;
    unsigned char unknownfbc[0x8];
    int nextAction;
    int autoGuard;
    int playerType;
    unsigned char unknownfd0[0xb8];
    int hpDamageBlock;
    unsigned char unknown108c[0x4];
    int syncroSeChk;

    // Evidenced body ignores its argument and returns it unchanged.
    unsigned long GetNowGmPadCheck(unsigned long value) { return value; }
    void SetNextAction(int value) { nextAction = value; }
    int IsSyncroSeChk() { return syncroSeChk; }
    void SetSyncroSeChk(int value) { syncroSeChk = value; }
    void *StartActPmv() { return actPmv; }
    void *GetActPmvTgt() { return actPmvTgt; }
    void SetHpDamageBlock(int value) { hpDamageBlock = value; }
    // Evidenced body ignores all three arguments and returns void.
    void SetCurrentMove(int, int, int) {}
    // GetLocate and GetLocateV read the identical offset (0x600).
    void *GetLocate() { return &locate; }
    void *GetLocateV() { return &locate; }
    void *GetLocateV_Btm() { return &locateBtm; }
    void *GetLocateV_Null() { return &locateNull; }
    void *GetNowLocate() { return &nowLocate; }
    float GetRotateY() { return rotateY; }
    float GetTargetAngle() { return targetAngle; }
    int GetCharSts() { return charSts; }
    int GetMyPause() { return myPause; }
    int GetPadDisable() { return padDisable; }
    void *GetPadCnfig() { return &padCnfig; }
    int GetPadChk() { return padChk; }
    int GetPadChk2() { return padChk2; }
    int GetPlayerType() { return playerType; }
    void *GetActTblC() { return actTblC; }
    void *GetActTblBase() { return actTblBase; }
    int GetPadOffMask() { return padOffMask; }
    // GetTarget and GetTargetModel read the identical offset (0xcf4).
    void *GetTarget() { return target; }
    void *GetTargetModel() { return target; }
    int GetCurrentArmNo() { return currentArmNo; }
    int GetPadNo() { return padNo; }
    int GetPadNoReal() { return padNoReal; }
    int GetBonusFlg() { return bonusFlg; }
    int GetArmUseCnt() { return armUseCnt; }
    int GetPadType() { return padType; }
    float GetLastSyncRate() { return lastSyncRate; }
    float GetLastSyncRateMax() { return lastSyncRateMax; }
    void *GetChrParam() const { return chrParam; }
    void SetPadOffMask(int value) { padOffMask = value; }
    void SetAutoGuard(int value) { autoGuard = value; }
};

class CCharaBase {
public:
    unsigned char unknown000[0x1bc];
    int nowMotion;
    unsigned char unknown1c0[0x150];
    void *doukiParent;
    unsigned char unknown314[0x2c];
    void *baseModel;
    unsigned char unknown344[0x18];
    float rotY;
    float bipRotY;
    unsigned char unknown364[0x4];
    int index;
    int dataIdx;
    int charNo;
    int colorNo;
    unsigned char unknown378[0xc];
    int castIndex;
    unsigned char unknown388[0xc];
    int charDataSts;
    unsigned char unknown398[0x8];
    int shadow;
    unsigned char unknown3a4[0x68];
    void *currentWeapon;
    void *currentWeaponTmp;
    void *curWeaponSnd;
    unsigned char unknown418[0x18];
    int charCol;
    int charColG;
    int charColK;
    unsigned char unknown43c[0x4];
    float motionSpeed;
    unsigned char unknown444[0xc0];
    unsigned int charSe;
    unsigned char unknown508[0xe4];
    int charCom;
    int yhoseiOffPmv;
    int ybaseSetPmv;

    int GetCharCol() { return charCol; }
    int GetCharColG() { return charColG; }
    int GetCharColK() { return charColK; }
    void *GetCharSe() { return &charSe; }
    int GetIndex() { return index; }
    int GetDataIdx() { return dataIdx; }
    int GetCharNo() { return charNo; }
    int GetColorNo() { return colorNo; }
    int GetCharDataSts() { return charDataSts; }
    int GetShadow() { return shadow; }
    int GetCastIndex() { return castIndex; }
    void SetCastIndex(int value) { castIndex = value; }
    void SetMotionSpeed(float value) { motionSpeed = value; }
    void *GetCurrentWeapon() { return currentWeapon; }
    void *GetCurrentWeaponTmp() { return currentWeaponTmp; }
    void *GetCurWeaponSnd() { return curWeaponSnd; }
    void *GetDoukiParent() { return doukiParent; }
    // Evidenced bodies ignore all arguments and return a fixed value (usually
    // zero); this is a stub shape, not a claim about why these are stubs
    // (e.g. an unfinished feature, disabled debug path, or base-class default
    // meant to be overridden elsewhere).
    void SetCurrentAct(int, int, int) {}
    int SetCurrentStatus(int, int, TypeArmParam *, int) { return 0; }
    void SetCurrentOwnCtrl(int) {}
    void SetCurrentMove(int, int, int) {}
    void *GetActTblC() { return 0; }
    void *GetActTblBase() { return 0; }
    void *GetTargetModel() { return 0; }
    float CalcDamage(float damage, int) { return damage; }
    int CheckPadPress(unsigned int) { return 0; }
    int CheckPadOn(unsigned int) { return 0; }
    float GetRotY() { return rotY; }
    float GetBipRotY() { return bipRotY; }
    void *GetBaseModel() { return baseModel; }
    int GetNowMotion() { return nowMotion; }
    void PreNutralMotionJump() {}
    void PreAction2() {}
    int HitCheckAll() { return 0; }
    int ActionCntrl() { return 0; }
    int IsDoukiAct(int) { return 0; }
    void ActionCntrlExcute(int) {}
    void PreUpdatePmv(float) {}
    void SetYhoseiOffPmv(int value) { yhoseiOffPmv = value; }
    void SetYbaseSetPmv(int value) { ybaseSetPmv = value; }
    int GetCharCom() { return charCom; }
};

class CWeapon {
public:
    void *armParam;
    unsigned char unknown004[0x4];
    void *chara;
    int linkBoneType;
    unsigned char unknown010[0x4];
    int armType;
    int tblNo;
    int subWeapon;
    int pmv;

    void *GetArmParam() { return armParam; }
    void *GetChara() { return chara; }
    int GetLinkBoneType() { return linkBoneType; }
    int IsSubWeapon() { return subWeapon; }
    int GetArmType() { return armType; }
    int GetTblNo() { return tblNo; }
    void SetPmv(int value) { pmv = value; }
    // Evidenced bodies ignore all arguments and either do nothing or return a
    // fixed zero; a stub shape only, not a claim about why (see the same note
    // on CCharaBase's stub methods).
    void InitWeapon() {}
    void InitColFlag() {}
    void SetAttackFlag(int) {}
    void SetCatchFlag(int) {}
    int GetCol(int) { return 0; }
    void SetSubMotion(MotionNo, int, float) {}
    int SetWeapon(int) { return 0; }
    void ResetWeapon() {}
    int IsAirAction() { return 0; }
    void SetEffect(int, int) {}
    void SetWeponCng() {}
    void ReSetWeponCng() {}
    void ActionUpdate() {}
    void DebRender() {}
    void RenderN() {}
    void RenderA() {}
    void RenderE() {}
    int GetModel() { return 0; }
    int GetSubModelNum(int) { return 0; }
    void SetCurrentSubModel(int, int) {}
};

class CMotion3 {
public:
    unsigned char unknown000[0xa4];
    void *dataBase;
    unsigned char unknown0a8[0x8];
    float nextFrame;
    int nextLabel;
    CMotion3 *nextJumpDC;
    int motionNo;
    int subMotionNo;
    int motionIndex;
    int nextMotionNo;
    int nextSubMotionNo;
    int nextIndex;
    int nextMotionNoS;
    int nextSubMotionNoS;
    int nextIndexS;
    int jumpMode;
    int loopCount;
    unsigned char unknown0e8[0x4];
    int isLoop;
    int isError;

    // Evidenced body ignores its arguments and returns void.
    void OnOpenNewMotion() {}
    int GetLoopCount() { return loopCount; }
    int IsLoop() { return isLoop; }
    void *GetDataBase() { return dataBase; }
    int GetMotionNo() { return motionNo; }
    int GetSubMotionNo() { return subMotionNo; }
    int GetMotionIndex() { return motionIndex; }
    int GetNextMotionNo() { return nextMotionNo; }
    int GetNextSubMotionNo() { return nextSubMotionNo; }
    int GetNextIndex() { return nextIndex; }
    int GetNextMotionNoS() { return nextMotionNoS; }
    int GetNextSubMotionNoS() { return nextSubMotionNoS; }
    int GetNextIndexS() { return nextIndexS; }
    void SetNextJumpDC(CMotion3 *value) { nextJumpDC = value; }
    float GetNextFrame() { return nextFrame; }
    int GetNextLabel() { return nextLabel; }
    int GetJumpMode() { return jumpMode; }
    int IsError() { return isError; }
};

// Named only to reproduce the mangled parameter types in
// SetInterpolateType__7CMotion10InterpType and
// SetTargetType__7CMotion16MotionTargetType; no enumerators are evidenced
// beyond needing a nonempty definition to use these as parameter types.
enum InterpType { INTERP_TYPE_UNKNOWN };
enum MotionTargetType { MOTION_TARGET_TYPE_UNKNOWN };

class CMotion {
public:
    InterpType interpolateType;
    int scaleEnable;
    void *model;
    int attribute;
    unsigned char unknown010[0x8];
    float frame;
    float addFrame;
    unsigned char unknown020[0x4];
    int motion;
    unsigned char unknown028[0x20];
    int linkBone;
    unsigned char unknown04c[0x4];
    int endMotion;
    unsigned char unknown054[0x4];
    MotionTargetType targetType;
    unsigned char unknown05c[0x4];
    int enableColorMotion;

    void *GetModel() { return model; }
    void SetInterpolateType(InterpType value) { interpolateType = value; }
    void SetScaleEnable(int value) { scaleEnable = value; }
    void EnableColorMotion(int value) { enableColorMotion = value; }
    int IsEnableColorMotion() { return enableColorMotion; }
    MotionTargetType GetTargetType() { return targetType; }
    void SetTargetType(MotionTargetType value) { targetType = value; }
    float GetFrame() { return frame; }
    float GetAddFrame() { return addFrame; }
    int GetMotion() { return motion; }
    int GetAttribute() { return attribute; }
    // GetAttribute and GetNowAttributeClass read/address the identical
    // offset (0xc); whether the original source used one field or a
    // sub-object here is not established.
    void *GetNowAttributeClass() { return &attribute; }
    int IsEndMotion() { return endMotion; }
    int GetLinkBone() { return linkBone; }
};

class CGameCntrl {
public:
    unsigned char unknown000[0x40];
    int actBoyake;

    // Evidenced bodies ignore all arguments; most either do nothing or
    // return a fixed value. This is a stub shape only, not a claim about
    // why (see the same note on CCharaBase's stub methods).
    int GetStartCntrlMode() { return 10; }
    void StartDataInitialize() {}
    void StartDataInitializeAfter() {}
    void DataInitalizeEx() {}
    void CheckActCntrl() {}
    void PreActionCntrlFr() {}
    void AfterActionCntrlFr() {}
    int CheckThrowPause() { return 0; }
    void SetReturnStatus() {}
    int GetActBoyake() { return actBoyake; }
    int IsGameOver() { return 0; }
    void ActionCntrl() {}
    int GetPauseMenu() { return 0; }
    void PauseMenuAction() {}
};

// Named only to reproduce the mangled parameter type shared by both
// OnMotionJumpPre/After parameters (the second uses this compiler's "T1"
// back-reference to the first parameter's type rather than repeating the
// spelling); no members are evidenced.
class AprMotion;

class CPAppear {
public:
    unsigned char unknown000[0x10];
    unsigned int localMat;
    unsigned char unknown014[0x3c];
    unsigned int worldMat;
    unsigned char unknown054[0x3c];
    void *pMovie;
    void *ypcHead;
    void *nodeData;
    void *parent;
    unsigned char unknown0a0[0x1b4];
    int isMotionEnd;
    int isDisplay;
    float frame;
    unsigned int actionLink;
    unsigned char unknown264[0x8];
    unsigned int sceneTargetLink;

    void *GetPMovie() { return pMovie; }
    void *GetParent() { return parent; }
    void *GetYpcHead() { return ypcHead; }
    void *GetNodeData() { return nodeData; }
    void *GetLocalMatrix() { return &localMat; }
    void *GetWorldMatrix() { return &worldMat; }
    void *GetSceneTargetLink() { return &sceneTargetLink; }
    void *GetActionLink() { return &actionLink; }
    float GetFrame() { return frame; }
    int IsDisplay() { return isDisplay; }
    int IsMotionEnd() { return isMotionEnd; }
    // Evidenced bodies ignore both arguments and return void.
    void OnMotionJumpPre(AprMotion *, AprMotion *) {}
    void OnMotionJumpAfter(AprMotion *, AprMotion *) {}
};

// Named only to reproduce CheckGatyaStsArm__13CCharaDataSts9SArmTypeD's
// mangled parameter. The bare name (no P/R/G letter) shows this is an enum,
// not a class -- a same-shaped `class SArmTypeD {};` was tried first and
// produced the wrong name (`G9SArmTypeD`, the by-value-class encoding);
// confirmed as an enum on a standalone probe before use here. No
// enumerators beyond the placeholder are evidenced.
enum SArmTypeD { SARM_TYPE_D_UNKNOWN };

class CCharaDataSts {
public:
    unsigned char unknown000[0x180];
    unsigned int prgSts;
    unsigned char unknown184[0x94c];
    int nowMotNo;

    // Evidenced bodies ignore all arguments and return void; a stub shape
    // only (see the same note on CCharaBase's stub methods).
    void StatusCngAttrCheck() {}
    void StatusCheck() {}
    void StatusCheckPmv() {}
    void StatusJmpParam() {}
    void OnJmpMotion() {}
    void InitializeStatDataEx() {}
    void InitializeDataEx() {}
    void CheckGatyaStsArm(SArmTypeD) {}
    void *GetPrgSts() { return &prgSts; }
    void SetNowMotNo(int value) { nowMotNo = value; }
    void PreNutralJump() {}
    void ReturnArmObj() {}
};

// Named only to reproduce mangled parameter types for CMotionC's setters;
// no members are evidenced for either.
class CMotionSts;
class CActTbl;

class CMotionC {
public:
    unsigned char unknown000[0xf4];
    CMotionSts *motSts;
    CActTbl *actTbl;
    unsigned char unknown0fc[0x4];
    CMotionC *parent;
    CMotionC *child;
    CMotionC *subChild;
    CMotionC *parentAddFr;
    CMotionC *childAddFr;
    CMotionC *subChildAddFr;

    void SetMotSts(CMotionSts *value) { motSts = value; }
    void SetActTbl(CActTbl *value) { actTbl = value; }
    void SetParent(CMotionC *value) { parent = value; }
    void SetChild(CMotionC *value) { child = value; }
    void SetSubChild(CMotionC *value) { subChild = value; }
    void SetParentAddFr(CMotionC *value) { parentAddFr = value; }
    void SetChildAddFr(CMotionC *value) { childAddFr = value; }
    void SetSubChildAddFr(CMotionC *value) { subChildAddFr = value; }
};

class ActionObject {
public:
    unsigned char unknown000[0x10];
    int dispPosE;
    float dispPosZ;

    // Evidenced bodies ignore all arguments; most either do nothing or
    // return a fixed value (see the same note on CCharaBase's stub methods).
    void PreAction() {}
    void Action() {}
    void ActionM() {}
    void ReAction() {}
    int GetDispPosE() { return dispPosE; }
    float GetDispPosZ() { return dispPosZ; }
    int Display() { return 0; }
    void Reset() {}
    void SetMaterialCol(float) {}
    int GetHitSE() { return -1; }
};

// Named only to reproduce CCol::CallBack's mangled parameter; no members
// are evidenced.
class ColCheckResult;

class CCol {
public:
    unsigned char unknown000[0xc];
    int colNum;
    unsigned char unknown010[0x4];
    unsigned int boundingSphere;
    unsigned char unknown018[0xc];
    void *owner;
    unsigned char unknown028[0x8];
    unsigned int min;
    float lower;
    unsigned char unknown038[0x8];
    unsigned int max;
    float upper;
    unsigned char unknown048[0x8];
    int kind;

    void *GetOwner() { return owner; }
    int GetKind() { return kind; }
    int GetColNum() { return colNum; }
    void *GetBoundingSphere() { return &boundingSphere; }
    float GetUpper() { return upper; }
    float GetLower() { return lower; }
    void *GetMin() { return &min; }
    void *GetMax() { return &max; }
    // Evidenced body ignores all five arguments and returns a fixed zero.
    int CallBack(CCol *, int, int, ColCheckResult *, ColCheckResult *) { return 0; }
};

// Named only to reproduce ArmEffectBase::SetType's mangled enum parameter;
// no enumerators beyond the placeholder are evidenced.
enum ArmEffectType { ARM_EFFECT_TYPE_UNKNOWN };

class ArmEffectBase {
public:
    unsigned char unknown000[0x7c];
    void *chara;
    unsigned char unknown080[0x4];
    void *armParam;
    ArmEffectType type;

    // Evidenced bodies ignore all arguments and return void (see the same
    // note on CCharaBase's stub methods).
    void Draw2D() {}
    void HitAfter() {}
    void *GetChara() { return chara; }
    ArmEffectType GetType() { return type; }
    void ActionSameType() {}
    void SetType(ArmEffectType value) { type = value; }
    // Evidenced body returns the object's own address unchanged.
    void *GetPos() { return this; }
    void *GetArmParam() { return armParam; }
};

class CSubObject {
public:
    unsigned char unknown000[0xc];
    int original;
    int vertexListNum;
    int primListNum;
    unsigned char unknown018[0x78];
    int flags;

    // GetBody (address-of) and GetVertexListNum (value) read the identical
    // offset (0x10); modeled as one field with two accessor bodies, the
    // same pattern already seen elsewhere in this cluster.
    void *GetBody() { return &vertexListNum; }
    int GetOriginal() { return original; }
    int GetFlags() { return flags; }
    int GetVertexListNum() { return vertexListNum; }
    int GetPrimListNum() { return primListNum; }
};

class CPDataArmObj {
public:
    unsigned char unknown000[0x10c];
    int objType;
    int objIdx;
    int charNo;
    int armNo;
    int armMdlNo;
    unsigned char unknown120[0x4];
    int sclBoneNo;

    int GetObjType() { return objType; }
    int GetObjIdx() { return objIdx; }
    int GetArmNo() { return armNo; }
    int GetArmMdlNo() { return armMdlNo; }
    int GetCharNo() { return charNo; }
    int GetSclBoneNo() { return sclBoneNo; }
};

class CActTgt {
public:
    unsigned char unknown000[0x2d0];
    unsigned int actTgtParam;
    int tgtNo;
    int tgtArmNo;
    unsigned char unknown2dc[0x30];
    int checkEndType;
    unsigned char unknown310[0x8];
    int hitTgt;
    unsigned char unknown31c[0x18];
    int isExtraDmg;

    int GetHitTgt() { return hitTgt; }
    int GetTgtArmNo() { return tgtArmNo; }
    int CheckEndType() { return checkEndType; }
    void *GetActTgtParam() { return &actTgtParam; }
    int IsExtraDmg() { return isExtraDmg; }
    int GetTgtNo() { return tgtNo; }
};

class Labyrinth_ArmGet {
public:
    unsigned char unknown000[0xdc];
    int routine;
    unsigned char unknown0e0[0x8];
    unsigned int getArm;
    unsigned char unknown0ec[0xc];
    int fullBag;
    int delArm;
    int money;
    unsigned char unknown104[0x18];
    short checkChar;

    void *GetGetArm() { return &getArm; }
    int GetDelArm() { return delArm; }
    void SetDelArm(int value) { delArm = value; }
    int GetMoney() { return money; }
    int IsFullBag() { return fullBag; }
    short GetCheckChar() { return checkChar; }
    int GetRoutine() { return routine; }
};

class CMotion2 {
public:
    unsigned char unknown000[0x80];
    float defaultHokanFrame;
    float hokanFrameNext;
    float hokanFrame;
    unsigned char unknown08c[0x8];
    int hokanDisable;

    int IsHokanDisable() { return hokanDisable; }
    void SetHokanFrame(float value) { hokanFrame = value; }
    float GetHokanFrameNext() { return hokanFrameNext; }
    void SetHokanFrameNext(float value) { hokanFrameNext = value; }
    void SetDefaultHokanFrame(float value) { defaultHokanFrame = value; }
};

class CEffObject {
public:
    unsigned char unknown000[0xb0];
    unsigned int effSts;
    unsigned char unknown0b4[0x1c];
    int hitEff;
    int effOwner;
    int armTgt;

    void SetHitEff(int value) { hitEff = value; }
    int ChkHitEff() { return hitEff; }
    void *GetEffSts() { return &effSts; }
    int GetEffOwner() { return effOwner; }
    int GetArmTgt() { return armTgt; }
};

class CPAppear_PS2 {
public:
    // Evidenced bodies ignore all arguments and either return a fixed
    // value or do nothing (see the same note on CCharaBase's stub methods).
    int CalcObjectWorldMatrix(objMatrix *) { return 1; }
    int GetChildNodeNo(const char *) { return -1; }
    int Vib(int) { return 0; }
    void Hokan(int) {}
    void Draw() {}
};

class CCharaCntrl {
public:
    unsigned char unknown000[0x7c];
    int camCheck;
    int activeDraw;
    int activeActionCh;

    void SetCamCheck(int value) { camCheck = value; }
    void SetActiveDraw(int value) { activeDraw = value; }
    int IsActiveDraw() const { return activeDraw; }
    void SetActiveActionCh(int value) { activeActionCh = value; }
    int IsActiveActionCh() const { return activeActionCh; }
};

class CPrim {
public:
    unsigned char unknown000[0x4];
    int numVertex;
    // 64-bit fields: this compiler's `unsigned long` is 8 bytes, confirmed
    // by SetTex0's mangled `Ul` parameter compiling to `sd` (store
    // doubleword) at this offset.
    unsigned long prim;
    unsigned long tex0;

    int GetNumVertex() { return numVertex; }
    unsigned long GetPrim() { return prim; }
    void SetTex0(unsigned long value) { tex0 = value; }
    unsigned long GetTex0() { return tex0; }
    // GetTex0Addr (address-of) and GetTex0 (value) read the identical
    // offset (0x10); the same aliasing shape already seen elsewhere.
    void *GetTex0Addr() { return &tex0; }
};

class CStageSk {
public:
    unsigned char unknown000[0x1a0];
    int bgPos;
    int bgPosTop;
    int bgPosAlf0;
    int bgPosAlf1;

    int GetBgPos() { return bgPos; }
    int GetBgPosAlf0() { return bgPosAlf0; }
    int GetBgPosAlf1() { return bgPosAlf1; }
    int GetBgPosTop() { return bgPosTop; }
};

class CWeaponPmv {
public:
    unsigned char unknown000[0x28];
    void *model;
    CWeaponPmv *child;
    CWeaponPmv *parent;
    unsigned char unknown034[0x68];
    int parentOffsetPmv;

    void *GetModel() { return model; }
    void SetChild(CWeaponPmv *value) { child = value; }
    void SetParent(CWeaponPmv *value) { parent = value; }
    void CheckParentOffsetPmv(int value) { parentOffsetPmv = value; }
};

class CAlpha {
public:
    unsigned char unknown000[0x4];
    float alpha;
    float maxAlpha;
    float minAlpha;
    unsigned char unknown010[0x4];
    int fadeFrame;

    int GetFadeFrame() { return fadeFrame; }
    float GetAlpha() { return alpha; }
    float GetMaxAlpha() { return maxAlpha; }
    float GetMinAlpha() { return minAlpha; }
};

class CGameEffect_Base {
public:
    int activeAction;
    int activeDraw;

    int IsActiveAction() const { return activeAction; }
    int IsActiveDraw() const { return activeDraw; }
    void SetActiveAction(int value) { activeAction = value; }
    void SetActiveDraw(int value) { activeDraw = value; }
};

class CMCard2 {
public:
    unsigned char unknown000[0x5c4];
    int actNo;
    unsigned int actionParam;
    unsigned char unknown5cc[0x2c];
    int totalDataCapa;
    int dataCapa;

    int GetActNo() { return actNo; }
    void *GetActionParam() { return &actionParam; }
    int GetDataCapa() { return dataCapa; }
    int GetTotalDataCapa() { return totalDataCapa; }
};

// Named only to reproduce SetDispMode__5CFade11ACTOBJ_TYPE's mangled enum
// parameter; no enumerators beyond the placeholder are evidenced.
enum ACTOBJ_TYPE { ACTOBJ_TYPE_UNKNOWN };

class CFade {
public:
    unsigned char unknown000[0x18];
    ACTOBJ_TYPE dispMode;
    unsigned char unknown01c[0x18];
    int fadeExcute;
    int fadeOut;

    int isFadeExcute() { return fadeExcute; }
    int isFadeOut() { return fadeOut; }
    void SetDispMode(ACTOBJ_TYPE value) { dispMode = value; }
};

class CBgCtrl {
public:
    unsigned char unknown000[0x30];
    int bg;
    int nowBg;
    unsigned char unknown038[0xec];
    int disp;

    int GetBg() { return bg; }
    int GetNowBg() { return nowBg; }
    void SetDisp(int value) { disp = value; }
};

class CGameCntrlGm {
public:
    unsigned char unknown000[0xb0];
    float gameCtrlTimer;
    float gameCtrlTimeOver;
    unsigned char unknown0b8[0x6c];
    int pauseMenu;

    float GetGameCtrlTimer() const { return gameCtrlTimer; }
    float GetGameCtrlTimeOver() const { return gameCtrlTimeOver; }
    int GetPauseMenu() { return pauseMenu; }
};

class CMotionPMS {
public:
    unsigned char unknown000[0x128];
    int directFlag;
    unsigned int pmvMotSts;
    unsigned char unknown130[0x5c];
    int human;

    void *GetPmvMotSts() { return &pmvMotSts; }
    void SetHuman(int value) { human = value; }
    int GetDirectFlag() { return directFlag; }
};

class CPDataGef {
public:
    unsigned char unknown000[0x108];
    void *data;
    int gefNo;
    int scnNo;

    void *GetData() { return data; }
    int GetGefNo() { return gefNo; }
    int GetScnNo() { return scnNo; }
};

class CWeaponArm {
public:
    // Evidenced bodies ignore all arguments; two are no-op/fixed-zero stubs
    // (see the same note on CCharaBase's stub methods). GetSubNo computes
    // c + a from its three arguments (a, b, c), confirmed by operand order
    // on a standalone probe: c + a produced addu $2, $7, $5, an exact match,
    // while a + c produced the reversed addu $2, $5, $7.
    void ActionUpdate_Arm() {}
    int ActionUpdate_Arm3() { return 0; }
    int GetSubNo(int a, int b, int c) { return c + a; }
};

class CEffectArm {
public:
    unsigned char unknown000[0x44];
    int isAir;

    // Evidenced bodies are fixed-zero stubs (see the same note on
    // CCharaBase's stub methods).
    void *GetModel() { return 0; }
    int GetArmModelNum() { return 0; }
    int IsAir() { return isAir; }
};

class CCharCom {
public:
    // Named only to reproduce SetTrainingStatus's mangled nested-enum
    // parameter (Q28CCharCom17ComTrainingStatus); no enumerators beyond the
    // placeholder are evidenced.
    enum ComTrainingStatus { COM_TRAINING_STATUS_UNKNOWN };

    unsigned char unknown000[0x4];
    int manualGuardFlag;
    unsigned int comPad;
    unsigned char unknown00c[0x188];
    ComTrainingStatus trainingStatus;

    void *GetComPad() { return &comPad; }
    void SetManualGuardFlag(int value) { manualGuardFlag = value; }
    void SetTrainingStatus(ComTrainingStatus value) { trainingStatus = value; }
};

class CObjList {
public:
    unsigned char unknown000[0xc];
    int numObject;
    void *firstObject;
    void *lastObject;

    int GetNumObject() { return numObject; }
    void *GetFirstObject() { return firstObject; }
    void *GetLastObject() { return lastObject; }
};

class CGefBirth {
public:
    int enable;
    unsigned char unknown004[0x1c];
    int parentScene;
    float rate;

    int GetParentScene() { return parentScene; }
    int IsEnable() { return enable; }
    float GetRate() { return rate; }
};

class CHitEff {
public:
    unsigned char unknown000[0x70];
    int charNo;
    unsigned char unknown074[0x30];
    int isEnd;

    int IsEnd() { return isEnd; }
    int GetCharNo() { return charNo; }
    // Evidenced body ignores all arguments and returns void.
    void DrawHit() {}
};

class CArmEffect {
public:
    // Only GameEffectOn is recovered here: GetUpdateFlag and GetHead read
    // via $gp-relative addressing (lb/lw with a $gp base, not $this/$4) --
    // a static or file-scope variable, not an instance field. Reproducing
    // that would require matching the *entire original program's*
    // small-data-segment layout relative to $gp, which an isolated probe
    // cannot replicate without manufacturing an artificial global layout;
    // left unrecovered per STANDARDS.md's prohibition on manufactured
    // matches. See docs/tasks/LINKONCE_CLUSTER.md.
    void GameEffectOn(const objMatrix &) {}
};

class CEffPrimObj {
public:
    unsigned char unknown000[0x30];
    void *center;
    unsigned char unknown034[0x40];
    float alpha;

    float GetAlpha() { return alpha; }
    void *GetCenter() { return center; }
};

class CActBoyake {
public:
    unsigned char unknown000[0x68];
    int destroy;
    int actionSw;

    void SetDestroy(int value) { destroy = value; }
    void SetActionSw(int value) { actionSw = value; }
};

// Named only to reproduce SetBgType's mangled enum parameter; no
// enumerators beyond the placeholder are evidenced.
enum DispBgType { DISP_BG_TYPE_UNKNOWN };

class CStage {
public:
    unsigned char unknown000[0x1a0];
    DispBgType bgType;

    void SetBgType(DispBgType value) { bgType = value; }
    DispBgType GetBgType() { return bgType; }
};

#endif
