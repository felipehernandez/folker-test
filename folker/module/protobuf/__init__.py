from folker import stage_builder
from folker.module.protobuf.builder import ProtobufStageBuilder

stage_builder.register_builder(ProtobufStageBuilder())
