import json

from folker import trace, debug
from folker.logger.logger import TestLogger, ColorLogger
from folker.model.error.error import SourceException


class ConsoleSequentialTestLogger(TestLogger, ColorLogger):

    # Test
    def test_start(self, test_name: str, test_description: str = None):
        self._log(self.COLOR_HIGH_CYAN, 'TEST: ', '\t')
        self._log(self.COLOR_HIGH_CYAN, test_name)

        if test_description:
            self._log(self.COLOR_BLUE, test_description)

    def test_finish(self):
        self._log(self.COLOR_GREEN, 'Test successful')

    def test_finish_error(self, e: SourceException):
        self._log(self.COLOR_RED, 'Test successful')
        self._log(self.COLOR_RED, e)

    # Stage
    def stage_start(self, stage_name: str, test_context: dict):
        self._log(self.COLOR_HIGH_YELLOW, 'Stage: {name}'.format(name=stage_name))

        if trace:
            self._log(self.COLOR_GREY, 'CONTEXT: {}'.format(test_context))

    # Action
    def action_executed(self, stage_context: dict):
        if trace:
            self._log(self.COLOR_GREY, 'STAGE CONTEXT: {}'.format(stage_context))

    # Log
    def log_text(self, log: str):
        self._log(self.COLOR_WHITE, log)

    # Assertions
    def assertion_success(self, assertion: str):
        if debug or trace:
            self._log(self.COLOR_GREEN, '\t{}'.format(assertion))

    def assertion_fail(self, assertion: str, variables: dict):
        self._log(self.COLOR_RED, '\t{}'.format(assertion))
        self._log(self.COLOR_RED, json.dumps(variables))

    def assertion_error(self, assertion: str, exception: Exception = None):
        self._log(self.COLOR_RED, '\t{} - {}'.format(assertion, exception))

    def assert_test_result(self, total, success, failures):
        if success is not total:
            self._log(self.COLOR_HIGH_RED, '\tAsserts: Success[ {} ] Fail[ {} ] Total[ {} ]'.format(success, failures, total))
        elif debug or trace:
            self._log(self.COLOR_CYAN, '\tAsserts: Success[ {} ] Fail[ {} ] Total[ {} ]'.format(success, failures, total))

    # Util
    def _log(self, color, text, end=None):
        print(self._log_color(color, text, end))
