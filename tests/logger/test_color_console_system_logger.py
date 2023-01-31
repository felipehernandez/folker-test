import pytest

from folker.logger.system_logger import ColorConsoleSystemLogger, ConsoleColor


@pytest.mark.logger
class TestVisualColorConsoleSystemLogger:
    def full_log(self, logger):
        logger.system_setup_start()
        logger.loading_proto_files()
        logger.loading_file_skipped('a_skipped_file')
        logger.loading_file_ok('an_ok_file')
        logger.loading_file_error('an_error_file', 'error')
        logger.loading_proto_files_completed(['a_file', 'another_file'])
        logger.system_setup_completed()

        logger.execution_setup_start()

        logger.loading_profile_files()
        logger.loading_file_ok('an_ok_file')
        logger.loading_file_error('an_error_file', 'error')
        logger.loading_files_completed(['a_file', 'another_file'])

        logger.loaded_profile('a_profile')
        logger.loading_template_files()
        logger.loading_file_ok('an_ok_file')
        logger.loading_file_error('an_error_file', 'error')
        logger.loading_files_completed(['a_file', 'another_file'])

        logger.loaded_template('a_template_id')
        logger.loaded_template_stage('a_template_stage_id')
        logger.loaded_template('another_template_id')
        logger.loaded_template_stage('another_template_stage_id')
        logger.loading_files_completed(['a_file', 'another_file'])

        logger.loading_test_files()
        logger.loading_file_ok('an_ok_file')
        logger.loading_file_error('an_error_file', 'error')
        logger.loading_files_completed(['a_file', 'another_file'])

        logger.filtering_tests()
        logger.test_filter_out_skip_tags('a_test', {'skip_tag_1', 'skip_tag_2'})
        logger.test_filter_in_execution_tags('a_test', {'skip_tag_1', 'skip_tag_2'})
        logger.test_filter_out_execution_tags('a_test', ['missing_tag'])
        logger.test_filter_in_skip_tags('a_test')

        logger.execution_report(3, ['a_test', 'another_test'], ['yet_another_test'], None)
        logger.execution_report(3, ['a_test', 'another_test'], ['yet_another_test'], 2)

    def test_full_log_normal(self, normal_configuration):
        system_logger = ColorConsoleSystemLogger(config=normal_configuration)
        self.full_log(system_logger)

    def test_full_log_debug(self, debug_configuration):
        system_logger = ColorConsoleSystemLogger(config=debug_configuration)
        self.full_log(system_logger)

    def test_full_log_trace(self, trace_configuration):
        system_logger = ColorConsoleSystemLogger(config=trace_configuration)
        self.full_log(system_logger)


@pytest.mark.logger
class TestNormalSystemStartupColorConsoleSystemLogger:
    """
    Test all logging for system setup stage on normal mode
    """

    def test_system_setup_start(self, capsys, normal_configuration):
        system_logger = ColorConsoleSystemLogger(config=normal_configuration)

        system_logger.system_setup_start()

        captured = capsys.readouterr()
        assert captured.out == ''


@pytest.mark.logger
class TestDebugSystemStartupColorConsoleSystemLogger:
    """
    Test all logging for system setup stage on debug mode
    """

    def test_system_setup_start(self, capsys, debug_configuration):
        system_logger = ColorConsoleSystemLogger(config=debug_configuration)

        system_logger.system_setup_start()

        captured = capsys.readouterr()
        open_color = ConsoleColor.HIGH_WHITE.code()
        close_color = ConsoleColor.DEFAULT.code()
        expected_output = (
            f'{open_color}{"#" * 100}{close_color}\n'
            f'{open_color}SYSTEM SETUP : start{close_color}\n'
        )
        assert captured.out == expected_output


@pytest.mark.logger
class TestTraceSystemStartupColorConsoleSystemLogger:
    """
    Test all logging for system setup stage on trace mode
    """

    def test_system_setup_start(self, capsys, trace_configuration):
        system_logger = ColorConsoleSystemLogger(config=trace_configuration)

        system_logger.system_setup_start()

        captured = capsys.readouterr()
        open_color = ConsoleColor.HIGH_WHITE.code()
        close_color = ConsoleColor.DEFAULT.code()
        expected_output = (
            f'{open_color}{"#" * 100}{close_color}\n'
            f'{open_color}SYSTEM SETUP : start{close_color}\n'
        )
        assert captured.out == expected_output
