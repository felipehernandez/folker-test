from folker.model.stage.assertions import StageAssertions


class TestStageAssertionsValidation:
    def test_enrich_both_empty(self):
        stage = StageAssertions()
        template = StageAssertions()

        result = stage + template

        assert result.assertions == []

    def test_enrich_stage_empty(self):
        stage = StageAssertions()
        template = StageAssertions(assertions=['an_assertion'])

        result = stage + template

        assert result.assertions == ['an_assertion']

    def test_enrich_template_empty(self):
        stage = StageAssertions(assertions=['an_assertion'])
        template = StageAssertions()

        result = stage + template

        assert template.assertions == []
        assert stage.assertions == ['an_assertion']

    def test_enrich_none_empty(self):
        stage = StageAssertions(assertions=['an_assertion'])
        template = StageAssertions(assertions=['another_assertion'])

        result = stage + template

        assert result.assertions == ['an_assertion', 'another_assertion']

    def test_enrich_overlapping(self):
        stage = StageAssertions(assertions=['an_assertion', 'another_assertion'])
        template = StageAssertions(assertions=['another_assertion', 'and_another_assertion'])

        result = stage + template

        assert result.assertions == ['an_assertion', 'another_assertion', 'and_another_assertion']
