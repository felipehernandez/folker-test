from folker.model.error.error import SourceException


class MalformedAssertionException(SourceException):
    def __init__(self, assertion=None, *args: object) -> None:
        super().__init__(source='Assertion Executor',
                         error='Assertion does not resolve to a True/False value',
                         cause='Malformed assertion',
                         details={
                             'assertion': assertion
                         },
                         *args)
