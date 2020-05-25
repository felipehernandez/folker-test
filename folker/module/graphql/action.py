from copy import deepcopy

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.util.decorator import timed_action, resolvable_variables


class GraphQLAction(Action):
    host: str
    uri: str

    query: str
    mutation: str

    def __init__(self,
                 host: str = None,
                 uri: str = None,
                 query: str = None,
                 mutation: str = None,
                 **kargs) -> None:
        super().__init__()

        self.host = host
        self.uri = uri

        self.query = query
        self.mutation = mutation

    def __copy__(self):
        return deepcopy(self)

    def enrich(self, template: 'GraphQLAction'):
        self._set_attribute_if_missing(template, 'host')
        self._set_attribute_if_missing(template, 'uri')
        self._set_attribute_if_missing(template, 'query')
        self._set_attribute_if_missing(template, 'mutation')

    def validate(self):
        missing_fields = []

        if not hasattr(self, 'host') or not self.host:
            missing_fields.append('action.host')
        # if not hasattr(self, 'query') or not self.query:
        #     missing_fields.append('action.query')

        if len(missing_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields)

    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        url = self._build_url()
        query = ''
        if self.query:
            query = 'query Query {{ {} }}'.format(self.query)
        else:
            query = 'mutation Mutation {{ {} }}'.format(self.mutation)

        query = gql(query)

        transport = RequestsHTTPTransport(
            url=url,
            use_json=True,
            headers={
                "Content-type": "application/json",
            },
            verify=False
        )
        client = Client(
            transport=transport,
            fetch_schema_from_transport=True,
        )
        response = client.execute(query)

        stage_context['response'] = response

        return test_context, stage_context

    def _build_url(self):
        return (self.host + '/' + self.uri) if self.uri else self.host
