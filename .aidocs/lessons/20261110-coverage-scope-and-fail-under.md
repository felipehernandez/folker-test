# Scope coverage to the package, and gate in one place only

- **Date**: 2026-11-10
- **Status**: Active

## Rule

Configure coverage in `pyproject.toml` with `source_pkgs = ["folker"]` so every report measures only the product code. Enforce `fail_under` in exactly one command (`coverage report`). Run `coverage xml` and `coverage html` with `--fail-under=0` so they still write their files when the gate fails.

## Context

Applies whenever:
- a coverage number is quoted, compared or turned into a threshold,
- a CI step runs `coverage xml`, `coverage html` or `coverage json`,
- a Python version or the `coverage` version changes (re-measure first, then adjust the threshold by hand).

## Why

- Plain `coverage run` followed by `coverage report` counts every file that was imported, including `tests/` and pytest temp files such as `/tmp/pytest-of-root/.../folker_cwd_import_probe.py`. CI showed **94%** while `folker/` alone was **87%** (line) / **86.42%** (line + branch). A threshold set on the 94% would have been meaningless.
- `--omit` patterns written per command drift apart (the xml/html steps omitted `tests/`, the report step did not).
- `coverage xml` and `coverage html` also exit with status 2 when the total is below `fail_under`, not only `coverage report`. With `fail_under` set in the config and no `--fail-under=0`, a coverage drop fails the report step first and the artifacts are never produced, hiding the numbers needed to fix it.
- On Python 3.10, `coverage` reads `[tool.coverage.*]` from `pyproject.toml` only if `tomli` is installed. Depend on `coverage[toml]` explicitly instead of relying on pytest pulling it in.
- `source_pkgs` (not `source`) keeps report paths repo-relative (`folker/cli.py`), which matters for tools that map files to the repository.

## Examples

### Wrong

```yaml
- run: |
    coverage run -m pytest
    coverage report -m                              # counts tests/ and /tmp files: 94%
    coverage xml --omit='*/venv/*','tests/*' -o c.xml   # different scope from the line above
```

### Right

```toml
# pyproject.toml
[tool.coverage.run]
source_pkgs = ["folker"]
branch = true

[tool.coverage.report]
fail_under = 86.4   # ratchet: raised by hand, never lowered to pass a PR
precision = 2
```

```yaml
- run: coverage run -m pytest --junitxml codecoverage/unittests.xml
- run: |
    coverage xml --fail-under=0 -o codecoverage/coverage.xml
    coverage html --fail-under=0 -d codecoverage
- run: coverage report                 # the only gate
- store_artifacts:
    when: always                       # reports upload even if the gate fails
    path: codecoverage
```

## Related Lessons

[Test on the runtime Python version](20261105-test-on-runtime-python-version.md): measure the baseline on the same interpreter the image runs. Tracked as CI-03 in [the completed tasks](../plans/completed-tasks.md).
