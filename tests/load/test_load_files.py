import pytest

from folker.load.files import load_test_files
from folker.logger import SystemLogger
from folker.parameters import Configuration

VALID_TEST = (
    'name: A test\n'
    'stages:\n'
    '  - name: A stage\n'
    '    action:\n'
    '      type: VOID\n'
)


# BUG-07: the file path was built from `Path.as_uri()[7:]`, which percent-encodes the path
# (`a b` -> `a%20b`), so files in directories with such characters could not be opened.
@pytest.mark.parametrize('directory', [
    'with space',
    'with%percent',
    'with#hash',
    'with?question',
    'ünïcode',
], ids=['space', 'percent', 'hash', 'question', 'unicode'])
def test_test_files_in_unusual_paths_are_loaded(tmp_path, monkeypatch, mocker, directory):
    test_directory = tmp_path / directory
    test_directory.mkdir()
    (test_directory / 'test_a.yaml').write_text(VALID_TEST)
    monkeypatch.chdir(test_directory)
    logger = mocker.Mock(spec=SystemLogger)

    tests = load_test_files(Configuration(test_files=[]), logger)

    assert [test.name for test in tests] == ['A test']
    logger.loading_file_error.assert_not_called()


def test_test_files_in_a_parent_directory_with_spaces_are_loaded(tmp_path, monkeypatch, mocker):
    nested = tmp_path / 'my tests' / 'nested dir'
    nested.mkdir(parents=True)
    (nested / 'test_a.yaml').write_text(VALID_TEST)
    monkeypatch.chdir(tmp_path / 'my tests')
    logger = mocker.Mock(spec=SystemLogger)

    tests = load_test_files(Configuration(test_files=[]), logger)

    assert [test.name for test in tests] == ['A test']
    logger.loading_file_error.assert_not_called()
