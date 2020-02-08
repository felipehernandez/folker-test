from folker import trace, debug
from folker.logger.logger import SystemLogger


class FileSystemLogger(SystemLogger):
    file_name: str

    def __init__(self, file_name: str) -> None:
        super().__init__()
        self.file_name = file_name

    #
    # Setup
    #
    def loading_test_files(self):
        if debug or trace:
            self._log('Loading test files')

    def loading_file(self, filename):
        if trace:
            self._log('File: {filename}'.format(filename=filename))

    def loading_file_error(self, file_name: str, exception: Exception):
        self._log('Error loading file {}: {}'.format(file_name, str(exception)))

        def loading_files_completed(self, files):
            if debug or trace:
                self._log('Loaded files: [')
                for file in files:
                    self._log('\t{}'.format(file))
                self._log(']'.format(files))

    def loading_files_completed(self, files):
        if debug or trace:
            self._log('Loaded files: [')
            for file in files:
                self._log('\t{}'.format(file))
            self._log(']'.format(files))

    # Wrap up
    def assert_execution_result(self, total, success, failures):
        self._log('\n#################################################################################################')
        self._log('RESULTS:')
        self._log('Tests: Success[ {} ] Fail[ {} ] Total[ {} ]'.format(len(success), len(failures), total))

        for passed in success:
            self._log('\t{}'.format(passed))
        for fail in failures:
            self._log('\t{}'.format(fail))

    def _log(self, color, text, end=None):
        if end is not None:
            print('{}{}{}'.format(color, text, ), end=end)
        else:
            print('{}{}{}'.format(color, text, ))
