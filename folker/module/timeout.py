"""Network timeout shared by the modules that talk to a remote service (BUG-14).

An action may set `timeout` (seconds) in its definition; otherwise this default applies.
Without one, a dead endpoint blocks the run until the CI job itself times out.
"""

DEFAULT_TIMEOUT = 30


def effective_timeout(timeout) -> float:
    return DEFAULT_TIMEOUT if timeout is None else timeout
