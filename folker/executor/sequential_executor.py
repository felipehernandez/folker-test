from folker import profiles
from folker.executor import DEFAULT_PROFILE
from folker.logger import logger_factory, LoggerType
from folker.model import Context
from folker.model import Test
from folker.parameters import capture_parameters_context, \
    parameterised_profile, \
    capture_parameters_secrets


class SequentialExecutor:
    def execute(self, sequential_tests: [Test]):
        success_tests = []
        fail_tests = []
        profile = profiles.get(parameterised_profile(), DEFAULT_PROFILE)
        context = Context(
            test_variables={
                **(profile.context),
                **(capture_parameters_context())
            },
            secrets={
                **(profile.secrets),
                **(capture_parameters_secrets())
            })

        for test in sequential_tests:
            if test.execute(logger_factory.build_test_logger(LoggerType.SEQUENTIAL), context):
                success_tests.append(test.name)
            else:
                fail_tests.append(test.name)

        return success_tests, fail_tests
