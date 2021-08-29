import pytest

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
