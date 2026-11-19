# folker-test — Improvement Execution Plan

Created: 2026-11-05 · Last updated: 2026-11-10 · Baseline: branch `beta` @ `2c625c6`

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
| CI-08 | Update EOL executors and actions | Med | XS | ☐ |
| CI-09 | Image vulnerability scan, SBOM, multi-arch build | Med | S | ☐ |
| CI-10 | Versioning and release process | Med | M | ☐ |
| CI-11 | Renovate guardrails and grouping | Med | XS | ☐ |
| CI-13 | Branch rules as code, in sync with the pipeline | Med | S | ☐ |
| **2 · Testability** |||||
| TST-02 | Regression-test policy for bug fixes | High | — | ☐ |
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
| DEP-11 | Vuln: certifi: compromised emSign root CAs | High | XS | ☐ |
| DEP-12 | Vuln: httplib2: decompression bomb DoS | High | S | ☐ |
| DEP-13 | Vuln: kafka-python: unbounded SCRAM iteration count DoS | High | XS | ☐ |
| DEP-14 | Vuln: kafka-python: unvalidated protocol frame length DoS | High | XS | ☐ |
| DEP-15 | Vuln: pyOpenSSL: DTLS cookie callback buffer overflow | High | XS | ☐ |
| DEP-16 | Vuln: idna: `idna.encode()` bypasses the CVE-2024-3651 fix | Med | XS | ☐ |
| DEP-17 | Vuln: marshmallow: DoS in `Schema.load(many=...)` | Med | XS | ☐ |
| DEP-18 | Vuln: pylint: code execution through the pickled stats cache | Med | S | ☐ |
| DEP-19 | Vuln: pytest: insecure `tmpdir` handling | Med | S | ☐ |
| DEP-20 | Vuln: requests: insecure temp file reuse in `extract_zipped_paths()` | Med | XS | ☐ |
| DEP-21 | Vuln: certifi: GLOBALTRUST root certificate removed | Low | XS | ☐ |
| DEP-22 | Vuln: pyOpenSSL: TLS connection bypass through an unhandled SNI callback exception | Low | XS | ☐ |
| **4 · Bugs** |||||
| BUG-19 | A stage cannot switch a template flag off (`ack`, `ephemeral`) | Med | XS | ☐ |
| BUG-20 | `ZookeeperStageAction`: a stage without `version` overrides the template version | Med | XS | ☐ |
| BUG-21 | `method` of a template is silently kept when the stage names another | Low | S | ☐ |
| BUG-22 | A stage that references a template id that does not exist is a silent no-op 🔍 | Med | XS | ☐ |
| BUG-23 | ZooKeeper client is not stopped when an operation fails | Low | XS | ☐ |
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
| FEAT-06 | `--list` tests matching the filters | Low | XS | ☐ |
| FEAT-07 | Filter tests by name pattern (`-k`) | Low | S | ☐ |
| FEAT-08 | Configurable parallelism (`--workers N`) | Low | XS | ☐ |
| FEAT-09 | Blueprints: reusable step sequences inlined into tests 📐 | High | M | ☐ |

---

## 1 · CI/CD

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

### CI-13 — Branch rules as code, in sync with the pipeline
- **What / why:** The required status checks on `beta` and `main` live only in GitHub settings, and nothing ties them to the CircleCI job names. Deleting `validate-integration-tests` in CI-05 left the PR waiting forever on a check that no longer existed. Today: `beta` has a ruleset (24 required checks, strict, no bypass), `main` still has the old classic protection requiring `validate-integration-tests`, so the first `beta` → `main` PR will get stuck the same way. `ci/circleci: unit-tests-3.10` is not required on either, so a PR can merge with failing unit tests.
- **Impact:** Med. Merges can't be blocked by a ghost check, and a failing unit-test or lint job can't be merged by mistake.
- **Cost:** S. `.github/rulesets/beta.json` and `main.json` (exported from the live ruleset, normalised), `scripts/check_rulesets.py` run in the `lint` job, and optionally `scripts/apply_rulesets.sh`.
- **Benefit:** Reviewable branch rules. The check script fails when a required check doesn't match a job in `.circleci/config.yml` (matrix expanded), or when a job such as lint or unit tests isn't required, so a rename or removal is caught in the PR that makes it.
- **Depends on:** CI-05 (done). Needs a repo admin to apply the rulesets; the API refuses non-admins. Remove the classic protection on `main` once its ruleset exists.
- **Note:** the unit-test check name carries the Python version (`unit-tests-3.10`), so DEP-04 must update the required check in the same change.

---

## 2 · Testability

### TST-02 — Regression-test policy for bug fixes
- **What / why:** Every BUG-xx gets a test that fails before the fix and passes after. The probe scripts from the analysis are the starting point.
- **Impact:** High. Bugs stay fixed.
- **Cost:** Built into each BUG task.
- **Benefit:** The suite grows where bugs actually happen.

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
- **Security:** DEP-18 (pylint advisory) builds on this.
- **Depends on:** can be done now, or as part of DEP-01.

### DEP-03 — Remove unused / stale transitive pins
- **What / why:** `google==3.0.0` (an unrelated Google-search scraper), `certifi==2023.11.17` (stale CA bundle), `chardet`, `idna` and `pyOpenSSL` are never imported directly. Pinning them freezes transitive dependencies at old, vulnerable versions.
- **Impact:** Med. Security (CA bundle, OpenSSL).
- **Cost:** XS. Verify with `grep` and a test run, then delete.
- **Benefit:** Less to maintain. Fewer resolver conflicts.
- **Security:** also resolves the `certifi`, `idna` and `pyOpenSSL` advisories (DEP-11, DEP-15, DEP-16, DEP-21, DEP-22). Whichever lands first, confirm the Dependabot alerts close.

### DEP-04 — Python 3.10 → 3.12/3.13
- **What / why:** Python 3.10 reached end of life in October 2026. Update the Dockerfiles, devcontainer and CI.
- **Impact:** High. Security patches, plus 10–25% faster execution.
- **Cost:** S.
- **Benefit:** Supported runtime.
- **Depends on:** BUG-01, CI-01, DEP-06.
- **Note:** the `unit-tests-<python>` check name changes with the version. Update the required checks in the same change (CI-13), or merges block on a check that never reports.

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

### DEP-11 — Vuln: certifi: compromised emSign root CAs
- **What / why:** Dependabot (critical, [GHSA-6q48-6c7w-9gw2](https://github.com/advisories/GHSA-6q48-6c7w-9gw2)), alerts #30, #31 on `beta` (one per manifest: `requirements.txt` and `setup.py`). Pin: `certifi==2023.11.17` → `>= 2026.10.18`. The bundle trusts emSign root CAs whose intermediate CA keys are compromised, so a certificate issued with them would be accepted by every `requests`, `google-*` and `gql` call. Folker never imports `certifi`; it arrives through `requests` and the Google clients, and the pin freezes it.
- **Impact:** High.
- **Cost:** XS. Delete the pin (preferred, see DEP-03) or raise it to `2026.10.18` or later in `requirements.txt` and `setup.py`. Run the suite and one REST/GraphQL example against HTTPS.
- **Benefit:** The alerts close.
- **Supersedes:** DEP-21 is closed by the same bump.
- **Related:** DEP-03.

### DEP-12 — Vuln: httplib2: decompression bomb DoS
- **What / why:** Dependabot (high, [GHSA-j5g9-f88f-gfj3](https://github.com/advisories/GHSA-j5g9-f88f-gfj3), CVE-2026-59939), alerts #22, #23 on `beta` (one per manifest: `requirements.txt` and `setup.py`). Pin: `httplib2==0.22.0` → `>= 0.32.0`. A gzip/deflate response is decompressed without a size limit, so a hostile server can exhaust memory. Only the Gmail module uses `httplib2` directly (`folker/module/gmail/action.py`), together with `oauth2client` and `google-api-python-client`.
- **Impact:** High.
- **Cost:** S. Bump the pin in both files. `pyproject.toml` ignores a `DeprecationWarning` from `httplib2` (pyparsing); re-check it and drop the ignore if the new release no longer triggers it. Check `google-api-python-client==2.179.0` and `oauth2client==4.1.3` still resolve.
- **Benefit:** The alerts close.
- **Related:** DEP-07 (drops the `httplib2` coupling and would remove the need for the pin).

### DEP-13 — Vuln: kafka-python: unbounded SCRAM iteration count DoS
- **What / why:** Dependabot (high, [GHSA-2jcm-hq8r-84wx](https://github.com/advisories/GHSA-2jcm-hq8r-84wx), CVE-2026-10143), alerts #24, #25 on `beta` (one per manifest: `requirements.txt` and `setup.py`). Pin: `kafka-python==2.2.15` → `>= 2.3.2`. A broker (or a man in the middle) can send an enormous SCRAM iteration count and make the client spend its CPU on it. The Kafka module connects to whatever `host` a test names, so a hostile or compromised broker is the exposure.
- **Impact:** High.
- **Cost:** XS. Bump the pin in both files together with DEP-14 (same fix version). Run the Kafka unit tests and the Kafka integration job.
- **Benefit:** The alerts close.
- **Related:** DEP-14.

### DEP-14 — Vuln: kafka-python: unvalidated protocol frame length DoS
- **What / why:** Dependabot (high, [GHSA-m3px-q5gj-j9x7](https://github.com/advisories/GHSA-m3px-q5gj-j9x7), CVE-2026-10142), alerts #26, #27 on `beta` (one per manifest: `requirements.txt` and `setup.py`). Pin: `kafka-python==2.2.15` → `>= 2.3.2`. The client trusts the length announced in a protocol frame, so a hostile broker can make it allocate or wait for an arbitrary amount of data.
- **Impact:** High.
- **Cost:** XS. Same bump as DEP-13; do both in one PR and confirm both alerts close.
- **Benefit:** The alerts close.
- **Related:** DEP-13.

### DEP-15 — Vuln: pyOpenSSL: DTLS cookie callback buffer overflow
- **What / why:** Dependabot (high, [GHSA-5pwr-322w-8jr4](https://github.com/advisories/GHSA-5pwr-322w-8jr4), CVE-2026-27459), alerts #15, #16 on `beta` (one per manifest: `requirements.txt` and `setup.py`). Pin: `pyOpenSSL==23.3.0` → `>= 26.0.0`. Only affects code that sets a DTLS cookie callback. Folker does not import `OpenSSL` and does not use DTLS, so it is not reachable today, but the pin keeps the alert open and holds `cryptography` back.
- **Impact:** High.
- **Cost:** XS. Delete the pin (preferred, see DEP-03) or raise it to `26.0.0` or later. Check which package, if any, still needs it with `pipdeptree -r -p pyOpenSSL`.
- **Benefit:** The alerts close.
- **Related:** DEP-03, DEP-22 (same fix version).

### DEP-16 — Vuln: idna: `idna.encode()` bypasses the CVE-2024-3651 fix
- **What / why:** Dependabot (moderate, [GHSA-65pc-fj4g-8rjx](https://github.com/advisories/GHSA-65pc-fj4g-8rjx), CVE-2026-45409), alerts #20, #21 on `beta` (one per manifest: `requirements.txt` and `setup.py`). Pin: `idna==3.10` → `>= 3.15`. Specially crafted input makes `idna.encode()` slow again. `requests` encodes the host of every request, and REST and GraphQL hosts come from test definitions, so the exposure is a hostile test file or a variable fed from a response.
- **Impact:** Med.
- **Cost:** XS. Delete the pin (preferred, see DEP-03) or raise it to `3.15` or later.
- **Benefit:** The alerts close.
- **Related:** DEP-03.

### DEP-17 — Vuln: marshmallow: DoS in `Schema.load(many=...)`
- **What / why:** Dependabot (moderate, [GHSA-428g-f7cq-pgp5](https://github.com/advisories/GHSA-428g-f7cq-pgp5), CVE-2025-68480), alerts #11, #12 on `beta` (one per manifest: `requirements.txt` and `setup.py`). Pin: `marshmallow==3.22.0` → `>= 3.26.2` (stay on 3.x). Loading a very large collection with `many=True` can exhaust memory or CPU. Folker loads test files with marshmallow (`folker/load/schemas.py` and every module schema), so a hostile YAML file is the exposure.
- **Impact:** Med.
- **Cost:** XS. Bump within 3.x in both files. DEP-09 already removed the 4.x deprecations, so the suite should stay green; confirm `marshmallow-oneofschema==3.1.1` still resolves.
- **Benefit:** The alerts close.
- **Related:** DEP-09 (done).

### DEP-18 — Vuln: pylint: code execution through the pickled stats cache
- **What / why:** Dependabot (moderate, [GHSA-22qq-2fwx-7p67](https://github.com/advisories/GHSA-22qq-2fwx-7p67), CVE-2026-114608), alerts #32, #33 on `beta` (one per manifest: `requirements.txt` and `setup.py`). Pin: `pylint==3.2.7` → `>= 4.0.9`. Pylint unpickles its stats cache from `PYLINT_HOME`, so a poisoned cache runs code on a developer or CI machine. Pylint is a development tool, yet `setup.py` lists it in `install_requires`, so it also ships to users and into the image. It is a major bump (3.x → 4.x), so new checks may fire.
- **Impact:** Med.
- **Cost:** S. First move it out of the runtime dependencies (DEP-02), then pin `>= 4.0.9` in the lint requirements (`requirements-lint.txt`) and fix or disable the new messages.
- **Benefit:** The alerts close.
- **Depends on:** DEP-02 recommended first.
- **Related:** DEP-01.

### DEP-19 — Vuln: pytest: insecure `tmpdir` handling
- **What / why:** Dependabot (moderate, [GHSA-6w46-j5rx-g56g](https://github.com/advisories/GHSA-6w46-j5rx-g56g), CVE-2025-71176), alert #19 on `beta` (`requirements.txt` only; `setup.py` does not list pytest). Pin: `pytest==7.4.4` → `>= 9.0.3`. Predictable temporary directories allow another local user to interfere with a test run. Only `requirements.txt` has it (it is missing from `setup.py`). It is two major versions ahead, so check `pytest-mock`, `pytest-cov` and `pytest-html` support it and that the `DeprecationWarning`-as-error filter in `pyproject.toml` does not trip on new pytest warnings.
- **Impact:** Med.
- **Cost:** S. Raise the pin, run the suite on the runtime Python (see the lesson on testing on the runtime version) and fix what breaks. Move it to a dev-only group when DEP-01/DEP-02 land.
- **Benefit:** The alerts close.
- **Related:** DEP-02, DEP-01.

### DEP-20 — Vuln: requests: insecure temp file reuse in `extract_zipped_paths()`
- **What / why:** Dependabot (moderate, [GHSA-gc5v-m9x4-r6x2](https://github.com/advisories/GHSA-gc5v-m9x4-r6x2), CVE-2026-25645), alerts #17, #18 on `beta` (one per manifest: `requirements.txt` and `setup.py`). Pin: `requests==2.32.4` → `>= 2.33.0`. A helper that extracts files from a zipped path reuses a predictable temp file. Folker does not call it, but `requests` is used by the REST module and (through `gql`) the GraphQL module, and the pin keeps the alert open.
- **Impact:** Med.
- **Cost:** XS. Bump in both files and re-run `tests/module/rest`, `tests/module/test_timeouts.py` and one REST example: the timeout work (BUG-14) relies on the `timeout=` argument.
- **Benefit:** The alerts close.
- **Related:** BUG-14 (done).

### DEP-21 — Vuln: certifi: GLOBALTRUST root certificate removed
- **What / why:** Dependabot (low, [GHSA-248v-346w-9cwc](https://github.com/advisories/GHSA-248v-346w-9cwc), CVE-2024-39689), alerts #9, #10 on `beta` (one per manifest: `requirements.txt` and `setup.py`). Pin: `certifi==2023.11.17` → `>= 2024.7.4`. The old bundle still trusts the GLOBALTRUST root, which Mozilla removed. Any bump that fixes DEP-11 (`>= 2026.10.18`) also fixes this, so there is nothing to do beyond confirming the alerts close.
- **Impact:** Low.
- **Cost:** XS. Do it together with DEP-11; close this task when alerts #9 and #10 disappear.
- **Benefit:** The alerts close.
- **Depends on:** DEP-11.

### DEP-22 — Vuln: pyOpenSSL: TLS connection bypass through an unhandled SNI callback exception
- **What / why:** Dependabot (low, [GHSA-vp96-hxj8-p424](https://github.com/advisories/GHSA-vp96-hxj8-p424), CVE-2026-27448), alerts #13, #14 on `beta` (one per manifest: `requirements.txt` and `setup.py`). Pin: `pyOpenSSL==23.3.0` → `>= 26.0.0`. Only affects servers that set `set_tlsext_servername_callback`. Folker is a client and does not import `OpenSSL`, so it is not reachable today.
- **Impact:** Low.
- **Cost:** XS. Same change as DEP-15; confirm alerts #13 and #14 close.
- **Benefit:** The alerts close.
- **Depends on:** DEP-15.

---

## 4 · Bugs

### BUG-19 — A stage cannot switch a template flag off (`ack`, `ephemeral`)
- **What / why:** `__add__` uses `if enrichment.ack:` / `if enrichment.ephemeral:`, so `ack: false` in a stage cannot override `ack: true` from the template. Affects `RabbitMQStageAction.ack`, `PubSubStageAction.ack` and `ZookeeperStageAction.ephemeral`. Compare with `is not None`, as the `timeout` fields already do (BUG-14); `ephemeral` defaults to `False`, so it needs a `None` default too.
- **Impact:** Med.
- **Cost:** XS.
- **Benefit:** A stage can disable what its template enables.
- **Found by:** TST-08. Regression tests: the three `TestFlags::test_the_stage_can_switch_it_off` cases in `tests/model/stage/test_action_merge_matrix.py` (strict `xfail` today; remove them from `KNOWN_DEFECTS` with the fix). IMP-05 would fix this generically.

### BUG-20 — `ZookeeperStageAction`: a stage without `version` overrides the template version
- **What / why:** `version` defaults to `-1`, which is truthy, so in `template + stage` an unset stage `version` replaces the template's (`version: 3` becomes `-1`, i.e. "any version"). Default it to `None` and apply `-1` when executing, and merge with `is not None`.
- **Impact:** Med.
- **Cost:** XS.
- **Benefit:** A template's optimistic-locking version is honoured.
- **Found by:** TST-08. Regression test: `TestScalarFields::test_only_the_template_defines_it[zookeeper.version]` (strict `xfail` today).

### BUG-21 — `method` of a template is silently kept when the stage names another
- **What / why:** `code` and `grpc` take the stage's `method` when merging; REST, Kafka, Postgres, RabbitMQ, ZooKeeper, Pub/Sub, File and Protobuf keep the template's, so a stage overriding it runs the template's operation with no warning. For the actions whose class depends on `method` (Postgres, RabbitMQ, ZooKeeper, Pub/Sub, Kafka) the merged object is also the template's subclass, so honouring the override needs a decision: merge `method` and re-pick the class, or reject the override with a clear error at load time.
- **Impact:** Low.
- **Cost:** S.
- **Benefit:** One documented rule for every action.
- **Found by:** TST-08. `TestMethod` in `tests/model/stage/test_action_merge_matrix.py` pins today's behaviour; update it with the decision. IMP-05 should settle it for all modules at once. 🔍 Decide the intended behaviour first.

### BUG-22 — A stage that references a template id that does not exist is a silent no-op 🔍
- **What / why:** `_enrich_stages` (`folker/load/files.py`) only enriches a stage whose id is in `stage_templates`. A stage with just an `id` and no `action` gets a `VOID` action by default, so a typo (`id: get_usr`) or a template file that failed to load (see IMP-01) produces a stage that does nothing, and a test that passes without checking anything. A stage that has an id and its own definition is fine; the problem is the id-only stage with no template.
- **Impact:** Med. False greens.
- **Cost:** XS. Report it as a load error when a stage has an id, no `action` of its own and no matching template (verify first that no existing example relies on it).
- **Benefit:** Typos in template references fail at load time.
- **Found by:** TST-04. `TestStageEnrichment::test_a_reference_to_a_template_that_does_not_exist_is_reported` is a strict `xfail` today; remove the mark with the fix.

### BUG-23 — ZooKeeper client is not stopped when an operation fails
- **What / why:** `exists`, `get`, `set` and `delete` in `folker/module/zookeeper/action.py` call `zookeeper.stop()` after the operation, not in a `finally`. When the operation raises (for example `NoNodeError` for `get` on a missing node, which is not caught), the exception fails the test and the client keeps its connection thread and session open until the process ends. In a long suite or in parallel workers this accumulates connections, and ephemeral nodes of that session stay alive. `create` is not affected (it catches its errors).
- **Impact:** Low.
- **Cost:** XS. `try` / `finally` around the operation in each action, ideally in one helper, since BUG-14 already put the connection in `_connect`.
- **Benefit:** No leaked sessions after a failed stage.
- **Found by:** TST-06. `TestZookeeperFailures::test_the_client_is_stopped_when_the_operation_raises` is a strict `xfail` today (four cases); remove the mark with the fix. Whether those operations should also catch the error and save it as `error`, as `create` does, is part of IMP-02.

---

## 5 · Improvements

### IMP-01 — Strict loading: broken YAML fails the run
- **What / why:** `load_schema` logs and swallows any load or validation error, so a malformed test file silently disappears from the run (only `-n` catches it). Make load errors fail the run by default, with an opt-out (`--lenient`).
- **Impact:** High. Prevents false greens.
- **Cost:** S.
- **Benefit:** CI fails on broken test definitions.
- **Depends on:** TST-04 (done). `TestBrokenFiles` in `tests/load/test_files_loading.py` pins today's behaviour (log and skip, the run goes on) for tests, templates and profiles, and a validation error after enrichment already raises out of the loader instead: update them with this change, and decide whether the two paths should behave the same.

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
- **Depends on:** TST-08 (done: `tests/model/stage/test_action_merge_matrix.py`; its `KNOWN_DEFECTS` table and the `TestMethod` cases show what the generic merge must decide: BUG-19, BUG-20, BUG-21).

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
- **What / why:** Delete the empty `main.py`. Remove the stray class attributes in `RestStageAction`. Fix the `enrichment.body_json or enrichment.body_json` typo (`folker/module/rest/action.py:81`). Update `docs/Documentation.md` for the behaviour changes from BUG-06, BUG-15 and IMP-01 (BUG-11 is already documented).
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

1. **Safety net:** done (TST-03, BUG-10)
1b. **Security advisories (≈½ day, do first):** DEP-11, DEP-21, DEP-13, DEP-14, DEP-12, DEP-15, DEP-22, DEP-16, DEP-17, DEP-20, DEP-19, DEP-18 (DEP-03 and DEP-02 close several of them for free)
2. **Remaining bugs (≈2 days):** BUG-19, BUG-20, BUG-21, BUG-22, BUG-23, IMP-01, IMP-12
3. **Pipeline hardening (≈2–3 days):** CI-08, CI-13
4. **Dependency overhaul (≈1 week, ADRs first):** DEP-02, DEP-03, DEP-01, DEP-05, DEP-06, DEP-04, DEP-07, DEP-08, CI-11
5. **Structural (incremental):** IMP-07, IMP-10, IMP-03, IMP-04, DEP-10, IMP-05, IMP-02, IMP-06, IMP-09, IMP-11
6. **Release and features:** CI-09, CI-10, FEAT-01, FEAT-02, FEAT-03, FEAT-04, FEAT-06, FEAT-07, FEAT-08, FEAT-09, IMP-08
