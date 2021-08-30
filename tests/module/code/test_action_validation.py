import pytest

from folker.module.code.action import CodeStageAction


@pytest.mark.action_correctness
@pytest.mark.action_code
class TestCodeStageActionValidation:
    def test_validate_empty(self):
        action = CodeStageAction()

        assert not action
        assert not action.validation_report
        assert 'action.module' in action.validation_report.missing_fields
        assert 'action.method' in action.validation_report.missing_fields

    def test_correct(self):
        action = CodeStageAction(module='a_module',
                                 method='a_method')

        assert action
        assert action.validation_report

    def test_correct_parameters(self):
        action = CodeStageAction(module='a_module',
                                 method='a_method',
                                 parameters={'a_name': 'a_value'})

        assert action
        assert action.validation_report
