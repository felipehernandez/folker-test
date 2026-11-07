# Test on the same Python version the product runs on, and treat deprecations as errors

- **Date**: 2026-11-05
- **Status**: Active

## Rule

Always run the unit test suite on the exact Python version used by the shipped runtime (the Docker base image), plus the next version we plan to move to. Configure pytest to turn `DeprecationWarning` into errors so removals show up before the upgrade, not after.

## Context

Applies whenever:
- the local or CI interpreter differs from the runtime image (`FROM python:X.Y-...` in `Dockerfile`, `Dockerfile-integration`, `.devcontainer`),
- the Python version or a base image is bumped (see DEP-04 in the improvement plan),
- a bug is reproduced or verified locally: check which interpreter ran the check before claiming it passes or fails "in production".

## Why

A green test run only proves the code works on the interpreter that ran it. In this project the suite passed (409 tests) on local Python 3.9, while the shipped image runs Python 3.10, where `collections.Mapping` no longer exists. `folker/model/context/context.py:202` therefore crashes in production on any nested `save`. The only signal was a `DeprecationWarning` buried among about 150 other warnings. Version drift between test and runtime environments turns stdlib removals and syntax changes (for example invalid escape sequences becoming errors) into production-only failures.

## Examples

### Wrong

```yaml
# CI uses whatever the orb provides; Dockerfile says python:3.10
build:
  executor: python/default
  steps:
    - run: pytest
```

```python
from collections import Mapping   # warns on 3.9, AttributeError/ImportError on 3.10+
```

### Right

```yaml
build:
  parameters:
    python: { type: string }
  docker:
    - image: cimg/python:<< parameters.python >>
  steps:
    - run: pytest
workflows:
  test:
    jobs:
      - build:
          matrix:
            parameters:
              python: ["3.10", "3.12"]   # runtime version + next target
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
filterwarnings = ["error::DeprecationWarning"]
```

```python
from collections.abc import Mapping
```

## Related Lessons

None. Tracked as tasks CI-01 and TST-01 in [the improvement plan](../plans/improvement-plan.md).
