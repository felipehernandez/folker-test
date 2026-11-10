# folker-test — Completed tasks

Tasks moved out of [improvement-plan.md](improvement-plan.md) once done, in the same groups as the plan.
Completion date = merge date of the change that landed the task on `beta`; for tasks that shipped inside the squashed PRs #602 / #604 it is the PR merge date. The dates for CI-03, CI-05 and TST-07 are the date of their commit (2026-11-10).
Tasks only partly done (◐) stay in the plan.

## 1 · CI/CD

| ID | Title | Impact | Cost | Completed |
|---|---|---|---|---|
| CI-01 | Run unit tests on the runtime Python version (matrix) | High | S | 2026-11-06 |
| CI-02 | Lint / static-analysis quality gate | Med | S | 2026-11-06 |
| CI-03 | Coverage gate (scoped to `folker/`, ratchet) | Med | XS | 2026-11-10 |
| CI-04 | Test the exact image you publish | High | M | 2026-11-07 |
| CI-05 | Remove retry loop and no-op validation job | Med | S | 2026-11-10 |
| CI-06 | De-duplicate the three CircleCI workflows | Med | S | 2026-11-07 |
| CI-12 | Single source of truth for the Python version | Med | S | 2026-11-07 |

### CI-01 — Run unit tests on the runtime Python version
- **Completed:** 2026-11-06
- **What / why:** CircleCI's `build` job uses `python/default`, but the Docker images run `python:3.10`. Locally the suite passes on 3.9 while the shipped runtime crashes (BUG-01). Add a Python version matrix covering the Docker image's version (plus the next one).
- **Impact:** High. Catches version-specific breakage before release.
- **Cost:** S. ~20 lines in `.circleci/config.yml`.
- **Benefit:** The test suite becomes a real signal for what's shipped. Makes DEP-04 safe.
- **Depends on:** none (do first).
- **Lesson:** [Test on the runtime Python version](../lessons/20261105-test-on-runtime-python-version.md)

### CI-02 — Lint / static-analysis quality gate
- **Completed:** 2026-11-06
- **What / why:** `pylint` is installed (even at runtime) but never run in CI. Add `ruff` (fast; replaces most pylint checks), non-blocking first, then blocking once the baseline is clean.
- **Impact:** Med. Prevents new dead code, unused imports, shadowed builtins and similar.
- **Cost:** S. CI job plus config; fixing the baseline may touch many files mechanically.
- **Benefit:** Consistent style. Reviewers focus on logic.
- **Depends on:** DEP-01 (config lives in `pyproject.toml`).
- **Done:** `ruff.toml` (moves into `pyproject.toml` with DEP-01), blocking `lint` job from the start (CircleCI has no "allow failure", and `|| true` would hide results), `ruff==0.17.4` pinned in `requirements-lint.txt` so Renovate bumps it, `make lint` / `make lint-fix`. Rules: `E4, E7, E9, F, W6`, with a clean baseline. Fixing it uncovered 3 tests that never ran because of duplicate names; one of them needed its assertion corrected.
- **Follow-ups:** widen the rules one family at a time (`B`, `UP`, `I`, `SIM`; about 220 findings today), `ruff format` (126 files would change; do it in a dedicated commit and add it to `.git-blame-ignore-revs`), drop `pylint` together with DEP-02.

### CI-03 — Coverage gate
- **Completed:** 2026-11-10
- **What / why:** Coverage is generated but not enforced, and the `--omit` patterns don't restrict it to `folker/`. Use `--source=folker`, record the baseline, and fail when it drops (ratchet).
- **Impact:** Med.
- **Cost:** XS. A few config lines.
- **Benefit:** Stops coverage erosion, especially for the BUG work.
- **Depends on:** TST-01.
- **Done:** the printed total was 94% because it counted `tests/`, and the xml/html reports also picked up pytest temp files. Coverage is now `source_pkgs = ["folker"]` with branch coverage, configured in `pyproject.toml` (`coverage[toml]==7.16.2`, so `tomli` is explicit on 3.10). Baseline is 86.42% (2902 statements, 530 branches) on Python 3.10, and `fail_under = 86.4`. The threshold is raised by hand when coverage rises and never lowered. A Renovate bump of `coverage` may shift the number; the gate catching that is intended. When a Python version is added to the matrix (DEP-04), re-measure on it, because `fail_under` must hold on every version. The xml/html steps run with `--fail-under=0`, so `coverage report` (the `Coverage gate` step) is the only gate, and artifacts upload with `when: always`.

### CI-04 — Test the exact image you publish
- **Completed:** 2026-11-07
- **What / why:** Integration tests run images built from `Dockerfile-integration` by docker-compose, while `build-docker-image` separately builds `Dockerfile`. The published artifact is never tested. Build once with a multi-stage `runtime` target, layer the integration fixtures on top of it, and publish the tested digest.
- **Impact:** High. Release confidence.
- **Cost:** M. Dockerfiles, compose and CI jobs.
- **Benefit:** "Green CI" means the published image works. Removes the duplicated Dockerfile.
- **Depends on:** CI-06 recommended first.
- **Done:** one `Dockerfile` with `builder` → `runtime` (published) → `integration` (runtime + `example/` fixtures) targets; `Dockerfile-integration` removed. `build-docker-image` builds both and saves them in one tar, the integration jobs `docker load` it (and fail if it is missing, so compose can never rebuild), and publishing re-tags and pushes the same `runtime` image. Verified locally: the runtime layers are an exact prefix of the integration image, and code/void/template/protobuf/grpc/kafka pass through compose without a rebuild. The image is now built on every branch, not only `beta`/`main`.

### CI-05 — Remove retry loop and no-op validation job
- **Completed:** 2026-11-10
- **What / why:** Integration jobs retry up to 3× with `sleep 10`, which hides flakiness and real failures. `validate-integration-tests` only runs `echo`. Replace the retry with readiness checks (TST-07). Use real `requires` fan-in, or delete the job.
- **Impact:** Med. Flaky failures become visible and get fixed.
- **Cost:** S.
- **Benefit:** Faster, honest pipelines.
- **Depends on:** TST-07.
- **Done:** `run-integration-tests` runs `docker-compose run` once (no retry, no `sleep`), after a step that prints the compose version. `validate-integration-tests` is deleted and `publish-beta`/`publish-latest` require `run-integration-tests` directly (CircleCI waits for every matrix variant). Done together with TST-07 in one change.
- **Follow-up:** deleting `validate-integration-tests` left the PR waiting on that check, because `beta` required it in GitHub's branch protection (the API call that was meant to confirm this had been refused to a non-admin token, which looked like "no protection"). The required checks were then updated in a `beta` ruleset; `main` still needs the same. Tracked as CI-13.

### CI-06 — De-duplicate the three CircleCI workflows
- **Completed:** 2026-11-07
- **What / why:** `development`, `beta` and `main` each copy the same 21-entry integration matrix. Use YAML anchors or pipeline parameters for the shared part.
- **Impact:** Med. Adding a module currently needs 3 edits plus the Makefile plus compose.
- **Cost:** S. Config shrinks by ~100 lines.
- **Benefit:** One place to change. Fewer "forgot one workflow" mistakes.
- **Depends on:** none.
- **Done:** the three workflows are merged into one `build-test-publish` workflow; only `publish-beta` (`beta`) and `publish-latest` (`main`) are branch-filtered. Config 290 → 219 lines; adding a module is one matrix entry plus one compose service (which now shares a YAML anchor).

### CI-12 — Single source of truth for the Python version
- **Completed:** 2026-11-07
- **What / why:** The Python version is repeated in `Dockerfile`, `Dockerfile-integration`, `.devcontainer`, the CI executor and (after DEP-01) `requires-python`. CI-01 fixes today's mismatch, but the next bump can drift again. Declare the version once (`.python-version`), pass it to the Dockerfiles as `ARG PYTHON_VERSION`, read it into the CI matrix, and add a CI check that fails if any of these disagree.
- **Impact:** Med. Prevents the class of bug behind BUG-01 from coming back.
- **Cost:** S. ~30 lines across Dockerfiles, devcontainer and CI config, plus a small check script.
- **Benefit:** Version bumps (DEP-04) become a one-line change. Test and runtime environments can't diverge silently.
- **Depends on:** CI-01. Best done right before DEP-04.
- **Lesson:** [Test on the runtime Python version](../lessons/20261105-test-on-runtime-python-version.md)
- **Done:** `.python-version` is the source. Dockerfile takes `ARG PYTHON_VERSION` (CI passes the file's value), CI executors and the unit-test matrix use the `python-version` pipeline parameter, compose and the devcontainer pass it through. `scripts/check_python_version.py` (run in the `lint` job) fails on any disagreement and on hard-coded versions. This found and fixed the devcontainer still on 3.9 (and its unquoted `3.9`, which YAML would read as `3.1` for `3.10`). DEP-04 becomes: edit `.python-version`, run the script, follow its errors.

## 2 · Testability

| ID | Title | Impact | Cost | Completed |
|---|---|---|---|---|
| TST-01 | Fix pytest configuration (markers, warnings as errors) | Med | XS | 2026-11-09 |
| TST-07 | Deterministic integration environment (healthchecks) | Med | S | 2026-11-10 |

### TST-01 — Fix pytest configuration
- **Completed:** 2026-11-09
- **What / why:** `tests/pytest.ini` isn't used when pytest runs from the repo root (about 150 "unknown mark" warnings), and its marker list mixes tabs and spaces. Move the config to `pyproject.toml`, add `--strict-markers`, and set `filterwarnings = error::DeprecationWarning` (this alone would have caught BUG-01).
- **Impact:** Med.
- **Cost:** XS.
- **Benefit:** Typos in marks fail. Deprecations surface early.
- **Depends on:** DEP-01 (or do it in a root `pytest.ini` now).
- **Lesson:** [Test on the runtime Python version](../lessons/20261105-test-on-runtime-python-version.md)
- **Done:** `tests/pytest.ini` removed (pytest never loaded it from the repo root, and the marker list mixed tabs and spaces). `[tool.pytest.ini_options]` in `pyproject.toml` registers the same markers, sets `--strict-markers`, and treats `DeprecationWarning` as an error. Two ignores remain, both outside our code: `pkg_resources` (pulled in by `google-cloud-pubsub` 1.7.2; goes away with DEP-05) and `pyparsing` (called by the pinned `httplib2`). The file has no `[project]` table; dependency consolidation stays with DEP-01. Turning the filter on required the two marshmallow fixes tracked as DEP-09, otherwise collection dies at import.

### TST-07 — Deterministic integration environment
- **Completed:** 2026-11-10
- **What / why:** Integration jobs rely on retries instead of readiness checks. Add `healthcheck` plus `depends_on: condition: service_healthy` for kafka, rabbitmq, postgres, zookeeper and the emulators.
- **Impact:** Med.
- **Cost:** S.
- **Benefit:** Unlocks CI-05. Fewer flaky reruns.
- **Done:** every service a test depends on has a `healthcheck`, and every `depends_on` uses `condition: service_healthy`; the obsolete `version:` line is removed. What each probe proves (tool in brackets): postgres accepts TCP connections, `-h 127.0.0.1` so it can't pass on the init-time temporary server (`pg_isready`); RabbitMQ is running *and* the imported queues exist (`rabbitmq-diagnostics`, `rabbitmqctl`); Kafka answers an API request, `interval/timeout 10s` because each probe starts a JVM (`kafka-broker-api-versions.sh`); ZooKeeper answers `srvr` (`nc`); gRPC, GraphQL and the Pub/Sub emulator accept connections on their port (bash `/dev/tcp`; the emulator image opens 8682 only after it has created its topics); MockServer uses the image's own healthcheck. Probes in `latest` images depend on their tools staying present until CI-07 pins them. If CI's `docker-compose` is too old for `condition: service_healthy`, fall back to `docker-compose up -d` plus a bounded `docker inspect` health poll in the job.

## 3 · Dependencies

| ID | Title | Impact | Cost | Completed |
|---|---|---|---|---|
| DEP-09 | marshmallow deprecations (prepare for 4.x) | Low | XS | 2026-11-09 |

### DEP-09 — marshmallow deprecations
- **Completed:** 2026-11-09
- **What / why:** `fields.Boolean(default=False)` (`folker/load/schemas.py:47`) is deprecated and removed in marshmallow 4. Use `load_default`, and check the other schemas for the same pattern.
- **Impact:** Low (Renovate will propose 4.x eventually).
- **Cost:** XS.
- **Benefit:** Smooth major upgrade.
- **Done:** `default=False` is now `dump_default=False`. That is the 3.13 rename of `default` (dump-only); `load_default` would have changed loading, and omitted `parallel` already falls through to `Test.__init__`'s `False`. The only other marshmallow 4 warning was `fields.String(strict=False)` on the wait schema, which was unused metadata (the `pre_load` hook already stringifies `time`), so the argument was removed. No `RemovedInMarshmallow4Warning` left in the unit suite.

## 4 · Bugs

| ID | Title | Impact | Cost | Completed |
|---|---|---|---|---|
| BUG-01 | `collections.Mapping` crash on Python ≥ 3.10 ✅ | High | XS | 2026-11-06 |
| BUG-02 | Parallel tests lose the selected profile | High | S | 2026-11-10 |
| BUG-03 | `foreach` stops after first failing iteration | High | XS | 2026-11-10 |
| BUG-04 | VOID template + real action → `action = None` | High | XS | 2026-11-10 |
| BUG-05 | Stage's own `foreach` lost when using a template | Med | XS | 2026-11-10 |
| BUG-06 | Validation ignores `wrong_fields` | Med | XS | 2026-11-10 |
| BUG-07 | Test files in paths with spaces fail to load | Med | XS | 2026-11-10 |
| BUG-08 | Shared mutable default `foreach={}` in `Test` | Low | XS | 2026-11-10 |
| BUG-09 | Integer identity comparison in assertions | Low | XS | 2026-11-10 |
| BUG-10 | Non-raw regex string (warning in 3.12+) | Low | XS | 2026-11-10 |
| BUG-11 | Multiple profiles: random one picked, rest ignored | Med | XS | 2026-11-10 |
| BUG-13 | Secrets leaked in REST debug logs | Med | S | 2026-11-10 |
| BUG-14 | Network calls without timeouts can hang forever | High | S | 2026-11-10 |
| BUG-15 | Failing `if:` condition silently skips the stage | Med | XS | 2026-11-10 |
| BUG-16 | REST debug logging can turn a request into an error | Low | XS | 2026-11-10 |
| BUG-17 | Working-directory modules not importable from an installed CLI ✅ | High | XS | 2026-11-07 |

### BUG-01 — `collections.Mapping` crash on Python ≥ 3.10 ✅
- **Completed:** 2026-11-06
- **What / why:** `folker/model/context/context.py:202` uses `collections.Mapping`, which was removed in Python 3.10. Any nested `save` into an existing dict raises `AttributeError` in the shipped 3.10 image.
- **Impact:** High.
- **Cost:** XS. 1 line (`collections.abc.Mapping`).
- **Benefit:** Nested saves work in production.

### BUG-02 — Parallel tests lose the selected profile
- **Completed:** 2026-11-10
- **What / why:** `parallel_executor.py:13-15` reads the global `folker.profiles` inside the worker. Under `spawn` (macOS) or `forkserver` (Linux from 3.14) it's empty. Reproduced: the same test passes sequentially and fails with "Missing reference" when `parallel: true`. Fix: resolve the profile into the `Context` in the parent and pass it to the worker.
- **Impact:** High.
- **Cost:** S. ~15 lines.
- **Benefit:** Parallel runs behave like sequential ones.
- **Depends on:** TST-03 recommended. Root cause addressed in IMP-03.
- **Done:** `ParallelExecutor.execute` now resolves the selected profile in the parent process and passes it to each worker, instead of the worker reading the global `folker.profiles` (empty under `spawn`/`forkserver`). Reproduced first on Python 3.10: sequential and `fork` passed, `spawn` and `forkserver` failed every test with "Missing reference". Regression tests in `tests/executor/test_parallel_executor.py` run the executor under all three start methods; the profile test failed under `spawn`/`forkserver` before the fix. Root cause (global registries) is still addressed by IMP-03.

### BUG-03 — `foreach` stops after first failing iteration
- **Completed:** 2026-11-10
- **What / why:** `folker/model/test.py:55`: `executions_result and self._execute(...)` short-circuits, so iterations after a failure never run or report.
- **Impact:** High. Data-driven tests hide failures.
- **Cost:** XS. Evaluate first, then combine.
- **Benefit:** Complete results for data-driven tests.
- **Done:** `Test.execute` runs each `foreach` iteration first and combines the results afterwards, so a failing iteration no longer skips the ones after it. Tests in `tests/model/test_test_execution.py`: a failure in the first of three iterations still runs all three, and every iteration is reported (3 starts, 2 errors, 1 finish); both failed before the fix. An all-pass guard test was added. The existing failure test only failed on the last iteration, so it never exercised the bug.

### BUG-04 — VOID template + real action → `action = None`
- **Completed:** 2026-11-10
- **What / why:** `VoidStageAction.__add__` (`folker/module/void/action.py:12`) returns `None`, so a template stage without an action, extended by a stage with an action, ends up with no action and crashes. It should return the enrichment (or a copy of self when the enrichment is also VOID).
- **Impact:** High.
- **Cost:** XS.
- **Benefit:** Templates usable for shared save/log/assert blocks.
- **Done:** `VoidStageAction.__add__` returns a copy of the enrichment (so VOID + real action gives the real action, and VOID + VOID stays VOID) instead of `None`. Reproduced first on Python 3.10: a VOID template stage extended by a `WaitStageAction` stage ended with `action = None`. Regression tests: `tests/module/void/test_action_enrichment.py` and `test_enrich_action_of_void_template` in `tests/model/stage/test_stage_enrichment.py`; they failed before the fix. The reverse order (real template + VOID stage) already worked.

### BUG-05 — Stage's own `foreach` lost when using a template
- **Completed:** 2026-11-10
- **What / why:** `folker/model/stage/stage.py:62` writes the merged dict to `result.params` instead of `result.foreach`.
- **Impact:** Med.
- **Cost:** XS. 1 line.
- **Benefit:** `foreach` works with templates.
- **Done:** `Stage.__add__` now assigns the merged dict to `result.foreach` (it wrote `result.params`, which nothing reads), so a stage's own `foreach` survives being merged onto a template stage: template and stage keys are combined and the stage wins on conflicts. Tests in `tests/model/stage/test_stage_enrichment.py` (stage `foreach` kept, template `foreach` kept, merge and override, template not modified); the first and third failed before the fix.

### BUG-06 — Validation ignores `wrong_fields`
- **Completed:** 2026-11-10
- **What / why:** `folker/model/validation.py:16`: `len(self.missing_fields) == len(self.missing_fields) == 0` checks `missing_fields` twice, so an invalid Postgres `method` passes validation and fails at runtime.
- **Impact:** Med. May surface previously hidden errors in user suites, so call it out in the changelog.
- **Cost:** XS.
- **Benefit:** Errors at load time instead of mid-run.
- **Done:** `ValidationReport.__bool__` now checks both `missing_fields` and `wrong_fields`. Correction to the description above: on Python 3.10 an invalid `method` on Postgres or File was *already* rejected at load time, because the action's mandatory-field check also adds `action.method` to `missing_fields`, which masked the defect. The bug was real but latent: a report with only `wrong_fields` counted as valid, so any validator whose only finding is a wrong field passed silently. Because the current actions already failed through `missing_fields`, the fix changes no behaviour for existing suites: all 35 example suites load with 0 errors before and after, so no changelog warning is needed. Tests in `tests/model/test_validation_report.py` (report, `merge_with_prefix`, `generate_error`, and an action whose only problem is a wrong field); four of them failed before the fix.

### BUG-07 — Test files in paths with spaces fail to load
- **Completed:** 2026-11-10
- **What / why:** `folker/load/files.py:82`: `filename.resolve().as_uri()[7:]` yields `%20`-encoded paths.
- **Impact:** Med. Common on macOS/Windows.
- **Cost:** XS. Use `str(filename.resolve())`.
- **Benefit:** Works in any directory.
- **Done:** `load_schema` uses `str(filename.resolve())` instead of `filename.resolve().as_uri()[7:]`. The URI form is percent-encoded, so it broke on spaces and also on `%`, `#`, `?` and non-ASCII characters in any directory of the path, not only spaces. Tests in `tests/load/test_load_files.py` load a test file from directories named with each of those characters, and from a nested directory under a parent with spaces; all six failed before the fix.

### BUG-08 — Shared mutable default `foreach={}`
- **Completed:** 2026-11-10
- **What / why:** `folker/model/test.py:24`: all `Test` instances share the same default dict.
- **Impact:** Low (latent).
- **Cost:** XS.
- **Benefit:** Removes a source of cross-test contamination.
- **Done:** `Test.__init__` takes `foreach: dict = None` and stores `foreach if foreach else {}`, the same pattern it already used for `tags` and `stages`, so each `Test` gets its own dict. It was the only mutable default argument in `folker/`. Test in `tests/model/test_test_defaults.py`: mutating the `foreach` of one default-constructed `Test` no longer shows up in another (failed before the fix); guard tests cover an explicit `{}`, a given `foreach`, and `tags`/`stages`.

### BUG-09 — Integer identity comparison in assertions
- **Completed:** 2026-11-10
- **What / why:** `folker/model/stage/assertions.py:77`: `success is not executed` only works because CPython caches small ints. Use `!=`.
- **Impact:** Low.
- **Cost:** XS.
- **Benefit:** Correct for any count. Removes a `SyntaxWarning`.
- **Done:** both counts are now compared with `!=`, in `StageAssertions._wrap_up_test` (the one the task names) and in `TestLogger.assert_test_result` (`folker/logger/test_logger.py`, same pattern, not listed in the task). Beyond CPython's small-int cache (-5..256), a stage with more than 256 passing assertions raised a failure with an empty failure list, and the logger reported a passing run as failed. Tests: 300 passing assertions no longer raise, one failure among 300 is still the only reported failure, and the logger prints a failure line only when the counts differ (the logger test builds its ints at runtime, since two equal literals in one function are the same object). The task's remark about removing a `SyntaxWarning` was not verified: no such warning was seen on Python 3.10.

### BUG-10 — Non-raw regex string
- **What / why:** `folker/model/context/context.py:12`: `'\${...}'` raises a `SyntaxWarning` on 3.12+ and will eventually be an error.
- **Impact:** Low.
- **Cost:** XS.
- **Benefit:** Clean on modern Python (prerequisite for DEP-04).
- **Completed:** 2026-11-10
- **Done:** already fixed when picked up: `contains_variable_reference` uses `r'\${([^{}]+)}'` (raw string, since `8620ad8`), and compiling every `.py` file under `folker/`, `tests/` and `example/` on Python 3.12 with warnings as errors reports nothing. What was missing was a guard, so `tests/test_source_warnings.py` compiles each source file with warnings as errors (an invalid escape is a `DeprecationWarning` on 3.10/3.11 and a `SyntaxWarning` on 3.12+, and pytest misses it whenever a cached `.pyc` exists) and checks that it detects a bad escape. It fails on the pre-fix `context.py` on 3.10 and 3.12 and passes now. The guard has no third-party imports, so it also runs on 3.12 with only pytest (`--noconftest`), which is useful for DEP-04 while `grpcio-tools==1.48.1` still won't install there (DEP-06).

### BUG-11 — Multiple profiles: random one picked, rest ignored
- **What / why:** `config.profiles` is a `set`, and both executors use `list(config.profiles)[0]`. With `-p a -p b` the chosen profile is arbitrary and the others are ignored without a warning. Short-term fix: error out or warn when more than one is given, and fail on an unknown profile name (it currently falls back to DEFAULT silently). Merging is FEAT-05.
- **Impact:** Med.
- **Cost:** XS.
- **Benefit:** Deterministic configuration.
- **Completed:** 2026-11-10
- **Done:** (superseded for several profiles by FEAT-05: they are now merged instead of rejected) verified on the old code: `-p stagin` (a typo) and `-p base -p staging` both exited 0 and ran with DEFAULT or an arbitrary profile. New `select_profile(config)` in `folker/executor/__init__.py`, used by both executors, now returns DEFAULT when no profile is given and otherwise requires exactly one loaded profile: an unknown name or several names raise `InvalidProfileSelectionException`, listing what was selected and which profiles exist. `folker/cli.py` calls it right after loading, so the run fails before any test executes, including when no test would reach an executor. The docs claimed `-p a -p b` was supported, so the `-p` row of `docs/Documentation.md` now says exactly one profile. Tests in `tests/executor/test_profile_selection.py` and `tests/test_cli.py` (end to end through the CLI). Changelog (CI-10): a profile name that does not exist now fails the run. See FEAT-05 for several profiles.

### BUG-13 — Secrets leaked in REST debug logs
- **What / why:** `RestStageAction._log_debug` dumps headers, auth and body after variable resolution, so secrets referenced via `${...}` print in clear text with `--debug`. Apply the same obfuscation the test logger uses for secrets.
- **Impact:** Med. Credentials end up in CI logs.
- **Cost:** S. Probably a shared redaction helper used by all modules.
- **Benefit:** Safe to enable debug in CI.
- **Completed:** 2026-11-10
- **Done:** the fix is in the logger, not in each module, so REST, RabbitMQ and Pub/Sub are covered at once and new modules are safe by default. `TestLogger.action_prelude` (called by every action) records the values of `context.secrets` (nested values included, empty ones ignored), and `action_debug`, `action_error` and `action_warn` mask them with `*` of the same length, as the SECRETS trace dump already did. Masking also matches the JSON-escaped form of a secret, because debug messages are `json.dumps` output where quotes, backslashes and non-ASCII characters are escaped. Longest secrets are masked first. Tests in `tests/logger/test_secret_redaction.py`, including a REST action run with secrets in headers and authorization; all but two failed before the fix. Limits: only values in `context.secrets` are masked (not secrets copied into test variables with `save`), and `message` (the print action), assertion debug dumps and trace `TEST CONTEXT` are not redacted.

### BUG-14 — Network calls without timeouts can hang forever
- **What / why:** `requests.*` (REST), postgres, rabbitmq, zookeeper and graphql calls have no timeouts (only Kafka has any). A dead endpoint hangs the CI job until the global timeout. Add sensible defaults, overridable per action.
- **Impact:** High.
- **Cost:** S.
- **Benefit:** Fails fast with a clear error.
- **Related:** FEAT-04.
- **Completed:** 2026-11-10
- **Decision:** [ADR 20261110](../adrs/20261110-network-timeouts-default-and-per-action.md).
- **Done:** REST, Postgres, RabbitMQ, ZooKeeper, GraphQL, gRPC and Pub/Sub now time out after `DEFAULT_TIMEOUT` (30 s, `folker/module/timeout.py`), and each action accepts an optional `timeout` in seconds (schema field, merged by templates, validated centrally in `StageAction`: zero, negative and non-numeric values are `action.timeout` wrong fields). What it bounds, per module:
  - REST and GraphQL: `requests` timeout (connect and each read, not the total transfer time). A timeout is reported as the action `error`, as any other request failure.
  - Postgres: `connect_timeout` (rounded up to whole seconds) and `statement_timeout`, so a query slower than the timeout fails too. `execute` also crashed with `UnboundLocalError` in `finally` when the connection failed, hiding the real error; `connection` and `cursor` are now initialised first.
  - RabbitMQ: `socket_timeout`, `stack_timeout` and `blocked_connection_timeout` of the connection.
  - ZooKeeper: `KazooClient.start(timeout=...)` (it was already 15 s); a failed start now stops the client, which otherwise keeps its thread alive. The failure still propagates and fails the test.
  - gRPC: the call deadline (`timeout=` on the stub method), which for a server-streaming call covers the whole stream.
  - Pub/Sub: `future.result(timeout=...)` for publish, and the `timeout` of `pull`, `acknowledge`, `list_topics` and `list_subscriptions`. gRPC and Pub/Sub were not in the original list.
  - Tests in `tests/module/test_timeouts.py`; 71 of them failed before the fix.
- **Not covered:** Kafka already had its own 10 s timeouts and takes no `timeout` field. RabbitMQ and ZooKeeper operations after connecting are not individually bounded. Changelog (CI-10): a request or query slower than 30 s now fails unless the action sets a larger `timeout`.

### BUG-15 — Failing `if:` condition silently skips the stage
- **Completed:** 2026-11-10
- **What / why:** `Stage.skip_stage_execution` catches every `eval` exception and returns "skip". A typo or type error in a condition looks like "condition false". It should fail the test with the condition and the error.
- **Impact:** Med. Behaviour change, so note it in the changelog.
- **Cost:** XS.
- **Benefit:** Condition mistakes become visible.
- **Done:** a condition that cannot be evaluated (undefined name, syntax error, division by zero, non-string condition) now raises the new `UnresolvableConditionException` with the `condition`, the underlying `error` and the `stage` in its details, so the test fails instead of the stage being skipped. A condition that evaluates to false still skips. `Stage.execute` attaches the stage to any `SourceException` raised while resolving the condition, including `VariableReferenceResolutionException`, which already failed the test before. The existing `test_stage_conditional_execution_error` asserted the old skip behaviour; it is now parametrised over four bad conditions and expects the exception (failed before the fix). The only example using `if:` (`example/test/dummy/test_dummy_conditional.yaml`) is a valid condition. Changelog (CI-10): conditions that previously errored and were skipped will now fail the run.

### BUG-16 — REST debug logging can turn a request into an error
- **What / why:** `_log_debug` calls `json.dumps(parameters)` inside the request `try`. Non-JSON-serialisable values (for example file handles in `data`) would raise before the request is sent and be reported as an action error. Verify, then serialise with `default=str`.
- **Impact:** Low.
- **Cost:** XS.
- **Benefit:** Debug mode never changes behaviour.
- **Completed:** 2026-11-10
- **Done:** verified, and worse than described: `_log_debug` serialises before `action_debug` checks the debug flag, so a non-serialisable value in the request broke the action even without `--debug`. `data` is a free-form dict, so YAML values such as a date (`2026-11-10`) or `!!binary` bytes reach it. The action then reported `Object of type ... is not JSON serializable` and never sent the request. `_log_debug` now uses `json.dumps(parameters, default=str)`. Tests in `tests/module/rest/test_rest_action_debug_logging.py` (date, bytes and an arbitrary object, with debug on and off; the request is sent with the original values and the value is still logged); all seven failed before the fix. Not changed: the identical `_log_debug` in RabbitMQ and Pub/Sub only receives strings today, and `assertion_fail` also `json.dumps` its variables.

### BUG-17 — Working-directory modules not importable from an installed CLI ✅
- **Completed:** 2026-11-07
- **What / why:** Generated `protos/*_pb2.py` (protobuf, grpc, rest-proto) and CODE action modules are imported relative to the working directory, but folker never put it on `sys.path`. It only worked because the old Dockerfile used `pip install -e .` from `/`. After the multi-stage Dockerfile (`0e8c453`), the `folker-test` console script only had `/usr/local/bin` on the path, and the protobuf, grpc and code integration tests failed with `No module named 'protos'` / `'testcode'`. Plain `pip install` users were affected too. Fix: `make_working_directory_importable()` in `folker/cli.py` adds the working directory to `sys.path` at startup.
- **Impact:** High. Three modules were unusable from any non-editable install, including the new image.
- **Cost:** XS. ~10 lines plus a CLI regression test (`tests/test_cli.py`).
- **Benefit:** Same behaviour for Docker, pip and editable installs.
- **Note:** `0e8c453` also changed the image `WORKDIR` from `/` to `/app`. Mention it in the changelog (CI-10) for users who mount test files into the container.

---

## 6 · Features

| ID | Title | Impact | Cost | Completed |
|---|---|---|---|---|
| FEAT-05 | Ordered merging of multiple profiles | Med | S | 2026-11-10 |

### FEAT-05 — Ordered merging of multiple profiles
- **What / why:** Allow `-p base -p staging`, merged in order (later wins), for example shared defaults plus per-environment overrides.
- **Impact:** Med.
- **Cost:** S.
- **Benefit:** Fewer duplicated profile files.
- **Completed:** 2026-11-10
- **Done:** `-p base -p staging` (or `-p base,staging`) builds one profile, named `base,staging`, merging the definitions in command-line order. `Configuration.profiles` is now an ordered list (it was a set, which has no order); empty names (`-p a,,b`) are ignored and a name repeated later takes precedence again. `select_profile` (`folker/executor/__init__.py`) merges `context` and `secrets` with `mergedeep`: nested mappings combine key by key, and on any other conflict (scalar vs scalar, list vs list, mapping vs scalar) the later profile's value replaces the earlier one. Lists are replaced, not concatenated. The registered profiles are not modified, and the single-profile case returns the profile itself. A name that is not loaded still fails with `InvalidProfileSelectionException` (BUG-11 fixed the silent fallback to DEFAULT). Precedence overall is unchanged: `-c` / `-s` values beat any profile. `-p` row of `docs/Documentation.md` updated. Tests in `tests/executor/test_profile_selection.py`, `tests/test_parameters.py`, `tests/test_cli.py` (end to end, both orders) and `tests/executor/test_parallel_executor.py` (merged profile reaches workers under fork, spawn and forkserver).

