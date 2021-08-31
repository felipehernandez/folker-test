from multiprocessing.pool import Pool
from os import cpu_count

from folker import profiles
from folker.executor import DEFAULT_PROFILE
from folker.logger import logger_factory, LoggerType
from folker.model import Context
from folker.model import Test
from folker.parameters import Configuration


def _test_execution(config: Configuration, test: Test):
    param_profile = config.profiles[0] if config.profiles else None
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
    return (test.execute(logger_factory.build_test_logger(config, LoggerType.PARALLEL), context),
            test.name)


class ParallelExecutor:
    def execute(self, config: Configuration, tests: [Test]):
        pool = Pool(cpu_count())
        results = pool.starmap(_test_execution, [(config, tests)])
        pool.close()
        return [name for (result, name) in results if result], \
               [name for (result, name) in results if not result]
