from pathlib import Path

import yaml

from folker import templates, stage_templates, profiles
from folker.load.schemas import TestSchema, ProfileSchema
from folker.logger import SystemLogger
from folker.model import Test
from folker.parameters import Configuration


def load_template_files(config: Configuration, logger: SystemLogger) -> [Test]:
    schema = TestSchema()
    logger.loading_template_files()
    schemas = load_schemas(config=config,
                           logger=logger,
                           file_name=config.template_files_re,
                           schema=schema,
                           template=True)

    for schema in schemas:
        templates[schema.id] = schema
        logger.loaded_template(schema.id)
        for stage in schema.stages:
            stage_templates[stage.id] = stage
            logger.loaded_template_stage(stage.id)

    return templates, stage_templates


def load_test_files(config: Configuration, logger: SystemLogger) -> [Test]:
    schema = TestSchema()
    logger.loading_test_files()
    schemas = load_schemas(config=config,
                           logger=logger,
                           file_name=config.test_files_re,
                           schema=schema,
                           template=False)

    return schemas


def _enrich_stages(schema_definition: Test):
    schema_definition.stages = [stage_templates.get(stage.id) + stage
                                if stage.id is not None and stage.id in stage_templates
                                else stage
                                for stage in schema_definition.stages]
    if not schema_definition:
        schema_definition.validation_report.generate_error()


def load_schemas(config: Configuration,
                 logger: SystemLogger,
                 file_name: str,
                 schema,
                 template: bool = False):
    schemas = []
    valid_files = []
    selected_test_files = config.test_files

    for filename in Path('./').absolute().glob(file_name):
        if _should_load_file(filename.name, template, selected_test_files):
            schema_definition = load_schema(filename, schema, valid_files, logger)
            if schema_definition is not None:
                if not template:
                    _enrich_stages(schema_definition)
                schemas.append(schema_definition)

    logger.loading_files_completed(valid_files)
    return schemas


def _should_load_file(filename: str, template: bool, selected_test_files: [str]):
    if template:
        return True
    if len(selected_test_files) == 0:
        return True
    return filename in selected_test_files


def load_schema(filename: str, schema, valid_test_files, logger: SystemLogger):
    file_path = filename.resolve().as_uri()[7:]
    try:
        test_definition = load_definition(file_path, schema)
        logger.loading_file_ok(filename)
        valid_test_files.append(file_path)
        return test_definition
    except Exception as e:
        logger.loading_file_error(filename, e)


def load_definition(file_path, schema):
    with open(file_path, 'r') as stream:
        safe_load = yaml.safe_load(stream)
        return schema.load(safe_load)


def load_profile_files(config: Configuration, logger: SystemLogger):
    logger.loading_profile_files()
    schemas = load_schemas(config=config,
                           logger=logger,
                           file_name=config.profile_files_re,
                           schema=ProfileSchema(),
                           template=True)

    for schema in schemas:
        profiles[schema.name] = schema
        logger.loaded_profile(schema.name)

    return profiles
