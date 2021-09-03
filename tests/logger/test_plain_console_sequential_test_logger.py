import pytest

from folker.logger.test_logger import PlainConsoleSequentialTestLogger
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
        logger = PlainConsoleSequentialTestLogger(config=normal_configuration)
        self.full_log(logger)

    def test_full_log_debug(self, debug_configuration):
        logger = PlainConsoleSequentialTestLogger(config=debug_configuration)
        self.full_log(logger)

    def test_full_log_trace(self, trace_configuration):
        logger = PlainConsoleSequentialTestLogger(config=trace_configuration)
        self.full_log(logger)


@pytest.mark.logger
class TestVisualPlainSequentialConsoleTestLogger:
    def full_log(self, logger):
        logger.test_start(test_name='a_name', test_description='a_description')

    def test_full_log_normal(self, normal_configuration):
        logger = PlainConsoleSequentialTestLogger(config=normal_configuration)
        self.full_log(logger)

    def test_full_log_debug(self, debug_configuration):
        logger = PlainConsoleSequentialTestLogger(config=debug_configuration)
        self.full_log(logger)

    def test_full_log_trace(self, trace_configuration):
        logger = PlainConsoleSequentialTestLogger(config=trace_configuration)
        self.full_log(logger)


@pytest.mark.logger
class TestNormalTestPlainConsoleSequentialTestLogger:
    """
    Test all logging for test level execution on normal mode
    """

    def test_test_start_with_description(self, capsys, normal_configuration):
        logger = PlainConsoleSequentialTestLogger(config=normal_configuration)

        logger.test_start(test_name='a_name', test_description='a_description')

        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'TEST: ' + 'a_name' + '\n' \
               + 'a_description' + '\n'

    def test_test_start_without_description(self, capsys, normal_configuration):
        logger = PlainConsoleSequentialTestLogger(config=normal_configuration)

        logger.test_start(test_name='a_name')

        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'TEST: ' + 'a_name' + '\n'
