from unittest.mock import Mock

import pytest
from pytest import raises

from folker.model.context import Context
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.module.printt.action import PrintStageAction


class TestVoidAction:
    action: PrintStageAction

    @pytest.fixture(autouse=True)
    def setup(self):
        self.action = PrintStageAction()
        yield

    def test_validate_missing_message(self):
        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert 'action.message' in execution_context.value.details['missing_fields']

    def test_validate_correct(self):
        self.action.message = 'a_message'

        self.action.validate()

    def test_execution(self):
        logger = Mock()

        self.action.message = 'Hello world'

        context = self.action.execute(logger, context=Context())

        assert {} == context.test_variables
        assert 'elapsed_time' in context.stage_variables
        logger.message.assert_called_with('Hello world')
