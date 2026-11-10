# folker-test — Improvement Execution Plan

Created: 2026-11-05 · Baseline: branch `beta` @ `2c625c6`

Pick tasks by ID ("work on BUG-03"). Each task is meant to be one small PR.
Completed tasks (☑) live in [completed-tasks.md](completed-tasks.md), with their completion dates and notes.
✅ = reproduced during analysis · 🔍 = suspected, verify first · 📐 = needs an ADR (per `.aidocs/STRATEGY.md`)

## Scales

| Impact | Meaning |
|---|---|
| **High** | Wrong results, crashes, broken releases, or security exposure |
| **Med** | Reliability or developer experience noticeably better |
| **Low** | Nice to have / hygiene |

| Cost | Effort | Code changed |
|---|---|---|
| **XS** | < 1 h | < 10 lines |
| **S** | ≤ ½ day | < 100 lines |
| **M** | 1–3 days | 100–500 lines |
| **L** | > 3 days | > 500 lines / many modules |

**Working rule:** every BUG task ships with a regression test that fails before the fix (see TST-02).

---

## Index

| ID | Title | Impact | Cost | Status |
|---|---|---|---|---|
| **1 · CI/CD** |||||
| CI-07 | Pin integration service images (Kafka/ZooKeeper done) | High | S | ◐ |
| CI-08 | Update EOL executors and actions | Med | XS | ☐ |
| CI-09 | Image vulnerability scan, SBOM, multi-arch build | Med | S | ☐ |
| CI-10 | Versioning and release process | Med | M | ☐ |
| CI-11 | Renovate guardrails and grouping | Med | XS | ☐ |
| **2 · Testability** |||||
| TST-02 | Regression-test policy for bug fixes | High | — | ☐ |
| TST-03 | Executor tests (sequential/parallel, start methods) | High | S | ☐ |
| TST-04 | Loader tests (`folker/load/files.py`) | Med | S | ☐ |
| TST-05 | In-process CLI end-to-end tests (no Docker) | High | M | ☐ |
| TST-06 | Execution tests for untested actions | Med | M | ☐ |
| TST-08 | Template/enrichment merge test matrix | Med | S | ☐ |
| **3 · Dependencies** |||||
| DEP-01 | Single dependency source: `pyproject.toml` + lock 📐 | High | M | ☐ |
| DEP-02 | Move dev tools out of runtime dependencies | Med | XS | ☐ |
| DEP-03 | Remove unused / stale transitive pins | Med | XS | ☐ |
| DEP-04 | Python 3.10 (EOL) → 3.12/3.13 | High | S | ☐ |
| DEP-05 | `google-cloud-pubsub` 1.7.2 → 2.x 📐 | High | M | ☐ |
| DEP-06 | Align `grpcio` / `grpcio-tools` / `protobuf` | High | S | ☐ |
| DEP-07 | Gmail: `oauth2client` → `google-auth` | Med | S | ☐ |
| DEP-08 | `gql` 2.0 → 3.x | Med | S | ☐ |
| DEP-10 | Optional extras per module 📐 | Med | S | ☐ |
| **4 · Bugs** |||||
| BUG-03 | `foreach` stops after first failing iteration ✅ | High | XS | ☐ |
| BUG-05 | Stage's own `foreach` lost when using a template ✅ | Med | XS | ☐ |
| BUG-06 | Validation ignores `wrong_fields` ✅ | Med | XS | ☐ |
| BUG-07 | Test files in paths with spaces fail to load ✅ | Med | XS | ☐ |
| BUG-08 | Shared mutable default `foreach={}` in `Test` ✅ | Low | XS | ☐ |
| BUG-09 | Integer identity comparison in assertions | Low | XS | ☐ |
| BUG-10 | Non-raw regex string (warning in 3.12+) | Low | XS | ☐ |
| BUG-11 | Multiple profiles: random one picked, rest ignored | Med | XS | ☐ |
| BUG-12 | Proto generation failures reported as success | Med | XS | ☐ |
| BUG-13 | Secrets leaked in REST debug logs | Med | S | ☐ |
| BUG-14 | Network calls without timeouts can hang forever | High | S | ☐ |
| BUG-15 | Failing `if:` condition silently skips the stage | Med | XS | ☐ |
| BUG-16 | REST debug logging can turn a request into an error 🔍 | Low | XS | ☐ |
| **5 · Improvements** |||||
| IMP-01 | Strict loading: broken YAML fails the run | High | S | ☐ |
| IMP-02 | Narrow broad `except Exception` handling | Med | M | ☐ |
| IMP-03 | Replace global registries with an explicit registry 📐 | Med | M | ☐ |
| IMP-04 | Lazy / plugin-based module loading 📐 | Med | M | ☐ |
| IMP-05 | Dataclass-based actions + one generic merge | Med | L | ☐ |
| IMP-06 | Logger composition (formatter × sink) | Low | M | ☐ |
| IMP-07 | Executor cleanup (shared context, pool lifecycle, workers) | Med | S | ☐ |
| IMP-08 | Safer expression evaluation 📐 | Med | M | ☐ |
| IMP-09 | Correct type hints + type checking | Low | M | ☐ |
| IMP-10 | Proper variable-path parser (`a.b[0].c`) | Med | S | ☐ |
| IMP-11 | Proto generation scope and caching | Low | S | ☐ |
| IMP-12 | Housekeeping | Low | XS | ☐ |
| **6 · Features** |||||
| FEAT-01 | JUnit XML / JSON report output | High | M | ☐ |
| FEAT-02 | `--validate` dry-run mode | Med | S | ☐ |
| FEAT-03 | Environment-variable references (`${env.X}`) | Med | S | ☐ |
| FEAT-04 | Stage-level `retry` / `timeout` | High | M | ☐ |
| FEAT-05 | Ordered merging of multiple profiles | Med | S | ☐ |
| FEAT-06 | `--list` tests matching the filters | Low | XS | ☐ |
| FEAT-07 | Filter tests by name pattern (`-k`) | Low | S | ☐ |
| FEAT-08 | Configurable parallelism (`--workers N`) | Low | XS | ☐ |
| FEAT-09 | Blueprints: reusable step sequences inlined into tests 📐 | High | M | ☐ |

---

## 1 · CI/CD

### CI-07 — Pin integration service images
- **What / why:** `mockserver:latest`, `gcloud-pubsub-emulator:latest` and `postgres` (untagged) drift silently. Pin by version (ideally digest) and let Renovate bump them.
- **Already happened (2026-11-05):** ✅ Bitnami removed its free images from `docker.io/bitnami`, and CI failed with `manifest for bitnami/kafka:3 not found`. A `bitnamilegacy` hotfix was replaced by official images: `apache/kafka:4.1.0` in single-node KRaft mode (no ZooKeeper dependency) and `zookeeper:3.9.4`. The unused `kafka2` service was removed (verified: kafka 1/1, zookeeper 4/4). **Remaining:** pin `mockserver`, the pubsub emulator and `postgres`; update the commented-out Bitnami services in `.devcontainer/docker-compose.yml`.
- **Impact:** High. External changes can break CI with no code change.
- **Cost:** S. `docker-compose.yaml` and `.devcontainer/docker-compose.yml`.
- **Benefit:** Reproducible builds. Upgrades become visible PRs.
- **Depends on:** none.

### CI-08 — Update EOL executors and actions
- **What / why:** `circleci/buildpack-deps:stretch` (Debian 9, EOL) and `github/codeql-action@v2` (deprecated) need replacing with `cimg/base` and `@v3`. Review orb versions.
- **Impact:** Med. Avoids sudden pipeline breakage and unpatched build hosts.
- **Cost:** XS.
- **Benefit:** Supported, faster tooling.
- **Depends on:** none.

### CI-09 — Image vulnerability scan, SBOM, multi-arch build
- **What / why:** There's no scanning of the published image, and it's built for one architecture only. Add a Trivy/Grype scan (fail on critical), generate an SBOM, and use `buildx` for amd64 + arm64 (Apple Silicon users).
- **Impact:** Med.
- **Cost:** S.
- **Benefit:** Security visibility. Native performance on ARM.
- **Depends on:** CI-04.

### CI-10 — Versioning and release process
- **What / why:** `setup.py` says `2.5` while CI tags images `3.0.<pipeline>`. The beta build also tags `latest` locally. Use a single version source (git tag → package version → image tag), semantic versioning and a CHANGELOG.
- **Impact:** Med. Users can't tell what they're running.
- **Cost:** M.
- **Benefit:** Traceable releases and reliable rollbacks.
- **Depends on:** DEP-01, CI-04.

### CI-11 — Renovate guardrails and grouping
- **What / why:** Minor and patch updates automerge with only unit tests as the gate. `google-api-python-client` gets a PR almost every week while `google-cloud-pubsub` stays years behind. Group Google/grpc/protobuf packages, keep automerge only behind CI-01..03, and enable the dependency dashboard.
- **Impact:** Med.
- **Cost:** XS. `renovate.json`.
- **Benefit:** Fewer, safer dependency PRs.
- **Depends on:** CI-01, CI-02, CI-03.

---

## 2 · Testability

### TST-02 — Regression-test policy for bug fixes
- **What / why:** Every BUG-xx gets a test that fails before the fix and passes after. The probe scripts from the analysis are the starting point.
- **Impact:** High. Bugs stay fixed.
- **Cost:** Built into each BUG task.
- **Benefit:** The suite grows where bugs actually happen.

### TST-03 — Executor tests
- **What / why:** `ParallelExecutor` and `SequentialExecutor` have no tests. BUG-02 shipped because of that. Test both executors, including the parallel one under the `spawn` and `forkserver` start methods (macOS default; Linux default from 3.14).
- **Impact:** High.
- **Cost:** S. ~100 lines of tests.
- **Benefit:** Safe refactoring of execution (IMP-03, IMP-07).
- **Depends on:** none.
- **Progress:** `ParallelExecutor` already has tests in `tests/executor/test_parallel_executor.py` (context, profile and failure reporting under `fork`, `spawn` and `forkserver`), added with BUG-02. Still open: `SequentialExecutor` tests and the remaining parallel cases (empty list, result ordering, foreach tests).

### TST-04 — Loader tests
- **What / why:** `folker/load/files.py` (globbing, template enrichment, profile loading, error handling) is mostly untested. Cover paths with spaces (BUG-07), broken YAML, missing template ids and `-tf` filtering, using `tmp_path`.
- **Impact:** Med.
- **Cost:** S.
- **Benefit:** Enables IMP-01 and IMP-03.

### TST-05 — In-process CLI end-to-end tests
- **What / why:** Docker-free modules (print, void, wait, save, foreach, conditional, template, profile, code, file) only get end-to-end coverage in the Docker integration jobs. Run them in-process via `click.testing.CliRunner` against `example/test/...` copied into `tmp_path`.
- **Impact:** High. Seconds instead of minutes, and runs locally.
- **Cost:** M.
- **Benefit:** Fast end-to-end feedback. Reduces reliance on the flaky Docker matrix.
- **Depends on:** TST-01.

### TST-06 — Execution tests for untested actions
- **What / why:** `code`, `file`, `gmail`, `graphql`, `postgres`, `protobuf` and `zookeeper` only have enrichment/validation tests, so their `execute()` is untested. Add tests with mocked clients (`pytest-mock`, `responses`/`requests-mock`).
- **Impact:** Med.
- **Cost:** M. One file per module.
- **Benefit:** Dependency upgrades (DEP-05..08) become verifiable without Docker.

### TST-08 — Template/enrichment merge test matrix
- **What / why:** `__add__` merges caused BUG-04 and BUG-05. Add a parametrised matrix: for each action type × (template has field / stage has field / both / neither), assert the merged result.
- **Impact:** Med.
- **Cost:** S.
- **Benefit:** Safety net for IMP-05.

---

## 3 · Dependencies

### DEP-01 — Single dependency source: `pyproject.toml` + lock 📐
- **What / why:** `setup.py` and `requirements.txt` duplicate each other and have drifted (pytest only in one, a different order). Move to `pyproject.toml` (PEP 621) with a lock file (`uv` or `pip-tools`) and dependency groups (`dev`, `test`).
- **Impact:** High. Reproducible installs, and the basis for all the other DEP tasks.
- **Cost:** M. Packaging, Makefile, Dockerfiles, CI.
- **Benefit:** One source of truth. Deterministic Docker builds.
- **ADR:** yes (packaging / tooling change).

### DEP-02 — Move dev tools out of runtime dependencies
- **What / why:** `pylint` and `coverage` are in `install_requires`, so they ship to every user and into the image.
- **Impact:** Med. Smaller image, smaller attack surface.
- **Cost:** XS.
- **Benefit:** Leaner runtime.
- **Depends on:** can be done now, or as part of DEP-01.

### DEP-03 — Remove unused / stale transitive pins
- **What / why:** `google==3.0.0` (an unrelated Google-search scraper), `certifi==2023.11.17` (stale CA bundle), `chardet`, `idna` and `pyOpenSSL` are never imported directly. Pinning them freezes transitive dependencies at old, vulnerable versions.
- **Impact:** Med. Security (CA bundle, OpenSSL).
- **Cost:** XS. Verify with `grep` and a test run, then delete.
- **Benefit:** Less to maintain. Fewer resolver conflicts.

### DEP-04 — Python 3.10 → 3.12/3.13
- **What / why:** Python 3.10 reached end of life in October 2026. Update the Dockerfiles, devcontainer and CI.
- **Impact:** High. Security patches, plus 10–25% faster execution.
- **Cost:** S.
- **Benefit:** Supported runtime.
- **Depends on:** BUG-01, BUG-10, CI-01, DEP-06.

### DEP-05 — `google-cloud-pubsub` 1.7.2 → 2.x 📐
- **What / why:** The 2020 release holds `google-api-core`, `grpcio` and `protobuf` back. During analysis the resolver couldn't find any buildable grpc set alongside it on Python 3.9/arm64. The 2.x API changed (request objects, `subscribe` flow), so `folker/module/gcp/pubsub/action.py` (313 lines) needs porting.
- **Impact:** High. Unblocks the whole Google/grpc stack.
- **Cost:** M.
- **Benefit:** Modern, supported client.
- **Depends on:** TST-06 (pubsub execution tests exist; extend them).
- **ADR:** yes (core SDK change).

### DEP-06 — Align `grpcio` / `grpcio-tools` / `protobuf`
- **What / why:** `grpcio==1.70.0` vs `grpcio-tools==1.48.1`. The tools version fails to build wheels on modern platforms, and mismatched protoc/runtime versions produce incompatible `_pb2` files.
- **Impact:** High. Installation currently fails on some platforms.
- **Cost:** S.
- **Benefit:** Installable everywhere. Correct generated code.
- **Depends on:** DEP-05.

### DEP-07 — Gmail: `oauth2client` → `google-auth`
- **What / why:** `oauth2client` has been deprecated since 2017. `google-auth-oauthlib` is already a dependency.
- **Impact:** Med.
- **Cost:** S. `folker/module/gmail/action.py`.
- **Benefit:** Removes a dead library. Drops the `httplib2` coupling.

### DEP-08 — `gql` 2.0 → 3.x
- **What / why:** gql 2.0.0 is from 2019. 3.x changed the transport API (`RequestsHTTPTransport`, `Client(transport=...)`).
- **Impact:** Med.
- **Cost:** S. `folker/module/graphql/action.py`.
- **Benefit:** Supported client.
- **Depends on:** TST-06 (graphql).

### DEP-10 — Optional extras per module 📐
- **What / why:** Every install pulls Kafka, Postgres, Google, grpc, ZooKeeper and RabbitMQ clients. Offer `folker-test[rest,kafka,gcp,...]` plus `[all]`, and keep `[all]` for the Docker image.
- **Impact:** Med. Smaller installs, fewer conflicts for pip users.
- **Cost:** S.
- **Benefit:** Users only carry what they use.
- **Depends on:** DEP-01, IMP-04.
- **ADR:** yes (distribution contract).

---

## 4 · Bugs

### BUG-03 — `foreach` stops after first failing iteration ✅
- **What / why:** `folker/model/test.py:55`: `executions_result and self._execute(...)` short-circuits, so iterations after a failure never run or report.
- **Impact:** High. Data-driven tests hide failures.
- **Cost:** XS. Evaluate first, then combine.
- **Benefit:** Complete results for data-driven tests.

### BUG-05 — Stage's own `foreach` lost when using a template ✅
- **What / why:** `folker/model/stage/stage.py:62` writes the merged dict to `result.params` instead of `result.foreach`.
- **Impact:** Med.
- **Cost:** XS. 1 line.
- **Benefit:** `foreach` works with templates.

### BUG-06 — Validation ignores `wrong_fields` ✅
- **What / why:** `folker/model/validation.py:16`: `len(self.missing_fields) == len(self.missing_fields) == 0` checks `missing_fields` twice, so an invalid Postgres `method` passes validation and fails at runtime.
- **Impact:** Med. May surface previously hidden errors in user suites, so call it out in the changelog.
- **Cost:** XS.
- **Benefit:** Errors at load time instead of mid-run.

### BUG-07 — Test files in paths with spaces fail to load ✅
- **What / why:** `folker/load/files.py:82`: `filename.resolve().as_uri()[7:]` yields `%20`-encoded paths.
- **Impact:** Med. Common on macOS/Windows.
- **Cost:** XS. Use `str(filename.resolve())`.
- **Benefit:** Works in any directory.

### BUG-08 — Shared mutable default `foreach={}` ✅
- **What / why:** `folker/model/test.py:24`: all `Test` instances share the same default dict.
- **Impact:** Low (latent).
- **Cost:** XS.
- **Benefit:** Removes a source of cross-test contamination.

### BUG-09 — Integer identity comparison in assertions
- **What / why:** `folker/model/stage/assertions.py:77`: `success is not executed` only works because CPython caches small ints. Use `!=`.
- **Impact:** Low.
- **Cost:** XS.
- **Benefit:** Correct for any count. Removes a `SyntaxWarning`.

### BUG-10 — Non-raw regex string
- **What / why:** `folker/model/context/context.py:12`: `'\${...}'` raises a `SyntaxWarning` on 3.12+ and will eventually be an error.
- **Impact:** Low.
- **Cost:** XS.
- **Benefit:** Clean on modern Python (prerequisite for DEP-04).

### BUG-11 — Multiple profiles: random one picked, rest ignored
- **What / why:** `config.profiles` is a `set`, and both executors use `list(config.profiles)[0]`. With `-p a -p b` the chosen profile is arbitrary and the others are ignored without a warning. Short-term fix: error out or warn when more than one is given, and fail on an unknown profile name (it currently falls back to DEFAULT silently). Merging is FEAT-05.
- **Impact:** Med.
- **Cost:** XS.
- **Benefit:** Deterministic configuration.

### BUG-12 — Proto generation failures reported as success
- **What / why:** `folker/load/protos.py`: `subprocess.run` without `check=True` means protoc errors are logged "OK". It also calls `python3` instead of `sys.executable`, so it can pick the wrong interpreter or venv.
- **Impact:** Med. Confusing downstream import errors.
- **Cost:** XS.
- **Benefit:** Failures reported where they happen.

### BUG-13 — Secrets leaked in REST debug logs
- **What / why:** `RestStageAction._log_debug` dumps headers, auth and body after variable resolution, so secrets referenced via `${...}` print in clear text with `--debug`. Apply the same obfuscation the test logger uses for secrets.
- **Impact:** Med. Credentials end up in CI logs.
- **Cost:** S. Probably a shared redaction helper used by all modules.
- **Benefit:** Safe to enable debug in CI.

### BUG-14 — Network calls without timeouts can hang forever
- **What / why:** `requests.*` (REST), postgres, rabbitmq, zookeeper and graphql calls have no timeouts (only Kafka has any). A dead endpoint hangs the CI job until the global timeout. Add sensible defaults, overridable per action.
- **Impact:** High.
- **Cost:** S.
- **Benefit:** Fails fast with a clear error.
- **Related:** FEAT-04.

### BUG-15 — Failing `if:` condition silently skips the stage
- **What / why:** `Stage.skip_stage_execution` catches every `eval` exception and returns "skip". A typo or type error in a condition looks like "condition false". It should fail the test with the condition and the error.
- **Impact:** Med. Behaviour change, so note it in the changelog.
- **Cost:** XS.
- **Benefit:** Condition mistakes become visible.

### BUG-16 — REST debug logging can turn a request into an error 🔍
- **What / why:** `_log_debug` calls `json.dumps(parameters)` inside the request `try`. Non-JSON-serialisable values (for example file handles in `data`) would raise before the request is sent and be reported as an action error. Verify, then serialise with `default=str`.
- **Impact:** Low.
- **Cost:** XS.
- **Benefit:** Debug mode never changes behaviour.

---

## 5 · Improvements

### IMP-01 — Strict loading: broken YAML fails the run
- **What / why:** `load_schema` logs and swallows any load or validation error, so a malformed test file silently disappears from the run (only `-n` catches it). Make load errors fail the run by default, with an opt-out (`--lenient`).
- **Impact:** High. Prevents false greens.
- **Cost:** S.
- **Benefit:** CI fails on broken test definitions.
- **Depends on:** TST-04.

### IMP-02 — Narrow broad exception handling
- **What / why:** There are 34 `except Exception` blocks (25 in modules). Many hide the real cause (REST stores errors in `context.error`; JSON parse errors are ignored). Catch specific exceptions and keep tracebacks in `--trace`.
- **Impact:** Med.
- **Cost:** M. Touches every module; do it module by module.
- **Benefit:** Debuggable failures.

### IMP-03 — Replace global registries with an explicit registry 📐
- **What / why:** `folker.profiles`, `templates`, `stage_templates` and `ActionSchema.type_schemas` are module-level mutable globals. They are the root cause of BUG-02 and make tests order-dependent. Introduce a `Registry` / `Session` object created in `cli.run` and passed down.
- **Impact:** Med.
- **Cost:** M.
- **Benefit:** Isolated tests. Embeddable as a library. Multiprocessing-safe.
- **Depends on:** TST-03, TST-04.
- **ADR:** yes (architecture of module wiring).

### IMP-04 — Lazy / plugin-based module loading 📐
- **What / why:** `folker/__init__.py` imports every module (grpc, kafka, psycopg2, Google, ...) at startup, even for a REST-only suite. Register modules via entry points (`folker.actions`) and import them only when an action type is first used.
- **Impact:** Med. Faster startup; enables DEP-10 and third-party modules.
- **Cost:** M.
- **Benefit:** Extensibility without forking.
- **Depends on:** IMP-03.
- **ADR:** yes.

### IMP-05 — Dataclass-based actions + one generic merge
- **What / why:** 15 hand-written `__init__` / `__add__` / validation implementations, plus stray class attributes (`body = str`, `params = dict()` in `RestStageAction`). This boilerplate is where BUG-04 and BUG-05 came from. Use dataclasses with field metadata (`mandatory`, merge strategy) and one generic merge (dicts deep-merge, lists union, scalars override).
- **Impact:** Med. Large maintainability gain.
- **Cost:** L. Do it incrementally, one module per PR.
- **Benefit:** Adding a module means declaring fields, not writing merge code.
- **Depends on:** TST-08.

### IMP-06 — Logger composition
- **What / why:** Seven logger classes cover plain/colour × console/file × sequential/parallel. Split into a formatter (plain, colour) and a sink (console, file, buffered for parallel runs).
- **Impact:** Low.
- **Cost:** M.
- **Benefit:** FEAT-01 (reporters) slots in as another sink.

### IMP-07 — Executor cleanup
- **What / why:** Context construction is duplicated across both executors. `Pool` isn't used as a context manager (no cleanup on exceptions). `cpu_count()` is hard-coded. Results only come back when everything finishes. Extract `build_context(config)`, use `with Pool(...)`, and stream results with `imap_unordered`.
- **Impact:** Med.
- **Cost:** S.
- **Benefit:** Cleaner shutdown, live progress, and a base for FEAT-08.
- **Depends on:** BUG-02.

### IMP-08 — Safer expression evaluation 📐
- **What / why:** Assertions, `save` and `if:` use bare `eval`, which allows arbitrary code and gives poor error messages. Evaluate a restricted evaluator (`simpleeval`, or an AST whitelist), with an escape hatch for existing suites.
- **Impact:** Med. Security boundary, and a potentially breaking change for users.
- **Cost:** M.
- **Benefit:** Safer for shared or untrusted test repos. Clearer errors.
- **ADR:** yes (security boundary and user contract).

### IMP-09 — Correct type hints + type checking
- **What / why:** Many annotations aren't valid types (`[str]`, `(str, str)`, `{str}`). `StageStep.execute` declares a signature none of its subclasses use. Fix them and add `mypy` or `pyright` to CI, non-blocking at first.
- **Impact:** Low.
- **Cost:** M (mechanical).
- **Benefit:** IDE support. Catches contract mismatches.

### IMP-10 — Proper variable-path parser
- **What / why:** `_resolve_variable_reference` splits on `.` and only supports indexes as separate segments (`a.[0]`). It catches everything, so the error message doesn't say which segment failed. Support `a.b[0].c` and report the failing segment.
- **Impact:** Med. User-facing ergonomics.
- **Cost:** S.
- **Benefit:** Intuitive syntax and actionable errors.
- **Note:** keep backward compatibility with `a.[0]`.

### IMP-11 — Proto generation scope and caching
- **What / why:** Every run scans `**/*.proto` from the current directory (only excluding `/lib/python3.`) and regenerates everything. Use configurable proto roots, exclude venv/node_modules, and skip files whose output is newer than the source.
- **Impact:** Low (performance on big repos).
- **Cost:** S.
- **Benefit:** Faster startup.
- **Depends on:** BUG-12.

### IMP-12 — Housekeeping
- **What / why:** Delete the empty `main.py`. Remove the stray class attributes in `RestStageAction`. Fix the `enrichment.body_json or enrichment.body_json` typo (`folker/module/rest/action.py:81`). Update `docs/Documentation.md` for the behaviour changes from BUG-06, BUG-15 and IMP-01.
- **Impact:** Low.
- **Cost:** XS.
- **Benefit:** Less confusion for contributors.

---

## 6 · Features

### FEAT-01 — JUnit XML / JSON report output
- **What / why:** Results only go to console or a log file. `--report junit:out.xml` (and `json:`) would let any CI (CircleCI, GitHub, Jenkins) show per-test results and timings.
- **Impact:** High for CI users.
- **Cost:** M.
- **Benefit:** First-class CI integration.
- **Depends on:** IMP-06 recommended.

### FEAT-02 — `--validate` dry-run mode
- **What / why:** Load, enrich and validate all profiles, templates and tests, then exit without executing anything. Useful as a fast pre-commit or PR check for test repos.
- **Impact:** Med.
- **Cost:** S.
- **Benefit:** Catches definition errors in seconds.
- **Depends on:** IMP-01.

### FEAT-03 — Environment-variable references
- **What / why:** Secrets currently come from `-s key value` (visible in shell history and `ps`) or profile files. Support `${env.NAME}` in context and secrets resolution.
- **Impact:** Med. Security and CI ergonomics.
- **Cost:** S.
- **Benefit:** Native CI secret injection.

### FEAT-04 — Stage-level `retry` / `timeout`
- **What / why:** Async systems (Kafka, RabbitMQ, Pub/Sub) need polling. Today users chain `WAIT` stages and hope. Add `retry: {attempts, delay}` (re-run action + asserts until pass) and `timeout`.
- **Impact:** High. Less flaky user tests.
- **Cost:** M.
- **Benefit:** Robust tests against eventually-consistent systems.
- **Depends on:** BUG-14.

### FEAT-05 — Ordered merging of multiple profiles
- **What / why:** Allow `-p base -p staging`, merged in order (later wins), for example shared defaults plus per-environment overrides.
- **Impact:** Med.
- **Cost:** S.
- **Benefit:** Fewer duplicated profile files.
- **Depends on:** BUG-11.

### FEAT-06 — `--list`
- **What / why:** Print the tests that would run with the current tag and file filters, without running them.
- **Impact:** Low.
- **Cost:** XS.
- **Benefit:** Easier debugging of tag filters.

### FEAT-07 — Filter by name pattern (`-k`)
- **What / why:** Run tests whose name matches a pattern, complementing tags and file filters.
- **Impact:** Low.
- **Cost:** S.
- **Benefit:** Faster local iteration.

### FEAT-08 — Configurable parallelism (`--workers N`)
- **What / why:** The worker count is fixed at `cpu_count()`, which can overload shared services in CI.
- **Impact:** Low.
- **Cost:** XS.
- **Benefit:** Control over load on systems under test.
- **Depends on:** IMP-07.

### FEAT-09 — Blueprints: reusable step sequences inlined into tests 📐
- **What / why:** A blueprint is a named, ordered list of stages, defined once and inserted anywhere in a test's `stages` list. At load time it expands into its stages, which then run exactly as if they had been written inline at that position: same test context, `save` results visible to later stages, assertions failing the test. Today the only reuse is stage templates, which enrich **one** stage by `id`. Common multi-step flows (log in → get token, reset mock server → register expectations, publish → wait → consume) get copy-pasted between tests.
- **Proposed YAML** (to be fixed in the ADR):
  ```yaml
  # blueprint_login.yaml  (loaded like templates/profiles, pattern blueprint*.yaml)
  id: login
  description: Authenticate and store the token
  stages:
    - name: request token
      action: { type: REST, method: POST, host: "${auth_host}", uri: token, json: { user: "${user}" } }
      save: { token: "${response_json.access_token}" }
      assert: ["${status_code} == 200"]
    - name: check token
      assert: ["len(${token}) > 0"]

  # test_orders.yaml
  stages:
    - name: setup
      save: { auth_host: http://auth:8080, user: alice }
    - blueprint: login        # expands to the 2 stages above, in place
    - name: create order
      action: { type: REST, method: POST, host: "${api}", headers: { Authorization: "Bearer ${token}" } }
  ```
- **Design points to settle (ADR):**
  - **Parameters:** inputs only via the existing test context (simplest), or an explicit `with: {user: bob}` on the include, scoped to the expanded stages.
  - **Composition:** whether a blueprint include may carry `if:` / `foreach:` that apply to the whole block (fits the current Stage model; otherwise disallow at first).
  - **Nesting:** blueprints including blueprints, with cycle detection and a depth limit.
  - **Interplay with stage templates:** a blueprint stage with an `id` should still be enriched by stage templates. Define the order (expand blueprints first, then apply templates).
  - **Errors:** an unknown blueprint id must fail loading with a clear message. Today `SchemaReferenceNotFoundException` exists but is never raised, and unknown stage-template ids are silently ignored; don't repeat that. Duplicate blueprint ids across files must also fail.
  - **Logging:** prefix expanded stage names (`login › request token`) so failures point to the blueprint.
- **Implementation sketch:** a `BlueprintSchema` plus a `blueprint*.yaml` pattern in `folker/parameters.py` and `folker/load/files.py`, a registry next to `templates`/`stage_templates` (or in the IMP-03 registry), and expansion in `_enrich_stages` before stage-template enrichment. Execution code is unchanged: expansion happens at load time, so sequential and parallel executors (pickled tests) need nothing new.
- **Impact:** High. A big reduction in duplicated YAML for users with many similar tests; changes to a shared flow happen in one place.
- **Cost:** M. ~200–300 lines (schema, loader, expansion, error handling) plus unit tests (expansion order, nesting/cycles, unknown id, template interplay), an integration example in `example/test/blueprint/` with a CI job, and `docs/Documentation.md`.
- **Benefit:** Test suites become composable. It also lays the groundwork for shared blueprint libraries across repos.
- **Depends on:** TST-04 (loader tests), IMP-01 (strict loading, so a broken blueprint fails the run). IMP-03 recommended so blueprints don't add another global registry. TST-08 helps for the template interplay.
- **ADR:** yes. It adds a new user-facing YAML construct, which is hard to change once suites depend on it.

---

## Suggested order (waves)

1. **Safety net (≈1–2 days):** TST-03, BUG-03, BUG-05, BUG-07, BUG-08, BUG-09, BUG-10
2. **Remaining bugs (≈2 days):** BUG-06, BUG-11, BUG-12, BUG-13, BUG-14, BUG-15, BUG-16, IMP-01, IMP-12
3. **Pipeline hardening (≈2–3 days):** CI-07, CI-08, TST-04, TST-05
4. **Dependency overhaul (≈1 week, ADRs first):** DEP-02, DEP-03, DEP-01, DEP-05, DEP-06, DEP-04, DEP-07, DEP-08, CI-11
5. **Structural (incremental):** IMP-07, IMP-10, IMP-03, IMP-04, DEP-10, TST-08, IMP-05, IMP-02, IMP-06, IMP-09, IMP-11
6. **Release and features:** CI-09, CI-10, FEAT-01, FEAT-02, FEAT-03, FEAT-04, FEAT-05, FEAT-06, FEAT-07, FEAT-08, FEAT-09, IMP-08
