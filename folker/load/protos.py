import subprocess
import sys
from pathlib import Path

from folker.logger import SystemLogger


def generate_protos(logger: SystemLogger):
    logger.loading_proto_files()

    valid_files = []

    for filename in Path('./').glob('**/*.proto'):
        file_name = str(filename)
        if '/lib/python3.' in file_name:
            logger.loading_file_skipped(file_name)
        else:
            proto_run = [sys.executable,
                         '-m',
                         'grpc_tools.protoc',
                         '-I.',
                         '--python_out=.',
                         '--grpc_python_out=.',
                         './' + file_name]
            try:
                subprocess.run(proto_run, check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                # protoc reports what is wrong with the file on stderr
                logger.proto_generation_failed(file_name, (e.stderr or e.stdout or str(e)).strip())
            except Exception as e:
                logger.proto_generation_failed(file_name, e)
            else:
                valid_files.append(file_name)
                logger.loading_file_ok(file_name)

    logger.loading_proto_files_completed(valid_files)
