# Agent Environment Design

## Purpose

This repository is an **agent-operated engineering workplace**.
Autonomous workers should be able to enter with little project-specific
context, learn the local rules, perform useful work, verify it, preserve
what they learn, and leave the workplace more capable for the next
worker.

> **Individual sessions are disposable. Verified knowledge is not.**

The objective is not to maximize the capability of every worker. It is
to maximize the capability, reliability, and cost-effectiveness of the
**worker + workplace system**.

The repository therefore serves as product, workplace, onboarding
system, institutional memory, governance layer, verification system, and
asynchronous communication channel between workers that may never share
a context window.

## Core loop

    inherit knowledge
      -> perform work
      -> investigate
      -> verify objectively
      -> extract reusable knowledge
      -> update methods/tools/tests
      -> commit
      -> next worker starts farther ahead

A discovery should ideally be paid for once. Repeated reasoning becomes
documentation. Repeated deterministic reasoning should be evaluated for
conversion into tooling. Discovered invariants should be evaluated for
conversion into tests or audits. Expensive novel reasoning should become
reusable institutional knowledge.

# 1. STANDARDS.md: the constitution

`STANDARDS.md` is the authoritative definition of acceptable **work**,
not merely coding style. It should be explicitly referenced by every
major entry point and protected from opportunistic modification.

It defines:

-   artifact/code standards, authenticity, provenance, and prohibited
    shortcuts;
-   objective correctness and completion gates;
-   testing requirements;
-   tool-creation requirements;
-   documentation requirements;
-   commit requirements;
-   honest-deferral requirements;
-   escalation rules;
-   and governance boundaries.

## Testing standard

Specify focused tests for iteration, mandatory final tests, regression
handling, and evidence required before claiming verification.

> **Every discovered invariant must be evaluated for mechanical
> enforcement.**

## Tool-creation standard

> **When the same deterministic analysis is performed manually three
> times, evaluate whether it should become a tool.**

This is a trigger for evaluation, not a command to create needless
utilities.

New tools should have defined inputs/outputs, explicit failure behavior,
tests, documented limitations, example usage, and a clear distinction
between analysis and mutation.

A tool is **institutionalized reasoning**.

## Honest deferral

The organization rewards correct deferral rather than fake completion. A
correct deferral records a real investigation, exact blocker, evidence,
attempted pathways, a clean candidate/reproducible state where
appropriate, and proof that no regression was introduced.

> **Prefer honest incompleteness over dishonest completion.**

# 2. Institutional memory

## SUCCESSES.md

Store generalized mechanisms, not merely completed-task lists.

Each useful entry should record:

-   **Symptom** --- recognizable condition or failure signature.
-   **Mechanism** --- why it occurs.
-   **Successful pathway** --- standards-compliant resolution.
-   **Discriminating evidence** --- how a future worker knows it
    applies.
-   **Verification** --- objective confirmation.
-   **Scope** --- toolchain/version/subsystem/configuration.
-   **Limits/counterexamples**.
-   **References** --- commits, tests, task notes, or source examples.

The purpose is **compressed successful search experience**.

## FAILURES.md

Failures are organizational assets when precise.

Record:

-   hypothesis/pathway;
-   why it was plausible;
-   observed result;
-   mechanism of failure;
-   supporting evidence;
-   conditions under which it should be reconsidered;
-   and conclusions the evidence does **not** justify.

"X did not work" is weak memory. Mechanism-specific negative knowledge
eliminates future search cost.

## Task-local notes

Keep addresses, exact diffs, traces, raw measurements, temporary
hypotheses, and project-specific evidence near the task. Promote only
generalized lessons into shared memory.

# 3. TASK_XXX_METHODOLOGY.md

Methodology documents are **living algorithms**, not historical essays.

Each should contain:

-   objective;
-   preconditions;
-   inputs;
-   expected outputs;
-   ordered procedure;
-   decision points;
-   verification;
-   known failure modes;
-   recovery procedure;
-   escalation criteria;
-   completion criteria;
-   tool contracts;
-   and knowledge-extraction requirements.

> **When a worker discovers a better verified procedure, update the
> methodology so the next worker receives it by default.**

Preserve superseded reasoning where useful, but do not force future
workers to rediscover the improved process from history.

# 4. Mandatory knowledge-extraction phase

Passing the artifact gate is not the final step.

Before completion, ask:

1.  What new thing was learned?
2.  Does the successful technique generalize?
3.  Did a failed hypothesis eliminate future search?
4.  Was deterministic reasoning repeated enough to justify a tool?
5.  Should an invariant become a test/audit?
6.  Did the best procedure differ from the methodology?
7.  Did a tool become part of normal workflow?
8.  Did existing documentation become false or misleading?

Update the appropriate knowledge, methodology, tooling, or tests before
closing the task.

# 5. Evidence hierarchy

Prefer evidence in this order:

1.  objective mechanical verification;
2.  direct measurement/trace/compiler or tool output;
3.  source/specification evidence;
4.  repeated verified empirical observation;
5.  single verified empirical observation;
6.  plausible hypothesis;
7.  model confidence/assertion.

**Model prestige is not evidence.**

A weaker worker with mechanically verified results outranks a flagship
model's unsupported conclusion.

Useful labels include `VERIFIED`, `OBSERVED`, `STRONG HEURISTIC`,
`CANDIDATE PATHWAY`, `HYPOTHESIS`, `SUPERSEDED`, and `DISPROVED`.

# 6. Portable and local knowledge

Separate local project intelligence from portable domain intelligence.

For an agbcc decomp, local knowledge includes game structures,
addresses, assets, functions, maps, scripts, and subsystem
relationships.

Portable knowledge includes compiler behavior, source-shape effects,
matching pathways, linker/section pitfalls, bootstrap methodology,
verification techniques, anti-patterns, and reusable tools.

Portable findings should remove unnecessary game-specific names and
express knowledge as mechanisms and potential pathways. Record
toolchain/version, flags, evidence count/diversity, known
counterexamples, confidence, and references where practical.

A new repository can therefore begin at **day one for game knowledge but
day N for compiler and methodology knowledge**.

# 7. Cost-aware orchestration

Optimize for **verified progress per unit of scarce compute or money**,
not model rank.

    cheapest adequate cognition
      -> deterministic tooling where possible
      -> parallel cheap exploration when useful
      -> structured escalation for genuine novelty
      -> compress expensive discovery into shared knowledge/tooling
      -> return work to cheaper cognition

## Production vs R&D

**Production** applies known methods. Optimize for low cost, throughput,
correctness, parallelism, and protocol adherence.

**R&D** handles novel blockers outside current institutional knowledge.
Optimize for mechanism discovery and generalization.

A frontier model may be wasteful for routine production but economical
as an R&D specialist if one expensive discovery unlocks many cheap
tasks.

## Structured escalation packets

Do not escalate with "this will not work." Provide the objective,
current candidate, relevant disassembly/trace, exact mismatch,
callers/types/context, pathways attempted, results, relevant
successes/failures, probes/tests, and the precise research question.

Expensive cognition should receive a prepared research problem, not a
cold repository.

## R&D output contract

A specialist is not finished after fixing one artifact. It must
determine why the fix worked, whether it generalizes, whether it should
become a pathway/tool/test, and which unresolved tasks should be
revisited.

# 8. Heterogeneous workforce policy

Do not treat models as a single strict ladder. Different families,
generations, and reasoning levels may have different search
distributions, persistence, hypotheses, conservatism, tool use, and
blind spots.

> **Unequal capability is not the same as redundant capability.**

Older or cheaper models may remain valuable exploratory workers when all
outputs face the same objective verification.

When one family repeatedly fails, independent heterogeneous attempts may
be more valuable than repeatedly buying the same flagship.

**Authority belongs to evidence, not model rank.**

# 9. Subagents

When supported, coordinators may spawn temporary workers for safely
separable tasks: independent functions, assets, audits, tests,
classification, subsystem investigations, or competing hypotheses.

Avoid uncontrolled parallel writes to high-conflict files.

The coordinator remains responsible for decomposition, dependencies,
integration, verification, conflict resolution, and knowledge
extraction. Subagent output is untrusted until it passes normal gates.

## Queue-worker onboarding and scope

Give a queue worker an acclimation prompt before delegating implementation:

> Acclimate yourself to this workspace and choose a job from the queue
> without interfering with other work, then commit your results according
> to procedure.

The prompt is a starting point, not a substitute for repository instructions.
Before editing, each worker must read `AGENTS.md`, `STANDARDS.md`,
`AGENT_ENVIRONMENT.md`, current status and work queue, the relevant
methodology, and applicable successes/failures. It must inspect the live
worktree and recent activity, then select one bounded queue item and report
its exact files/scope and intended evidence to the coordinator. The worker
must choose another item if its proposed scope touches another worker's
declared work or existing uncommitted changes. Once the scope is demonstrably
disjoint, it may proceed without waiting for another approval when autonomous
work has been authorized.

Before editing, each simultaneous worker must create its own Git worktree and
branch. It owns its implementation, task evidence, applicable verification,
scoped staging, and commit with all required `STANDARDS.md` §17 trailers. It
must inspect its own final commit and verify that the changed-file list matches
its task and trailers, then report the commit hash and verification outcome.
This leaves routine commit and task-check work with the worker. The coordinator
handles task decomposition, integration conflicts, combined gates, and shared
status/queue updates unless explicitly delegated.

When the operator supplies a delegated-contributor label, use it exactly in
the `Agent-Model` trailer. For example, `GPT-6: Luna (Subagent)` records the
coordinator's requested attribution for delegated work; `Agent-Role` still
describes the worker's selected task. Without an operator-supplied label, use
the runtime identity or the fail-closed value required by `STANDARDS.md` §17.

### Concurrent Git safety

Disjoint file paths do not isolate Git staging: agents in one checkout share
the same index and branch. Separate worktrees are required for concurrent
workers that commit independently. Do not run simultaneous `git add` or
`git commit` operations from one shared checkout. A worker that discovers it
cannot use an isolated worktree must stop before editing and ask the coordinator
to serialize its work/commit. If an unintended file is included, preserve
history, notify the coordinator, and record the incident; do not amend or reset
without owner authorization.

## Nested delegation

An agent may spawn up to two simultaneous workers only when the user or
coordinator explicitly grants permission to delegate further. General support
for subagents is not itself permission. Each nested worker must receive the
same acclimation, bounded-scope, non-interference, separate-worktree,
self-verification, and commit instructions above. Its task must be unrelated
to the spawning agent's selected task and disjoint from all other active work;
the spawning agent remains responsible for their coordination and integration.
Do not recursively delegate again unless that authority is explicitly granted
too.

# 10. Automated specialist escalation

A modest coordinator may invoke stronger models as temporary
organizational resources when:

-   documented pathways are exhausted;
-   multiple cheap workers reach the same blocker;
-   evidence suggests a new mechanism;
-   continued cheap search is expected to cost more;
-   or the discovery could unlock substantial queued work.

This allows an organization managed by a lower-capability model to
accomplish work beyond that model's unaided capability.

The stronger model becomes an **R&D resource**, not the permanent
workforce.

# 11. Tool/test accumulation

The workplace should grow more capable even if its models never improve.

    manual reasoning
      -> documented pathway
      -> repeatable methodology
      -> deterministic tool
      -> automated test/audit

Not every problem reaches the final stage, but workers should consider
whether they can move recurring work one step downward.

# 12. Context-budget discipline

Institutional memory becomes harmful if every worker must read enormous
logs.

Use layers:

1.  `README.md` --- short on-ramp.
2.  `STANDARDS.md` --- constitution.
3.  Methodology index --- routing.
4.  `SUCCESSES.md` / `FAILURES.md` --- compressed knowledge.
5.  Task-local notes --- detailed evidence on demand.
6.  Raw reports/history --- deepest layer.

Prefer **compiled institutional knowledge** over endlessly growing
prose. A good entry reduces future search.

# 13. Onboarding funnel

A new worker should not require a custom manager prompt.

    README
      -> STANDARDS
      -> current objective/work queue
      -> relevant methodology
      -> relevant successes/failures
      -> task-local evidence
      -> work

Every entry point should converge on the same vocabulary, standards,
verification rules, and knowledge architecture.

# 14. Incentives

If scoring is used, reward standards-compliant work, correct deferrals,
reusable mechanisms, reasoning converted into tools, invariants
converted into tests, technical-debt reduction, methodology
improvements, and portable knowledge.

Penalize fake completion, weakening standards, manipulating audit
baselines, hiding regressions, or claiming unperformed verification.

Scores must derive from artifacts and tool output, not self-report.

# 15. Governance

Protect files that define how all other work is judged: `STANDARDS.md`,
audit implementations/baselines, core verification logic, and scoring
definitions.

Agents must not modify the constitution merely because it blocks an easy
solution. Governance changes require explicit owner approval or a
dedicated process.

# 16. Supervisor role

The human supervisor primarily defines objectives, maintains governance,
resolves genuine ambiguity, approves constitutional changes, allocates
resources, reviews organizational health, and redirects priorities.

The desired state is **institutional steering rather than
prompt-by-prompt steering**.

# 17. Definition of done

"Done" is an organizational state, not an agent opinion.

For a decompilation this may require reproducible builds, exact ROM
comparison, no prohibited constructs, editable source assets, complete
provenance, passing tests/audits, no unexplained raw regions beyond
accepted categories, properly deferred unresolved work, updated
methodologies, extracted successes/failures, and clean commits.

# 18. Measure organizational learning

Track metrics such as:

-   verified work per dollar/compute unit;
-   frontier usage per verified unit of progress;
-   share of work completed by low-cost models;
-   specialist escalations by problem class;
-   recurrence of previously solved failures;
-   time from entry to productive contribution;
-   reusable findings created;
-   procedures converted into tools;
-   invariants converted into tests;
-   correct-deferral and regression rates;
-   cross-model success on formerly difficult tasks.

A desired long-term trend is:

> **frontier inference / verified progress decreases over time**

even as remaining problems become harder.

# 19. Cross-repository learning

Portable knowledge should transfer between projects sharing a
domain/toolchain.

    Project A --    Project B ----> shared domain memory ----> all projects
    Project C --/             ^
                              |
                     new verified discoveries

A new project inherits mature compiler/tool/methodology knowledge while
maintaining separate local knowledge.

# 20. Failure containment

Institutional memory can amplify mistakes. Therefore hypotheses must be
labeled, generalized claims require evidence, counterexamples remain
visible, superseded findings are marked rather than silently rewritten,
portable claims are conservative, tools have tests, methodologies have
verification, and objective gates outrank documentation.

The system must make it difficult for one confident hallucination to
become organizational doctrine.

# 21. Organizational capability principle

> **The capability required of the individual worker can decrease as the
> intelligence accumulated by the workplace increases.**

A lower-capability worker can exceed its unaided task ceiling when the
workplace supplies accumulated discoveries, proven procedures, negative
knowledge, deterministic tools, tests, examples, objective feedback,
specialist escalation, and a clear definition of acceptable work.

This does not make every worker equally capable. It makes the
**worker-plus-workplace system** more capable than the isolated worker.

# 22. End-state vision

A mature workplace should allow a comparatively inexpensive coordinator
to receive a high-level objective, bootstrap or inherit the repository,
create work queues, delegate independent tasks, use low-cost workers for
known pathways, create tools when reasoning repeats, escalate novel
blockers to temporary specialists, require specialists to generalize
discoveries, propagate those discoveries back to the workforce, expand
tests/audits, and continue until the mechanically defined endpoint is
reached.

In the strongest form, one coordinating session could take a previously
unseen ROM from raw input to a standards-compliant decompilation by
orchestrating tools, subagents, tests, methodology, and temporary
frontier R&D without requiring the coordinator itself to possess
frontier-level unaided capability.

The important artifact would not only be the finished project.

It would also be the auditable record of **a computational organization
becoming capable enough to produce it**.

## Summary principles

1.  Standards belong to the organization, not the current worker.
2.  Claims yield to objective evidence.
3.  Successes and failures both become institutional memory.
4.  Methodologies are living algorithms.
5.  Repeated cognition should become documentation, tools, tests, or
    audits.
6.  Expensive reasoning should be reserved for novel uncertainty and
    then amortized.
7.  Heterogeneous workers are a feature when evidence adjudicates
    results.
8.  Honest deferral is productive work.
9.  Portable knowledge should flow between compatible workplaces.
10. Every completed task should leave the workplace at least as capable
    as it found it.
