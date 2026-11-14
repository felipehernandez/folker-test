import pytest

from folker.model import StageAction
from folker.model.error import InvalidSchemaDefinitionException
from folker.model.validation import ValidationReport


class OnlyWrongFieldAction(StageAction):
    """An action with nothing mandatory missing, whose only problem is a wrong field."""

    def __init__(self) -> None:
        super().__init__()
        self.validation_report.wrong_fields.add('action.method')

    def mandatory_fields(self) -> [str]:
        return []

    def execute(self, logger, context):
        return context


class TestValidationReport:
    def test_empty_report_is_valid(self):
        assert ValidationReport()

    def test_missing_fields_make_it_invalid(self):
        assert not ValidationReport(missing_fields={'action.host'})

    # BUG-06: `len(self.missing_fields) == len(self.missing_fields) == 0` never looked at
    # wrong_fields, so a report with only wrong fields counted as valid.
    def test_wrong_fields_make_it_invalid(self):
        assert not ValidationReport(wrong_fields={'action.method'})

    def test_missing_and_wrong_fields_make_it_invalid(self):
        assert not ValidationReport(missing_fields={'action.host'},
                                    wrong_fields={'action.method'})

    def test_merged_wrong_fields_make_it_invalid(self):
        report = ValidationReport()

        report.merge_with_prefix('stage[a].', ValidationReport(wrong_fields={'action.method'}))

        assert not report
        assert report.wrong_fields == {'stage[a].action.method'}

    def test_generate_error_for_wrong_fields(self):
        report = ValidationReport(wrong_fields={'action.method'})

        with pytest.raises(InvalidSchemaDefinitionException):
            report.generate_error()

    def test_generate_error_does_nothing_when_valid(self):
        ValidationReport().generate_error()


class TestActionWithOnlyWrongFields:
    def test_action_with_only_wrong_fields_is_invalid(self):
        assert not OnlyWrongFieldAction()
