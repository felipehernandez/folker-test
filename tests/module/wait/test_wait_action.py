import pytest

from folker.model.context import Context
from folker.module.wait.action import WaitStageAction


@pytest.mark.action_wait
class TestWaitAction:
    action: WaitStageAction

    @pytest.fixture(autouse=True)
    def setup(self):
        self.action = WaitStageAction()
        yield

    def test_execution(self, plain_console_test_logger_on_trace):
        self.action.time = 0.1

        context = self.action.execute(logger=(plain_console_test_logger_on_trace),
                                      context=Context())

        assert {} == context.test_variables
        assert 'elapsed_time' in context.stage_variables
        assert context.stage_variables['elapsed_time'] >= 100
