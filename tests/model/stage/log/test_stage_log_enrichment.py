from folker.model.stage.log import StageLog


class TestStageLogValidation:
    def test_enrich_both_empty(self):
        stage = StageLog()
        template = StageLog()

        result = stage + template

        assert result.logs == set()

    def test_enrich_stage_empty(self):
        stage = StageLog()
        template = StageLog(['a_log'])

        result = stage + template

        assert result.logs == {'a_log'}

    def test_enrich_template_empty(self):
        stage = StageLog(['a_log'])
        template = StageLog()

        result = stage + template

        assert result.logs == {'a_log'}

    def test_enrich_none_empty(self):
        stage = StageLog(['a_log'])
        template = StageLog(['another_log'])

        result = stage + template

        assert result.logs == {'a_log', 'another_log'}

    def test_enrich_overlapping(self):
        stage = StageLog(['a_log', 'another_log'])
        template = StageLog(['another_log', 'and_another_one'])

        result = stage + template

        assert result.logs == {'a_log', 'another_log', 'and_another_one'}
