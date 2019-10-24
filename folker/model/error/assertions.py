from folker.model import StageData
from folker.model.error.error import SourceException


class TestFailException(SourceException):
    def __init__(self, stage: StageData, failure_messages: [str], *args: object) -> None:
        super().__init__(source=stage.name,
                         error='Assertions failed',
                         cause='Assertions failed',
                         details={
                             'errors': failure_messages
                         },
                         *args)
