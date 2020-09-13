from multiprocessing.pool import Pool
from os import cpu_count

from folker import profiles
from folker.executor import DEFAULT_PROFILE
from folker.logger import logger_factory, LoggerType
from folker.model import Context
from folker.model import Test
from folker.parameters import capture_parameters_context, \
    parameterised_profile, \
    capture_parameters_secrets


def _test_execution(test: Test):
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
    return test.execute(logger_factory.build_test_logger(LoggerType.PARALLEL), context), test.name


class ParallelExecutor:
    def execute(self, parallel_tests: [Test]):
        pool = Pool(cpu_count())
        results = pool.map(_test_execution, parallel_tests)
        pool.close()
        return [name for (result, name) in results if result], \
               [name for (result, name) in results if not result]
