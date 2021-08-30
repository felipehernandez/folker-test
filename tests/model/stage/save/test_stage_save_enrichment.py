from folker.model import StageSave


class TestStageSaveValidation:
    def test_enrich_both_empty(self):
        stage = StageSave()
        template = StageSave()

        result = stage + template

        assert result.save == {}

    def test_enrich_stage_empty(self):
        stage = StageSave()
        template = StageSave({'a_key': 'a_value'})

        result = stage + template

        assert result.save == {'a_key': 'a_value'}

    def test_enrich_template_empty(self):
        stage = StageSave({'a_key': 'a_value'})
        template = StageSave()

        result = stage + template

        assert result.save == {'a_key': 'a_value'}

    def test_enrich_none_empty(self):
        stage = StageSave({'a_key': 'a_value'})
        template = StageSave({'another_key': 'another_value'})

        result = stage + template

        assert result.save == {'a_key': 'a_value', 'another_key': 'another_value'}

    def test_enrich_overlapping(self):
        stage = StageSave({'a_key': 'a_value', 'another_key': 'another_value'})
        template = StageSave({'another_key': 'another_value',
                              'and_another_key': 'and_another_value'})

        result = stage + template

        assert result.save == {'a_key': 'a_value',
                               'another_key': 'another_value',
                               'and_another_key': 'and_another_value'}
