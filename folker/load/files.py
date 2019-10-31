from pathlib import Path

import yaml

from folker import logger, templates, stage_templates
from folker.load.schemas import TestSchema, TemplateSchema
from folker.logger import Logger
from folker.model.entity import Test


def load_template_files() -> [Test]:
    schema = TemplateSchema()
    Logger().loading_template_files()
    schemas = load_schemas('**/folker_template*.yaml', schema)

    for schema in schemas:
        templates[schema.id] = schema
        for stage in schema.stages:
            stage_templates[stage.data.id] = stage

    return templates, stage_templates


def load_test_files() -> [Test]:
    schema = TestSchema()
    Logger().loading_test_files()
    schemas = load_schemas('**/folker_test*.yaml', schema)

    return schemas


def load_schemas(file_naming, schema):
    schemas = []
    valid_files = []

    for filename in Path('./').absolute().glob(file_naming):
        schemas.append(load_schema(filename, schema, valid_files))

    Logger().loading_files_completed(valid_files)
    return schemas


def load_schema(filename, schema, valid_test_files):
    file_path = filename.resolve().as_uri()[7:]
    Logger().loading_file(filename)
    try:
        test_definition = load_definition(file_path, schema)
        valid_test_files.append(file_path)
        return test_definition
    except Exception as e:
        logger.loading_file_error(e)


def load_definition(file_path, schema):
    with open(file_path, 'r') as stream:
        safe_load = yaml.safe_load(stream)
        return schema.load(safe_load)
