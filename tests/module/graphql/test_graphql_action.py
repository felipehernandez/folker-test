"""GraphQL execution against a real local HTTP server, so that the `gql` client itself is exercised
(introspection, query validation, transport) and the tests stay valid across a `gql` upgrade (DEP-08).

The server answers the introspection query with `introspection.json` (the schema below) and every
other request with whatever the test configured.
"""
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest

from folker.model import Context
from folker.module.graphql.action import GraphQLStageAction

# The schema `introspection.json` was generated from:
#   type Query { hello(name: String): String  user: User }
#   type User { id: ID  name: String }
#   type Mutation { setGreeting(text: String!): String }
INTROSPECTION = json.loads((Path(__file__).parent / 'introspection.json').read_text())


class FakeGraphQLServer:
    def __init__(self):
        self.requests = []          # (path, headers, json body), introspection included
        self.answer = lambda query: (200, {'data': {}})
        server = self
        self.threads = []

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                server.requests.append((self.path, dict(self.headers), body))
                if '__schema' in body['query']:
                    status, payload = 200, INTROSPECTION
                else:
                    status, payload = server.answer(body['query'])
                raw = json.dumps(payload).encode()
                self.send_response(status)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

            def log_message(self, *args):
                pass

        self.httpd = HTTPServer(('127.0.0.1', 0), Handler)
        self.url = f'http://127.0.0.1:{self.httpd.server_port}'
        thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        thread.start()
        self.threads.append(thread)

    @property
    def queries(self):
        return [(path, headers, body['query'])
                for path, headers, body in self.requests if '__schema' not in body['query']]

    def close(self):
        self.httpd.shutdown()
        self.httpd.server_close()


@pytest.fixture
def server():
    fake = FakeGraphQLServer()
    yield fake
    fake.close()


def execute(logger, server, uri=None, **fields):
    action = GraphQLStageAction(host=server.url, uri=uri, **fields)
    return action.execute(logger=logger, context=Context())


@pytest.mark.action_graphql
class TestGraphQLQuery:
    def test_the_response_is_saved(self, server, plain_console_test_logger_on_trace):
        server.answer = lambda query: (200, {'data': {'hello': 'hi there'}})

        context = execute(plain_console_test_logger_on_trace, server, query='hello')

        assert context.stage_variables['response'] == {'hello': 'hi there'}
        assert 'elapsed_time' in context.stage_variables

    def test_the_query_is_wrapped_in_a_named_query_operation(
            self, server, plain_console_test_logger_on_trace):
        execute(plain_console_test_logger_on_trace, server, query='hello(name: "folker")')

        (_, _, sent), = server.queries
        assert 'query Query' in sent and 'hello(name: "folker")' in sent

    def test_a_nested_selection(self, server, plain_console_test_logger_on_trace):
        server.answer = lambda query: (200, {'data': {'user': {'id': '1', 'name': 'folker'}}})

        context = execute(plain_console_test_logger_on_trace, server, query='user { id name }')

        assert context.stage_variables['response'] == {'user': {'id': '1', 'name': 'folker'}}

    def test_the_request_is_a_json_post_to_the_host(self, server,
                                                    plain_console_test_logger_on_trace):
        execute(plain_console_test_logger_on_trace, server, query='hello')

        (path, headers, _), = server.queries
        assert path == '/'
        assert headers['Content-type'] == 'application/json'

    def test_the_uri_is_appended_to_the_host(self, server, plain_console_test_logger_on_trace):
        execute(plain_console_test_logger_on_trace, server, uri='graphql', query='hello')

        # the introspection request and the query
        assert {request[0] for request in server.requests} == {'/graphql'}

    def test_the_schema_is_fetched_before_the_query(self, server,
                                                    plain_console_test_logger_on_trace):
        execute(plain_console_test_logger_on_trace, server, query='hello')

        assert '__schema' in server.requests[0][2]['query']
        assert len(server.requests) == 2


@pytest.mark.action_graphql
class TestGraphQLMutation:
    def test_the_mutation_is_sent_and_its_response_saved(
            self, server, plain_console_test_logger_on_trace):
        server.answer = lambda query: (200, {'data': {'setGreeting': 'done'}})

        context = execute(plain_console_test_logger_on_trace, server,
                          mutation='setGreeting(text: "hello")')

        (_, _, sent), = server.queries
        assert 'mutation Mutation' in sent and 'setGreeting(text: "hello")' in sent
        assert context.stage_variables['response'] == {'setGreeting': 'done'}

    def test_a_query_wins_over_a_mutation(self, server, plain_console_test_logger_on_trace):
        execute(plain_console_test_logger_on_trace, server, query='hello',
                mutation='setGreeting(text: "x")')

        (_, _, sent), = server.queries
        assert 'query Query' in sent and 'mutation' not in sent


@pytest.mark.action_graphql
class TestGraphQLFailures:
    """There is no error handling: a failure ends the test through the stage"""

    def test_a_query_that_does_not_match_the_schema_raises_without_being_sent(
            self, server, plain_console_test_logger_on_trace):
        with pytest.raises(Exception):
            execute(plain_console_test_logger_on_trace, server, query='doesNotExist')

        assert server.queries == []

    def test_a_server_error_raises(self, server, plain_console_test_logger_on_trace):
        server.answer = lambda query: (500, {'errors': [{'message': 'boom'}]})

        with pytest.raises(Exception):
            execute(plain_console_test_logger_on_trace, server, query='hello')

    def test_errors_in_the_response_raise(self, server, plain_console_test_logger_on_trace):
        server.answer = lambda query: (200, {'errors': [{'message': 'resolver failed'}],
                                             'data': None})

        with pytest.raises(Exception, match='resolver failed'):
            execute(plain_console_test_logger_on_trace, server, query='hello')

    def test_an_unreachable_server_raises(self, server, plain_console_test_logger_on_trace):
        url = server.url
        server.close()

        with pytest.raises(Exception):
            GraphQLStageAction(host=url, query='hello', timeout=2).execute(
                logger=plain_console_test_logger_on_trace, context=Context())
