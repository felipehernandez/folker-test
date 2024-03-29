class SourceException(Exception):
    source: str
    error: str
    cause: str
    details: dict

    def __init__(self,
                 source='Unknown',
                 error='Unknown',
                 cause='Unknown',
                 details=None,
                 *args: object) -> None:
        super().__init__(*args)
        self.source = source
        self.error = error
        self.cause = cause
        self.details = details

    def __str__(self) -> str:
        formatted_details = ''
        for detail in self.details:
            formatted_details = formatted_details + \
                                f'\n\t{detail}: {self.details.get(detail).__str__()}'

        return f'{self.error} / {self.cause}\nDetails: {formatted_details}'
