from folker.logger.console_test_logger import ConsoleTestLogger
from folker.model.error import SourceException
from folker.parameters import Configuration


class ConsoleParallelTestLogger(ConsoleTestLogger):
    report: str

    def __init__(self, config: Configuration) -> None:
        super().__init__(config)
        self.report = ''

    # Test
    def test_finish(self):
        self._log(self.COLOR_GREEN, 'Test successful')
        print(self.report)
        self.report = ''

    def test_finish_error(self, e: SourceException):
        self._log(self.COLOR_RED, 'Test unsuccessful')
        self._log(self.COLOR_RED, e)
        print(self.report)
        self.report = ''

    # Util
    def _log(self, color, text, end=None):
        self.report += self._log_color(color, text, end) + '\n'
