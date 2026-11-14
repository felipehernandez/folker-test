"""Protobuf execution with real generated messages: a small .proto is compiled at test time with
the same `grpc_tools.protoc` the product uses (see `folker/load/protos.py`)."""
import subprocess
import sys

import pytest

from folker.logger import TestLogger
from folker.model import Context
from folker.module.protobuf.action import ProtobufStageCreateAction, ProtobufStageLoadAction

PROTO = '''syntax = "proto3";
package folkerprobe;

message Address { string city = 1; }

message Person {
  string name = 1;
  int32 age = 2;
  repeated string tags = 3;
  Address address = 4;
}
'''
PACKAGE = 'folker_protobuf_probe'


@pytest.fixture(scope='module', autouse=True)
def generated_messages(tmp_path_factory):
    directory = tmp_path_factory.mktemp('protos')
    (directory / f'{PACKAGE}.proto').write_text(PROTO)
    subprocess.run([sys.executable, '-m', 'grpc_tools.protoc', f'-I{directory}',
                    f'--python_out={directory}', str(directory / f'{PACKAGE}.proto')],
                   check=True, capture_output=True)
    sys.path.insert(0, str(directory))
    yield
    sys.path.remove(str(directory))
    sys.modules.pop(f'{PACKAGE}_pb2', None)


@pytest.fixture
def logger(mocker):
    return mocker.Mock(spec=TestLogger)


def create(logger, data, clazz='Person', package=PACKAGE, context=None):
    return ProtobufStageCreateAction(method='CREATE', package=package, clazz=clazz, data=data) \
        .execute(logger=logger, context=context or Context())


def load(logger, message, clazz='Person', package=PACKAGE):
    return ProtobufStageLoadAction(method='LOAD', package=package, clazz=clazz, message=message) \
        .execute(logger=logger, context=Context())


@pytest.mark.action_protobuf
class TestProtobufCreate:
    def test_the_message_is_built_from_the_data(self, logger):
        context = create(logger, {'name': 'folker', 'age': 7, 'tags': ['a', 'b'],
                                  'address': {'city': 'Madrid'}})

        message = context.stage_variables['proto_object']
        assert (message.name, message.age, list(message.tags), message.address.city) \
            == ('folker', 7, ['a', 'b'], 'Madrid')
        assert 'error' not in context.stage_variables

    def test_the_message_is_serialised_in_the_three_forms(self, logger):
        context = create(logger, {'name': 'abc'})

        assert context.stage_variables['proto_serialize_str'] == b'\n\x03abc'
        assert context.stage_variables['proto_serialize_utf8'] == '\n\x03abc'
        assert b'"name": "abc"' in context.stage_variables['proto_serialize_json']

    def test_a_message_that_is_not_valid_utf8_has_an_empty_utf8_form(self, logger):
        context = create(logger, {'age': 200})   # varint 0xc8: not valid utf-8

        assert context.stage_variables['proto_serialize_str'] == b'\x10\xc8\x01'
        assert context.stage_variables['proto_serialize_utf8'] == ''

    def test_variables_are_resolved_in_the_data(self, logger):
        context = create(logger, {'name': '${who}'},
                         context=Context(test_variables={'who': 'folker'}))

        assert context.stage_variables['proto_object'].name == 'folker'

    @pytest.mark.parametrize('data, expected', [
        ({'nope': 1}, 'nope'),                    # a field the message does not have
        ({'age': 'not a number'}, 'age'),         # a value of the wrong type
    ], ids=['unknown field', 'wrong type'])
    def test_data_that_does_not_fit_the_message_is_reported(self, logger, data, expected):
        context = create(logger, data)

        assert expected in str(context.stage_variables['error'])
        logger.action_error.assert_called_once()
        assert 'proto_object' not in context.stage_variables

    def test_a_message_class_that_does_not_exist_is_reported(self, logger):
        context = create(logger, {'name': 'x'}, clazz='NoSuchMessage')

        assert isinstance(context.stage_variables['error'], AttributeError)

    def test_a_package_that_does_not_exist_is_reported(self, logger):
        context = create(logger, {'name': 'x'}, package='folker_no_such_package')

        assert isinstance(context.stage_variables['error'], ModuleNotFoundError)


@pytest.mark.action_protobuf
class TestProtobufLoad:
    def test_a_serialised_message_is_loaded_in_the_three_forms(self, logger):
        context = load(logger, '\n\x03abc')

        message = context.stage_variables['proto_object']
        assert message.name == 'abc'
        assert context.stage_variables['proto_dict'] == {'name': 'abc'}
        assert '"name": "abc"' in context.stage_variables['proto_json']
        assert 'error' not in context.stage_variables

    def test_what_create_produced_can_be_loaded_back(self, logger):
        created = create(logger, {'name': 'folker', 'tags': ['x']})

        loaded = load(logger, created.stage_variables['proto_serialize_utf8'])

        assert loaded.stage_variables['proto_dict'] == {'name': 'folker', 'tags': ['x']}

    def test_an_empty_message_loads_as_an_empty_object(self, logger):
        context = load(logger, '')

        assert context.stage_variables['proto_dict'] == {}

    def test_bytes_that_are_not_a_message_are_reported(self, logger):
        context = load(logger, '\xff\xff\xff')

        assert 'error' in context.stage_variables
        logger.action_error.assert_called_once()
        assert 'proto_object' not in context.stage_variables

    def test_a_message_class_that_does_not_exist_is_reported(self, logger):
        context = load(logger, '\n\x03abc', clazz='NoSuchMessage')

        assert isinstance(context.stage_variables['error'], AttributeError)
