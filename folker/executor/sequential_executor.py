from typing import List

from folker.executor import select_profile
from folker.logger import logger_factory, LoggerType
from folker.model import Context
from folker.model import Test
from folker.parameters import Configuration


class SequentialExecutor:
    def execute(self, config: Configuration, tests: [Test]) -> (List[str], List[str]):
        success_tests = []
        fail_tests = []
        profile = select_profile(config)

        for test in tests:
            context = Context(
                test_variables={**profile.context, **config.context},
                secrets={**profile.secrets, **config.secrets}
            )

            if test.execute(logger_factory.build_test_logger(config, LoggerType.SEQUENTIAL),
                            context):
                success_tests.append(test.name)
            else:
                fail_tests.append(test.name)

        return success_tests, fail_tests
