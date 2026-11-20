# Test against the dependency set the image installs, and build real clients at least once

- **Date**: 2026-11-19
- **Status**: Active

## Rule

The versions the unit tests run against (`requirements.txt`) must be the ones the image installs (`setup.py`). For every third-party client the code constructs, at least one unit test builds the real class, with no mock in between.

## Context

Applies whenever:
- a dependency is bumped in `setup.py` or `requirements.txt` (including Renovate PRs),
- code calls a third-party constructor or factory with keyword arguments,
- a test patches the client class (`@patch('...PublisherClient')`).

## Why

- `setup.py` pinned `google-cloud-pubsub==2.39.0` while `requirements.txt` still had `2.18.0` and the tests replaced `PublisherClient` with a `Mock`. Version 2.x dropped `PublisherClient(channel=...)`, so every PubSub stage failed in the image (`PublisherClient.__init__() got an unexpected keyword argument 'channel'`). All 1373 unit tests stayed green; only `run-integration-tests-pubsub` failed, and it only ran once the unit-test job went green.
- A mock accepts any arguments, so it cannot notice an API change in the library it replaces.

## How to apply

- When bumping a pin, change it in both files in the same commit. `google-cloud-pubsub`, `grpcio`, `grpcio-tools` and `protobuf` move together.
- Keep the mocked tests for behaviour, and add a test like `tests/module/gcp/pubsub/test_pubsub_clients.py` that calls the real constructor (the connection is lazy, so no server is needed).
- To reproduce an integration failure, build the image (`docker build --target integration`) and run `docker-compose run integration-tests-<name>`; it takes about two minutes and prints the same traceback as CI.
