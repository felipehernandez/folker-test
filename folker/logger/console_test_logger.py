import json
from enum import Enum

from folker import is_debug, is_trace
from folker.logger.logger import TestLogger, ColorLogger
from folker.model.context import Context
from folker.model.error.error import SourceException


class ConsoleTestLogger(TestLogger, ColorLogger):

    # Test
    def test_start(self, test_name: str, test_description: str = None):
        self._log(self.COLOR_HIGH_CYAN, 'TEST: ', '\t')
        self._log(self.COLOR_HIGH_CYAN, test_name)

        if test_description:
            self._log(self.COLOR_BLUE, test_description)

    def test_finish(self):
        self._log(self.COLOR_GREEN, 'Test successful')
        print(self.report)

    def test_finish_error(self, e: SourceException):
        self._log(self.COLOR_RED, 'Test unsuccessful')
        self._log(self.COLOR_RED, e)
        print(self.report)

    # Stage
    def stage_start(self, stage_name: str, context: Context):
        self._log(self.COLOR_HIGH_YELLOW, 'Stage: {name}'.format(name=stage_name))

        if is_trace():
            self._log(self.COLOR_GREY, 'TEST CONTEXT: {}'.format(context.test_variables))
            self._log(self.COLOR_GREY, 'STAGE CONTEXT: {}'.format(context.stage_variables))

    # Action
    def action_prelude(self, action: dict, context: Context):
        self._log(self.COLOR_GREY, 'PRELUDE')
        self._log(self.COLOR_GREY, json.dumps({'ACTION': self._to_serialized(action),
                                               'SECRETS': self._ofuscate_secrets(self._to_serialized(context.secrets)),
                                               'TEST CONTEXT': self._to_serialized(context.test_variables),
                                               'STAGE CONTEXT': self._to_serialized(context.stage_variables)
                                               },
                                              sort_keys=True,
                                              indent=4))

    def action_conclusion(self, action: dict, context: Context):
        self._log(self.COLOR_GREY, 'CONCLUSION')
        self._log(self.COLOR_GREY, json.dumps({'ACTION': self._to_serialized(action),
                                               'SECRETS': self._ofuscate_secrets(self._to_serialized(context.secrets)),
                                               'TEST CONTEXT': self._to_serialized(context.test_variables),
                                               'STAGE CONTEXT': self._to_serialized(context.stage_variables)
                                               },
                                              sort_keys=True,
                                              indent=4))

    def _ofuscate_secrets(self, secrets: dict):
        return {key: '*' * len(value) for key, value in secrets.items()}

    def _to_serialized(self, dictionary: dict):
        serialized = {}
        for key, value in dictionary.items():
            if isinstance(value, Enum):
                serialized[key] = value.name
            else:
                try:
                    json.dumps(value)
                    serialized[key] = value
                except:
                    serialized[key] = str(value)
        return serialized

    def message(self, message):
        self._log(self.COLOR_GREEN, message)

    def action_debug(self, message):
        if is_debug():
            self._log(self.COLOR_GREY, message)

    def action_error(self, message):
        self._log(self.COLOR_HIGH_RED, message)

    def action_warn(self, message):
        self._log(self.COLOR_HIGH_PINK, message)

    # Log
    def log_text(self, log: str):
        self._log(self.COLOR_WHITE, log)

    # Assertions
    def assertion_success(self, assertion: str):
        if is_debug():
            self._log(self.COLOR_GREEN, '\t{}'.format(assertion))

    def assertion_fail(self, assertion: str, variables: dict):
        self._log(self.COLOR_RED, '\t{}'.format(assertion))
        self._log(self.COLOR_RED, json.dumps(variables))

    def assertion_error(self, assertion: str, exception: Exception = None):
        self._log(self.COLOR_RED, '\t{} - {}'.format(assertion, exception))

    def assert_test_result(self, total, success, failures):
        if success is not total:
            self._log(self.COLOR_HIGH_RED, '\tAsserts: Success[ {} ] Fail[ {} ] Total[ {} ]'.format(success, failures, total))
        elif is_debug():
            self._log(self.COLOR_CYAN, '\tAsserts: Success[ {} ] Fail[ {} ] Total[ {} ]'.format(success, failures, total))

    # Util
    def _log(self, color, text, end=None):
        self.report += self._log_color(color, text, end) + '\n'
