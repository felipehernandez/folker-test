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

    def test_execution(self,
                       capsys,
                       plain_console_test_logger_on_trace):
        self.action.message = 'Hello world'

        context = self.action.execute(logger=plain_console_test_logger_on_trace, context=Context())

        assert {} == context.test_variables
        assert 'elapsed_time' in context.stage_variables

        captured = capsys.readouterr()
        assert 'Hello world' in captured.out
