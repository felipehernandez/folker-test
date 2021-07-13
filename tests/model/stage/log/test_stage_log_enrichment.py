from folker.model.stage.log import StageLog


class TestStageLogValidation:
    def test_enrich_both_empty(self):
        stage = StageLog()
        template = StageLog()

        stage + template

        assert stage.logs == template.logs == set()

    def test_enrich_stage_empty(self):
        stage = StageLog()
        template = StageLog(['a_log'])

        stage + template

        assert stage.logs == template.logs == {'a_log'}

    def test_enrich_template_empty(self):
        stage = StageLog(['a_log'])
        template = StageLog()

        stage + template

        assert template.logs == set()
        assert stage.logs == {'a_log'}

    def test_enrich_none_empty(self):
        stage = StageLog(['a_log'])
        template = StageLog(['another_log'])

        stage + template

        assert template.logs == {'another_log'}
        assert set(stage.logs) == {'a_log', 'another_log'}

    def test_enrich_overlapping(self):
        stage = StageLog(['a_log', 'another_log'])
        template = StageLog(['another_log', 'and_another_one'])

        stage + template

        assert template.logs == {'another_log', 'and_another_one'}
        assert set(stage.logs) == {'a_log', 'another_log', 'and_another_one'}
