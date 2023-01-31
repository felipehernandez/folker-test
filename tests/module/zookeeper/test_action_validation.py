import pytest

from folker.module.zookeeper.action import (
    ZookeeperStageAction,
    ZookeeperMethod,
    ZookeeperStageExistsAction,
    ZookeeperStageCreateAction,
    ZookeeperStageDeleteAction,
    ZookeeperStageGetAction,
    ZookeeperStageSetAction,
)


@pytest.mark.action_correctness
@pytest.mark.action_zookeeper
class TestZookeeperActionValidation:
    def test_validate_empty(self):
        action = ZookeeperStageAction()

        assert not action
        assert "action.method" in action.validation_report.missing_fields
        assert "action.host" in action.validation_report.missing_fields
        assert "action.node" in action.validation_report.missing_fields


@pytest.mark.action_correctness
@pytest.mark.action_zookeeper
class TestZookeeperCreateActionValidation:
    def test_create_correct(self):
        action = ZookeeperStageCreateAction(
            method=ZookeeperMethod.CREATE.name, host="a_host", node="a_node"
        )

        assert action
        assert action.validation_report


@pytest.mark.action_correctness
@pytest.mark.action_zookeeper
class TestZookeeperDeleteActionValidation:
    def test_delete_correct(self):
        action = ZookeeperStageDeleteAction(
            method=ZookeeperMethod.DELETE.name, host="a_host", node="a_node"
        )

        assert action
        assert action.validation_report


@pytest.mark.action_correctness
@pytest.mark.action_zookeeper
class TestZookeeperGetActionValidation:
    def test_get_correct(self):
        action = ZookeeperStageGetAction(
            method=ZookeeperMethod.GET.name, host="a_host", node="a_node"
        )

        assert action
        assert action.validation_report


@pytest.mark.action_correctness
@pytest.mark.action_zookeeper
class TestZookeeperSetActionValidation:
    def test_set_correct(self):
        action = ZookeeperStageSetAction(
            method=ZookeeperMethod.SET.name,
            host="a_host",
            node="a_node",
            data="some_data",
        )

        assert action
        assert action.validation_report

    def test_set_missing_data(self):
        action = ZookeeperStageSetAction(
            method=ZookeeperMethod.SET.name, host="a_host", node="a_node"
        )

        assert not action
        assert not action.validation_report
        assert "action.data" in action.validation_report.missing_fields
