# Keep the loader schemas free of top-level imports from action modules

- **Date**: 2026-11-25
- **Status**: Active

## Rule

Do not import anything from `folker.module.*` at the top of `folker/load/schemas.py` (or of any file that a module package imports to register itself). When loader code needs a module class, import it inside the function that uses it, with a comment saying why.

## Context

Applies whenever:
- loader code (`folker/load/schemas.py`, `StageSchema`, `TestSchema`, `ActionSchema`) needs a concrete action such as `VoidStageAction`, for example to build a default,
- a new action module is added, since its `__init__.py` follows the same registration pattern,
- an `ImportError: cannot import name 'ActionSchema' from partially initialized module 'folker.load.schemas'` appears.

## Why

- Importing the `folker` package runs `folker/__init__.py`, which imports every `folker.module.<name>` package. Each package's `__init__.py` starts with `from folker.load.schemas import ActionSchema` and registers its schema in `ActionSchema.type_schemas`.
- So `folker.load.schemas` is imported while the modules are being imported. If `schemas.py` itself imports `folker.module.void.action` at top level, Python first runs `folker/module/void/__init__.py`, which imports `ActionSchema` from the half-initialized `schemas.py`, and loading fails. Every test fails at collection, and the CLI cannot start.
- Importing a submodule (`folker.module.void.action`) still runs the package's `__init__.py` first, so importing "only the action file" does not avoid the cycle.
- In BUG-22 the obvious change (build the default `VoidStageAction` in `StageSchema.make_stage`, imported at the top) broke the whole suite this way. A function-level import runs only when stages are loaded, after all modules have registered.
- IMP-03 / IMP-04 (explicit registry, lazy module loading) should remove the cycle properly; until then this rule applies.

## Examples

### Wrong

```python
# folker/load/schemas.py
from folker.model import Test, Stage
from folker.module.void.action import VoidStageAction   # circular: void/__init__ imports this file

class StageSchema(Schema):
    @post_load
    def make_stage(self, data, **kwargs):
        data.setdefault('action', VoidStageAction())
        return Stage(**data)
```

### Right

```python
# folker/load/schemas.py
class StageSchema(Schema):
    @post_load
    def make_stage(self, data, **kwargs):
        if 'action' not in data:
            # Imported here: every module package imports this file to register its schema
            from folker.module.void.action import VoidStageAction
            data['action'] = VoidStageAction()
        return Stage(**data)
```

Check with `python -c "import folker.cli"` after touching the loader's imports.

## Related Lessons

None. Related plan items: IMP-03 and IMP-04 in [the improvement plan](../plans/improvement-plan.md); found in BUG-22 ([the completed tasks](../plans/completed-tasks.md)).
