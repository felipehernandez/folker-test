from folker.model.error.error import SourceException


class VariableReferenceResolutionException(SourceException):
    def __init__(self, variable_reference=None, *args: object) -> None:
        super().__init__(source='Variable reference resolution',
                         error='Variable reference cannot be resolved',
                         cause='Missing reference in context',
                         details={
                             'reference': variable_reference
                         },
                         *args)
