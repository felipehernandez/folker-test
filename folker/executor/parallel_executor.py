from itertools import repeat
from multiprocessing.pool import Pool
from os import cpu_count

from folker.executor import select_profile
from folker.logger import logger_factory, LoggerType
from folker.model import Context
from folker.model import Profile
from folker.model import Test
from folker.parameters import Configuration


def _test_execution(config: Configuration, test: Test, profile: Profile):
    context = Context(
        test_variables={
            **(profile.context),
            **(config.context)
        },
        secrets={
            **(profile.secrets),
            **(config.secrets)
        })

    test_logger = logger_factory.build_test_logger(config, LoggerType.PARALLEL)
    return (test.execute(logger=test_logger, context=context), test.name)


class ParallelExecutor:
    def execute(self, config: Configuration, tests: [Test]):
        # Resolve the profile here, in the parent: workers started with spawn/forkserver
        # don't inherit the global `folker.profiles` registry (BUG-02).
        profile = select_profile(config)

        pool = Pool(cpu_count())
        results = pool.starmap(_test_execution, zip(repeat(config), tests, repeat(profile)))
        pool.close()
        return [name for (result, name) in results if result], \
               [name for (result, name) in results if not result]
