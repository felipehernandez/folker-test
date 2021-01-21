from folker.logger import build_system_logger, build_test_logger, LoggerType
from folker.logger.console_parallel_test_logger import ConsoleParallelTestLogger
from folker.logger.console_sequential_test_logger import ConsoleSequentialTestLogger
from folker.logger.console_system_logger import ConsoleSystemLogger
from folker.logger.file_parallel_test_logger import FileParallelTestLogger
from folker.logger.file_sequential_test_logger import FileSequentialTestLogger
from folker.logger.file_system_logger import FileSystemLogger


def test_build_system_logger_when_log_to_file(mocker):
    mocker.patch('folker.logger.logger_factory.log_to_file', return_value='A_FILE')

    logger = build_system_logger()

    assert isinstance(logger, FileSystemLogger), 'Wrong logger'
    assert 'A_FILE' == logger.file_name


def test_build_system_logger_when_log_to_console(mocker):
    mocker.patch('folker.logger.logger_factory.log_to_file', return_value=None)

    logger = build_system_logger()

    assert isinstance(logger, ConsoleSystemLogger), 'Wrong logger'


def test_build_test_logger_when_log_to_file_and_sequential(mocker):
    mocker.patch('folker.logger.logger_factory.log_to_file', return_value='A_FILE')

    logger = build_test_logger(LoggerType.SEQUENTIAL)

    assert isinstance(logger, FileSequentialTestLogger), 'Wrong logger'
    assert 'A_FILE' == logger.file_name


def test_build_test_logger_when_log_to_console_and_sequential(mocker):
    mocker.patch('folker.logger.logger_factory.log_to_file', return_value=None)

    logger = build_test_logger(LoggerType.SEQUENTIAL)

    assert isinstance(logger, ConsoleSequentialTestLogger), 'Wrong logger'


def test_build_test_logger_when_log_to_file_and_parallel(mocker):
    mocker.patch('folker.logger.logger_factory.log_to_file', return_value='A_FILE')

    logger = build_test_logger(LoggerType.PARALLEL)

    assert isinstance(logger, FileParallelTestLogger), 'Wrong logger'
    assert 'A_FILE' == logger.file_name


def test_build_test_logger_when_log_to_console_and_parallel(mocker):
    mocker.patch('folker.logger.logger_factory.log_to_file', return_value=None)

    logger = build_test_logger(LoggerType.PARALLEL)

    assert isinstance(logger, ConsoleParallelTestLogger), 'Wrong logger'
