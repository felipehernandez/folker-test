from folker import logger
from folker.load.files import load_test_files, load_template_files
from folker.model.error.folker import TestSuiteResultException

load_template_files()
tests = load_test_files()
executed, success, failures = 0, [], []
for test in tests:
    if test.execute():
        success.append(test.name)
    else:
        failures.append(test.name)
    executed += 1

logger.assert_folker_result(executed, success, failures)

if success is not executed:
    raise TestSuiteResultException(failures)
