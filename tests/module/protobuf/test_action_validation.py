import pytest

from folker.module.protobuf.action import ProtobufStageAction, ProtobufMethod


@pytest.mark.action_correctness
@pytest.mark.action_protobuf
class TestProtobufActionValidation:
    def test_validate_empty(self):
        action = ProtobufStageAction()

        assert not action
        assert not action.validation_report
        assert 'action.method' in action.validation_report.missing_fields
        assert 'action.package' in action.validation_report.missing_fields

    def test_get_correct_create(self):
        action = ProtobufStageAction(method=ProtobufMethod.CREATE.name,
                                     package='a_protobuf_package',
                                     clazz='AClass',
                                     data={'attribute_1': 'value_1'})

        assert action
        assert action.validation_report

    def test_get_correct_load(self):
        action = ProtobufStageAction(method=ProtobufMethod.LOAD.name,
                                     package='a_protobuf_package',
                                     clazz='AClass',
                                     message='a_message')

        assert action
        assert action.validation_report

    def test_validate_missing_attribute_method(self):
        action = ProtobufStageAction(package='a_protobuf_package',
                                     clazz='AClass',
                                     data={'attribute_1': 'value_1'})

        assert not action
        assert not action.validation_report
        assert 'action.method' in action.validation_report.missing_fields

    def test_validate_missing_attribute_package(self):
        action = ProtobufStageAction(method=ProtobufMethod.CREATE.name,
                                     clazz='AClass',
                                     data={'attribute_1': 'value_1'})

        assert not action
        assert not action.validation_report
        assert 'action.package' in action.validation_report.missing_fields

    def test_validate_missing_attribute_class(self):
        action = ProtobufStageAction(method=ProtobufMethod.CREATE.name,
                                     package='a_protobuf_package',
                                     data={'attribute_1': 'value_1'})

        assert not action
        assert not action.validation_report
        assert 'action.class' in action.validation_report.missing_fields

    def test_validate_missing_attribute_data(self):
        action = ProtobufStageAction(method=ProtobufMethod.CREATE.name,
                                     package='a_protobuf_package',
                                     clazz='AClass')

        assert not action
        assert not action.validation_report
        assert 'action.data' in action.validation_report.missing_fields

    def test_validate_missing_attribute_message(self):
        action = ProtobufStageAction(method=ProtobufMethod.LOAD.name,
                                     package='a_protobuf_package',
                                     clazz='AClass')

        assert not action
        assert not action.validation_report
        assert 'action.message' in action.validation_report.missing_fields
