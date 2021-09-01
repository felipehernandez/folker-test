import pytest

from folker.logger.system_logger import PlainFileSystemLogger
from folker.parameters import Configuration


@pytest.mark.logger
class TestNormalSystemStartupPlainFileSystemLogger:
    """
    Test all logging for system setup stage on normal mode
    """

    def test_system_setup_start(self, tmpdir):
        log_file = tmpdir.join('test.log')
        system_logger = PlainFileSystemLogger(config=Configuration(log_file=str(log_file)))

        system_logger.system_setup_start()

        assert not log_file.exists()


@pytest.mark.logger
class TestDebugSystemStartupPlainFileSystemLogger:
    """
    Test all logging for system setup stage on debug mode
    """

    def test_system_setup_start(self, tmpdir):
        log_file = tmpdir.join('test.log')
        system_logger = PlainFileSystemLogger(config=Configuration(log_file=str(log_file),
                                                                   debug=True))

        system_logger.system_setup_start()

        assert log_file.read() == '#' * 100 + '\n' \
               + 'SYSTEM SETUP : start\n'


@pytest.mark.logger
class TestNormalSystemStartupPlainFileSystemLogger:
    """
    Test all logging for system setup stage on trace mode
    """

    def test_system_setup_start(self, tmpdir):
        log_file = tmpdir.join('test.log')
        system_logger = PlainFileSystemLogger(config=Configuration(log_file=str(log_file),
                                                                   trace=True))

        system_logger.system_setup_start()

        assert log_file.read() == '#' * 100 + '\n' \
               + 'SYSTEM SETUP : start\n'
