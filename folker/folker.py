from folker.executor.parallel_executor import ParallelExecutor
from folker.executor.sequential_executor import SequentialExecutor
from folker.load.files import load_test_files, load_and_initialize_template_files, load_profile_files
from folker.load.protos import generate_protos
from folker.logger import logger_factory
from folker.model.entity import Test
from folker.model.error.folker import TestSuiteResultException, TestSuiteNumberExecutionsException
from folker.util.parameters import load_command_arguments, parameterised_tags, parameterised_number_of_tests


def run():
    load_command_arguments()

    logger = logger_factory.build_system_logger()

    generate_protos(logger)

    load_profile_files(logger)
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
    expected_number_of_tests = parameterised_number_of_tests()
    logger.assert_number_tests_executed(expected_number_of_tests, executed)
    if len(success) != executed:
        raise TestSuiteResultException(failures)
    if expected_number_of_tests and int(expected_number_of_tests) != executed:
        raise TestSuiteNumberExecutionsException(expected_number_of_tests, executed)


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
