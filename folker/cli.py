from typing import List
from folker.executor import ParallelExecutor, SequentialExecutor
from folker.load.files import load_profile_files, load_template_files, \
    load_test_files
from folker.load.protos import generate_protos
from folker.logger import logger_factory
from folker.logger.system_logger import SystemLogger
from folker.model import Test
from folker.model.error import TestSuiteResultException, TestSuiteNumberExecutionsException
from folker.parameters import Configuration, parameterised


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
    system_logger.execution_report(total=executed,
                                   successes=sorted(success),
                                   failures=sorted(failures),
                                   expected=config.expected_test_count)
    expected_number_of_tests = config.expected_test_count
    if len(success) != executed:
        raise TestSuiteResultException(failures)
    if expected_number_of_tests and int(expected_number_of_tests) != executed:
        raise TestSuiteNumberExecutionsException(expected_number_of_tests, executed)


def run_system_setup(system_logger: SystemLogger):
    system_logger.system_setup_start()
    generate_protos(system_logger)
    system_logger.system_setup_completed()


def run_execution_setup(config: Configuration, system_logger: SystemLogger):
    system_logger.execution_setup_start()
    load_profile_files(config=config, logger=system_logger)
    load_template_files(config=config, logger=system_logger)
    tests = load_test_files(config=config, logger=system_logger)

    return filter_tests_by_tags(system_logger=system_logger, config=config, tests=tests)


def filter_tests_by_tags(system_logger: SystemLogger, config: Configuration, tests: List[Test]):
    system_logger.filtering_tests()
    ignore_skip_tags = len(config.skip_tags) == 0
    ignore_execute_tags = len(config.execute_tags) == 0

    if ignore_skip_tags and ignore_execute_tags:
        for test in tests:
            system_logger.test_filter_tags(test.name)
        return tests

    filtered_tests = []
    for test in tests:
        test_tags = set(test.tags)
        if not ignore_skip_tags:
            matching_skip_tags = config.skip_tags.intersection(test_tags)
            if len(matching_skip_tags) > 0:
                system_logger.test_filter_out_skip_tags(test.name, matching_skip_tags)
                continue
        if not ignore_execute_tags:
            matching_tags = config.execute_tags.intersection(test_tags)
            if len(matching_tags) == len(config.execute_tags):
                system_logger.test_filter_in_execution_tags(test_name=test.name,
                                                            matching_execute_tags=matching_tags)
                filtered_tests.append(test)
                continue
            else:
                system_logger.test_filter_out_execution_tags(test.name, config.execute_tags.difference(matching_tags))
                continue

        system_logger.test_filter_in_skip_tags(test.name)
        filtered_tests.append(test)

    return filtered_tests

def execute_tests(config: Configuration,
                  tests: List[Test],
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
    run()
