from folker.module.printt.action import PrintStageAction


class TestPrintActionValidation:
    def test_validate_empty(self):
        action = PrintStageAction()

        assert not action
        assert not action.validation_report
        assert 'action.message' in action.validation_report.missing_fields

    def test_validate_correct(self):
        action = PrintStageAction(message='a_message')

        assert action
        assert action.validation_report
