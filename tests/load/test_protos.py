import subprocess
import sys
from unittest.mock import Mock, patch

import pytest

from folker.load.protos import generate_protos
from folker.logger import logger_factory
from folker.parameters import Configuration

VALID_PROTO = 'syntax = "proto3";\nmessage Valid { string name = 1; }\n'
INVALID_PROTO = 'syntax = "proto3";\nmessage Broken { string name = ; }\n'


@pytest.fixture
def workdir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path


class TestProtoGeneration:
    def test_valid_proto_is_generated_and_reported_ok(self, workdir):
        (workdir / 'valid.proto').write_text(VALID_PROTO)
        logger = Mock()

        generate_protos(logger)

        assert (workdir / 'valid_pb2.py').exists()
        logger.loading_file_ok.assert_called_once_with('valid.proto')
        logger.proto_generation_failed.assert_not_called()
        logger.loading_proto_files_completed.assert_called_once_with(['valid.proto'])

    def test_a_protoc_failure_is_reported_and_not_counted_as_generated(self, workdir):
        (workdir / 'broken.proto').write_text(INVALID_PROTO)
        logger = Mock()

        generate_protos(logger)

        logger.loading_file_ok.assert_not_called()
        logger.loading_proto_files_completed.assert_called_once_with([])
        (file_name, error), _ = logger.proto_generation_failed.call_args
        assert file_name == 'broken.proto'
        assert 'broken.proto' in str(error)  # protoc says where it failed
        assert not (workdir / 'broken_pb2.py').exists()

    def test_one_failure_does_not_stop_the_other_files(self, workdir):
        (workdir / 'a_broken.proto').write_text(INVALID_PROTO)
        (workdir / 'b_valid.proto').write_text(VALID_PROTO)
        logger = Mock()

        generate_protos(logger)

        assert (workdir / 'b_valid_pb2.py').exists()
        logger.loading_proto_files_completed.assert_called_once_with(['b_valid.proto'])
        assert logger.proto_generation_failed.call_args[0][0] == 'a_broken.proto'

    def test_protoc_runs_with_the_interpreter_running_folker(self, workdir):
        (workdir / 'valid.proto').write_text(VALID_PROTO)

        with patch('folker.load.protos.subprocess.run') as run:
            generate_protos(Mock())

        assert run.call_args[0][0][:3] == [sys.executable, '-m', 'grpc_tools.protoc']

    def test_a_protoc_that_cannot_start_is_reported(self, workdir):
        (workdir / 'valid.proto').write_text(VALID_PROTO)
        logger = Mock()

        with patch('folker.load.protos.subprocess.run', side_effect=OSError('no interpreter')):
            generate_protos(logger)

        logger.loading_file_ok.assert_not_called()
        assert 'no interpreter' in str(logger.proto_generation_failed.call_args[0][1])

    def test_a_missing_protoc_module_is_reported_with_its_message(self, workdir):
        (workdir / 'valid.proto').write_text(VALID_PROTO)
        logger = Mock()
        failure = subprocess.CalledProcessError(
            1, ['python'], stderr="No module named grpc_tools\n")

        with patch('folker.load.protos.subprocess.run', side_effect=failure):
            generate_protos(logger)

        assert logger.proto_generation_failed.call_args[0][1] == 'No module named grpc_tools'

    def test_the_failure_is_visible_without_debug_or_trace(self, workdir, capsys):
        (workdir / 'broken.proto').write_text(INVALID_PROTO)
        logger = logger_factory.system_logger(Configuration(logger_type='PLAIN'))

        generate_protos(logger)

        output = capsys.readouterr().out
        assert 'broken.proto' in output
        assert 'could not be generated' in output
