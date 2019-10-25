from folker.model.data import StageData, ActionData
from folker.model.error.load import InvalidSchemaDefinitionException


class PrintActionData(ActionData):
    message: str

    def __init__(self, message=None, **kargs) -> None:
        super().__init__()
        missing_fields = []

        if message:
            self.message = message
        else:
            missing_fields.append('action.message')

        if len(missing_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields)


class PrintStageData(StageData):
    action: PrintActionData

    def __init__(self, id, name, description=None, type=str, **kargs) -> None:
        super().__init__(id, name, description, type, **kargs)

        if 'action' not in kargs:
            raise InvalidSchemaDefinitionException(missing_fields=['action'])

        self.action = PrintActionData(**kargs['action'])
