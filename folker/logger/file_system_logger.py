from folker.parameters import is_debug, is_trace
from folker.logger.logger import SystemLogger, FileLogger


class FileSystemLogger(SystemLogger, FileLogger):

    def __init__(self, file_name: str) -> None:
        super().__init__(file_name)

    # Setup
    def loading_profile_files(self):
        if is_debug():
            self._log('Loading profile files')

    def loading_template_files(self):
        if is_debug():
            self._log('Loading template files')

    def loading_test_files(self):
        if is_debug():
            self._log('Loading test files')

    def loading_file(self, filename):
        if is_trace():
            self._log('File: {filename}'.format(filename=filename))

    def loading_file_error(self, file_name: str, exception: Exception):
        self._log('Error loading file {}: {}'.format(file_name, str(exception)))

    def loading_files_completed(self, files):
        if is_debug():
            self._log('Loaded files: [')
            for file in files:
                self._log('\t{}'.format(file))
            self._log(']'.format(files))

    # Protos
    def loading_proto_files(self):
        if is_debug():
            self._log('Loading proto files')

    def loading_proto_file(self, filename):
        if is_trace():
            self._log('Proto file: {filename}'.format(filename=filename))

    def loading_proto_file_skipped(self, filename):
        if is_trace():
            self._log('Skipped Proto file: {filename}'.format(filename=filename))

    def loading_proto_file_error(self, file_name: str, proto_command: str, exception: Exception):
        self._log('Error loading proto file {} [{}]: {}'.format(file_name,
                                                                proto_command,
                                                                str(exception)))

    def loading_proto_files_completed(self, files):
        if is_debug():
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

        self._write_to_file()
