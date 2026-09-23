# Negative knowledge — code/compiler frontier

Authority: [STANDARDS.md](STANDARDS.md). Scope: this file is the dedicated
negative-knowledge log for the "Claude / code" queue lead (boot ELF
reconstruction, linkonce accessor recovery, EE GCC compiler identification),
kept separate from the shared [`FAILURES.md`](FAILURES.md) so concurrent
asset/localization work never needs to touch the same file. Earlier
code-frontier failures recorded before this file existed remain in
`FAILURES.md` and are not duplicated here; new ones go here going forward.

Entry format matches `FAILURES.md`: hypothesis/pathway, why it was
plausible, observed result, mechanism of failure, supporting evidence,
reconsideration conditions, and what the evidence does not justify.

## Hand-written struct field lists silently drift from evidenced offsets

Hypothesis: for a small class (2-3 fields), writing the `unsigned char
unknownXXX[N]` gap-filler struct by hand is faster than invoking the
offset-sorting generator script, and just as reliable once the offsets are
copied from the disassembly.
Observed result: happened twice in the linkonce cluster recovery
(`CCol` in the ActionObject/CCol/CMotionC/ArmEffectBase batch;
`CMotionPMS` in the CFade/CBgCtrl/CGameCntrlGm/CMotionPMS/CPDataGef batch).
Both times an extra or misplaced `unsigned char unknownXXX[N]` gap was
inserted between two real fields, silently shifting every field after it to
the wrong offset -- which would have produced wrong `lw`/`sw`/`addiu`
offsets in the compiled candidate.
Mechanism: manually re-deriving "gap size = next offset − previous end" by
eye is exactly the kind of small arithmetic that is easy to get right most
of the time and silently wrong occasionally, especially once there are more
than two fields. Nothing catches the mistake until either a spot check
against the generator or an actual failing `compare_sections.py`/`make
verify-ee` run.
Both caught this session before reaching the EE GCC compile step, by
re-deriving the same struct with the small Python offset-sorting generator
used throughout this task (sort `(offset, name, kind)` tuples, emit a gap
whenever `offset > cursor`) and diffing it against the hand-written version.
Reconsider hand-writing only for genuinely single-field classes, where there
is no ordering to get wrong.
References: [linkonce cluster task](tasks/LINKONCE_CLUSTER.md).
