from folker.executor import ParallelExecutor, SequentialExecutor
from folker.load.files import load_profile_files, load_and_initialize_template_files, \
    load_test_files
from folker.load.protos import generate_protos
from folker.logger import logger_factory, SystemLogger
from folker.model import Test
from folker.model.error import TestSuiteResultException, TestSuiteNumberExecutionsException
from folker.parameters import parameterised, Configuration


@parameterised
def run(config: Configuration):
    system_logger = logger_factory.system_logger(config)

    run_system_setup(system_logger)

    tests = run_execution_setup(config=config, system_logger=system_logger)

    # Execution
    executed, success, failures = 0, [], []
    executed = execute_tests(config=config,
                             tests=[test for test in tests if test.parallel],
                             executor=ParallelExecutor(),
                             executed_tests=executed,
                             cumulative_failures=failures,
                             cumulative_success=success)
    executed = execute_tests(config=config,
                             tests=[test for test in tests if not test.parallel],
                             executor=SequentialExecutor(),
                             executed_tests=executed,
                             cumulative_failures=failures,
                             cumulative_success=success)

    # Report
    system_logger.assert_execution_result(executed, sorted(success), sorted(failures))
    expected_number_of_tests = config.expected_test_count
    system_logger.assert_number_tests_executed(expected_number_of_tests, executed)
    if len(success) != executed:
        raise TestSuiteResultException(failures)
    if expected_number_of_tests and int(expected_number_of_tests) != executed:
        raise TestSuiteNumberExecutionsException(expected_number_of_tests, executed)


def run_system_setup(system_logger: SystemLogger):
    system_logger.system_setup_start()
    generate_protos(system_logger)
    system_logger.system_setup_completed()


def run_execution_setup(config: Configuration, system_logger: SystemLogger):
    load_profile_files(config=config, logger=system_logger)
    load_and_initialize_template_files(config=config, logger=system_logger)
    tests = load_test_files(config=config, logger=system_logger)

    return filter_tests_by_tags(config=config, tests=tests)


def filter_tests_by_tags(config: Configuration, tests: [Test]):
    tags = config.execute_tags
    if len(tags) == 0:
        return tests
    return [test for test in tests if all(tag in test.tags for tag in tags)]


def execute_tests(config: Configuration,
                  tests: [Test],
                  executor,
                  executed_tests,
                  cumulative_failures,
                  cumulative_success):
    success_tests, fail_tests = executor.execute(config=config, tests=tests)
    cumulative_success.extend(success_tests)
    cumulative_failures.extend(fail_tests)
    executed_tests += len(success_tests) + len(fail_tests)
    return executed_tests


if __name__ == '__main__':
    run(Configuration())
