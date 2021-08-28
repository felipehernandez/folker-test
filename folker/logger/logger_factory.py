from enum import Enum

from folker.logger.console_system_logger import ConsoleSystemLogger
from folker.logger.file_system_logger import FileSystemLogger
from folker.parameters import Configuration


class LoggerType(Enum):
    SEQUENTIAL = 1
    PARALLEL = 2


def build_system_logger(config: Configuration):
    if config.log_file:
        return FileSystemLogger(config)
    else:
        return ConsoleSystemLogger(config, )
