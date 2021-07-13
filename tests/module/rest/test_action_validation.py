from folker.module.rest.action import RestStageAction, RestMethod


class TestRestActionValidation:
    def test_validate_empty(self):
        action = RestStageAction()

        assert not action
        assert not action.validation_report
        assert 'action.method' in action.validation_report.missing_fields
        assert 'action.host' in action.validation_report.missing_fields

    def test_get_correct(self):
        action = RestStageAction(method=RestMethod.GET.name,
                                 host='a_host')

        assert action
        assert action.validation_report

    def test_get_incorrect_host(self):
        action = RestStageAction(method=RestMethod.GET.name)

        assert not action
        assert not action.validation_report
        assert 'action.host' in action.validation_report.missing_fields
