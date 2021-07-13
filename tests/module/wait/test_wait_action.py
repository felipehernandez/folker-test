from unittest.mock import Mock

import pytest
from pytest import raises

from folker.model.context import Context
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.module.wait.action import WaitStageAction


class TestWaitAction:
    action: WaitStageAction

    @pytest.fixture(autouse=True)
    def setup(self):
        self.action = WaitStageAction()
        yield

    def test_execution(self):
        logger = Mock()

        self.action.time = 0.1

        context = self.action.execute(logger, context=Context())

        assert {} == context.test_variables
        assert 'elapsed_time' in context.stage_variables
        assert context.stage_variables['elapsed_time'] >= 100
