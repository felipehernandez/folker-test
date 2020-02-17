import json

from folker import is_debug, is_trace
from folker.logger.logger import TestLogger, FileLogger
from folker.model.error.error import SourceException


class FileSequentialTestLogger(TestLogger, FileLogger):

    def __init__(self, file_name: str) -> None:
        super().__init__(file_name)

    # Test
    def test_start(self, test_name: str, test_description: str = None):
        self._log('TEST: ', '\t')
        self._log(test_name)

        if test_description:
            self._log(test_description)

    def test_finish(self):
        self._log('Test successful')
        self._write_to_file()

    def test_finish_error(self, e: SourceException):
        self._log('Test successful')
        self._log(e)
        self._write_to_file()

    # Stage
    def stage_start(self, stage_name: str, test_context: dict):
        self._log('Stage: {name}'.format(name=stage_name))

        if is_trace():
            self._log('CONTEXT: {}'.format(test_context))

    # Action
    def action_executed(self, stage_context: dict):
        if is_trace():
            self._log('STAGE CONTEXT: {}'.format(stage_context))

    def message(self, message):
        self._log(message)

    def action_debug(self, message):
        if is_debug():
            self._log(message)

    def action_error(self, message):
        self._log(message)

    # Log
    def log_text(self, log: str):
        self._log(log)

    # Assertions
    def assertion_success(self, assertion: str):
        if is_debug():
            self._log('\t{}'.format(assertion))

    def assertion_fail(self, assertion: str, variables: dict):
        self._log('\t{}'.format(assertion))
        self._log(json.dumps(variables))

    def assertion_error(self, assertion: str, exception: Exception = None):
        self._log('\t{} - {}'.format(assertion, exception))

    def assert_test_result(self, total, success, failures):
        if success is not total:
            self._log('\tAsserts: Success[ {} ] Fail[ {} ] Total[ {} ]'.format(success, failures, total))
        elif is_debug():
            self._log('\tAsserts: Success[ {} ] Fail[ {} ] Total[ {} ]'.format(success, failures, total))
