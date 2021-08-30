from abc import ABC, abstractmethod

from folker.model import Context
from folker.model.error import SourceException
from folker.parameters import Configuration


class ColorLogger(ABC):
    COLOR_DEFAULT = '\033[0m'

    COLOR_BLACK = '\033[0;30m'
    COLOR_RED = '\033[0;31m'
    COLOR_GREEN = '\033[0;32m'
    COLOR_GREEN = '\033[0;32m'
    COLOR_YELLOW = '\033[0;33m'
    COLOR_BLUE = '\033[0;34m'
    COLOR_PINK = '\033[0;35m'
    COLOR_CYAN = '\033[0;36m'
    COLOR_WHITE = '\033[0;37m'
    COLOR_GREY = '\033[0;38m'

    COLOR_HIGH_BLACK = '\033[0;97m'
    COLOR_HIGH_RED = '\033[0;91m'
    COLOR_HIGH_GREEN = '\033[0;92m'
    COLOR_HIGH_YELLOW = '\033[0;93m'
    COLOR_HIGH_BLUE = '\033[0;94m'
    COLOR_HIGH_PINK = '\033[0;95m'
    COLOR_HIGH_CYAN = '\033[0;96m'
    COLOR_HIGH_WHITE = '\033[0;99m'

    def _log_color(self, color, text, end=None) -> str:
        if end is not None:
            return '{}{}{}{}'.format(color, text, self.COLOR_DEFAULT, end)
        else:
            return '{}{}{}'.format(color, text, self.COLOR_DEFAULT)


class FileLogger(ABC):
    file_name: str
    report: [str]
    current_index = 0

    def __init__(self, config: Configuration) -> None:
        self.file_name = config.log_file
        self.report = []
        super().__init__()

    # Util
    def _delayed_log(self, text, end=None):
        self.report.append((text, end))

    def _log(self, text, end=None):
        self.report.append((text, end))
        self._write_to_file()

    def _write_to_file(self):
        f = open(self.file_name, 'a+')
        for report_entry, report_end in self.report:
            print(report_entry, end=report_end, file=f)
        f.close()
        self.report = []


class SystemLogger(ABC):
    debug: bool
    trace: bool

    def __init__(self, config: Configuration) -> None:
        self.debug = config.debug_mode
        self.trace = config.trace_mode

    # Setup
    @abstractmethod
    def system_setup_start(self):
        pass

    @abstractmethod
    def system_setup_completed(self):
        pass


class TestLogger(ABC):
    debug: bool
    trace: bool

    def __init__(self, config: Configuration) -> None:
        self.debug = config.debug_mode
        self.trace = config.trace_mode

    # Test
    @abstractmethod
    def test_start(self, test_name: str, test_description: str = None): pass

    @abstractmethod
    def test_finish(self): pass

    @abstractmethod
    def test_finish_error(self, e: SourceException): pass

    # Stage
    @abstractmethod
    def stage_start(self, stage_name: str, context: Context): pass

    @abstractmethod
    def stage_skip(self, stage_name: str, context: Context): pass

    # Action
    @abstractmethod
    def action_prelude(self, action: dict, context: Context): pass

    @abstractmethod
    def action_conclusion(self, action: dict, context: Context): pass

    @abstractmethod
    def message(self, message): pass

    @abstractmethod
    def action_error(self, message): pass

    @abstractmethod
    def action_warn(self, message): pass

    @abstractmethod
    def action_debug(self, message): pass

    # Assertions
    @abstractmethod
    def assertion_success(self, assertion: str): pass

    @abstractmethod
    def assertion_fail(self, assertion: str, variables: dict): pass

    @abstractmethod
    def assertion_error(self, assertion: str, exception: Exception = None): pass

    @abstractmethod
    def assert_test_result(self, total, success, failures): pass

    # Log
    def log_text(self, log: str): pass
