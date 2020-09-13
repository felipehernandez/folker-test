from folker.logger.console_test_logger import ConsoleTestLogger
from folker.model.error import SourceException


class ConsoleSequentialTestLogger(ConsoleTestLogger):

    # Test
    def test_finish(self):
        self._log(self.COLOR_GREEN, 'Test successful')

    def test_finish_error(self, e: SourceException):
        self._log(self.COLOR_RED, 'Test unsuccessful')
        self._log(self.COLOR_RED, e)

    # Util
    def _log(self, color, text, end=None):
        print(self._log_color(color, text, end))
