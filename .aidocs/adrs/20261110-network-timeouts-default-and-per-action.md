# Bound every network call with a default timeout and an optional per-action `timeout`

- **Date**: 2026-11-10
- **Status**: Accepted

## Context

Folker actions talk to remote systems (REST, GraphQL, gRPC, Postgres, RabbitMQ, ZooKeeper, Pub/Sub, Kafka). Until BUG-14, only Kafka had timeouts (10 s). Against a dead or black-holed endpoint the other modules blocked until the CI job's own limit, and then reported nothing useful about which stage was stuck.

Forces:

- Test suites run unattended in CI, so failing fast with a clear error matters more than waiting for a slow service.
- Some tests legitimately wait longer (a large query, a slow gRPC stream), so a fixed value is not enough.
- Each client library models time differently: `requests` has per-connect and per-read timeouts, psycopg2 has `connect_timeout` (whole seconds) plus the server-side `statement_timeout` (ms), pika has three connection timeouts, kazoo has a `start()` timeout, gRPC has a per-call deadline, the Pub/Sub client has per-call timeouts and `future.result(timeout=...)`.
- The `timeout` field becomes part of the test-definition format that users write in YAML. Once suites use it, removing or renaming it is a breaking change.
- Stage-level `retry` / `timeout` is planned separately (FEAT-04) and should not be blocked by this decision.

## Decision

We will give every action that opens a network connection a `timeout`, in seconds:

- `folker/module/timeout.py` defines `DEFAULT_TIMEOUT = 30` and `effective_timeout()`. An action uses its own `timeout` when set and the default otherwise.
- `timeout` is an optional numeric field (`fields.Float()`) in the schema of REST, Postgres, RabbitMQ, ZooKeeper, GraphQL, gRPC and Pub/Sub actions. Templates merge it like any other field: an enrichment overrides it only when it defines one.
- `StageAction._validate_timeout` validates it for all actions in one place. Zero, negative, boolean and non-numeric values are reported as the wrong field `action.timeout` when the suite loads.
- Each module maps the single value onto what its client supports (REST/GraphQL: request timeout; Postgres: `connect_timeout` and `statement_timeout`; RabbitMQ: socket, stack and blocked-connection timeouts; ZooKeeper: `start(timeout=...)`; gRPC: call deadline; Pub/Sub: per-call timeout and `future.result`). The meaning is "the longest we wait on one remote operation", not a limit on the whole stage.
- A timeout is reported through the module's usual error path (the action `error` variable where the module already catches failures, otherwise the exception fails the test). It is never swallowed.
- Kafka keeps its own 10 s values for now and does not take the field.

## Consequences

### Positive

- A dead endpoint fails the stage within about 30 s with the client's own error message, instead of hanging the job.
- One field with one meaning across seven modules, validated at load time, so a typo in `timeout` cannot silently fall back to the default.
- New network modules have an obvious pattern to follow (`effective_timeout` plus the schema field).

### Negative

- Behaviour change: a request, query or stream that takes longer than 30 s now fails unless the action sets a larger `timeout`. This must be called out in the changelog (CI-10).
- The value is per operation, not per stage: a REST call can still run longer than `timeout` in total if the server keeps sending data, and a gRPC server-streaming call is limited as a whole. A stage-wide limit remains FEAT-04.
- The Postgres `statement_timeout` makes the same value a query time limit, which users might not expect from a "connection" setting.
- RabbitMQ operations after the connection is up, and ZooKeeper operations after `start()`, are not individually bounded.
- `timeout` is now part of the YAML contract and has to be kept.

### Neutral

- Kafka is the one network module without the field.
- The action's `timeout` shows up in the trace output with the other action attributes.

## Alternatives Considered

### Fixed defaults only, no per-action field

- **Description**: Hard-code 30 s in each module.
- **Reason for rejection**: Tests that legitimately wait longer would have no way to opt out, so the default could not be chosen safely.

### A global CLI option or profile setting

- **Description**: One `--timeout` flag or a profile value applied to all actions.
- **Reason for rejection**: A suite mixes fast health checks with slow queries, and a global value is either too tight for the slow ones or too loose for the rest. It can still be added later as a default for `DEFAULT_TIMEOUT`.

### Separate connect and read timeouts per action

- **Description**: Expose `connect_timeout` and `read_timeout` (or a pair) like `requests` does.
- **Reason for rejection**: Only some clients support the split, so most modules could not honour it faithfully, and it doubles the surface of the YAML contract for little gain.

### Wait for stage-level timeout and retry (FEAT-04)

- **Description**: Do not touch the modules and bound the whole stage from the executor with a timer or a worker thread.
- **Reason for rejection**: It cannot interrupt a blocked client call cleanly (threads cannot be killed, and the connection stays open), and it is a larger change. Per-call timeouts stay useful under FEAT-04, which can be built on top.
