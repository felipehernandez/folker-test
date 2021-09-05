import pytest

from folker.logger.test_logger import PlainConsoleParallelTestLogger


@pytest.mark.logger
class TestVisualPlainParallelConsoleTestLogger:
    def full_log(self, logger):
        logger.test_start(test_name='a_name', test_description='a_description')
        logger.test_finish()

    def test_full_log_normal(self, normal_configuration):
        logger = PlainConsoleParallelTestLogger(config=normal_configuration)
        self.full_log(logger)

    def test_full_log_debug(self, debug_configuration):
        logger = PlainConsoleParallelTestLogger(config=debug_configuration)
        self.full_log(logger)

    def test_full_log_trace(self, trace_configuration):
        logger = PlainConsoleParallelTestLogger(config=trace_configuration)
        self.full_log(logger)


@pytest.mark.logger
class TestNormalTestPlainConsoleParallelTestLogger:
    """
    Test all logging for test level execution on normal mode
    """

    def test_test_start_with_description(self, capsys, normal_configuration):
        logger = PlainConsoleParallelTestLogger(config=normal_configuration)

        logger.test_start(test_name='a_name', test_description='a_description')

        captured = capsys.readouterr()
        assert captured.out == ''
        assert len(logger.report) != 0

    def test_test_start_without_description(self, capsys, normal_configuration):
        logger = PlainConsoleParallelTestLogger(config=normal_configuration)

        logger.test_start(test_name='a_name')

        captured = capsys.readouterr()
        assert captured.out == ''
        assert len(logger.report) != 0
