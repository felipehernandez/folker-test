from folker import profiles
from folker.executor import DEFAULT_PROFILE
from folker.logger import logger_factory, LoggerType
from folker.model import Context
from folker.model import Test
from folker.parameters import Configuration


class SequentialExecutor:
    def execute(self, config: Configuration, tests: [Test]):
        success_tests = []
        fail_tests = []
        param_profile = list(config.profiles)[0] if config.profiles else None
        profile = profiles.get(param_profile, DEFAULT_PROFILE)
        context = Context(
            test_variables={
                **(profile.context),
                **(config.context)
            },
            secrets={
                **(profile.secrets),
                **(config.secrets)
            })

        for test in tests:
            if test.execute(logger_factory.build_test_logger(config, LoggerType.SEQUENTIAL),
                            context):
                success_tests.append(test.name)
            else:
                fail_tests.append(test.name)

        return success_tests, fail_tests
