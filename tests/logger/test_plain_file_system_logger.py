import pytest

from folker.logger.file_system_logger import FileSystemLogger
from folker.parameters import Configuration


@pytest.mark.logger
class TestSystemSetupFileSystemLogger:
    """
    Test all logging for system setup stage
    """

    def test_system_setup_start_on_normal(self, tmpdir):
        """
        GIVEN normal_configuration
        WHEN system_setup_start
        THEN no output
        """
        log_file = tmpdir.join('test.log')
        system_logger = FileSystemLogger(config=Configuration(log_file=str(log_file)))

        system_logger.system_setup_start()

        assert not log_file.exists()

    def test_system_setup_start_on_debug(self, tmpdir):
        """
        GIVEN debug_configuration
        WHEN system_setup_start
        THEN no output
        """
        log_file = tmpdir.join('test.log')
        system_logger = FileSystemLogger(config=Configuration(log_file=str(log_file), debug=True))

        system_logger.system_setup_start()

        assert not log_file.exists()

    def test_system_setup_start_on_trace(self, tmpdir):
        """
        GIVEN trace_configuration
        WHEN system_setup_start
        THEN output
        """
        log_file = tmpdir.join('test.log')
        system_logger = FileSystemLogger(config=Configuration(log_file=str(log_file),
                                                              trace=True))

        system_logger.system_setup_start()

        assert log_file.read() == 'SETUP : start\n'

    def test_system_setup_completed_on_normal(self, tmpdir):
        """
        GIVEN normal_configuration
        WHEN system_setup_completed
        THEN no output
        """

        log_file = tmpdir.join('test.log')
        system_logger = FileSystemLogger(config=Configuration(log_file=str(log_file)))

        system_logger.system_setup_completed()

        assert not log_file.exists()

    def test_system_setup_completed_on_debug(self, tmpdir):
        """
        GIVEN normal_configuration
        WHEN system_setup_completed
        THEN no output
        """

        log_file = tmpdir.join('test.log')
        system_logger = FileSystemLogger(config=Configuration(log_file=str(log_file),
                                                              debug=True))

        system_logger.system_setup_completed()

        assert not log_file.exists()

    def test_system_setup_completed_on_trace(self, tmpdir):
        """
        GIVEN trace_configuration
        WHEN system_setup_completed
        THEN output
        """
        log_file = tmpdir.join('test.log')
        system_logger = FileSystemLogger(config=Configuration(log_file=str(log_file),
                                                              trace=True))

        system_logger.system_setup_completed()

        assert log_file.read() == 'SETUP : completed\n'
