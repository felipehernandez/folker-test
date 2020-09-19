from unittest.mock import Mock

import pytest
from pytest import raises

from folker.model.context import Context
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.module.wait.action import WaitAction


class TestWaitAction:
    action: WaitAction

    @pytest.fixture(autouse=True)
    def setup(self):
        self.action = WaitAction()
        yield

    def test_validate_missing_time(self):
        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert 'action.time' in execution_context.value.details['missing_fields']

    def test_validate_correct(self):
        self.action.time = 3

        self.action.validate()

    def test_execution(self):
        logger = Mock()

        self.action.time = 0.1

        context = self.action.execute(logger, context=Context())

        assert {} == context.test_variables
        assert 'elapsed_time' in context.stage_variables
        assert context.stage_variables['elapsed_time'] >= 100
