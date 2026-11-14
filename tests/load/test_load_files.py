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

    tests = load_test_files(Configuration(), logger)

    assert [test.name for test in tests] == ['A test']
    logger.loading_file_error.assert_not_called()


def test_test_files_in_a_parent_directory_with_spaces_are_loaded(tmp_path, monkeypatch, mocker):
    nested = tmp_path / 'my tests' / 'nested dir'
    nested.mkdir(parents=True)
    (nested / 'test_a.yaml').write_text(VALID_TEST)
    monkeypatch.chdir(tmp_path / 'my tests')
    logger = mocker.Mock(spec=SystemLogger)

    tests = load_test_files(Configuration(), logger)

    assert [test.name for test in tests] == ['A test']
    logger.loading_file_error.assert_not_called()


# BUG-18: `Configuration.test_files` defaulted to None, so loading with a hand-built
# Configuration() raised `TypeError: object of type 'NoneType' has no len()`
class TestSelectedTestFiles:
    @pytest.fixture
    def suite(self, tmp_path, monkeypatch):
        for name in ('test_a.yaml', 'test_b.yaml'):
            (tmp_path / name).write_text(VALID_TEST.replace('A test', name))
        monkeypatch.chdir(tmp_path)

    def test_default_configuration_selects_no_file_in_particular(self):
        assert Configuration().test_files == set()

    @pytest.mark.parametrize('test_files', [None, [], set()], ids=['none', 'list', 'set'])
    def test_no_selection_loads_every_file(self, suite, mocker, test_files):
        tests = load_test_files(Configuration(test_files=test_files), mocker.Mock(spec=SystemLogger))

        assert sorted(test.name for test in tests) == ['test_a.yaml', 'test_b.yaml']

    @pytest.mark.parametrize('test_files', [['test_b.yaml'], {'test_b.yaml'}], ids=['list', 'set'])
    def test_selection_loads_only_the_named_files(self, suite, mocker, test_files):
        tests = load_test_files(Configuration(test_files=test_files), mocker.Mock(spec=SystemLogger))

        assert [test.name for test in tests] == ['test_b.yaml']
