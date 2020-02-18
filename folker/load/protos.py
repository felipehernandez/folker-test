import subprocess
from pathlib import Path

from folker.logger.logger import SystemLogger


def generate_protos(logger: SystemLogger):
    # logger.loading_proto_files()

    valid_files = []

    for filename in Path('./protos').glob('**/*.proto'):
        file_name = str(filename)
        # logger.loading_proto_file(file_name)
        proto_run = ['python3',
                     '-m',
                     'grpc_tools.protoc',
                     '-I.',
                     '--python_out=.',
                     '--grpc_python_out=.',
                     './' + file_name]
        try:
            result = subprocess.run(proto_run)
            valid_files.append(file_name)
        except Exception as e:
            # logger.loading_proto_file_error(file_name, proto_run, e)
            pass

    # logger.loading_proto_files_completed(valid_files)
