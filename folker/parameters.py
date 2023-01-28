from enum import Enum, auto
from typing import List

import click

DEFAULT_TEST_FILES_RE = 'test*.yaml'
DEFAULT_TEMPLATE_FILES_RE = 'template*.yaml'
DEFAULT_PROFILE_FILES_RE = 'profile*.yaml'


class Configuration:
    class LoggerType(Enum):
        PLAIN = auto()
        COLOR = auto()

    debug_mode: bool
    trace_mode: bool
    log_file: str
    logger_type: LoggerType
    execute_tags: set
    skip_tags: set
    profiles: set
    context: dict
    secrets: dict
    expected_test_count: int
    test_files: set
    test_files_re: str
    template_files_re: str
    profile_files_re: str

    def __init__(self,
                 debug: bool = False,
                 trace: bool = False,
                 log_file: str = None,
                 logger_type: str = None,
                 tags: {str} = None,
                 skip_tags: {str} = None,
                 profiles: {str} = None,
                 context: dict = None,
                 secrets: dict = None,
                 expected_test_count: int = None,
                 test_files: {str} = None,
                 test_files_re: str = None
                 ) -> None:
        self.debug_mode = debug or trace
        self.trace_mode = trace

        self.log_file = log_file
        self.logger_type = Configuration.LoggerType[logger_type] \
            if logger_type \
            else Configuration.LoggerType.COLOR
        self.test_files = test_files
        resolved_test_files_re = test_files_re if test_files_re else DEFAULT_TEST_FILES_RE
        self.test_files_re = f'**/{resolved_test_files_re}'
        self.template_files_re = f'**/{DEFAULT_TEMPLATE_FILES_RE}'
        self.profile_files_re = f'**/{DEFAULT_PROFILE_FILES_RE}'
        self.execute_tags = set(tags) if tags else set()
        self.skip_tags = set(skip_tags) if skip_tags else set()
        self.profiles = profiles if profiles else set()
        self.context = context if context else dict()
        self.secrets = secrets if secrets else dict()
        self.expected_test_count = int(expected_test_count) if expected_test_count else None


def parameterised(func):
    @click.command()
    @click.option('-d', '--debug',
                  'debug',
                  is_flag=True,
                  default=False,
                  show_default=True,
                  help='Run in DEBUG mode')
    @click.option('--trace',
                  'trace',
                  is_flag=True,
                  default=False,
                  show_default=True,
                  help='Run in TRACE mode')
    @click.option('-lf', '--log-file',
                  'log_file',
                  help='Log to file XXX.XX')
    @click.option('--logger-type',
                  'logger_type',
                  type=click.Choice(
                      [logger_type.name for logger_type in Configuration.LoggerType],
                      case_sensitive=False),
                  default=Configuration.LoggerType.COLOR.name,
                  show_default=True,
                  help='Logger type')
    @click.option('-t', '--tag',
                  'tags',
                  multiple=True,
                  help='Run all tests with specified tags')
    @click.option('-p', '--profile',
                  'profiles',
                  multiple=True,
                  help='Use a profile to initialise context and secrets')
    @click.option('-c', '--context',
                  'context',
                  type=(str, str),
                  multiple=True,
                  help='Add to context key value')
    @click.option('-s', '--secret',
                  'secrets',
                  type=(str, str),
                  multiple=True,
                  help='Add to secret key value')
    @click.option('-n',
                  'expected_test_count',
                  type=int,
                  help='Assert the total number of executed tests')
    @click.option('-tf', '--test-file',
                  'test_files',
                  multiple=True,
                  help='Run all tests whose file name are listed. Use quotes ("") if necessary')
    @click.option('-TF', '--TEST-FILES',
                  'test_files_re',
                  default=DEFAULT_TEST_FILES_RE,
                  show_default=True,
                  help='Run all tests whose file name match the regular expression')
    @click.pass_context
    def wrapper(ctx=None,
                debug: bool = False,
                trace: bool = False,
                log_file: str = None,
                logger_type: str = None,
                tags: List[str] = None,
                skip_tags: List[str] = None,
                profiles: str = None,
                context: (str, str) = None,
                secrets: (str, str) = None,
                expected_test_count: int = None,
                test_files: [str] = None,
                test_files_re: str = None,
                *args, **kargs):
        config = Configuration(debug=debug,
                               trace=trace,
                               tags={tag
                                     for tag_group in tags
                                     for tag in tag_group.split(',')
                                     },
                               skip_tags={skip_tag
                                          for tag_group in skip_tags
                                          for skip_tag in tag_group.split(',')
                                          },
                               profiles={profile
                                         for profile_group in profiles
                                         for profile in profile_group.split(',')
                                         },
                               context={key: value for key, value in context},
                               secrets={key: value for key, value in secrets},
                               expected_test_count=expected_test_count,
                               log_file=log_file,
                               logger_type=logger_type,
                               test_files={file for file in test_files},
                               test_files_re=test_files_re)

        return func(config=config)

    return wrapper
