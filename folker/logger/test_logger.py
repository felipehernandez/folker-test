import json
from abc import ABC
from enum import Enum
from typing import List

from folker.logger.logger import LogEntry, ColorLogger, ConsoleColor, LogEntryType
from folker.model import Context
from folker.model.error import SourceException
from folker.parameters import Configuration


def _obfuscate_secrets(secrets: dict):
    return {key: '*' * len(value) for key, value in secrets.items()}


def _flatten_secrets(secrets) -> set:
    """Every non-empty leaf value of a (possibly nested) secrets structure, as text"""
    if isinstance(secrets, dict):
        values = secrets.values()
    elif isinstance(secrets, (list, tuple, set)):
        values = secrets
    else:
        return set() if secrets is None or str(secrets) == '' else {str(secrets)}

    result = set()
    for value in values:
        result |= _flatten_secrets(value)
    return result


def _to_serialized(dictionary: dict):
    SKIP_ATTRIBUTES = {'validation_report'}
    serialized = {}
    for key, value in dictionary.items():
        if key in SKIP_ATTRIBUTES:
            continue
        if isinstance(value, Enum):
            serialized[key] = value.name
        else:
            try:
                json.dumps(value)
                serialized[key] = value
            except Exception:
                serialized[key] = str(value)
    return serialized


class TestLogger(ABC):
    DELIMITER_0 = '#' * 100
    DELIMITER_1 = '-' * 100
    DELIMITER_2 = '.' * 100

    debug: bool
    trace: bool
    log_file: str

    report: List[LogEntry]
    _secret_values: List[str]

    def __init__(self, config: Configuration) -> None:
        self.debug = config.debug_mode
        self.trace = config.trace_mode
        self.log_file = config.log_file
        self.report = []
        self._secret_values = []

    def _watch_secrets(self, secrets: dict):
        # Longest first, so a secret that contains another one is masked as a whole
        self._secret_values = sorted(_flatten_secrets(secrets), key=len, reverse=True)

    def _redact(self, message):
        """Masks the value of every secret of the running action in a log message"""
        if not isinstance(message, str):
            return message
        for secret in self._secret_values:
            mask = '*' * len(secret)
            message = message.replace(secret, mask)
            # Messages are often JSON dumps, where quotes, backslashes and non-ASCII
            # characters of the secret appear escaped
            escaped = json.dumps(secret)[1:-1]
            if escaped != secret:
                message = message.replace(escaped, mask)
            escaped = json.dumps(secret, ensure_ascii=False)[1:-1]
            if escaped != secret:
                message = message.replace(escaped, mask)
        return message

    def _log(self):
        pass

    def _log_complete(self):
        pass

    def test_start(self, test_name: str, test_description: str = None):
        self.report.append(LogEntry(type=LogEntryType.TEST_INFO, text=self.DELIMITER_1))
        self.report.append(LogEntry(type=LogEntryType.TEST_INFO,
                                    text=f'TEST: {test_name}'))
        if test_description is not None:
            self.report.append(LogEntry(type=LogEntryType.TEST_DEBUG, text=test_description))
        self._log()

    def test_finish(self):
        self.report.append(LogEntry(type=LogEntryType.TEST_SUCCESS,
                                    text=' Test successful '.center(100, '-')))
        self._log()
        self._log_complete()

    def test_finish_error(self, e: SourceException):
        self.report.append(LogEntry(type=LogEntryType.TEST_FAILURE,
                                    text=' Test fail '.center(100, '-')))
        self.report.append(LogEntry(type=LogEntryType.TEST_FAILURE_DETAILS,
                                    text=e))
        self._log()
        self._log_complete()

    # Stage
    def stage_start(self, stage_name: str):
        if self.trace:
            self.report.append(LogEntry(type=LogEntryType.STAGE_INFO, text=self.DELIMITER_2))
        self.report.append(LogEntry(type=LogEntryType.STAGE_INFO,
                                    text=f'Stage: {stage_name}'))
        self._log()

    def stage_skip(self, stage_name: str):
        if self.trace:
            self.report.append(LogEntry(type=LogEntryType.STAGE_SKIP, text=self.DELIMITER_2))
        self.report.append(LogEntry(type=LogEntryType.STAGE_SKIP,
                                    text=f'Stage: {stage_name} <SKIPPED>'))
        self._log()

    # Action
    def action_prelude(self, action: dict, context: Context):
        self._watch_secrets(context.secrets)
        if self.trace:
            self.report.append(LogEntry(type=LogEntryType.ACTION_TRACE,
                                        text=' PRELUDE '.center(100, '.')))
            prelude = {
                'ACTION': _to_serialized(action),
                'SECRETS': _obfuscate_secrets(_to_serialized(context.secrets)),
                'TEST CONTEXT': _to_serialized(context.test_variables),
                'STAGE CONTEXT': _to_serialized(context.stage_variables)
            }
            self.report.append(LogEntry(type=LogEntryType.ACTION_TRACE,
                                        text=json.dumps(prelude,
                                                        sort_keys=True,
                                                        indent=4)))
        self._log()

    def action_conclusion(self, action: dict, context: Context):
        if self.trace:
            self.report.append(LogEntry(type=LogEntryType.ACTION_TRACE,
                                        text=' CONCLUSION '.center(100, '.')))
            prelude = {
                'ACTION': _to_serialized(action),
                'SECRETS': _obfuscate_secrets(_to_serialized(context.secrets)),
                'TEST CONTEXT': _to_serialized(context.test_variables),
                'STAGE CONTEXT': _to_serialized(context.stage_variables)
            }
            self.report.append(LogEntry(type=LogEntryType.ACTION_TRACE,
                                        text=json.dumps(prelude,
                                                        sort_keys=True,
                                                        indent=4)))

        self._log()

    def message(self, message: str):
        self.report.append(LogEntry(type=LogEntryType.ACTION_PRINT, text=message))
        self._log()

    def action_debug(self, message: str):
        if self.debug:
            self.report.append(LogEntry(type=LogEntryType.ACTION_DEBUG,
                                        text=self._redact(message)))
        self._log()

    def action_error(self, message: str):
        self.report.append(LogEntry(type=LogEntryType.ACTION_ERROR,
                                    text=self._redact(message)))
        self._log()

    def action_warn(self, message):
        self.report.append(LogEntry(type=LogEntryType.ACTION_WARN,
                                    text=self._redact(message)))
        self._log()

    # Log
    def log_text(self, log: str):
        self.report.append(LogEntry(type=LogEntryType.ACTION_LOG_PRINT, text=log))
        self._log()

    # Assertions
    def assertion_success(self, assertion: str):
        if self.debug:
            self.report.append(LogEntry(type=LogEntryType.ACTION_ASSERTION_SUCCESS,
                                        text='\t' + assertion))
        self._log()

    def assertion_fail(self, assertion: str, variables: dict):
        self.report.append(LogEntry(type=LogEntryType.ACTION_ASSERTION_FAIL,
                                    text='\t' + assertion))
        if self.debug:
            self.report.append(LogEntry(type=LogEntryType.ACTION_DEBUG,
                                        text=json.dumps(variables)))
        self._log()

    def assertion_error(self, assertion: str, exception: Exception = None):
        self.report.append(LogEntry(type=LogEntryType.ACTION_ASSERTION_ERROR,
                                    text=f'\t{assertion} - {exception}'))
        self._log()

    def assert_test_result(self, total, success, failures):
        message = f'\tAsserts: Success[ {success} ] Fail[ {failures} ] Total[ {total} ]'
        if success != total:
            self.report.append(LogEntry(type=LogEntryType.ACTION_ASSERTION_REPORT_FAIL,
                                        text=message))
        elif self.debug:
            self.report.append(LogEntry(type=LogEntryType.ACTION_ASSERTION_REPORT_OK,
                                        text=message))
        self._log()


class PlainConsoleSequentialTestLogger(TestLogger):
    def _log(self):
        for log_entry in self.report:
            print(log_entry.text, end=log_entry.end)
        self.report = []


class ColorConsoleSequentialTestLogger(TestLogger, ColorLogger):
    def _log(self):
        for log_entry in self.report:
            prefix_color = self.COLOR_MAPPINGS.get(log_entry.type, ConsoleColor.DEFAULT).code()
            text = f'{prefix_color}{log_entry.text}{ConsoleColor.DEFAULT.code()}'
            print(text, end=log_entry.end)
        self.report = []


class PlainFileSequentialTestLogger(TestLogger):
    def _log(self):
        f = open(self.log_file, 'a+')
        for log_entry in self.report:
            print(log_entry.text, end=log_entry.end, file=f)
        f.close()
        self.report = []


class PlainConsoleParallelTestLogger(TestLogger):
    def _log_complete(self):
        for log_entry in self.report:
            print(log_entry.text, end=log_entry.end)
        self.report = []


class ColorConsoleParallelTestLogger(TestLogger, ColorLogger):
    def _log_complete(self):
        for log_entry in self.report:
            prefix_color = self.COLOR_MAPPINGS.get(log_entry.type, ConsoleColor.DEFAULT).code()
            text = f'{prefix_color}{log_entry.text}{ConsoleColor.DEFAULT.code()}'
            print(text, end=log_entry.end)
        self.report = []


class PlainFileParallelTestLogger(TestLogger):
    def _log_complete(self):
        f = open(self.log_file, 'a+')
        for log_entry in self.report:
            print(log_entry.text, end=log_entry.end, file=f)
        f.close()
        self.report = []
