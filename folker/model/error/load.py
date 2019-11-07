from folker.model.error.error import SourceException


class FileException(SourceException):
    def __init__(self, file: str, e: Exception):
        super().__init__(source='SchemaLoader',
                         error='Error in file schema definition',
                         cause=str(e),
                         details={
                             'file': file
                         })


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

    def __init__(self,
                 missing_fields: [str] = None,
                 wrong_fields: [str] = None,
                 *args: object) -> None:
        details = {}
        if missing_fields:
            details['missing_fields'] = missing_fields
        if wrong_fields:
            details['wrong_fields'] = wrong_fields

        super().__init__(source='Schema loader',
                         error='Schema definition error',
                         cause='Missing mandatory fields',
                         details=details,
                         *args)


class SchemaReferenceNotFoundException(SourceException):

    def __init__(self,
                 reference_id,
                 *args: object) -> None:
        super().__init__(source='Schema loader',
                         error='Reference not found error',
                         cause='Stage reference not found in the preloaded ones',
                         details={'reference_id': reference_id},
                         *args)
