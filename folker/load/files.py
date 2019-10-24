from pathlib import Path

import yaml

from folker import logger
from folker.load.schemas import TestSchema
from folker.model.entity import Test


def load_test_files() -> [Test]:
    logger.loading_files()
    valid_test_files = []
    schemas = []

    for filename in Path('./').absolute().glob('**/folker*.yaml'):
        file_path = filename.resolve().as_uri()[7:]
        logger.loading_file(filename)
        try:
            test_definition = load_test_definition(file_path)
            schemas.append(test_definition)
            valid_test_files.append(file_path)
        except Exception as e:
            logger.loading_file_error(e)

    logger.loading_files_completed(valid_test_files)
    return schemas


def load_test_definition(file_path):
    with open(file_path, 'r') as stream:
        safe_load = yaml.safe_load(stream)
        return TestSchema().load(safe_load)
