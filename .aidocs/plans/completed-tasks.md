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
| BUG-07 | Test files in paths with spaces fail to load | Med | XS | 2026-11-10 |
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

### BUG-07 — Test files in paths with spaces fail to load
- **Completed:** 2026-11-10
- **What / why:** `folker/load/files.py:82`: `filename.resolve().as_uri()[7:]` yields `%20`-encoded paths.
- **Impact:** Med. Common on macOS/Windows.
- **Cost:** XS. Use `str(filename.resolve())`.
- **Benefit:** Works in any directory.
- **Done:** `load_schema` uses `str(filename.resolve())` instead of `filename.resolve().as_uri()[7:]`. The URI form is percent-encoded, so it broke on spaces and also on `%`, `#`, `?` and non-ASCII characters in any directory of the path, not only spaces. Tests in `tests/load/test_load_files.py` load a test file from directories named with each of those characters, and from a nested directory under a parent with spaces; all six failed before the fix.

### BUG-17 — Working-directory modules not importable from an installed CLI ✅
- **Completed:** 2026-11-07
- **What / why:** Generated `protos/*_pb2.py` (protobuf, grpc, rest-proto) and CODE action modules are imported relative to the working directory, but folker never put it on `sys.path`. It only worked because the old Dockerfile used `pip install -e .` from `/`. After the multi-stage Dockerfile (`0e8c453`), the `folker-test` console script only had `/usr/local/bin` on the path, and the protobuf, grpc and code integration tests failed with `No module named 'protos'` / `'testcode'`. Plain `pip install` users were affected too. Fix: `make_working_directory_importable()` in `folker/cli.py` adds the working directory to `sys.path` at startup.
- **Impact:** High. Three modules were unusable from any non-editable install, including the new image.
- **Cost:** XS. ~10 lines plus a CLI regression test (`tests/test_cli.py`).
- **Benefit:** Same behaviour for Docker, pip and editable installs.
- **Note:** `0e8c453` also changed the image `WORKDIR` from `/` to `/app`. Mention it in the changelog (CI-10) for users who mount test files into the container.
