from folker.model.error.error import SourceException


class VariableReferenceResolutionException(SourceException):
    def __init__(self, variable_reference=None, *args: object) -> None:
        super().__init__(source='VariableResolver',
                         error='Missing reference in context',
                         cause='Variable reference cannot be resolved',
                         details={
                             'reference': variable_reference
                         },
                         *args)
