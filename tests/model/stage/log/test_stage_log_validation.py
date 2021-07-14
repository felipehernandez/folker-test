from folker.model.stage.log import StageLog


class TestStageLogValidation:
    def test_validate_empty(self):
        stage = StageLog()

        assert stage

    def test_validate_not_empty(self):
        stage = StageLog(logs=['a_log'])

        assert stage
