from unittest.mock import Mock

import pytest

from folker.model.context import Context
from folker.module.printt.action import PrintStageAction


@pytest.mark.action_print
class TestVoidAction:
    action: PrintStageAction

    @pytest.fixture(autouse=True)
    def setup(self):
        self.action = PrintStageAction()
        yield

    def test_execution(self):
        logger = Mock()

        self.action.message = 'Hello world'

        context = self.action.execute(logger=logger, context=Context())

        assert {} == context.test_variables
        assert 'elapsed_time' in context.stage_variables
        logger.message.assert_called_with('Hello world')
