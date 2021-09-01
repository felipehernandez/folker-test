import json
from enum import Enum

from folker.logger import TestLogger
from folker.logger.logger import FileLogger
from folker.model import Context
from folker.model.error import SourceException


class FileTestLogger(TestLogger, FileLogger):
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
        self._log('Test unsuccessful')
        self._log(e)
        self._write_to_file()

    # Stage
    def stage_start(self, stage_name: str, context: Context):
        self._log('Stage: {name}'.format(name=stage_name))

    def stage_skip(self, stage_name: str, context: Context):
        self._log('Stage: {name} <SKIPPED>'.format(name=stage_name))

    # Action
    def action_prelude(self, action: dict, context: Context):
        self._log('PRELUDE')
        self._log(json.dumps({'ACTION': self._to_serialized(action),
                              'SECRETS': self._ofuscate_secrets(
                                  self._to_serialized(context.secrets)),
                              'TEST CONTEXT': self._to_serialized(context.test_variables),
                              'STAGE CONTEXT': self._to_serialized(context.stage_variables)
                              },
                             sort_keys=True,
                             indent=4))

    def action_conclusion(self, action: dict, context: Context):
        self._log('CONCLUSION')
        self._log(json.dumps({'ACTION': self._to_serialized(action),
                              'SECRETS': self._ofuscate_secrets(
                                  self._to_serialized(context.secrets)),
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
                except Exception as ex:
                    serialized[key] = str(value)
        return serialized

    def action_executed(self, stage_context: dict):
        if self.trace:
            self._log('STAGE CONTEXT: {}'.format(stage_context))

    def message(self, message):
        self._log(message)

    def action_debug(self, message):
        if self.debug:
            self._log(message)

    def action_error(self, message):
        self._log(message)

    def action_warn(self, message):
        self._log(message)

    # Log
    def log_text(self, log: str):
        self._log(log)

    # Assertions
    def assertion_success(self, assertion: str):
        if self.debug:
            self._log('\t{}'.format(assertion))

    def assertion_fail(self, assertion: str, variables: dict):
        self._log('\t{}'.format(assertion))
        self._log(json.dumps(variables))

    def assertion_error(self, assertion: str, exception: Exception = None):
        self._log('\t{} - {}'.format(assertion, exception))

    def assert_test_result(self, total, success, failures):
        if success is not total:
            self._log(
                '\tAsserts: Success[ {} ] Fail[ {} ] Total[ {} ]'.format(success, failures, total))
        elif self.debug:
            self._log(
                '\tAsserts: Success[ {} ] Fail[ {} ] Total[ {} ]'.format(success, failures, total))
