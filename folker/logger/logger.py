from abc import ABC
from enum import Enum, auto


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
    TEST_INFO = auto()
    TEST_DEBUG = auto()
    TEST_SUCCESS = auto()
    TEST_FAILURE = auto()
    TEST_FAILURE_DETAILS = auto()
    STAGE_INFO = auto()
    STAGE_SKIP = auto()
    ACTION_DEBUG = auto()
    ACTION_TRACE = auto()
    ACTION_WARN = auto()
    ACTION_ERROR = auto()
    ACTION_PRINT = auto()
    ACTION_LOG_PRINT = auto()
    ACTION_ASSERTION_SUCCESS = auto()
    ACTION_ASSERTION_FAIL = auto()
    ACTION_ASSERTION_ERROR = auto()
    ACTION_ASSERTION_REPORT_OK = auto()
    ACTION_ASSERTION_REPORT_FAIL = auto()


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


class ConsoleColor(Enum):
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
        LogEntryType.BLANK: ConsoleColor.DEFAULT,

        LogEntryType.SYSTEM_INFO: ConsoleColor.HIGH_WHITE,
        LogEntryType.SYSTEM_DEBUG: ConsoleColor.WHITE,
        LogEntryType.SYSTEM_TRACE: ConsoleColor.GREY,
        LogEntryType.SYSTEM_TRACE_SKIPPED: ConsoleColor.GREY,
        LogEntryType.SYSTEM_TRACE_OK: ConsoleColor.GREEN,
        LogEntryType.SYSTEM_TRACE_WARN: ConsoleColor.YELLOW,
        LogEntryType.SYSTEM_TRACE_FAIL: ConsoleColor.RED,

        LogEntryType.REPORT_INFO: ConsoleColor.HIGH_WHITE,
        LogEntryType.REPORT_FAILURE: ConsoleColor.HIGH_RED,
        LogEntryType.REPORT_FAILURE_DEBUG: ConsoleColor.RED,
        LogEntryType.REPORT_SUCCESS: ConsoleColor.HIGH_GREEN,
        LogEntryType.REPORT_SUCCESS_DEBUG: ConsoleColor.GREEN,

        LogEntryType.TEST_INFO: ConsoleColor.HIGH_CYAN,
        LogEntryType.TEST_DEBUG: ConsoleColor.BLUE,
        LogEntryType.TEST_SUCCESS: ConsoleColor.HIGH_GREEN,
        LogEntryType.TEST_FAILURE: ConsoleColor.HIGH_RED,
        LogEntryType.TEST_FAILURE_DETAILS: ConsoleColor.RED,
        LogEntryType.STAGE_INFO: ConsoleColor.HIGH_YELLOW,
        LogEntryType.STAGE_SKIP: ConsoleColor.YELLOW,
        LogEntryType.ACTION_DEBUG: ConsoleColor.PINK,
        LogEntryType.ACTION_TRACE: ConsoleColor.GREY,
        LogEntryType.ACTION_WARN: ConsoleColor.YELLOW,
        LogEntryType.ACTION_ERROR: ConsoleColor.HIGH_RED,
        LogEntryType.ACTION_PRINT: ConsoleColor.HIGH_CYAN,
        LogEntryType.ACTION_LOG_PRINT: ConsoleColor.HIGH_WHITE,
        LogEntryType.ACTION_ASSERTION_SUCCESS: ConsoleColor.GREEN,
        LogEntryType.ACTION_ASSERTION_FAIL: ConsoleColor.RED,
        LogEntryType.ACTION_ASSERTION_ERROR: ConsoleColor.HIGH_RED,
        LogEntryType.ACTION_ASSERTION_REPORT_OK: ConsoleColor.CYAN,
        LogEntryType.ACTION_ASSERTION_REPORT_FAIL: ConsoleColor.HIGH_RED,
    }
