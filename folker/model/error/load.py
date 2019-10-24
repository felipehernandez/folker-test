from folker.model.error.error import SourceException


class UnrecognisedSchemaException(SourceException):

    def __init__(self, stage_definition: dict, *args: object) -> None:
        super().__init__(source='SchemaLoader',
                         error='Stage building',
                         cause='No builder found for stage definition',
                         details={
                             'stage_definition': stage_definition
                         },
                         *args)
