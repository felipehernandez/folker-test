from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from folker.logger.logger import TestLogger
from folker.model.context import Context
from folker.model.stage.action import Action
from folker.util.decorator import timed_action, resolvable_variables, loggable


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

    def mandatory_fields(self) -> [str]:
        return [
            'host'
        ]

    def validate_specific(self, missing_fields):
        if (not hasattr(self, 'query') or not self.__getattribute__('query')) and \
                (not hasattr(self, 'mutation') or not self.__getattribute__('mutation')):
            missing_fields.extend(['action.query', 'action.mutation'])

        return missing_fields

    @loggable
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
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

        context.save_on_stage('response', response)

        return context

    def _build_url(self):
        return (self.host + '/' + self.uri) if self.uri else self.host
