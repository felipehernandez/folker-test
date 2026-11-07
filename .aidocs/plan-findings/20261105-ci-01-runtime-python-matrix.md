# Plan Challenge: CI-01 — Run unit tests on the runtime Python version (preceded by BUG-01)

- **Date**: 2026-11-05 (updated 2026-11-06)
- **Plan**: /Users/felipe.hernandez/.claude/plans/i-want-to-work-fuzzy-minsky.md
- **Iterations**: 3 (2 on the BUG-01 + CI-01 plan, 1 on the rewritten CI-01 plan)
- **Status**: Open (1 finding)

## Resolved in plan

- [CRITICAL] The BUG-01 regression test didn't reach the bug. The shallow `a.b` / `a.c` saves never evaluate the `Mapping` check. Replaced with the verified deep shape `a.b.c` / `a.b.d`, with the warning filter scoped to the save calls.
- [MODERATE] Unverified orb `tag` parameter: verified in the `circleci/python@2.2.0` source. `python/default` takes `tag` (default `"3.8"`, which is why CI previously tested on 3.8). The expanded config shows `cimg/python:3.10`.
- [MODERATE] Pip cache not keyed by Python version: not an issue. `install-packages` defaults to `include-python-in-cache-key: true`.
- [MINOR] The "gate check" pushed a throwaway commit: replaced by a local gate proof (pre-fix `context.py` on `cimg/python:3.10` → 4 failures). Nothing was pushed.
- [MODERATE] Stacked-branch rebase after the first PR merges: moot. PR #597 was squash-merged before CI-01 started, so `ci/CI-01-runtime-python-matrix` branches directly from `beta`.
- [MINOR] Local verification would leave files in the repo: verification ran on a `git archive` copy in the scratchpad.
- [MINOR] `python --version` only prints the version: accepted. The real check against the Dockerfile version is CI-12.

## Unresolved findings

### [MODERATE] TST-01 has a hidden dependency on DEP-09

- **Severity**: Moderate
- **Description**: Turning `DeprecationWarning` into errors globally fails at import time, because marshmallow's `fields.Boolean(default=...)` in `folker/load/schemas.py:47` raises `RemovedInMarshmallow4Warning`.
- **Impact**: TST-01 can't be implemented as described until DEP-09 is done (or until marshmallow warnings are filtered separately).
- **Suggestion**: Update `.aidocs/plans/improvement-plan.md`: TST-01 depends on DEP-09. Mention it in the lesson `20261105-test-on-runtime-python-version.md`.
- **Decision**: Left unresolved by user choice.
