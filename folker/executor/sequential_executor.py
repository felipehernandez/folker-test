import copy

from folker import profiles
from folker.logger import logger_factory
from folker.logger.logger_factory import LoggerType
from folker.model.entity import Test
from folker.util.parameters import capture_parameters_context, parameterised_profile


class SequentialExecutor:
    def execute(self, sequential_tests: [Test]):
        success_tests = []
        fail_tests = []
        test_context = {
            **(profiles.get(parameterised_profile(), {})),
            **(capture_parameters_context())
        }

        for test in sequential_tests:
            if test.execute(logger_factory.build_test_logger(LoggerType.SEQUENTIAL),
                            copy.deepcopy(test_context)):
                success_tests.append(test.name)
            else:
                fail_tests.append(test.name)

        return success_tests, fail_tests
