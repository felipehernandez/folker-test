import click

DEBUG_KEY = 'debug'
TRACE_KEY = 'trace'
TAGS_KEY = 'tags'
PROFILE_KEY = 'profile'
CONTEXT_KEY = 'context'
SECRETS_KEY = 'secrets'
LOG_KEY = 'log'
NUMBER_KEY = 'number'
FILES_KEY = 'files'
TEST_FILE_RE_KEY = 'test_file_re'
TEMPLATE_FILE_RE_KEY = 'template_file_re'
PROFILE_FILE_RE_KEY = 'profile_file_re'

RE_TEST_DEFAULT = 'test*.yaml'
RE_TEMPLATE_DEFAULT = 'template*.yaml'
RE_PROFILE_DEFAULT = 'profile*.yaml'

command_options = {
    TEST_FILE_RE_KEY: RE_TEST_DEFAULT,
    TEMPLATE_FILE_RE_KEY: RE_TEMPLATE_DEFAULT,
    PROFILE_FILE_RE_KEY: RE_PROFILE_DEFAULT
}


def is_debug():
    return command_options.get(DEBUG_KEY, False) or is_trace()


def is_trace():
    return command_options.get(TRACE_KEY, False)


def parameterised_tags():
    return command_options.get(TAGS_KEY, [])


def parameterised_profile():
    return command_options.get(PROFILE_KEY, None)


def capture_parameters_context():
    return command_options.get(CONTEXT_KEY, {})


def capture_parameters_secrets():
    return command_options.get(SECRETS_KEY, {})


def log_to_file():
    return command_options.get(LOG_KEY, None)


def parameterised_number_of_tests():
    return command_options.get(NUMBER_KEY, None)


def parameterised_test_files():
    return command_options.get(FILES_KEY, [])


def test_file_regular_expression():
    re = command_options.get(TEST_FILE_RE_KEY)
    if not re:
        re = RE_TEST_DEFAULT
    return '**/{}'.format(re)


def template_file_regular_expression():
    re = command_options.get(TEMPLATE_FILE_RE_KEY)
    if not re:
        re = RE_TEMPLATE_DEFAULT
    return '**/{}'.format(re)


def profile_file_regular_expression():
    re = command_options.get(PROFILE_FILE_RE_KEY)
    if not re:
        re = RE_PROFILE_DEFAULT
    return '**/{}'.format(re)


def parameterised(func):
    @click.command()
    @click.option('-d', '--debug', DEBUG_KEY,
                  is_flag=True,
                  default=False,
                  show_default=True,
                  help='Run in DEBUG mode')
    @click.option('--trace', TRACE_KEY,
                  is_flag=True,
                  default=False,
                  show_default=True,
                  help='Run in TRACE mode')
    @click.option('-t', '--tag', TAGS_KEY,
                  multiple=True,
                  help='Run all tests with specified tags')
    @click.option('-p', '--profile', PROFILE_KEY,
                  help='Use a profile to initialise context and secrets')
    @click.option('-c', '--context', CONTEXT_KEY,
                  type=(str, str),
                  multiple=True,
                  help='Add to context key value')
    @click.option('-s', '--secret', SECRETS_KEY,
                  type=(str, str),
                  multiple=True,
                  help='Add to secret key value')
    @click.option('-l', '--log', LOG_KEY,
                  help='Log to file XXX.XX')
    @click.option('-n', NUMBER_KEY,
                  type=int,
                  help='Assert the total number of executed tests')
    @click.option('-f', '--file', FILES_KEY,
                  multiple=True,
                  help='Run all tests whose file name are listed. Use quotes ("") if necessary')
    @click.option('-F', '--FILE', TEST_FILE_RE_KEY,
                  default=RE_TEST_DEFAULT,
                  show_default=True,
                  help='Run all tests whose file name match the regular expression')
    @click.pass_context
    def wrapper(ctx, *args, **kargs):
        command_options[DEBUG_KEY] = kargs[DEBUG_KEY]
        command_options[TRACE_KEY] = kargs[TRACE_KEY]
        command_options[TAGS_KEY] = [tag for tag in kargs[TAGS_KEY]]
        command_options[PROFILE_KEY] = kargs[PROFILE_KEY]
        command_options[CONTEXT_KEY] = {key: value for key, value in kargs[CONTEXT_KEY]}
        command_options[SECRETS_KEY] = {key: value for key, value in kargs[SECRETS_KEY]}
        command_options[LOG_KEY] = kargs[LOG_KEY]
        command_options[NUMBER_KEY] = kargs[NUMBER_KEY]
        command_options[FILES_KEY] = [file for file in kargs[FILES_KEY]]
        command_options[TEST_FILE_RE_KEY] = kargs[TEST_FILE_RE_KEY]

        return func(*args, **kargs)

    return wrapper
