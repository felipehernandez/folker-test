from abc import ABC

from folker.model.error import InvalidSchemaDefinitionException


class ValidationReport:
    missing_fields: set
    wrong_fields: set

    def __init__(self, missing_fields: set = None, wrong_fields: set = None) -> None:
        super().__init__()
        self.missing_fields = missing_fields if missing_fields else set()
        self.wrong_fields = wrong_fields if wrong_fields else set()

    def __bool__(self):
        return len(self.missing_fields) == len(self.missing_fields) == 0

    def __add__(self, other: 'ValidationReport'):
        self.missing_fields.update(other.missing_fields)
        self.wrong_fields.update(other.wrong_fields)

    def merge_with_prefix(self, prefix: str, report: 'ValidationReport'):
        self.missing_fields.update({f'{prefix}{field}' for field in report.missing_fields})
        self.wrong_fields.update({f'{prefix}{field}' for field in report.wrong_fields})

    def generate_error(self):
        if not self:
            raise InvalidSchemaDefinitionException(missing_fields=self.missing_fields,
                                                   wrong_fields=self.wrong_fields)


class Validatable(ABC):
    validation_report: ValidationReport

    def __init__(self):
        self.validation_report = ValidationReport()
