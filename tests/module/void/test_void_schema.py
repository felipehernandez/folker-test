from folker.module.void import VoidActionSchema
from folker.module.void.action import VoidStageAction


def test_action_build():
    schema = VoidActionSchema()

    action = schema.make_action(data={})

    assert isinstance(action, VoidStageAction)
