from folker import trace, debug
from folker.logger.logger import ColorLogger, SystemLogger


class ConsoleSystemLogger(SystemLogger, ColorLogger):

    # Setup
    def loading_template_files(self):
        if debug or trace:
            self._log(self.COLOR_HIGH_CYAN, 'Loading template files')

    def loading_test_files(self):
        if debug or trace:
            self._log(self.COLOR_HIGH_CYAN, 'Loading test files')

    def loading_file(self, filename):
        if trace:
            self._log(self.COLOR_HIGH_YELLOW, 'File: {filename}'.format(filename=filename))

    def loading_file_error(self, file_name: str, exception: Exception):
        self._log(self.COLOR_HIGH_RED, 'Error loading file {}: {}'.format(file_name, str(exception)))

    def loading_files_completed(self, files):
        if debug or trace:
            self._log(self.COLOR_WHITE, 'Loaded files: [')
            for file in files:
                self._log(self.COLOR_WHITE, '\t{}'.format(file))
            self._log(self.COLOR_WHITE, ']'.format(files))

    # Wrap up
    def assert_execution_result(self, total, success, failures):
        self._log(self.COLOR_HIGH_CYAN, '\n#################################################################################################')
        self._log(self.COLOR_HIGH_CYAN, 'RESULTS:')
        print_color = self.COLOR_HIGH_GREEN if len(success) is total else self.COLOR_HIGH_RED
        self._log(print_color, 'Tests: Success[ {} ] Fail[ {} ] Total[ {} ]'.format(len(success), len(failures), total))

        for passed in success:
            self._log(self.COLOR_GREEN, '\t{}'.format(passed))
        for fail in failures:
            self._log(self.COLOR_RED, '\t{}'.format(fail))

    # Util
    def _log(self, color, text, end=None):
        print(self._log_color(color, text, end))