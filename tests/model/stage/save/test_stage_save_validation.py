from folker.model import StageSave


class TestStageSaveValidation:
    def test_validate_empty(self):
        stage = StageSave()

        assert stage

    def test_validate_not_empty(self):
        stage = StageSave(save={'a_key': 'a_value'})

        assert stage
