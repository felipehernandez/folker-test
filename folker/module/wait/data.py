from folker.model.data import StageData, ActionData
from folker.model.error.load import InvalidSchemaDefinitionException


class WaitActionData(ActionData):
    time: int

    def __init__(self, time=None, **kargs) -> None:
        super().__init__()
        missing_fields = []

        if time:
            self.time = time
        else:
            missing_fields.append('action.time')

        if len(missing_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields)


class WaitStageData(StageData):
    action: WaitActionData

    def __init__(self, id, name, description=None, type=str, **kargs) -> None:
        super().__init__(id, name, description, type, **kargs)

        if 'action' not in kargs:
            raise InvalidSchemaDefinitionException(missing_fields=['action'])

        self.action = WaitActionData(**kargs['action'])
