from enum import Enum

from folker.logger.console_parallel_test_logger import ConsoleParallelTestLogger
from folker.logger.console_sequential_test_logger import ConsoleSequentialTestLogger
from folker.logger.console_system_logger import ConsoleSystemLogger
from folker.logger.file_system_logger import FileSystemLogger
from folker.util.parameters import log_to_file


class LoggerType(Enum):
    SEQUENTIAL = 1
    PARALLEL = 2


def build_system_logger():
    file = log_to_file()
    if file:
        return FileSystemLogger(file)
    else:
        return ConsoleSystemLogger()


def build_test_logger(type: LoggerType = LoggerType.SEQUENTIAL):
    file = log_to_file()
    if file:
        pass
    else:
        return {
            LoggerType.SEQUENTIAL: ConsoleSequentialTestLogger,
            LoggerType.PARALLEL: ConsoleParallelTestLogger
        }[type]()
