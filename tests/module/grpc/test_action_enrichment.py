from folker.module.grpc.action import GrpcStageAction
from folker.module.void.action import VoidStageAction


class TestGrpcActionEnrichment:
    def test_enrich_override(self):
        original = GrpcStageAction(host='a_host',
                                   package='a_package',
                                   method='a_method')
        enrichment = GrpcStageAction(data='some_data')

        enriched = original + enrichment

        assert enriched.host == 'a_host'
        assert enriched.package == 'a_package'
        assert enriched.method == 'a_method'
        assert enriched.data == 'some_data'

    def test_enrich_void(self):
        original = GrpcStageAction(host='a_host',
                                   package='a_package',
                                   method='a_method')
        enrichment = VoidStageAction()

        enriched = original + enrichment

        assert enriched.host == 'a_host'
        assert enriched.package == 'a_package'
        assert enriched.method == 'a_method'
