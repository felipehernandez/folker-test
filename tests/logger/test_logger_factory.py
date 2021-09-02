import pytest

from folker.logger import logger_factory, LoggerType
from folker.logger.system_logger import PlainFileSystemLogger, PlainConsoleSystemLogger, \
    ColorConsoleSystemLogger
from folker.logger.test_logger import PlainFileParallelTestLogger, PlainFileSequentialTestLogger, \
    PlainConsoleParallelTestLogger, PlainConsoleSequentialTestLogger, \
    ColorConsoleSequentialTestLogger, ColorConsoleParallelTestLogger
from folker.parameters import Configuration


@pytest.mark.logger
class TestLoggerFactorySystem:
    def test_given_log_file_then_file_system_logger(self):
        config = Configuration(log_file='a_file.log')

        logger = logger_factory.system_logger(config=config)

        assert type(logger) is PlainFileSystemLogger

    def test_given_no_log_file_and_plain_logger_type_then_plain_console_system_logger(self):
        config = Configuration(log_file=None,
                               logger_type=Configuration.LoggerType.PLAIN.name)

        logger = logger_factory.system_logger(config=config)

        assert type(logger) is PlainConsoleSystemLogger

    def test_given_no_log_file_and_color_logger_type_then_color_console_system_logger(self):
        config = Configuration(log_file=None,
                               logger_type=Configuration.LoggerType.COLOR.name)

        logger = logger_factory.system_logger(config=config)

        assert type(logger) is ColorConsoleSystemLogger


@pytest.mark.logger
class TestLoggerFactoryTest:
    def test_given_file_default(self):
        config = Configuration(log_file='a_file.log')

        logger = logger_factory.build_test_logger(config=config)

        assert type(logger) is PlainFileParallelTestLogger

    def test_given_file_sequential(self):
        config = Configuration(log_file='a_file.log')

        logger = logger_factory.build_test_logger(config=config, type=LoggerType.SEQUENTIAL)

        assert type(logger) is PlainFileSequentialTestLogger

    def test_given_file_sequential(self):
        config = Configuration(log_file='a_file.log')

        logger = logger_factory.build_test_logger(config=config, type=LoggerType.PARALLEL)

        assert type(logger) is PlainFileParallelTestLogger

    def test_given_console_default(self):
        config = Configuration()

        logger = logger_factory.build_test_logger(config=config)

        assert type(logger) is ColorConsoleParallelTestLogger

    def test_given_console_plain_when_sequential(self):
        config = Configuration(logger_type=Configuration.LoggerType.PLAIN.name)

        logger = logger_factory.build_test_logger(config=config, type=LoggerType.SEQUENTIAL)

        assert type(logger) is PlainConsoleSequentialTestLogger

    def test_given_console_plain_when_parallel(self):
        config = Configuration(logger_type=Configuration.LoggerType.PLAIN.name)

        logger = logger_factory.build_test_logger(config=config, type=LoggerType.PARALLEL)

        assert type(logger) is PlainConsoleParallelTestLogger

    def test_given_console_color_when_default(self):
        config = Configuration(logger_type=Configuration.LoggerType.COLOR.name)

        logger = logger_factory.build_test_logger(config=config)

        assert type(logger) is ColorConsoleParallelTestLogger

    def test_given_console_color_when_sequential(self):
        config = Configuration(logger_type=Configuration.LoggerType.COLOR.name)

        logger = logger_factory.build_test_logger(config=config, type=LoggerType.SEQUENTIAL)

        assert type(logger) is ColorConsoleSequentialTestLogger

    def test_given_console_color_when_parallel(self):
        config = Configuration(logger_type=Configuration.LoggerType.COLOR.name)

        logger = logger_factory.build_test_logger(config=config, type=LoggerType.PARALLEL)

        assert type(logger) is ColorConsoleParallelTestLogger

    def test_given_console_default_when_default(self):
        config = Configuration()

        logger = logger_factory.build_test_logger(config=config)

        assert type(logger) is ColorConsoleParallelTestLogger

    def test_given_console_default_when_sequential(self):
        config = Configuration()

        logger = logger_factory.build_test_logger(config=config, type=LoggerType.SEQUENTIAL)

        assert type(logger) is ColorConsoleSequentialTestLogger

    def test_given_console_default_when_parallel(self):
        config = Configuration()

        logger = logger_factory.build_test_logger(config=config, type=LoggerType.PARALLEL)

        assert type(logger) is ColorConsoleParallelTestLogger
