from enum import Enum

from folker.logger import SystemLogger
from folker.logger.color_console_system_logger import ColorConsoleSystemLogger
from folker.logger.console_parallel_test_logger import ConsoleParallelTestLogger
from folker.logger.console_sequential_test_logger import ConsoleSequentialTestLogger
from folker.logger.file_parallel_test_logger import FileParallelTestLogger
from folker.logger.file_sequential_test_logger import FileSequentialTestLogger
from folker.logger.file_system_logger import FileSystemLogger
from folker.logger.plain_console_system_logger import PlainConsoleSystemLogger
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
        return FileSystemLogger(config)
    else:
        return {
            Configuration.LoggerType.PLAIN: PlainConsoleSystemLogger,
            Configuration.LoggerType.COLOR: ColorConsoleSystemLogger
        }.get(config.logger_type)(config, )


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
        }[type]()
