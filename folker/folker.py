from folker.executor.parallel_executor import ParallelExecutor
from folker.executor.sequential_executor import SequentialExecutor
from folker.load.files import load_test_files, load_and_initialize_template_files
from folker.load.protos import generate_protos
from folker.logger import logger_factory
from folker.model.entity import Test
from folker.model.error.folker import TestSuiteResultException
from folker.util.parameters import load_command_arguments, parameterised_tags


def run():
    load_command_arguments()

    logger = logger_factory.build_system_logger()

    generate_protos(logger)

    load_and_initialize_template_files(logger)
    tests = load_test_files(logger)

    tests = filter_tests_by_tags(tests)

    executed, success, failures = 0, [], []
    executed = execute_tests(tests=[test for test in tests if test.parallel],
                             executor=ParallelExecutor(),
                             executed_tests=executed,
                             cumulative_failures=failures,
                             cumulative_success=success)
    executed = execute_tests(tests=[test for test in tests if not test.parallel],
                             executor=SequentialExecutor(),
                             executed_tests=executed,
                             cumulative_failures=failures,
                             cumulative_success=success)

    logger.assert_execution_result(executed, sorted(success), sorted(failures))
    if len(success) is not executed:
        raise TestSuiteResultException(failures)


def execute_tests(tests, executor, executed_tests, cumulative_failures, cumulative_success):
    success_tests, fail_tests = executor.execute(tests)
    cumulative_success.extend(success_tests)
    cumulative_failures.extend(fail_tests)
    executed_tests += len(success_tests) + len(fail_tests)
    return executed_tests


def filter_tests_by_tags(tests: [Test]):
    tags = parameterised_tags()
    if len(tags) == 0:
        return tests
    return [test for test in tests if all(tag in test.tags for tag in tags)]
