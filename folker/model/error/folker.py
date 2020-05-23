from folker.model.error.error import SourceException


class TestSuiteResultException(SourceException):

    def __init__(self,
                 failure_test: [str] = None,
                 *args: object) -> None:
        super().__init__(source='Folker-tesT',
                         error='Failure tests',
                         cause='Tests are not passing',
                         details={'failure_test': failure_test},
                         *args)


class TestSuiteNumberExecutionsException(SourceException):
    def __init__(self,
                 expected: int = None,
                 executed: int = None,
                 *args: object) -> None:
        super().__init__(source='Folker-tesT',
                         error='Insufficient tests',
                         cause='Unexpected number of executed tests',
                         details={
                             'expected': expected,
                             'executed': executed
                         },
                         *args)
