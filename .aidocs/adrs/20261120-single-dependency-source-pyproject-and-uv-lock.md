# Declare dependencies once in `pyproject.toml` and lock them with `uv`

- **Date**: 2026-11-20
- **Status**: Accepted

## Context

Dependencies were declared in three files that drifted apart:

- `setup.py` (`install_requires`) was what the Docker image installed.
- `requirements.txt` was what CI and the dev container installed, and the only place that listed the test tools.
- `requirements-lint.txt` held `ruff`.

Drift had real cost. Until DEP-06 `grpcio-tools` and `google-cloud-pubsub` had different versions in the first two files. On 2026-11-19 the image shipped `google-cloud-pubsub` 2.39.0 while the unit tests ran against 2.18.0, and a breaking API change only showed up in the integration job (lesson `20261119-test-against-the-installed-dependency-set`).

Only the direct dependencies were pinned. Everything else (`urllib3`, `google-api-core`, `grpcio-status`, ...) was resolved again by `pip` on every build, so two builds of the same commit could ship different libraries, and a test run on CI could differ from the image.

Forces:

- The image, the unit tests and the dev container must install the same set.
- Renovate already updates `requirements*.txt` and `setup.py`; whatever replaces them must be understood by Renovate.
- The Python version is declared once (`.python-version`, CI-12) and checked by `scripts/check_python_version.py`.
- The test/lint tools must not reach the published image. (`coverage` and `pylint` still do; DEP-02 removes them.)
- Hard to reverse once suites and pipelines depend on the lock file, and it touches the packaging, Dockerfile, CI and developer workflow, which is why it is recorded here.

## Decision

We will declare dependencies only in `pyproject.toml` (PEP 621 / PEP 735) and lock them with `uv`:

- `[project].dependencies` holds the runtime dependencies, pinned exactly as before. `[dependency-groups]` holds `test` (pytest, pytest-cov, pytest-html, pytest-mock, coverage), `lint` (ruff) and `dev` (both). `uv.lock` is committed and pins the whole tree, transitive dependencies included, with hashes.
- `setup.py`, `requirements.txt`, `requirements-lint.txt`, `ruff.toml` and the unused `Dockerfile-integration` are removed. Ruff's configuration moves into `[tool.ruff]`. The build backend stays setuptools (`[tool.setuptools.packages.find] include = ["folker*"]`).
- The `uv` version is pinned in `requirements-uv.txt`, the one file CI, the Dockerfile and the dev container install it from (Renovate bumps it like any other requirements file). `[tool.uv] required-version` rejects older versions.
- Everything installs with `uv sync --frozen`, which never re-resolves: the unit-test and lint jobs, the Docker builder stage (into `/opt/venv`, copied to the runtime stage with `--no-dev`), `make install` and the dev container. `uv lock --check` runs in the `lint` job, so a `pyproject.toml` change without the matching `uv.lock` fails the build.
- Changing a dependency means editing `pyproject.toml` and running `make lock` (or accepting the Renovate PR, which updates both files).
- `scripts/check_python_version.py` also checks `requires-python` and ruff's `target-version` in `pyproject.toml` against `.python-version`.

## Consequences

### Positive

- One source of truth: the image, the unit tests and local development install the same locked set, so the DEP-06 / pubsub class of failure cannot come back through version drift.
- Reproducible builds: the same commit builds the same image, transitive dependencies included.
- Faster installs (uv) and a cached dependency layer in Docker that rebuilds only when `pyproject.toml` or `uv.lock` change.
- Dev tools stay out of the image (the venv is synced with `--no-dev`); this prepares DEP-02 and DEP-10 (extras per module).
- Renovate bumps the direct pins and refreshes `uv.lock` in the same PR.

### Negative

- Contributors need `uv` (one `pip install -r requirements-uv.txt`).
- `uv.lock` is a large generated file (about 330 KB) that shows up in diffs and can conflict between branches; the resolution is to re-run `uv lock`.
- Transitive versions only move when someone refreshes the lock (Renovate lock-file maintenance or `uv lock --upgrade`), so security fixes for transitive packages need that step.
- The venv in the image lives in `/opt/venv` instead of `/usr/local`; anything that assumed the old path breaks (nothing in the repo did).

### Neutral

- Open Renovate PRs against `requirements*.txt` / `setup.py` have to be closed; Renovate recreates them against `pyproject.toml`.
- The CI check name and the Python version matrix are unchanged.

## Alternatives Considered

### `pip-tools` (`pip-compile`) with `requirements.in` / `requirements.txt`

- **Description**: Keep pip, generate a fully pinned `requirements.txt` with hashes from `requirements.in` files (runtime, test, lint).
- **Reason for rejection**: It needs one `.in`/`.txt` pair per group and a second source of metadata (`setup.py` or `pyproject.toml`) for the package itself, so the duplication that caused the drift stays. `uv` produces a single universal lock from `pyproject.toml` and also builds the environment.

### Keep `setup.py` + `requirements.txt` and add a CI check that they agree

- **Description**: Leave the files and fail the build when the runtime pins differ.
- **Reason for rejection**: It detects drift instead of removing it, still leaves transitive dependencies unpinned, and adds a bespoke script to maintain.

### Poetry or PDM

- **Description**: Another project manager with its own lock file.
- **Reason for rejection**: Comparable result, but a slower resolver, its own non-standard metadata (Poetry), and no advantage for a project that only needs a lock and an installer. `uv` follows the standards (PEP 621, PEP 735) so the metadata stays portable.
