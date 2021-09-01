import pytest

from folker.module.zookeeper.action import ZookeeperStageAction, ZookeeperMethod


@pytest.mark.action_correctness
@pytest.mark.action_gcp_zookeeper
class TestZookeeperActionValidation:
    def test_validate_empty(self):
        action = ZookeeperStageAction()

        assert not action
        assert 'action.method' in action.validation_report.missing_fields
        assert 'action.host' in action.validation_report.missing_fields
        assert 'action.node' in action.validation_report.missing_fields

    def test_exists_correct(self):
        action = ZookeeperStageAction(method=ZookeeperMethod.EXISTS.name,
                                      host='a_host',
                                      node='a_node')

        assert action
        assert action.validation_report

    def test_create_correct(self):
        action = ZookeeperStageAction(method=ZookeeperMethod.CREATE.name,
                                      host='a_host',
                                      node='a_node')

        assert action
        assert action.validation_report

    def test_delete_correct(self):
        action = ZookeeperStageAction(method=ZookeeperMethod.DELETE.name,
                                      host='a_host',
                                      node='a_node')

        assert action
        assert action.validation_report

    def test_get_correct(self):
        action = ZookeeperStageAction(method=ZookeeperMethod.GET.name,
                                      host='a_host',
                                      node='a_node')

        assert action
        assert action.validation_report

    def test_set_correct(self):
        action = ZookeeperStageAction(method=ZookeeperMethod.SET.name,
                                      host='a_host',
                                      node='a_node',
                                      data='some_data')

        assert action
        assert action.validation_report

    def test_set_missing_data(self):
        action = ZookeeperStageAction(method=ZookeeperMethod.SET.name,
                                      host='a_host',
                                      node='a_node')

        assert not action
        assert not action.validation_report
        assert 'action.data' in action.validation_report.missing_fields
