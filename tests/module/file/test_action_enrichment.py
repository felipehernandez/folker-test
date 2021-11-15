import pytest

from folker.module.file.action import FileStageAction, FileMethod
from folker.module.void.action import VoidStageAction


@pytest.mark.action_file
class TestFileActionEnrichment:
    def test_enrich_file(self):
        original = FileStageAction(method=FileMethod.READ.name)
        enrichment = FileStageAction(method=FileMethod.READ.name,
                                     file='a_file')

        enriched = original + enrichment

        assert enriched.method == FileMethod.READ
        assert enriched.file == 'a_file'

    def test_override_file(self):
        original = FileStageAction(method=FileMethod.READ.name,
                                   file='a_file')
        enrichment = FileStageAction(method=FileMethod.READ.name,
                                     file='a_file2')

        enriched = original + enrichment

        assert enriched.method == FileMethod.READ
        assert enriched.file == 'a_file2'

    def test_enrich_void(self):
        original = FileStageAction(method=FileMethod.READ.name,
                                   file='a_file')
        enrichment = VoidStageAction()

        enriched = original + enrichment

        assert enriched.method == FileMethod.READ
        assert enriched.file == 'a_file'
