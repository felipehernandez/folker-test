from folker.executor.parallel_executor import ParallelExecutor
from folker.executor.sequential_executor import SequentialExecutor
from folker.load.files import load_test_files, load_and_initialize_template_files
from folker.load.protos import generate_protos
from folker.logger import logger_factory
from folker.util.parameters import load_command_arguments


def run():
    load_command_arguments()

    logger = logger_factory.build_system_logger()

    generate_protos(logger)

    sequential_executor = SequentialExecutor()
    parallel_executor = ParallelExecutor()

    load_and_initialize_template_files(logger)
    tests = load_test_files(logger)

    parallel_tests = [test for test in tests if test.parallel]
    sequential_tests = [test for test in tests if not test.parallel]

    executed, success, failures = 0, [], []

    success_tests, fail_tests = parallel_executor.execute(parallel_tests)
    success.extend(success_tests)
    failures.extend(fail_tests)
    executed += len(success_tests) + len(fail_tests)

    success_tests, fail_tests = sequential_executor.execute(sequential_tests)
    success.extend(success_tests)
    failures.extend(fail_tests)
    executed += len(success_tests) + len(fail_tests)

    logger.assert_execution_result(executed, success, failures)
    # if len(success) is not executed:
    #     raise TestSuiteResultException(failures)
