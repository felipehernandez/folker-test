import pytest

from folker.model import Context
from folker.module.file.action import (FileStageDeleteAction, FileStageReadAction,
                                        FileStageWriteAction)


@pytest.fixture
def logger(mocker):
    from folker.logger import TestLogger
    return mocker.Mock(spec=TestLogger)


@pytest.mark.action_file
class TestFileWrite:
    def test_the_content_is_written(self, tmp_path, logger):
        target = tmp_path / 'out.txt'

        context = FileStageWriteAction(method='WRITE', file=str(target), content='hello') \
            .execute(logger=logger, context=Context())

        assert target.read_text() == 'hello'
        assert 'error' not in context.stage_variables
        assert 'elapsed_time' in context.stage_variables

    def test_an_existing_file_is_replaced(self, tmp_path, logger):
        target = tmp_path / 'out.txt'
        target.write_text('a much longer previous content')

        FileStageWriteAction(method='WRITE', file=str(target), content='new') \
            .execute(logger=logger, context=Context())

        assert target.read_text() == 'new'

    def test_variables_are_resolved_in_the_path_and_the_content(self, tmp_path, logger):
        context = Context(test_variables={'name': 'greeting', 'text': 'hello'})

        FileStageWriteAction(method='WRITE', file=str(tmp_path / '${name}.txt'),
                             content='${text} world').execute(logger=logger, context=context)

        assert (tmp_path / 'greeting.txt').read_text() == 'hello world'

    def test_a_path_that_cannot_be_written_is_reported_without_failing_the_action(
            self, tmp_path, logger):
        target = tmp_path / 'no_such_directory' / 'out.txt'

        context = FileStageWriteAction(method='WRITE', file=str(target), content='x') \
            .execute(logger=logger, context=Context())

        assert isinstance(context.stage_variables['error'], FileNotFoundError)
        logger.action_error.assert_called_once()

    def test_writing_to_a_directory_is_reported(self, tmp_path, logger):
        context = FileStageWriteAction(method='WRITE', file=str(tmp_path), content='x') \
            .execute(logger=logger, context=Context())

        assert isinstance(context.stage_variables['error'], IsADirectoryError)


@pytest.mark.action_file
class TestFileRead:
    def test_the_content_is_saved(self, tmp_path, logger):
        (tmp_path / 'in.txt').write_text('line 1\nline 2\n')

        context = FileStageReadAction(method='READ', file=str(tmp_path / 'in.txt')) \
            .execute(logger=logger, context=Context())

        assert context.stage_variables['content'] == 'line 1\nline 2\n'
        assert 'error' not in context.stage_variables

    def test_an_empty_file_saves_an_empty_string(self, tmp_path, logger):
        (tmp_path / 'empty.txt').write_text('')

        context = FileStageReadAction(method='READ', file=str(tmp_path / 'empty.txt')) \
            .execute(logger=logger, context=Context())

        assert context.stage_variables['content'] == ''

    def test_a_missing_file_is_reported_without_failing_the_action(self, tmp_path, logger):
        context = FileStageReadAction(method='READ', file=str(tmp_path / 'missing.txt')) \
            .execute(logger=logger, context=Context())

        assert isinstance(context.stage_variables['error'], FileNotFoundError)
        assert 'content' not in context.stage_variables
        logger.action_error.assert_called_once()

    def test_what_a_previous_stage_wrote_is_read_back(self, tmp_path, logger):
        target = str(tmp_path / 'round.txt')
        FileStageWriteAction(method='WRITE', file=target, content='round trip') \
            .execute(logger=logger, context=Context())

        context = FileStageReadAction(method='READ', file=target) \
            .execute(logger=logger, context=Context())

        assert context.stage_variables['content'] == 'round trip'


@pytest.mark.action_file
class TestFileDelete:
    def test_the_file_is_removed(self, tmp_path, logger):
        target = tmp_path / 'gone.txt'
        target.write_text('x')

        context = FileStageDeleteAction(method='DELETE', file=str(target)) \
            .execute(logger=logger, context=Context())

        assert not target.exists()
        assert 'error' not in context.stage_variables
        logger.action_warn.assert_not_called()

    def test_a_missing_file_is_a_warning_not_an_error(self, tmp_path, logger):
        context = FileStageDeleteAction(method='DELETE', file=str(tmp_path / 'missing.txt')) \
            .execute(logger=logger, context=Context())

        assert 'error' not in context.stage_variables
        logger.action_warn.assert_called_once()
        logger.action_error.assert_not_called()

    def test_a_directory_cannot_be_deleted_and_is_reported(self, tmp_path, logger):
        context = FileStageDeleteAction(method='DELETE', file=str(tmp_path)) \
            .execute(logger=logger, context=Context())

        assert 'error' in context.stage_variables
        assert tmp_path.exists()
        logger.action_error.assert_called_once()
