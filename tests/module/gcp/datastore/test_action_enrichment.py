import pytest

from folker.module.gcp.datastore.action import DatastoreMethod, DatastoreStageAction
from folker.module.void.action import VoidStageAction


@pytest.mark.action_gcp_datastore
class TestDatastoreActionEnrichment:
    def test_enrich_override_entity(self):
        original = DatastoreStageAction(method=DatastoreMethod.GET.name,
                                        project='a_project',
                                        key={'kind': 'a_kind', 'id': 'an_id'},
                                        entity={'key': 'value'})
        enrichment = DatastoreStageAction(entity={'key2': 'value2'})

        enriched = original + enrichment

        assert enriched.method == DatastoreMethod.GET
        assert enriched.project == 'a_project'
        assert enriched.key == {'kind': 'a_kind', 'id': 'an_id'}
        assert enriched.entity == {'key2': 'value2'}

    def test_enrich_override_key(self):
        original = DatastoreStageAction(method=DatastoreMethod.GET.name,
                                        project='a_project',
                                        key={'kind': 'a_kind', 'id': 'an_id'},
                                        entity={'key': 'value'})
        enrichment = DatastoreStageAction(key={'kind2': 'a_kind2', 'id2': 'an_id2'})

        enriched = original + enrichment

        assert enriched.method == DatastoreMethod.GET
        assert enriched.project == 'a_project'
        assert enriched.entity == {'key': 'value'}
        assert enriched.key == {'kind2': 'a_kind2', 'id2': 'an_id2'}

    def test_enrich_void(self):
        original = DatastoreStageAction(method=DatastoreMethod.GET.name,
                                        project='a_project',
                                        key={'kind': 'a_kind', 'id': 'an_id'})
        enrichment = VoidStageAction()

        enriched = original + enrichment

        assert enriched.method == DatastoreMethod.GET
        assert enriched.project == 'a_project'
        assert enriched.key == {'kind': 'a_kind', 'id': 'an_id'}
