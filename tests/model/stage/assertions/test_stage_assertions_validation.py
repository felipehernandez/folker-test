from folker.model.stage.assertions import StageAssertions


class TestStageAssertionsValidation:
    def test_validate_empty(self):
        stage = StageAssertions()

        assert stage

    def test_validate_not_empty(self):
        stage = StageAssertions(assertions=['an_assertion'])

        assert stage
