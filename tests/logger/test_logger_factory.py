import pytest

from folker.logger import logger_factory
from folker.logger import PlainFileSystemLogger,\
    PlainConsoleSystemLogger, \
    ColorConsoleSystemLogger
from folker.parameters import Configuration


@pytest.mark.logger
class TestLoggerFactory:
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
