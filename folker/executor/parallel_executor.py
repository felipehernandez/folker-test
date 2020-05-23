import copy
from multiprocessing.pool import Pool
from os import cpu_count

from folker import profiles
from folker.logger import logger_factory
from folker.logger.logger_factory import LoggerType
from folker.model.entity import Test
from folker.util.parameters import capture_parameters_context, parameterised_profile


def _test_execution(test: Test):
    test_context = {
        **(profiles.get(parameterised_profile(), {})),
        **(capture_parameters_context())
    }
    return test.execute(logger_factory.build_test_logger(LoggerType.PARALLEL), copy.deepcopy(test_context)), test.name


class ParallelExecutor:
    def execute(self, parallel_tests: [Test]):
        pool = Pool(cpu_count())
        results = pool.map(_test_execution, parallel_tests)
        pool.close()
        return [name for (result, name) in results if result], \
               [name for (result, name) in results if not result]
