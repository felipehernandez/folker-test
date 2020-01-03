from folker import stage_builder
from folker.module.gcp.pubsub.builder import PubSubStageBuilder

stage_builder.register_builder(PubSubStageBuilder())
