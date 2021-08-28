import pytest
from click.testing import CliRunner

import folker.cli


@pytest.mark.cli
class TestCli:
    def test_empty_run(self):
        runner = CliRunner()
        result = runner.invoke(folker.cli.run, [])

        assert result.output == ''

    def test_debug_run(self):
        runner = CliRunner()
        result = runner.invoke(folker.cli.run, ['-d'])

        assert 'SETUP : start' in result.output
        assert 'SETUP : completed' in result.output

    def test_trace_run(self):
        runner = CliRunner()
        result = runner.invoke(folker.cli.run, ['--trace'])

        assert 'SETUP : start' in result.output
        assert 'SETUP : completed' in result.output

    def test_log_file_run(self, tmpdir):
        output_file = tmpdir.join('output.txt')

        runner = CliRunner()
        result = runner.invoke(folker.cli.run, ['-d', '-lf', str(output_file)])

        assert result.output == ''

        generated_logs = output_file.read()
        assert 'SETUP : start' in generated_logs
        assert 'SETUP : completed' in generated_logs
