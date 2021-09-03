import pytest

from folker.logger.system_logger import PlainConsoleSystemLogger
from folker.logger.test_logger import PlainConsoleSequentialTestLogger
from folker.parameters import Configuration


@pytest.fixture()
def normal_configuration():
    """
    Debug Configuration
    :return:
    """

    yield Configuration()


@pytest.fixture()
def debug_configuration():
    """
    Debug Configuration
    :return:
    """

    yield Configuration(debug=True)


@pytest.fixture()
def trace_configuration():
    """
    Debug Configuration
    :return:
    """

    yield Configuration(trace=True)


@pytest.fixture()
def plain_console_test_logger_on_trace(trace_configuration):
    """
    PlainConsoleLogger on trace mode
    """
    yield PlainConsoleSequentialTestLogger(config=trace_configuration)


@pytest.fixture()
def plain_console_system_logger_on_trace(trace_configuration):
    """
    PlainConsoleLogger on trace mode
    """
    yield PlainConsoleSystemLogger(config=trace_configuration)
