import pytest

from folker.module.gcp.datastore.action import (
    DatastoreStageAction,
    DatastoreMethod,
    DatastoreStageDeleteAction,
    DatastoreStageGetAction,
    DatastoreStagePutAction,
)


@pytest.mark.action_correctness
@pytest.mark.action_gcp_datastore
class TestDatastoreActionValidation:
    def test_validate_empty(self):
        action = DatastoreStageAction()

        assert not action
        assert not action.validation_report
        assert "action.method" in action.validation_report.missing_fields
        assert "action.project" in action.validation_report.missing_fields
        assert "action.key" in action.validation_report.missing_fields

    def test_validate_wrong_method(self):
        action = DatastoreStageAction(method="X")

        assert not action
        assert not action.validation_report
        assert "action.method" in action.validation_report.wrong_fields
        assert "action.project" in action.validation_report.missing_fields
        assert "action.key" in action.validation_report.missing_fields


@pytest.mark.action_correctness
@pytest.mark.action_gcp_datastore
class TestDatastorePutActionValidation:
    def test_action_gcp_datastore_validate_missing_project(self):
        action = DatastoreStagePutAction(method=DatastoreMethod.PUT.name)

        assert not action
        assert not action.validation_report
        assert "action.project" in action.validation_report.missing_fields
        assert "action.key" in action.validation_report.missing_fields

    def test_action_gcp_datastore_validate_missing_key_kind_on_put(self):
        action = DatastoreStagePutAction(method=DatastoreMethod.PUT.name, key={})
        assert not action
        assert not action.validation_report
        assert "action.key.kind" in action.validation_report.missing_fields

    def test_action_gcp_datastore_validate_missing_key_id_and_name_on_put(self):
        action = DatastoreStagePutAction(
            method=DatastoreMethod.PUT.name, key={"kind": "a_kind"}
        )

        assert not action
        assert not action.validation_report
        assert "action.key.id" in action.validation_report.missing_fields
        assert "action.key.name" in action.validation_report.missing_fields

    def test_action_gcp_datastore_validate_complete_put_with_id(self):
        action = DatastoreStagePutAction(
            method=DatastoreMethod.PUT.name,
            project="a_project",
            key={"kind": "a_kind", "id": "an_id"},
            entity={"key": "value"},
        )
        assert action
        assert action.validation_report

    def test_action_gcp_datastore_validate_complete_put_with_name(self):
        action = DatastoreStagePutAction(
            method=DatastoreMethod.PUT.name,
            project="a_project",
            key={"kind": "a_kind", "name": "a_name"},
            entity={"key": "value"},
        )

        assert action
        assert action.validation_report

    def test_action_gcp_datastore_validate_missing_entity_on_put(self):
        action = DatastoreStagePutAction(method=DatastoreMethod.PUT.name, key={})

        assert not action
        assert not action.validation_report
        assert "action.entity" in action.validation_report.missing_fields


@pytest.mark.action_correctness
@pytest.mark.action_gcp_datastore
class TestDatastoreGetActionValidation:
    def test_action_gcp_datastore_validate_missing_key_kind_on_get(self):
        action = DatastoreStageGetAction(method=DatastoreMethod.GET.name, key={})

        assert not action
        assert not action.validation_report
        assert "action.project" in action.validation_report.missing_fields
        assert "action.key" in action.validation_report.missing_fields

    def test_action_gcp_datastore_validate_missing_key_id_and_name_on_get(self):
        action = DatastoreStageGetAction(
            method=DatastoreMethod.GET.name, key={"kind": "a_kind"}
        )

        assert not action
        assert not action.validation_report
        assert "action.key.id" in action.validation_report.missing_fields
        assert "action.key.name" in action.validation_report.missing_fields

    def test_action_gcp_datastore_validate_complete_get_with_id(self):
        action = DatastoreStageGetAction(
            method=DatastoreMethod.GET.name,
            project="a_project",
            key={"kind": "a_kind", "id": "an_id"},
        )

        assert action
        assert action.validation_report

    def test_action_gcp_datastore_validate_complete_get_with_name(self):
        action = DatastoreStageGetAction(
            method=DatastoreMethod.GET.name,
            project="a_project",
            key={"kind": "a_kind", "name": "a_name"},
        )

        assert action
        assert action.validation_report


@pytest.mark.action_correctness
@pytest.mark.action_gcp_datastore
class TestDatastoreDeleteActionValidation:
    def test_action_gcp_datastore_validate_missing_key_kind_on_delete(self):
        action = DatastoreStageDeleteAction(method=DatastoreMethod.DELETE.name, key={})

        assert not action
        assert not action.validation_report
        assert "action.key.name" in action.validation_report.missing_fields

    def test_action_gcp_datastore_validate_missing_key_id_and_name_on_delete(self):
        action = DatastoreStageDeleteAction(
            method=DatastoreMethod.DELETE.name, key={"kind": "a_kind"}
        )

        assert not action
        assert not action.validation_report
        assert "action.key.id" in action.validation_report.missing_fields
        assert "action.key.name" in action.validation_report.missing_fields

    def test_action_gcp_datastore_validate_complete_delete_with_id(self):
        action = DatastoreStageDeleteAction(
            method=DatastoreMethod.DELETE.name,
            project="a_project",
            key={"kind": "a_kind", "id": "an_id"},
        )

        assert action
        assert action.validation_report

    def test_action_gcp_datastore_validate_complete_delete_with_name(self):
        action = DatastoreStageDeleteAction(
            method=DatastoreMethod.DELETE.name,
            project="a_project",
            key={"kind": "a_kind", "name": "a_name"},
        )

        assert action
        assert action.validation_report
