from folker.logger import SystemLogger
from folker.parameters import Configuration


class PlainConsoleSystemLogger(SystemLogger):

    def __init__(self, config: Configuration) -> None:
        SystemLogger.__init__(self, config)

    def system_setup_start(self):
        if self.trace:
            self._log('SETUP : start')

    def system_setup_completed(self):
        if self.trace:
            self._log('SETUP : completed')

    # Util
    def _log(self, text, end=None):
        print(text, end=end)
