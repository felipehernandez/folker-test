from pathlib import Path

import yaml

from folker.load.schemas import TestSchema  # , TemplateSchema
from folker.logger.logger import SystemLogger
from folker.model.entity import Test


# def load_and_initialize_template_files(logger: Logger) -> [Test]:
#     # schema = TemplateSchema()
#     logger.loading_template_files()
#     # schemas = load_schemas(logger, '**/folker_template*.yaml', schema)
#
#     # for schema in schemas:
#     #     templates[schema.id] = schema
#     #     for stage in schema.stages:
#     #         stage_templates[stage.data.id] = stage
#
#     return templates, stage_templates


def load_test_files(logger: SystemLogger) -> [Test]:
    schema = TestSchema()
    logger.loading_test_files()
    schemas = load_schemas(logger, '**/folker_test*.yaml', schema)

    return schemas


def load_schemas(logger: SystemLogger, file_name: str, schema):
    schemas = []
    valid_files = []

    for filename in Path('./').absolute().glob(file_name):
        schema_definition = load_schema(filename, schema, valid_files, logger)
        if schema_definition:
            schemas.append(schema_definition)

    logger.loading_files_completed(valid_files)
    return schemas


def load_schema(filename: str, schema, valid_test_files, logger: SystemLogger):
    file_path = filename.resolve().as_uri()[7:]
    logger.loading_file(filename)
    try:
        test_definition = load_definition(file_path, schema)
        valid_test_files.append(file_path)
        return test_definition
    except Exception as e:
        logger.loading_file_error(filename, e)


def load_definition(file_path, schema):
    with open(file_path, 'r') as stream:
        safe_load = yaml.safe_load(stream)
        return schema.load(safe_load)
