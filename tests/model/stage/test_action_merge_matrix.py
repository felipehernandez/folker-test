"""Template/stage merge matrix for every action type (TST-08).

A stage that uses a template is merged as `template + stage` (`folker/load/files.py`): the stage
is the enrichment and wins on conflicts. BUG-04 and BUG-05 were fields lost in a hand-written
`__add__`, so each field of each action is checked in the four situations that matter:

    neither defines it / only the template / only the stage / both (the stage wins)

Mappings are merged key by key, sequences are concatenated (template first), and the merge must
never modify the template or the stage it was given.
"""
from collections import namedtuple
from copy import deepcopy

import pytest

from folker.module.code.action import CodeStageAction
from folker.module.file.action import FileMethod, FileStageAction
from folker.module.gcp.pubsub.action import PubSubMethod, PubSubStageAction
from folker.module.gmail.action import GmailStageAction
from folker.module.graphql.action import GraphQLStageAction
from folker.module.grpc.action import GrpcStageAction
from folker.module.kafka.action import KafkaMethod, KafkaStageAction
from folker.module.postgres.action import PostgresMethod, PostgresStageAction
from folker.module.printt.action import PrintStageAction
from folker.module.protobuf.action import ProtobufMethod, ProtobufStageAction
from folker.module.rabbitmq.action import RabbitMQMethod, RabbitMQStageAction
from folker.module.rest.action import RestMethod, RestStageAction
from folker.module.void.action import VoidStageAction
from folker.module.wait.action import WaitStageAction
from folker.module.zookeeper.action import ZookeeperMethod, ZookeeperStageAction

# kwarg: constructor argument; attr: attribute it ends up in; the values are what the template and
# the stage define (and `merged` what a conflict-free merge of both holds, for mappings and sequences).
Scalar = namedtuple('Scalar', 'kwarg attr template stage')
Mapping = namedtuple('Mapping', 'kwarg attr template stage merged conflict_key')
Sequence = namedtuple('Sequence', 'kwarg attr template stage merged')


def scalar(kwarg, template='template-value', stage='stage-value', attr=None):
    return Scalar(kwarg, attr or kwarg, template, stage)


def mapping(kwarg, attr=None):
    return Mapping(kwarg, attr or kwarg,
                   {'only_template': 't', 'shared': 'from-template'},
                   {'only_stage': 's', 'shared': 'from-stage'},
                   {'only_template': 't', 'only_stage': 's', 'shared': 'from-stage'},
                   'shared')


def sequence(kwarg, template=('t1', 't2'), stage=('s1',)):
    return Sequence(kwarg, kwarg, list(template), list(stage), list(template) + list(stage))


ActionSpec = namedtuple('ActionSpec', 'name factory fields')

ACTIONS = [
    ActionSpec('code', CodeStageAction,
               [scalar('module'), scalar('method'), mapping('parameters')]),
    ActionSpec('file', FileStageAction,
               [scalar('file'), scalar('content')]),
    ActionSpec('gmail', GmailStageAction,
               [scalar('credentials_path'), scalar('sender'), scalar('subject'),
                scalar('text'), scalar('html'),
                sequence('recipients'), sequence('hidden_recipients')]),
    ActionSpec('graphql', GraphQLStageAction,
               [scalar('host'), scalar('uri'), scalar('query'), scalar('mutation'),
                scalar('timeout', 5, 9)]),
    ActionSpec('grpc', GrpcStageAction,
               [scalar('host'), scalar('uri'), scalar('package'), scalar('stub'),
                scalar('method'), scalar('data'), scalar('timeout', 5, 9)]),
    ActionSpec('kafka', KafkaStageAction,
               [scalar('host'), scalar('topic'), scalar('key'), scalar('message'),
                scalar('group')]),
    ActionSpec('postgres', PostgresStageAction,
               [scalar('host'), scalar('port'), scalar('user'), scalar('password'),
                scalar('database'), scalar('sql'), scalar('timeout', 5, 9)]),
    ActionSpec('print', PrintStageAction, [scalar('message')]),
    ActionSpec('protobuf', ProtobufStageAction,
               [scalar('package'), scalar('clazz'), scalar('data', {'a': 1}, {'b': 2}),
                scalar('message')]),
    ActionSpec('pubsub', PubSubStageAction,
               [scalar('host'), scalar('project'), scalar('credentials', attr='credentials_path'),
                scalar('topic'), scalar('subscription'), scalar('message'),
                scalar('timeout', 5, 9), mapping('attributes')]),
    ActionSpec('rabbitmq', RabbitMQStageAction,
               [scalar('host'), scalar('port'), scalar('vhost'), scalar('user'),
                scalar('password'), scalar('exchange'), scalar('message'), scalar('queue'),
                scalar('timeout', 5, 9)]),
    ActionSpec('rest', RestStageAction,
               [scalar('host'), scalar('uri'), scalar('body'), scalar('data', {'a': 'b'}, {'c': 'd'}),
                scalar('timeout', 5, 9), mapping('params'), mapping('headers'),
                mapping('authorization')]),
    ActionSpec('wait', WaitStageAction, [scalar('time', 1, 2)]),
    ActionSpec('zookeeper', ZookeeperStageAction,
               [scalar('host'), scalar('node'), scalar('data'), scalar('version', 3, 5),
                scalar('timeout', 5, 9)]),
]

# Scalars a stage must be able to switch off or reset, which a truthiness check cannot do
FLAG_ACTIONS = [
    ('rabbitmq', RabbitMQStageAction, 'ack'),
    ('pubsub', PubSubStageAction, 'ack'),
    ('zookeeper', ZookeeperStageAction, 'ephemeral'),
]

# Known defects, tracked in the improvement plan: (class, test, case id) -> reason. The xfail is
# `strict`, so fixing one makes its test fail until the entry is removed from this table.
KNOWN_DEFECTS = {
    ('TestScalarFields', 'test_only_the_template_defines_it', 'zookeeper.version'):
        'BUG-20: the stage default version -1 is truthy and overrides the template version',
    ('TestFlags', 'test_the_stage_can_switch_it_off', 'rabbitmq.ack'):
        'BUG-19: a falsy value in the stage cannot override the template',
    ('TestFlags', 'test_the_stage_can_switch_it_off', 'pubsub.ack'):
        'BUG-19: a falsy value in the stage cannot override the template',
    ('TestFlags', 'test_the_stage_can_switch_it_off', 'zookeeper.ephemeral'):
        'BUG-19: a falsy value in the stage cannot override the template',
}


@pytest.fixture(autouse=True)
def known_defects(request):
    key = (request.cls.__name__ if request.cls else None,
           request.node.originalname,
           request.node.callspec.id if hasattr(request.node, 'callspec') else None)
    if key in KNOWN_DEFECTS:
        request.applymarker(pytest.mark.xfail(strict=True, reason=KNOWN_DEFECTS[key]))


SCALARS = [pytest.param(spec.factory, field, id=f'{spec.name}.{field.kwarg}')
           for spec in ACTIONS for field in spec.fields if isinstance(field, Scalar)]
MAPPINGS = [pytest.param(spec.factory, field, id=f'{spec.name}.{field.kwarg}')
            for spec in ACTIONS for field in spec.fields if isinstance(field, Mapping)]
SEQUENCES = [pytest.param(spec.factory, field, id=f'{spec.name}.{field.kwarg}')
             for spec in ACTIONS for field in spec.fields if isinstance(field, Sequence)]
FACTORIES = [pytest.param(spec.factory, id=spec.name) for spec in ACTIONS]


def snapshot(action):
    # the validation report has no __eq__ and is not part of what is merged
    return {name: deepcopy(value) for name, value in vars(action).items()
            if name != 'validation_report'}


@pytest.mark.parametrize('factory, field', SCALARS)
class TestScalarFields:
    def test_neither_defines_it(self, factory, field):
        merged = factory() + factory()

        assert getattr(merged, field.attr) == getattr(factory(), field.attr)

    def test_only_the_template_defines_it(self, factory, field):
        merged = factory(**{field.kwarg: field.template}) + factory()

        assert getattr(merged, field.attr) == field.template

    def test_only_the_stage_defines_it(self, factory, field):
        merged = factory() + factory(**{field.kwarg: field.stage})

        assert getattr(merged, field.attr) == field.stage

    def test_both_define_it_and_the_stage_wins(self, factory, field):
        merged = (factory(**{field.kwarg: field.template})
                  + factory(**{field.kwarg: field.stage}))

        assert getattr(merged, field.attr) == field.stage


@pytest.mark.parametrize('factory, field', MAPPINGS)
class TestMappingFields:
    def test_neither_defines_it(self, factory, field):
        assert getattr(factory() + factory(), field.attr) == getattr(factory(), field.attr)

    def test_only_the_template_defines_it(self, factory, field):
        merged = factory(**{field.kwarg: field.template}) + factory()

        assert getattr(merged, field.attr) == field.template

    def test_only_the_stage_defines_it(self, factory, field):
        merged = factory() + factory(**{field.kwarg: field.stage})

        assert getattr(merged, field.attr) == field.stage

    def test_both_define_it_and_are_merged_key_by_key(self, factory, field):
        merged = (factory(**{field.kwarg: field.template})
                  + factory(**{field.kwarg: field.stage}))

        assert getattr(merged, field.attr) == field.merged
        assert getattr(merged, field.attr)[field.conflict_key] == field.stage[field.conflict_key]


@pytest.mark.parametrize('factory, field', SEQUENCES)
class TestSequenceFields:
    def test_neither_defines_it(self, factory, field):
        assert getattr(factory() + factory(), field.attr) == []

    def test_only_the_template_defines_it(self, factory, field):
        merged = factory(**{field.kwarg: field.template}) + factory()

        assert getattr(merged, field.attr) == field.template

    def test_only_the_stage_defines_it(self, factory, field):
        merged = factory() + factory(**{field.kwarg: field.stage})

        assert getattr(merged, field.attr) == field.stage

    def test_both_define_it_and_are_concatenated_template_first(self, factory, field):
        merged = (factory(**{field.kwarg: field.template})
                  + factory(**{field.kwarg: field.stage}))

        assert getattr(merged, field.attr) == field.merged


class TestKafkaHeaders:
    """Kafka headers are given as a mapping but stored as a list of (key, bytes) pairs"""

    def test_template_headers_come_first_and_the_stage_ones_are_added(self):
        merged = (KafkaStageAction(headers={'a': '1'}) + KafkaStageAction(headers={'b': '2'}))

        assert merged.headers == [('a', b'1'), ('b', b'2')]

    def test_only_one_side_defines_them(self):
        assert (KafkaStageAction(headers={'a': '1'}) + KafkaStageAction()).headers == [('a', b'1')]
        assert (KafkaStageAction() + KafkaStageAction(headers={'b': '2'})).headers == [('b', b'2')]


class TestRestJsonBody:
    """The JSON body is merged recursively, unlike the other mappings"""

    def test_only_one_side_defines_it(self):
        assert (RestStageAction(json={'a': 1}) + RestStageAction()).body_json == {'a': 1}
        assert (RestStageAction() + RestStageAction(json={'b': 2})).body_json == {'b': 2}

    def test_both_are_merged_recursively_and_the_stage_wins(self):
        template = RestStageAction(json={'user': {'name': 'template', 'age': 1}, 'only': 't'})
        stage = RestStageAction(json={'user': {'name': 'stage'}, 'extra': 's'})

        merged = template + stage

        assert merged.body_json == {'user': {'name': 'stage', 'age': 1},
                                    'only': 't', 'extra': 's'}


@pytest.mark.parametrize('name, factory, attribute', FLAG_ACTIONS,
                         ids=[f'{name}.{attribute}' for name, _, attribute in FLAG_ACTIONS])
class TestFlags:
    def test_only_the_template_sets_it(self, name, factory, attribute):
        assert getattr(factory(**{attribute: True}) + factory(), attribute)

    def test_only_the_stage_sets_it(self, name, factory, attribute):
        assert getattr(factory() + factory(**{attribute: True}), attribute)

    def test_the_stage_can_switch_it_off(self, name, factory, attribute):
        merged = factory(**{attribute: True}) + factory(**{attribute: False})

        assert not getattr(merged, attribute)


@pytest.mark.parametrize('factory', FACTORIES)
class TestMergeContract:
    def full(self, factory):
        spec = next(spec for spec in ACTIONS if spec.factory is factory)
        template = {f.kwarg: getattr(f, 'template') for f in spec.fields}
        stage = {f.kwarg: getattr(f, 'stage') for f in spec.fields}
        return factory(**template), factory(**stage)

    def test_neither_operand_is_modified(self, factory):
        template, stage = self.full(factory)
        template_before, stage_before = snapshot(template), snapshot(stage)

        template + stage

        assert snapshot(template) == template_before
        assert snapshot(stage) == stage_before

    def test_the_result_does_not_share_state_with_the_template(self, factory):
        # A template is merged into every stage that references it, so they must not alias it.
        # Sharing with the stage is harmless: the merged action replaces the stage.
        template, stage = self.full(factory)

        merged = template + stage

        assert merged is not template
        for name, value in vars(merged).items():
            if isinstance(value, (dict, list)) and value:
                assert value is not vars(template)[name]

    def test_void_stage_leaves_the_template_unchanged(self, factory):
        template, _ = self.full(factory)

        merged = template + VoidStageAction()

        assert merged is not template
        assert snapshot(merged) == snapshot(template)

    def test_void_template_gives_the_stage(self, factory):
        _, stage = self.full(factory)

        merged = VoidStageAction() + stage

        assert merged is not stage
        assert type(merged) is type(stage)
        assert snapshot(merged) == snapshot(stage)


# `method` is not merged consistently. These pin the current behaviour so that a change is
# deliberate (BUG-21): code and grpc take the stage's method, the actions below keep the template's.
METHOD_ENUMS = [
    ('rest', RestStageAction, RestMethod),
    ('kafka', KafkaStageAction, KafkaMethod),
    ('postgres', PostgresStageAction, PostgresMethod),
    ('rabbitmq', RabbitMQStageAction, RabbitMQMethod),
    ('zookeeper', ZookeeperStageAction, ZookeeperMethod),
    ('pubsub', PubSubStageAction, PubSubMethod),
    ('file', FileStageAction, FileMethod),
    ('protobuf', ProtobufStageAction, ProtobufMethod),
]


class TestMethod:
    @pytest.mark.parametrize('name, factory, methods', METHOD_ENUMS,
                             ids=[name for name, _, _ in METHOD_ENUMS])
    def test_the_template_method_is_kept_when_the_stage_names_another(self, name, factory, methods):
        first, second = list(methods)[:2]

        merged = factory(method=first.name) + factory(method=second.name)

        assert merged.method is first

    @pytest.mark.parametrize('name, factory, methods', METHOD_ENUMS,
                             ids=[name for name, _, _ in METHOD_ENUMS])
    def test_a_stage_without_method_keeps_the_template_method(self, name, factory, methods):
        first = list(methods)[0]

        assert (factory(method=first.name) + factory()).method is first

    @pytest.mark.parametrize('factory', [CodeStageAction, GrpcStageAction], ids=['code', 'grpc'])
    def test_the_stage_method_wins_for_actions_that_merge_it(self, factory):
        assert (factory(method='template') + factory(method='stage')).method == 'stage'
