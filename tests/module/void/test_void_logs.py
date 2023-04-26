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
        expected_output = (f'')
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
        expected_output = (f'')
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
            f'............................................. PRELUDE ..............................................\n'
            f'{{\n'
            f'    "ACTION": {{}},\n'
            f'    "SECRETS": {{}},\n'
            f'    "STAGE CONTEXT": {{}},\n'
            f'    "TEST CONTEXT": {{}}\n'
            f'}}\n'
            f'............................................ CONCLUSION ............................................\n'
            f'{{\n'
            f'    "ACTION": {{}},\n'
            f'    "SECRETS": {{}},\n'
            f'    "STAGE CONTEXT": {{\n'
            f'        "elapsed_time": 0\n'
            f'    }},\n'
            f'    "TEST CONTEXT": {{}}\n'
            f'}}\n'
        )
        assert captured.out == expected_output
