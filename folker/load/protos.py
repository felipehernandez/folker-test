import subprocess
from pathlib import Path

from folker.logger.system_logger import SystemLogger


def generate_protos(logger: SystemLogger):
    logger.loading_proto_files()

    valid_files = []

    for filename in Path('./').glob('**/*.proto'):
        file_name = str(filename)
        if '/lib/python3.' in file_name:
            logger.loading_file_skipped(file_name)
        else:
            proto_run = ['python3',
                         '-m',
                         'grpc_tools.protoc',
                         '-I.',
                         '--python_out=.',
                         '--grpc_python_out=.',
                         './' + file_name]
            try:
                subprocess.run(proto_run)
                valid_files.append(file_name)
                logger.loading_file_ok(file_name)
            except Exception as e:
                logger.loading_file_error(file_name, e)

    logger.loading_proto_files_completed(valid_files)
