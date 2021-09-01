from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List, Set

from folker.parameters import Configuration


class LogEntryType(Enum):
    BLANK = auto()
    SYSTEM_INFO = auto()
    SYSTEM_DEBUG = auto()
    SYSTEM_TRACE = auto()
    SYSTEM_TRACE_SKIPPED = auto()
    SYSTEM_TRACE_OK = auto()
    SYSTEM_TRACE_WARN = auto()
    SYSTEM_TRACE_FAIL = auto()
    REPORT_INFO = auto()
    REPORT_FAILURE = auto()
    REPORT_FAILURE_DEBUG = auto()
    REPORT_SUCCESS = auto()
    REPORT_SUCCESS_DEBUG = auto()


class LogEntry:
    type: LogEntryType
    text: str
    end: str

    def __init__(self, type: LogEntryType, text: str, end: str = None) -> None:
        self.type = type
        self.text = text
        self.end = end

    @classmethod
    def blank_line(cls):
        return LogEntry(type=LogEntryType.BLANK, text='', end=None)


class Color(Enum):
    DEFAULT = auto()

    BLACK = auto()
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    BLUE = auto()
    PINK = auto()
    CYAN = auto()
    WHITE = auto()
    GREY = auto()

    HIGH_WHITE = auto()
    HIGH_RED = auto()
    HIGH_GREEN = auto()
    HIGH_YELLOW = auto()
    HIGH_BLUE = auto()
    HIGH_PINK = auto()
    HIGH_CYAN = auto()
    HIGH_GREY = auto()

    def code(self):
        return {
            self.DEFAULT: '\033[0m',

            self.BLACK: '\033[0;30m',
            self.RED: '\033[0;31m',
            self.GREEN: '\033[0;32m',
            self.YELLOW: '\033[0;33m',
            self.BLUE: '\033[0;34m',
            self.PINK: '\033[0;35m',
            self.CYAN: '\033[0;36m',
            self.WHITE: '\033[0;38m',
            self.GREY: '\033[0;37m',

            self.HIGH_GREY: '\033[0;99m',
            self.HIGH_WHITE: '\033[0;97m',
            self.HIGH_RED: '\033[0;91m',
            self.HIGH_GREEN: '\033[0;92m',
            self.HIGH_YELLOW: '\033[0;93m',
            self.HIGH_BLUE: '\033[0;94m',
            self.HIGH_PINK: '\033[0;95m',
            self.HIGH_CYAN: '\033[0;96m',
        }.get(self, '\033[0m')


class ColorLogger(ABC):
    COLOR_MAPPINGS = {
        LogEntryType.BLANK: Color.DEFAULT,
        LogEntryType.SYSTEM_INFO: Color.HIGH_WHITE,
        LogEntryType.SYSTEM_DEBUG: Color.WHITE,
        LogEntryType.SYSTEM_TRACE: Color.GREY,
        LogEntryType.SYSTEM_TRACE_SKIPPED: Color.GREY,
        LogEntryType.SYSTEM_TRACE_OK: Color.GREEN,
        LogEntryType.SYSTEM_TRACE_WARN: Color.YELLOW,
        LogEntryType.SYSTEM_TRACE_FAIL: Color.RED,

        LogEntryType.REPORT_INFO: Color.HIGH_WHITE,
        LogEntryType.REPORT_FAILURE: Color.HIGH_RED,
        LogEntryType.REPORT_FAILURE_DEBUG: Color.RED,
        LogEntryType.REPORT_SUCCESS: Color.HIGH_GREEN,
        LogEntryType.REPORT_SUCCESS_DEBUG: Color.GREEN,
    }


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
                                        text='\t{} '.format(filename),
                                        end=''))
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_TRACE_SKIPPED, text='SKIP'))

    def loading_file_ok(self, filename):
        if self.trace:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_TRACE,
                                        text='\t{} '.format(filename),
                                        end=''))
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_TRACE_OK, text='OK'))

    def loading_file_error(self, filename, e):
        if self.trace:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_TRACE,
                                        text='\t{} '.format(filename),
                                        end=''))
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_TRACE_FAIL,
                                        text='{} - {}'.format('ERROR', e)))

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
                                        text='\t{} '.format(test_name),
                                        end=''))
            self.report.append(
                LogEntry(type=LogEntryType.SYSTEM_TRACE_WARN,
                         text='SKIP - Skip tag matching : {}'.format(matching_skip_tags)))
        self._log()

    def test_filter_in_execution_tags(self, test_name: str, matching_execute_tags: Set[str]):
        if self.debug:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_DEBUG,
                                        text='\t{} '.format(test_name),
                                        end=''))
            self.report.append(
                LogEntry(type=LogEntryType.SYSTEM_TRACE_OK,
                         text='EXECUTE - Execute tag matching : {}'.format(matching_execute_tags)))
        self._log()

    def test_filter_out_execution_tags(self, test_name: str):
        if self.debug:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_DEBUG,
                                        text='\t{} '.format(test_name),
                                        end=''))
            self.report.append(
                LogEntry(type=LogEntryType.SYSTEM_TRACE_WARN,
                         text='SKIP - No execute tag matching'))
        self._log()

    def test_filter_in_skip_tags(self, test_name: str):
        if self.debug:
            self.report.append(LogEntry(type=LogEntryType.SYSTEM_DEBUG,
                                        text='\t{} '.format(test_name),
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
                                    text='Total: {}'.format(total),
                                    end=''))
        if expected and int(expected) != total:
            self.report.append(LogEntry(type=LogEntryType.REPORT_FAILURE,
                                        text=' - Expected: {}'.format(total)))
        else:
            self.report.append(LogEntry.blank_line())
        self._log()

    def _log_report_failures(self, failures):
        self.report.append(LogEntry(type=LogEntryType.REPORT_FAILURE,
                                    text='Failures: ({})'.format(len(failures))))
        if self.debug:
            for failure in failures:
                self.report.append(LogEntry(type=LogEntryType.REPORT_FAILURE_DEBUG,
                                            text='\t{}'.format(failure)))

    def _log_report_successes(self, successes):
        self.report.append(LogEntry(type=LogEntryType.REPORT_SUCCESS,
                                    text='Success: ({})'.format(len(successes))))
        if self.debug:
            for success in successes:
                self.report.append(LogEntry(type=LogEntryType.REPORT_SUCCESS_DEBUG,
                                            text='\t{}'.format(success)))


class PlainConsoleSystemLogger(SystemLogger):
    def _log(self):
        for log_entry in self.report:
            print(log_entry.text, end=log_entry.end)
        self.report = []


class ColorConsoleSystemLogger(SystemLogger, ColorLogger):
    def _log(self):
        for log_entry in self.report:
            text = '{}{}{}'.format(self.COLOR_MAPPINGS.get(log_entry.type, Color.DEFAULT).code(),
                                   log_entry.text,
                                   Color.DEFAULT.code())
            print(text, end=log_entry.end)
        self.report = []


class PlainFileSystemLogger(SystemLogger):
    def _log(self):
        f = open(self.log_file, 'a+')
        for log_entry in self.report:
            print(log_entry.text, end=log_entry.end, file=f)
        f.close()
        self.report = []
