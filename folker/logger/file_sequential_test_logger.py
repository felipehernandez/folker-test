
from folker.logger.file_test_logger import FileTestLogger


class FileSequentialTestLogger(FileTestLogger):

    def __init__(self, file_name: str) -> None:
        super().__init__(file_name)

    def assertion_fail(self, assertion: str, variables: dict):
        self._log('\t{}'.format(assertion))
        self._log(json.dumps(variables))

    def assertion_error(self, assertion: str, exception: Exception = None):
        self._log('\t{} - {}'.format(assertion, exception))

    def assert_test_result(self, total, success, failures):
        if success is not total:
            self._log('\tAsserts: Success[ {} ] Fail[ {} ] Total[ {} ]'.format(success,
                                                                               failures,
                                                                               total))
        elif is_debug():
            self._log('\tAsserts: Success[ {} ] Fail[ {} ] Total[ {} ]'.format(success,
                                                                               failures,
                                                                               total))
            