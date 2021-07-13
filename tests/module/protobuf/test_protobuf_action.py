import pytest

from folker.module.protobuf.action import ProtobufStageAction


class TestProtobufAction:
    action: ProtobufStageAction

    @pytest.fixture(autouse=True)
    def setup(self):
        self.action = ProtobufStageAction()
        yield
