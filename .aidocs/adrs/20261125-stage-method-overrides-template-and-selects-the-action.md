# A stage's `method` overrides its template's and selects the action class

- **Date**: 2026-11-25
- **Status**: Accepted

## Context

A stage that has the `id` of a stage template is merged with it at load time (`_enrich_stages` in `folker/load/files.py`, then `Stage.__add__` and each action's `__add__`). For every scalar field the rule is the same: the stage's value wins when it sets one, and otherwise the template's value is kept (`tests/model/stage/test_action_merge_matrix.py`).

`method` was the exception, and it was not handled the same way across modules (BUG-21):

- `code` and `grpc` took the stage's `method`.
- REST, Kafka, Postgres, RabbitMQ, ZooKeeper, Pub/Sub, File and Protobuf ignored it and kept the template's, with no warning. A `SELECT` template plus an `INSERT` stage ran the `SELECT`.
- For the modules whose schema picks a subclass from `method` (`{...}.get(data["method"], Base)` in each `schema.py`), the subclass holds the behaviour (`execute`, specific validation). The merged object was a copy of the template, so it kept the template's class, and copying the stage's `method` alone would have left a `SELECT` class labelled `INSERT`.

This is a user-facing contract: it decides what existing YAML suites do. Once users write templates that rely on it, changing it again would silently change which operation their tests run.

## Decision

We will treat `method` like every other scalar field: **if the stage sets a `method`, it wins**. The merged action also takes the **stage's class**, so the operation that runs matches the `method`. The template's class is kept when the stage does not set a `method`, or when the stage's class is an ancestor of the template's (a stage built as the generic base class).

It is implemented once, in `StageAction._merge_method` (`folker/model/stage/stageaction.py`), and called at the start of `__add__` in REST, Kafka, Postgres, RabbitMQ, ZooKeeper, Pub/Sub, File, Protobuf and Gmail. `code` and `grpc`, whose `method` is a plain string, keep their own merge with the same result.

A template is therefore a reusable preset (connection, credentials, shared fields) that stages can use for different operations:

```yaml
# template
- id: db
  action: {type: POSTGRES, method: SELECT, host: db, user: app, password: ${secret}, database: app}
# test
- id: db
  name: insert a row
  action: {type: POSTGRES, method: INSERT, sql: "INSERT INTO t VALUES (1)"}   # runs an INSERT on `db`
```

## Consequences

### Positive

- One rule for every field and every module: the stage wins. It is pinned by `TestMethod` and `TestMethodDispatch` in `tests/model/stage/test_action_merge_matrix.py` and by an end-to-end test in `tests/load/test_stage_schema.py`.
- A stage that names another operation runs that operation instead of silently running the template's.
- One template can serve several operations on the same system, so fewer templates are duplicated.
- The rule carries over to the generic merge planned in IMP-05.

### Negative

- It changes behaviour: a suite whose stages repeat a template with a different `method` used to run the template's operation and now runs the stage's. Such suites were most likely wrong before, but their results can change.
- Changing the class of an existing object (`result.__class__ = type(enrichment)`) depends on all subclasses of a module sharing the base `__init__` and state and adding only behaviour. A future subclass with its own state in `__init__` would break this; IMP-05 (dataclass actions, one generic merge) should replace this with building the result from the right class.
- The template's `mandatory_fields` are no longer the ones that apply. Validation runs on the merged action, so the stage's class decides which fields are required, which is correct, but a template may now be valid for one operation and incomplete for another.

### Neutral

- Templates and stages of the method-dispatched modules used to need a `method` to load at all (`KeyError('method')` in the schema). BUG-24 fixed that: an action without `method` loads as the base class and takes the method and class of the other side, so a template can be a pure connection preset and a stage can override a single field.
- Gmail has a single method today, so only its merge code changes, not its behaviour.

## Alternatives Considered

### Reject a different `method` at load time

- **Description**: A stage may repeat the template's `method` but not change it; a different one is a load error on `action.method`. `code` and `grpc` would change from "stage wins" to the same error.
- **Reason for rejection**: It makes `method` the only field a stage cannot override, so the merge rules stay inconsistent, and it rules out using one template as a connection preset for several operations. It would also break `code` and `grpc` suites that already rely on overriding `method`.

### Keep the template's `method` (status quo)

- **Description**: Leave the behaviour as it was and document it.
- **Reason for rejection**: The stage's `method` is ignored without any warning, so a test can run a different operation from the one it shows. It also leaves `code` and `grpc` behaving the opposite way.

### Copy `method` but keep the template's class

- **Description**: Merge only the `method` field, as for any other scalar, without touching the class.
- **Reason for rejection**: For the method-dispatched modules the class runs the operation, so the action would say `INSERT` and execute the `SELECT` code. It is worse than either rule above.
