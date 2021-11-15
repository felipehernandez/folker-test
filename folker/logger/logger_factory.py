from enum import Enum

from folker.logger.system_logger import SystemLogger, \
    PlainConsoleSystemLogger, \
    ColorConsoleSystemLogger, \
    PlainFileSystemLogger
from folker.logger.test_logger import PlainFileSequentialTestLogger, \
    PlainFileParallelTestLogger, \
    TestLogger, PlainConsoleSequentialTestLogger, ColorConsoleSequentialTestLogger, \
    PlainConsoleParallelTestLogger, ColorConsoleParallelTestLogger
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


def build_test_logger(config: Configuration,
                      type: LoggerType = LoggerType.PARALLEL) -> TestLogger:
    if config.log_file:
        if type is LoggerType.SEQUENTIAL:
            return PlainFileSequentialTestLogger(config=config)
        return PlainFileParallelTestLogger(config=config)
    else:
        if type is LoggerType.SEQUENTIAL:
            if config.logger_type is Configuration.LoggerType.PLAIN:
                return PlainConsoleSequentialTestLogger(config=config)
            return ColorConsoleSequentialTestLogger(config=config)
        else:
            if config.logger_type is Configuration.LoggerType.PLAIN:
                return PlainConsoleParallelTestLogger(config=config)
            return ColorConsoleParallelTestLogger(config=config)
