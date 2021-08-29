from enum import Enum

from folker.logger import SystemLogger
from folker.logger.color_console_system_logger import ColorConsoleSystemLogger
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
