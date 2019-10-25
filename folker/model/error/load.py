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


class InvalidSchemaDefinitionException(SourceException):

    def __init__(self, missing_fields: [str], *args: object) -> None:
        super().__init__(source='Schema loader',
                         error='Schema definition error',
                         cause='Missing mandatory fields',
                         details={
                             'missing_fields': missing_fields
                         },
                         *args)
