from typing import List

import pytest

from folker.logger.test_logger import TestLogger
from folker.model import Stage, Context


@pytest.fixture()
def do_nothing_stage():
    class DoNothingStage(Stage):
        executions_count: int = 0
        execution_contexts: List[Context] = []

        def execute(self, logger: TestLogger, context: Context) -> Context:
            self.executions_count += 1
            self.execution_contexts.append(context)
            return context

    yield DoNothingStage()
