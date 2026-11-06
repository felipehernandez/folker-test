import pytest

from folker.logger.test_logger import PlainConsoleSequentialTestLogger
from folker.model import Context
from folker.module.void.action import VoidStageAction


@pytest.mark.logger
@pytest.mark.action_void
class TestVoidActionNormalLog:
    def test_basic_execution_logs(self, capsys, normal_configuration):
        action = VoidStageAction()

        logger = PlainConsoleSequentialTestLogger(config=normal_configuration)
        context = Context.empty_context()

        action.execute(logger=logger, context=context)

        captured = capsys.readouterr()
        expected_output = ('')
        assert captured.out == expected_output


@pytest.mark.logger
@pytest.mark.action_void
class TestVoidActionDebugLog:
    def test_basic_execution_logs(self, capsys, debug_configuration):
        action = VoidStageAction()

        logger = PlainConsoleSequentialTestLogger(config=debug_configuration)
        context = Context.empty_context()

        action.execute(logger=logger, context=context)

        captured = capsys.readouterr()
        expected_output = ('')
        assert captured.out == expected_output


@pytest.mark.logger
@pytest.mark.action_void
class TestVoidActionTraceLog:
    def test_basic_execution_logs(self, capsys, trace_configuration):
        action = VoidStageAction()

        logger = PlainConsoleSequentialTestLogger(config=trace_configuration)
        context = Context.empty_context()

        action.execute(logger=logger, context=context)

        captured = capsys.readouterr()
        expected_output = (
            '............................................. PRELUDE ..............................................\n'
            '{\n'
            '    "ACTION": {},\n'
            '    "SECRETS": {},\n'
            '    "STAGE CONTEXT": {},\n'
            '    "TEST CONTEXT": {}\n'
            '}\n'
            '............................................ CONCLUSION ............................................\n'
            '{\n'
            '    "ACTION": {},\n'
            '    "SECRETS": {},\n'
            '    "STAGE CONTEXT": {\n'
            '        "elapsed_time": 0\n'
            '    },\n'
            '    "TEST CONTEXT": {}\n'
            '}\n'
        )
        assert captured.out == expected_output
