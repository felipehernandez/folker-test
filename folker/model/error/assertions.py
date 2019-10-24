from folker.model import StageData
from folker.model.error.error import SourceException


class TestFailException(SourceException):
    def __init__(self, stage: StageData, failure_messages: [str], *args: object) -> None:
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
