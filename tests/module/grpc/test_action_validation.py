import pytest

from folker.module.grpc.action import GrpcStageAction


@pytest.mark.action_correctness
@pytest.mark.action_grpc
class TestGrpcActionValidation:
    def test_validate_basic_correct(self):
        action = GrpcStageAction(host='a_host',
                                 package='a_package',
                                 stub='a_stub',
                                 method='a_method')

        assert action
        assert action.validation_report

    def test_validate_full_correct(self):
        action = GrpcStageAction(host='a_host',
                                 uri='a_uri',
                                 package='a_package',
                                 stub='a_stub',
                                 method='a_method',
                                 data='a_data')

        assert action
        assert action.validation_report

    def test_validate_missing_attribute_host(self):
        action = GrpcStageAction(package='a_package',
                                 stub='a_stub',
                                 method='a_method')

        assert not action
        assert not action.validation_report
        assert 'action.host' in action.validation_report.missing_fields

    def test_validate_missing_attribute_package(self):
        action = GrpcStageAction(host='a_host',
                                 stub='a_stub',
                                 method='a_method')

        assert not action
        assert not action.validation_report
        assert 'action.package' in action.validation_report.missing_fields

    def test_validate_missing_attribute_stub(self):
        action = GrpcStageAction(host='a_host',
                                 package='a_package',
                                 method='a_method')

        assert not action
        assert not action.validation_report
        assert 'action.stub' in action.validation_report.missing_fields

    def test_validate_missing_attribute_method(self):
        action = GrpcStageAction(host='a_host',
                                 package='a_package',
                                 stub='a_stub')

        assert not action
        assert not action.validation_report
        assert 'action.method' in action.validation_report.missing_fields
