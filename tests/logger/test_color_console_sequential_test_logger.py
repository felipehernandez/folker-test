import pytest

from folker.logger.logger import ConsoleColor
from folker.logger.test_logger import ColorConsoleSequentialTestLogger
from folker.model import Context
from folker.model.error import SourceException
from folker.module.wait.action import WaitStageAction


@pytest.mark.logger
class TestVisualColorConsoleTestLogger:
    def full_log(self, logger):
        logger.test_start(test_name='a name', test_description='a description')

        logger.stage_start('a stage')
        logger.action_prelude(WaitStageAction(time=2).__dict__,
                              Context(test_variables={'test_key': 'test_value'},
                                      stage_variables={'stage_key': 'stage_value'},
                                      secrets={'secret_key': 'secret_value'}))
        logger.message('a message')
        logger.action_debug('an action debug message')
        logger.action_error('an error from action')
        logger.action_warn('a warn from action')
        logger.action_conclusion(WaitStageAction(time=2).__dict__,
                                 Context(test_variables={'test_key': 'test_value'},
                                         stage_variables={'stage_key': 'stage_value'},
                                         secrets={'secret_key': 'secret_value'}))
        logger.log_text('text to log')
        logger.assertion_success('a succ assert')
        logger.assertion_fail('a fail assert', variables={'vbl': 'value'})
        logger.assertion_error('an error on assert', exception=Exception('error'))
        logger.assert_test_result(10, 10, 0)
        logger.assert_test_result(10, 9, 1)

        logger.stage_skip('a stage')

        logger.stage_start('another stage')

        logger.test_finish()
        logger.test_finish_error(SourceException(source='a source',
                                                 error='an error',
                                                 cause='a cause',
                                                 details={'a detail_key': 'a detail_value'}, ))

    def test_full_log_normal(self, normal_configuration):
        logger = ColorConsoleSequentialTestLogger(config=normal_configuration)
        self.full_log(logger)

    def test_full_log_debug(self, debug_configuration):
        logger = ColorConsoleSequentialTestLogger(config=debug_configuration)
        self.full_log(logger)

    def test_full_log_trace(self, trace_configuration):
        logger = ColorConsoleSequentialTestLogger(config=trace_configuration)
        self.full_log(logger)


@pytest.mark.logger
class TestNormalTestColorConsoleSequentialTestLogger:
    """
    Test all logging for test level execution on normal mode
    """

    def test_test_start_with_description(self, capsys, normal_configuration):
        logger = ColorConsoleSequentialTestLogger(config=normal_configuration)
        test_name = 'a_name',
        test_description = 'a_description'

        logger.test_start(test_name=test_name, test_description=test_description)

        captured = capsys.readouterr()
        open_color_name = ConsoleColor.HIGH_CYAN.code()
        open_color_description = ConsoleColor.BLUE.code()
        close_color = ConsoleColor.DEFAULT.code()
        expected_output = (
            f'{open_color_name}{"-" * 100}{close_color}\n'
            f'{open_color_name}TEST: {test_name}{close_color}\n'
            f'{open_color_description}{test_description}{close_color}\n'
        )
        assert captured.out == expected_output

    def test_test_start_without_description(self, capsys, normal_configuration):
        logger = ColorConsoleSequentialTestLogger(config=normal_configuration)
        test_name = 'a_name'

        logger.test_start(test_name=test_name)

        captured = capsys.readouterr()
        open_color = ConsoleColor.HIGH_CYAN.code()
        delimiter = '-' * 100
        close_color = ConsoleColor.DEFAULT.code()
        expected_output = (
            f'{open_color}{delimiter}{close_color}\n'
            f'{open_color}TEST: {test_name}{close_color}\n'
        )
        assert captured.out == expected_output
