from enum import Enum

from folker.logger.console_parallel_test_logger import ConsoleParallelTestLogger
from folker.logger.console_sequential_test_logger import ConsoleSequentialTestLogger
from folker.logger.file_parallel_test_logger import FileParallelTestLogger
from folker.logger.file_sequential_test_logger import FileSequentialTestLogger
from folker.logger.system_logger import SystemLogger, \
    PlainConsoleSystemLogger, \
    ColorConsoleSystemLogger, \
    PlainFileSystemLogger
from folker.parameters import Configuration


class LoggerType(Enum):
    SEQUENTIAL = 1
    PARALLEL = 2


def system_logger(config: Configuration) -> SystemLogger:
    """
    Gets the SystemLogger implementation based on config data

    :param config:
    :return: SystemLogger
    """

    if config.log_file:
        return PlainFileSystemLogger(config)
    else:
        if config.logger_type is Configuration.LoggerType.PLAIN:
            return PlainConsoleSystemLogger(config=config)
        return ColorConsoleSystemLogger(config=config)


def build_test_logger(config: Configuration, type: LoggerType = LoggerType.SEQUENTIAL):
    file = config.log_file
    if file:
        return {
            LoggerType.SEQUENTIAL: FileSequentialTestLogger,
            LoggerType.PARALLEL: FileParallelTestLogger
        }[type](file)
    else:
        return {
            LoggerType.SEQUENTIAL: ConsoleSequentialTestLogger,
            LoggerType.PARALLEL: ConsoleParallelTestLogger
        }[type](config)
