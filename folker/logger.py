import json

from folker import debug, trace
from folker.model.data import StageData


class Logger:
    COLOR_DEFAULT = '\033[0m'

    COLOR_BLACK = '\033[0;30m'
    COLOR_RED = '\033[0;31m'
    COLOR_GREEN = '\033[0;32m'
    COLOR_YELLOW = '\033[0;33m'
    COLOR_BLUE = '\033[0;34m'
    COLOR_PINK = '\033[0;35m'
    COLOR_CYAN = '\033[0;36m'
    COLOR_WHITE = '\033[0;37m'
    COLOR_GREY = '\033[0;38m'

    COLOR_HIGH_BLACK = '\033[0;97m'
    COLOR_HIGH_RED = '\033[0;91m'
    COLOR_HIGH_GREEN = '\033[0;92m'
    COLOR_HIGH_YELLOW = '\033[0;93m'
    COLOR_HIGH_BLUE = '\033[0;94m'
    COLOR_HIGH_PINK = '\033[0;95m'
    COLOR_HIGH_CYAN = '\033[0;96m'
    COLOR_HIGH_WHITE = '\033[0;99m'

    def _test(self):
        self._print_color(self.COLOR_DEFAULT, 'COLOR_DEFAULT')

        self._print_color(self.COLOR_BLACK, 'COLOR_BLACK')
        self._print_color(self.COLOR_RED, 'COLOR_RED')
        self._print_color(self.COLOR_GREEN, 'COLOR_GREEN')
        self._print_color(self.COLOR_YELLOW, 'COLOR_YELLOW')
        self._print_color(self.COLOR_BLUE, 'COLOR_BLUE')
        self._print_color(self.COLOR_PINK, 'COLOR_PINK')
        self._print_color(self.COLOR_CYAN, 'COLOR_CYAN')
        self._print_color(self.COLOR_WHITE, 'COLOR_WHITE')
        self._print_color(self.COLOR_GREY, 'COLOR_GREY')

        self._print_color(self.COLOR_HIGH_BLACK, 'COLOR_HIGH_BLACK')
        self._print_color(self.COLOR_HIGH_RED, 'COLOR_HIGH_RED')
        self._print_color(self.COLOR_HIGH_GREEN, 'COLOR_HIGH_GREEN')
        self._print_color(self.COLOR_HIGH_YELLOW, 'COLOR_HIGH_YELLOW')
        self._print_color(self.COLOR_HIGH_BLUE, 'COLOR_HIGH_BLUE')
        self._print_color(self.COLOR_HIGH_PINK, 'COLOR_HIGH_PINK')
        self._print_color(self.COLOR_HIGH_CYAN, 'COLOR_HIGH_CYAN')
        self._print_color(self.COLOR_HIGH_WHITE, 'COLOR_HIGH_WHITE')

    # Load
    def loading_template_files(self):
        if trace:
            self._print_color(self.COLOR_HIGH_CYAN, 'Loading template files')

    def loading_test_files(self):
        if trace:
            self._print_color(self.COLOR_HIGH_CYAN, 'Loading test files')

    def loading_file(self, filename):
        if trace:
            self._print_color(self.COLOR_HIGH_YELLOW, 'File: {filename}'.format(filename=filename))

    def loading_file_error(self, exception: Exception):
        self._print_color(self.COLOR_HIGH_RED, exception)

    def loading_files_completed(self, files):
        if debug or trace:
            self._print_color(self.COLOR_WHITE, 'Files loaded: [')
            for file in files:
                self._print_color(self.COLOR_WHITE, '\t{}'.format(file))
            self._print_color(self.COLOR_WHITE, ']'.format(files))

    # Test
    def test_start(self, name, description=None):
        self._print_color(self.COLOR_HIGH_CYAN, 'TEST: ', '\t')
        self._print_color(self.COLOR_HIGH_CYAN, name)

        if description:
            self._print_color(self.COLOR_BLUE, description)

    def stage_start(self, stage: StageData):
        self._print_color(self.COLOR_HIGH_YELLOW, 'Stage: {name}'.format(id=stage.id, name=stage.name))

        if stage.description: self._print_color(self.COLOR_HIGH_BLUE, stage.description)

    # Stage
    def message(self, message):
        self._print_color(self.COLOR_GREEN, message)

    def action_completed(self, message):
        pass

    def action_debug(self, message):
        if trace:
            self._print_color(self.COLOR_GREY, message)

    # Assertions
    def assertion_success(self, assertion: str):
        if debug or trace:
            self._print_color(self.COLOR_GREEN, '\t{}'.format(assertion))

    def assertion_fail(self, assertion: str, variables: dict):
        self._print_color(self.COLOR_RED, '\t{}'.format(assertion))
        self._print_color(self.COLOR_RED, json.dumps(variables))

    def assertion_error(self, assertion: str, exception: Exception = None):
        self._print_color(self.COLOR_RED, '\t{} - {}'.format(assertion, exception))

    def assertion_execution_error(self, assertion: str, variables: dict, exception: Exception = None):
        self.assertion_error(assertion, exception)
        self._print_color(self.COLOR_RED, json.dumps(variables))

    def assert_test_result(self, total, success, failures):
        if success is not total:
            self._print_color(self.COLOR_HIGH_RED, '\tAsserts: Success[ {} ] Fail[ {} ] Total[ {} ]'.format(success, failures, total))
        elif debug or trace:
            self._print_color(self.COLOR_CYAN, '\tAsserts: Success[ {} ] Fail[ {} ] Total[ {} ]'.format(success, failures, total))

    # Log
    def log_text(self, log: str):
        self._print_color(self.COLOR_WHITE, log)

    def stage_exception(self, exception: Exception):
        self._print_color(self.COLOR_HIGH_RED, exception)

    # Results
    def assert_folker_result(self, total, success, failures):
        self._print_color(self.COLOR_HIGH_CYAN, '\n#################################################################################################')
        self._print_color(self.COLOR_HIGH_CYAN, 'RESULTS:')
        print_color = self.COLOR_HIGH_GREEN if len(success) is total else self.COLOR_HIGH_RED
        self._print_color(print_color, 'Tests: Success[ {} ] Fail[ {} ] Total[ {} ]'.format(len(success), len(failures), total))

        for passed in success:
            self._print_color(self.COLOR_HIGH_GREEN, '\t{}'.format(passed))
        for fail in failures:
            self._print_color(self.COLOR_HIGH_RED, '\t{}'.format(fail))

    #
    def _print_color(self, color, text, end=None):
        if end is not None:
            print('{}{}{}'.format(color, text, self.COLOR_DEFAULT), end=end)
        else:
            print('{}{}{}'.format(color, text, self.COLOR_DEFAULT))
