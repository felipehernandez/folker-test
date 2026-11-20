# Make compose wait for health, not for container start

- **Date**: 2026-11-10
- **Status**: Active

## Rule

Every service that tests depend on gets a `healthcheck` that proves what the tests need, and the test runners use `depends_on` in map form with `condition: service_healthy`. Do not paper over slow starts with retries or `sleep`.

## Context

Applies whenever:
- a service is added to `docker-compose.yaml` and an integration test connects to it,
- a CI job is tempted to retry the whole test command (`for i in 1 2 3`, `sleep 10`),
- an image used by a healthcheck is bumped or switched (probes depend on tools inside the image).

## Why

- `depends_on: [service]` (list form) only waits for the container to *start*. The test then races the service, and the 3x retry loop with `sleep 10` in CI hid it: flaky starts and real failures looked the same.
- "Port open" or "ping OK" is often earlier than "ready for the tests":
  - **Postgres:** the official image runs a temporary server during first-time init. `pg_isready` without `-h` checks the unix socket, which that server answers, so the service can report healthy and then restart under the test. Use `pg_isready -h 127.0.0.1` (the temporary server has TCP disabled).
  - **RabbitMQ:** ping can pass before `definitions.json` is imported. Also check that a queue from the definitions exists.
  - **Pub/Sub emulator (messagebird image):** it opens port 8682 only after creating the topics and subscriptions, so a TCP check on 8682 proves the fixtures exist.
- A `version: '3.x'` header can make old `docker-compose` v1 reject `condition:`. The `version:` key is obsolete in current Compose, so remove it, and print `docker-compose version` in CI so an old CLI shows up at once. Fallback if CI's CLI is too old: `up -d` plus a bounded `docker inspect --format '{{.State.Health.Status}}'` poll (a readiness wait, not a test retry).
- Check probes on the host architecture. Pulling an image with `--platform linux/amd64` on an arm64 laptop runs it under emulation, and RabbitMQ then crashed in its feature-flag code (`incompatible_feature_flags`), which looks like a healthcheck problem but is not one.
- Probes use tools inside `latest` images (`nc`, `curl`, bash `/dev/tcp`). Prefer bash `/dev/tcp` where bash exists, and pin the images (CI-07) so a tool does not disappear on an update.

## Examples

### Wrong

```yaml
integration-tests-postgres:
  depends_on:
    - postgres-server          # starts, but may not be ready
```

```sh
for i in $(seq 1 3); do
  docker-compose run integration-tests-x && break || sleep 10     # hides flakiness
done
```

### Right

```yaml
postgres-server:
  image: postgres
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -h 127.0.0.1 -U postgres"]   # -h: skip the init-time server
    interval: 5s
    timeout: 5s
    retries: 20
integration-tests-postgres:
  depends_on:
    postgres-server:
      condition: service_healthy
```

```sh
docker-compose run integration-tests-postgres      # once; a failure is a real failure
```

## Related Lessons

None. Tracked as TST-07 and CI-05 in [the completed tasks](../plans/completed-tasks.md).
