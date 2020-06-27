from folker import is_debug, is_trace
from folker.logger.logger import ColorLogger, SystemLogger


class ConsoleSystemLogger(SystemLogger, ColorLogger):

    # Setup
    def loading_profile_files(self):
        if is_debug():
            self._log(self.COLOR_HIGH_CYAN, 'Loading profile files')

    def loading_template_files(self):
        if is_debug():
            self._log(self.COLOR_HIGH_CYAN, 'Loading template files')

    def loading_test_files(self):
        if is_debug():
            self._log(self.COLOR_HIGH_CYAN, 'Loading test files')

    def loading_file(self, filename):
        if is_trace():
            self._log(self.COLOR_HIGH_YELLOW, 'File: {filename}'.format(filename=filename))

    def loading_file_error(self, file_name: str, exception: Exception):
        self._log(self.COLOR_HIGH_RED, 'Error loading file {}: {}'.format(file_name, str(exception)))

    def loading_files_completed(self, files):
        if is_debug():
            self._log(self.COLOR_WHITE, 'Loaded files: [')
            for file in files:
                self._log(self.COLOR_WHITE, '\t{}'.format(file))
            self._log(self.COLOR_WHITE, ']'.format(files))

    # Protos
    def loading_proto_files(self):
        if is_debug():
            self._log(self.COLOR_HIGH_CYAN, 'Loading proto files')

    def loading_proto_file(self, filename):
        if is_trace():
            self._log(self.COLOR_HIGH_YELLOW, 'Proto file: {filename}'.format(filename=filename))

    def loading_proto_file_skipped(self, filename):
        if is_trace():
            self._log(self.COLOR_GREY, 'Skipped Proto file: {filename}'.format(filename=filename))

    def loading_proto_file_error(self, file_name: str, proto_command: str, exception: Exception):
        self._log(self.COLOR_HIGH_RED, 'Error loading proto file {} [{}]: {}'.format(file_name, proto_command, str(exception)))

    def loading_proto_files_completed(self, files):
        if is_debug():
            self._log(self.COLOR_WHITE, 'Loaded proto files: [')
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

    def assert_number_tests_executed(self, expected: int, executed: int):
        if expected != executed:
            self._log(self.COLOR_RED, 'Expected: {} - Executed: '.format(executed, expected))

    # Util
    def _log(self, color, text, end=None):
        print(self._log_color(color, text, end))
