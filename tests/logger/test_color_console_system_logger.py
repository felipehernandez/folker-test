import pytest

from folker.logger.color_console_system_logger import ColorConsoleSystemLogger


@pytest.mark.logger
class TestSystemSetupColorConsoleSystemLogger:
    """
    Test all logging for system setup stage
    """

    def test_system_setup_start_on_normal(self, capsys, normal_configuration):
        """
        GIVEN normal_configuration
        WHEN system_setup_start
        THEN no output
        """
        system_logger = ColorConsoleSystemLogger(config=normal_configuration)

        system_logger.system_setup_start()

        captured = capsys.readouterr()
        assert captured.out == ''

    def test_system_setup_start_on_debug(self, capsys, debug_configuration):
        """
        GIVEN debug_configuration
        WHEN system_setup_start
        THEN no output
        """
        system_logger = ColorConsoleSystemLogger(config=debug_configuration)

        system_logger.system_setup_start()

        captured = capsys.readouterr()
        assert captured.out == ''

    def test_system_setup_start_on_trace(self, capsys, trace_configuration):
        """
        GIVEN trace_configuration
        WHEN system_setup_start
        THEN output
        """
        system_logger = ColorConsoleSystemLogger(config=trace_configuration)

        system_logger.system_setup_start()

        captured = capsys.readouterr()
        assert 'SETUP : start' in captured.out

    def test_system_setup_completed_on_normal(self, capsys, normal_configuration):
        """
        GIVEN normal_configuration
        WHEN system_setup_completed
        THEN no output
        """
        system_logger = ColorConsoleSystemLogger(config=normal_configuration)

        system_logger.system_setup_completed()

        captured = capsys.readouterr()
        assert captured.out == ''

    def test_system_setup_completed_on_debug(self, capsys, debug_configuration):
        """
        GIVEN normal_configuration
        WHEN system_setup_completed
        THEN not output
        """
        system_logger = ColorConsoleSystemLogger(config=debug_configuration)

        system_logger.system_setup_completed()

        captured = capsys.readouterr()
        assert captured.out == ''

    def test_system_setup_completed_on_trace(self, capsys, trace_configuration):
        """
        GIVEN trace_configuration
        WHEN system_setup_completed
        THEN output
        """
        system_logger = ColorConsoleSystemLogger(config=trace_configuration)

        system_logger.system_setup_completed()

        captured = capsys.readouterr()
        assert 'SETUP : completed' in captured.out
