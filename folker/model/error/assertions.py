from folker.model.error.error import SourceException


class TestFailException(SourceException):
    def __init__(self, failure_messages: [str], *args: object) -> None:
        super().__init__(source='AssertExecutor',
                         error='Assertions failed',
                         cause='Assertions failed',
                         details={
                             'errors': failure_messages
                         },
                         *args)


class UnresolvableAssertionException(SourceException):
    def __init__(self, assertion=None, *args: object) -> None:
        super().__init__(source='AssertExecutor',
                         error='Malformed assertion',
                         cause='Assertion does not compile',
                         details={
                             'assertion': assertion
                         },
                         *args)


class MalformedAssertionException(SourceException):
    def __init__(self, assertion=None, *args: object) -> None:
        super().__init__(source='AssertExecutor',
                         error='Malformed assertion',
                         cause='Assertion does not resolve to a True/False value',
                         details={
                             'assertion': assertion
                         },
                         *args)


class UnresolvableConditionException(SourceException):
    def __init__(self, condition=None, error=None, *args: object) -> None:
        super().__init__(source='Stage',
                         error='Malformed stage condition',
                         cause='Condition could not be evaluated',
                         details={
                             'condition': condition,
                             'error': error
                         },
                         *args)
