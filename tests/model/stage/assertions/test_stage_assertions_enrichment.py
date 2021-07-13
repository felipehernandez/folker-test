from folker.model.stage.assertions import StageAssertions


class TestStageAssertionsValidation:
    def test_enrich_both_empty(self):
        stage = StageAssertions()
        template = StageAssertions()

        stage + template

        assert stage.assertions == template.assertions == set()

    def test_enrich_stage_empty(self):
        stage = StageAssertions()
        template = StageAssertions(assertions=['an_assertion'])

        stage + template

        assert stage.assertions == template.assertions == {'an_assertion'}

    def test_enrich_template_empty(self):
        stage = StageAssertions(assertions=['an_assertion'])
        template = StageAssertions()

        stage + template

        assert template.assertions == set()
        assert stage.assertions == {'an_assertion'}

    def test_enrich_none_empty(self):
        stage = StageAssertions(assertions=['an_assertion'])
        template = StageAssertions(assertions=['another_assertion'])

        stage + template

        assert template.assertions == {'another_assertion'}
        assert set(stage.assertions) == {'an_assertion', 'another_assertion'}

    def test_enrich_overlapping(self):
        stage = StageAssertions(assertions=['an_assertion', 'another_assertion'])
        template = StageAssertions(assertions=['another_assertion', 'and_another_assertion'])

        stage + template

        assert template.assertions == {'another_assertion', 'and_another_assertion'}
        assert set(stage.assertions) == {'an_assertion', 'another_assertion', 'and_another_assertion'}
