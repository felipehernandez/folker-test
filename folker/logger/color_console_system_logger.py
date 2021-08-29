from folker.logger import SystemLogger
from folker.logger.logger import ColorLogger
from folker.parameters import Configuration


class ColorConsoleSystemLogger(SystemLogger, ColorLogger):
    SYSTEM_COLOR = ColorLogger.COLOR_HIGH_CYAN

    def __init__(self, config: Configuration) -> None:
        ColorLogger.__init__(self, )
        SystemLogger.__init__(self, config)

    def system_setup_start(self):
        if self.trace:
            self._log(self.SYSTEM_COLOR, 'SETUP : start')

    def system_setup_completed(self):
        if self.trace:
            self._log(self.SYSTEM_COLOR, 'SETUP : completed')

    # Util
    def _log(self, color, text, end=None):
        print(self._log_color(color, text, end))
