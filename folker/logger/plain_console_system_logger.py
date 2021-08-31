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

    # Setup
    def loading_profile_files(self):
        if self.debug:
            self._log('Loading profile files')

    def loading_template_files(self):
        if self.debug:
            self._log('Loading template files')

    def loading_test_files(self):
        if self.debug:
            self._log('Loading test files')

    def loading_file(self, filename):
        if self.trace:
            self._log('File: {filename}'.format(filename=filename))

    def loading_file_error(self, file_name: str, exception: Exception):
        self._log('Error loading file {}: {}'.format(file_name, str(exception)))

    def loading_files_completed(self, files):
        if self.debug:
            self._log('Loaded files: [')
            for file in files:
                self._log('\t{}'.format(file))
            self._log(']'.format(files))

    # Protos
    def loading_proto_files(self):
        if self.debug:
            self._log('Loading proto files')

    def loading_proto_file(self, filename):
        if self.trace:
            self._log('Proto file: {filename}'.format(filename=filename))

    def loading_proto_file_skipped(self, filename):
        if self.trace:
            self._log('Skipped Proto file: {filename}'.format(filename=filename))

    def loading_proto_file_error(self, file_name: str, proto_command: str, exception: Exception):
        self._log('Error loading proto file {} [{}]: {}'.format(file_name,
                                                                proto_command,
                                                                str(exception)))

    def loading_proto_files_completed(self, files):
        if self.debug:
            self._log('Loaded proto files: [')
            for file in files:
                self._log('\t{}'.format(file))
            self._log(']'.format(files))

    # Wrap up
    def assert_execution_result(self, total, success, failures):
        self._log('\n' + '#' * 100)
        self._log('RESULTS:')
        self._log('Tests: Success[ {} ] Fail[ {} ] Total[ {} ]'.format(len(success),
                                                                       len(failures),
                                                                       total))

        for passed in success:
            self._log('\t{}'.format(passed))
        for fail in failures:
            self._log('\t{}'.format(fail))

    def assert_number_tests_executed(self, expected: int, executed: int):
        if expected and int(expected) != executed:
            self._log('Expected: {} - Executed: {}'.format(expected, executed))

    # Util
    def _log(self, text, end=None):
        print(text, end=end)
