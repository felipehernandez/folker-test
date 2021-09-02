from abc import ABC, abstractmethod
from typing import List, Set

from folker.logger.logger import LogEntry, LogEntryType, ColorLogger, ConsoleColor
from folker.parameters import Configuration


class SystemLogger(ABC):
    DELIMITER_0 = '#' * 100
    DELIMITER_1 = '-' * 100
    DELIMITER_2 = '.' * 100

    debug: bool
    trace: bool
    log_file: str

    report: List[LogEntry]

    def __init__(self, config: Configuration) -> None:
        self.debug = config.debug_mode
        self.trace = config.trace_mode
        self.log_file = config.log_file
        self.report = []

    @abstractmethod
    def _log(self):
        pass

    # System setup
    def system_setup_start(self):
        if self.debug:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_INFO, text=self.DELIMITER_0))
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_INFO, text='SYSTEM SETUP : start'))
        self._log()

    def loading_proto_files(self):
        if self.debug:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_INFO, text=self.DELIMITER_1))
            self.report.append(
                LogEntry(type=LogEntryType.SYSTEM_DEBUG,
                         text='Proto files : generating sources'))
        self._log()

    def loading_file_skipped(self, filename):
        if self.trace:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_TRACE,
                                        text=f'\t{filename} ',
                                        end=''))
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_TRACE_SKIPPED, text='SKIP'))

    def loading_file_ok(self, filename):
        if self.trace:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_TRACE,
                                        text=f'\t{filename} ',
                                        end=''))
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_TRACE_OK, text='OK'))

    def loading_file_error(self, filename, e):
        if self.trace:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_TRACE,
                                        text=f'\t{filename} ',
                                        end=''))
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_TRACE_FAIL,
                                        text=f'ERROR - {e}'))

    def loading_proto_files_completed(self, processed_files):
        # if self.debug:
        #     text = 'Proto files : source generation completed' if self.trace else 'Proto files processed'
        #     self.report.append(LogEntry(type=LogEntryType.SYSTEM_DEBUG, text=text))
        #     self.report.append(LogEntry(type=LogEntryType.SYSTEM_DEBUG, text='['))
        #     for file in processed_files:
        #         self.report.append(
        #             LogEntry(type=LogEntryType.SYSTEM_DEBUG, text='\t{}'.format(file)))
        #     self.report.append(LogEntry(type=LogEntryType.SYSTEM_DEBUG, text=']'))
        self._log()

    def system_setup_completed(self):
        if self.debug:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_INFO, text=self.DELIMITER_1))
            self.report.append(
                LogEntry(type=LogEntryType.SYSTEM_INFO, text='SYSTEM SETUP : completed'))
        self._log()

    # Execution setup
    def execution_setup_start(self):
        if self.debug:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_INFO, text=self.DELIMITER_0))
            self.report.append(
                LogEntry(type=LogEntryType.SYSTEM_INFO, text='Execution SETUP : start'))
        self._log()

    def loading_profile_files(self):
        if self.debug:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_INFO, text=self.DELIMITER_1))
            self.report.append(
                LogEntry(type=LogEntryType.SYSTEM_DEBUG, text='Profile files : loading'))
        self._log()

    def loaded_profile(self, profile_name):
        if self.debug:
            self.report.append(
                LogEntry(type=LogEntryType.SYSTEM_DEBUG, text='Loaded profile: ', end=''))
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_TRACE_OK, text=profile_name))

    def loading_files_completed(self, processed_files):
        # if self.trace:
        #     self.report.append(LogEntry(type=LogEntryType.SYSTEM_DEBUG, text='Processed files'))
        #     self.report.append(LogEntry(type=LogEntryType.SYSTEM_DEBUG, text='['))
        #     for file in processed_files:
        #         self.report.append(
        #             LogEntry(type=LogEntryType.SYSTEM_DEBUG, text='\t{}'.format(file)))
        #     self.report.append(LogEntry(type=LogEntryType.SYSTEM_DEBUG, text=']'))
        self._log()

    def loading_template_files(self):
        if self.debug:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_INFO, text=self.DELIMITER_1))
            self.report.append(
                LogEntry(type=LogEntryType.SYSTEM_DEBUG, text='Template files : loading'))
        self._log()

    def loaded_template(self, template_id):
        if self.debug:
            self.report.append(
                LogEntry(type=LogEntryType.SYSTEM_DEBUG, text='Loaded template: ', end=''))
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_TRACE_OK, text=template_id))
        self._log()

    def loaded_template_stage(self, stage_id):
        if self.debug:
            self.report.append(
                LogEntry(type=LogEntryType.SYSTEM_DEBUG, text='\tStage: ', end=''))
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_TRACE_OK, text=stage_id))
        self._log()

    def loading_test_files(self):
        if self.debug:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_INFO, text=self.DELIMITER_1))
            self.report.append(
                LogEntry(type=LogEntryType.SYSTEM_DEBUG, text='Test files : loading'))
        self._log()

    def filtering_tests(self):
        if self.debug:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_INFO, text=self.DELIMITER_1))
            self.report.append(
                LogEntry(type=LogEntryType.SYSTEM_DEBUG, text='Test files : filtering'))
        self._log()

    def test_filter_out_skip_tags(self, test_name: str, matching_skip_tags: Set[str]):
        if self.debug:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_DEBUG,
                                        text=f'\t{test_name} ',
                                        end=''))
            self.report.append(
                LogEntry(type=LogEntryType.SYSTEM_TRACE_WARN,
                         text=f'SKIP - Skip tag matching : {matching_skip_tags}'))
        self._log()

    def test_filter_in_execution_tags(self, test_name: str, matching_execute_tags: Set[str]):
        if self.debug:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_DEBUG,
                                        text=f'\t{test_name} ',
                                        end=''))
            self.report.append(
                LogEntry(type=LogEntryType.SYSTEM_TRACE_OK,
                         text=f'EXECUTE - Execute tag matching : {matching_execute_tags}'))
        self._log()

    def test_filter_out_execution_tags(self, test_name: str):
        if self.debug:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_DEBUG,
                                        text=f'\t{test_name} ',
                                        end=''))
            self.report.append(
                LogEntry(type=LogEntryType.SYSTEM_TRACE_WARN,
                         text='SKIP - No execute tag matching'))
        self._log()

    def test_filter_in_skip_tags(self, test_name: str):
        if self.debug:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_DEBUG,
                                        text=f'\t{test_name} ',
                                        end=''))
            self.report.append(
                LogEntry(type=LogEntryType.SYSTEM_TRACE_OK,
                         text='EXECUTE - No skip tag matching'))
        self._log()

    # Report
    def execution_report(self,
                         total: int,
                         successes: List[str],
                         failures: List[str],
                         expected: int):
        self.report.append(LogEntry(type=LogEntryType.REPORT_INFO, text=self.DELIMITER_0))
        self.report.append(LogEntry(type=LogEntryType.REPORT_INFO, text='RESULTS:'))

        if len(failures) > 0:
            self._log_report_failures(failures)
        if len(successes) > 0:
            self._log_report_successes(successes)

        self.report.append(LogEntry(type=LogEntryType.REPORT_INFO,
                                    text=f'Total: {total}',
                                    end=''))
        if expected and int(expected) != total:
            self.report.append(LogEntry(type=LogEntryType.REPORT_FAILURE,
                                        text=f' - Expected: {total}'))
        else:
            self.report.append(LogEntry.blank_line())
        self._log()

    def _log_report_failures(self, failures):
        self.report.append(LogEntry(type=LogEntryType.REPORT_FAILURE,
                                    text=f'Failures: ({len(failures)})'))
        if self.debug:
            for failure in failures:
                self.report.append(LogEntry(type=LogEntryType.REPORT_FAILURE_DEBUG,
                                            text=f'\t{failure}'))

    def _log_report_successes(self, successes):
        self.report.append(LogEntry(type=LogEntryType.REPORT_SUCCESS,
                                    text=f'Success: ({len(successes)})'))
        if self.debug:
            for success in successes:
                self.report.append(LogEntry(type=LogEntryType.REPORT_SUCCESS_DEBUG,
                                            text=f'\t{success}'))


class PlainConsoleSystemLogger(SystemLogger):
    def _log(self):
        for log_entry in self.report:
            print(log_entry.text, end=log_entry.end)
        self.report = []


class ColorConsoleSystemLogger(SystemLogger, ColorLogger):
    def _log(self):
        for log_entry in self.report:
            prefix_color = self.COLOR_MAPPINGS.get(log_entry.type, ConsoleColor.DEFAULT).code()
            text = f'{prefix_color}{log_entry.text}{ConsoleColor.DEFAULT.code()}'
            print(text, end=log_entry.end)
        self.report = []


class PlainFileSystemLogger(SystemLogger):
    def _log(self):
        f = open(self.log_file, 'a+')
        for log_entry in self.report:
            print(log_entry.text, end=log_entry.end, file=f)
        f.close()
        self.report = []
