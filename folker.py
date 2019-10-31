from folker.load.files import load_test_files, load_template_files
from folker.logger import Logger
from folker.model.error.folker import TestSuiteResultException

load_template_files()
tests = load_test_files()
executed, success, failures = 0, [], []
for test in tests:
    test.set_logger(Logger())
    if test.execute():
        success.append(test.name)
    else:
        failures.append(test.name)
    executed += 1

Logger().assert_folker_result(executed, success, failures)

if len(success) is not executed:
    raise TestSuiteResultException(failures)
