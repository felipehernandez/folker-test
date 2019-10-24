import json


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

    # Assertions
    def assertion_success(self, assertion_definition: str):
        self._print_color(self.COLOR_GREEN, '\t{}'.format(assertion_definition))

    def assertion_fail(self, assertion_definition: str, ):
        pass

    def assertion_error(self, assertion_definition: str, exception: Exception = None):
        self._print_color(self.COLOR_RED, '\t{} - {}'.format(assertion_definition, exception))

    def assertion_execution_error(self, assertion_definition: str, variables: dict, exception: Exception = None):
        self.assertion_error(assertion_definition, exception)
        self._print_color(self.COLOR_RED, json.dumps(variables))

    def _print_color(self, color, text, end=None):
        if end is not None:
            print('{}{}{}'.format(color, text, self.COLOR_DEFAULT), end=end)
        else:
            print('{}{}{}'.format(color, text, self.COLOR_DEFAULT))
