from abc import ABC


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


class Validatable(ABC):
    validation_report: ValidationReport

    def __init__(self):
        self.validation_report = ValidationReport()
