import time
from copy import deepcopy

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.util.variable import replace_variables


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

    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        start = time.time()

        url = self._build_url(test_context, stage_context)
        query = ''
        if self.query:
            query = 'query Query {{ {} }}'.format(self.query)
        else:
            query = 'mutation Mutation {{ {} }}'.format(self.mutation)

        resolved_query = replace_variables(test_context=test_context,
                                           stage_context=stage_context,
                                           text=query)
        query = gql(resolved_query)

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
        # query.definitions[0].operation = 'mutation'
        response = client.execute(query)

        stage_context['response'] = response

        end = time.time()
        stage_context['elapsed_time'] = int((end - start) * 1000)

        return test_context, stage_context

    def _build_url(self, test_context: dict, stage_context: dict):
        url = self.host
        if self.uri:
            url = url + '/' + self.uri
        return replace_variables(test_context=test_context,
                                 stage_context=stage_context,
                                 text=url)
