from folker.module.protobuf.action import ProtobufStageAction, ProtobufMethod
from folker.module.void.action import VoidStageAction


class TestProtobufActionEnrichment:
    def test_enrich_empty_create(self):
        original = ProtobufStageAction(method=ProtobufMethod.CREATE.name)
        enrichment = ProtobufStageAction(method=ProtobufMethod.CREATE.name,
                                         package='a_protobuf_package',
                                         clazz='AClass',
                                         data={'attribute_1': 'value_1'})

        enriched = original + enrichment

        assert enriched.method == ProtobufMethod.CREATE
        assert enriched.package == 'a_protobuf_package'
        assert enriched.clazz == 'AClass'
        assert enriched.data == {'attribute_1': 'value_1'}

    def test_enrich_create_override_data(self):
        original = ProtobufStageAction(method=ProtobufMethod.CREATE.name,
                                       package='a_protobuf_package',
                                       clazz='AClass', )
        enrichment = ProtobufStageAction(method=ProtobufMethod.CREATE.name,
                                         data={'attribute_1': 'value_1'})

        enriched = original + enrichment

        assert enriched.method == ProtobufMethod.CREATE
        assert enriched.package == 'a_protobuf_package'
        assert enriched.clazz == 'AClass'
        assert enriched.data == {'attribute_1': 'value_1'}

    def test_enrich_load_override_data(self):
        original = ProtobufStageAction(method=ProtobufMethod.LOAD.name,
                                       package='a_protobuf_package',
                                       clazz='AClass', )
        enrichment = ProtobufStageAction(method=ProtobufMethod.CREATE.name,
                                         message='a_message')

        enriched = original + enrichment

        assert enriched.method == ProtobufMethod.LOAD
        assert enriched.package == 'a_protobuf_package'
        assert enriched.clazz == 'AClass'
        assert enriched.message == 'a_message'

    def test_enrich_void(self):
        original = ProtobufStageAction(method=ProtobufMethod.CREATE.name,
                                       package='a_protobuf_package',
                                       clazz='AClass',
                                       data={'attribute_1': 'value_1'})
        enrichment = VoidStageAction()

        enriched = original + enrichment

        assert enriched.method == ProtobufMethod.CREATE
        assert enriched.package == 'a_protobuf_package'
        assert enriched.clazz == 'AClass'
        assert enriched.data == {'attribute_1': 'value_1'}
