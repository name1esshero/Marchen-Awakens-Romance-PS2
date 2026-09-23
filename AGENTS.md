# Repository entry point

Read [docs/STANDARDS.md](docs/STANDARDS.md) and
[docs/AGENT_ENVIRONMENT.md](docs/AGENT_ENVIRONMENT.md) first.
Then read [current status](docs/STATUS.md), [the work queue](docs/WORK_QUEUE.md),
the relevant methodology, and successes/failures before editing.
For broad asset extraction, modding, or localization work, also apply
[the localization methodology](docs/LOCALIZATION_METHODOLOGY.md).

Keep status, work queue, task evidence and reusable knowledge current as part of
each meaningful task. Distinguish matching bytes, candidate semantics, authentic
source recovery, and unresolved raw regions. Never weaken pinned reference hashes.

Every new commit needs the five attribution/evidence trailers defined in
STANDARDS.md §17. Model, role and work type are values for the current contributor
and task; the example in the standards is not a fixed identity or default role.
Record only verification actually run. Preserve existing history unless the owner
explicitly authorizes rewriting it.

Primary gates for current bootstrap work:

```sh
make test verify-boot verify-source-only
make verify-ee  # when changing the historical compiler probe; setup: make setup-ee
```

These verify the boot executable only. The full disc and authentic high-level
game source are still incomplete; see the status page for precise limits.
