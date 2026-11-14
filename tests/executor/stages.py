"""Stages for the executor tests.

Module level and importable, so that parallel workers started with `spawn` or `forkserver` can
unpickle them.
"""
import time

from folker.model import Stage
from folker.model.error import TestFailException


class PassStage(Stage):
    def execute(self, logger, context):
        return context


class FailStage(Stage):
    def execute(self, logger, context):
        raise TestFailException(failure_messages=['failed on purpose'])


class CrashStage(Stage):
    """Fails with an exception that is not one of folker's own"""

    def execute(self, logger, context):
        raise RuntimeError('crashed on purpose')


class SleepStage(Stage):
    def __init__(self, seconds=0, **kwargs):
        super().__init__(**kwargs)
        self.seconds = seconds

    def execute(self, logger, context):
        time.sleep(self.seconds)
        return context


class SaveStage(Stage):
    """Saves a test variable, which a later test must not see"""

    def __init__(self, variable=None, value=None, **kwargs):
        super().__init__(**kwargs)
        self.variable = variable
        self.value = value

    def execute(self, logger, context):
        context.save_on_test(self.variable, self.value)
        return context


class AbsentVariableStage(Stage):
    """Fails if the variable is in the context"""

    def __init__(self, variable=None, **kwargs):
        super().__init__(**kwargs)
        self.variable = variable

    def execute(self, logger, context):
        try:
            context.resolve_variable_reference(self.variable)
        except Exception:
            return context
        raise TestFailException(failure_messages=[f'{self.variable} leaked into this test'])


class ExpectVariableStage(Stage):
    """Fails unless the variable has the expected value (in the test variables or the secrets)"""

    def __init__(self, variable=None, expected=None, **kwargs):
        super().__init__(**kwargs)
        self.variable = variable
        self.expected = expected

    def execute(self, logger, context):
        value = context.resolve_variable_reference(self.variable)
        if value != self.expected:
            raise TestFailException(
                failure_messages=[f'{self.variable} is {value!r}, expected {self.expected!r}'])
        return context


class FailOnValueStage(Stage):
    """Fails when `variable` (set by a test's foreach) has the given value"""

    def __init__(self, variable=None, value=None, **kwargs):
        super().__init__(**kwargs)
        self.variable = variable
        self.value = value

    def execute(self, logger, context):
        if context.resolve_variable_reference(self.variable) == self.value:
            raise TestFailException(failure_messages=[f'{self.variable} is {self.value}'])
        return context
