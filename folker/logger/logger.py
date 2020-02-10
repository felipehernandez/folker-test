from abc import ABC, abstractmethod

from folker.model.error.error import SourceException


class ColorLogger:
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


class SystemLogger(ABC):
    # Setup
    @abstractmethod
    def loading_template_files(self): pass

    @abstractmethod
    def loading_test_files(self): pass

    @abstractmethod
    def loading_file(self, filename): pass

    @abstractmethod
    def loading_file_error(self, file_name: str, exception: Exception): pass

    @abstractmethod
    def loading_files_completed(self, files): pass

    # Wrap up
    @abstractmethod
    def assert_execution_result(self, total, success, failures): pass


class TestLogger(ABC):

    # Test
    @abstractmethod
    def test_start(self, test_name: str, test_description: str = None): pass

    @abstractmethod
    def test_finish(self): pass

    @abstractmethod
    def test_finish_error(self, e: SourceException): pass

    # Stage
    @abstractmethod
    def stage_start(self, stage_name: str, test_context: dict): pass

    # Action
    @abstractmethod
    def action_executed(self, stage_context: dict): pass

    @abstractmethod
    def message(self, message): pass

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
