from folker.logger.logger import SystemLogger, FileLogger
from folker.parameters import Configuration


class FileSystemLogger(SystemLogger, FileLogger):

    def __init__(self, config: Configuration) -> None:
        FileLogger.__init__(self, config)
        SystemLogger.__init__(self, config)

    # Setup
    def system_setup_start(self):
        if self.debug:
            self._log('SETUP : start')

    def system_setup_completed(self):
        if self.debug:
            self._log('SETUP : completed')
