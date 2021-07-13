from folker.module.graphql.action import GraphQLStageAction


class TestGraphQLStageActionValidation:
    def test_validate_empty(self):
        action = GraphQLStageAction()

        assert not action
        assert not action.validation_report
        assert 'action.host' in action.validation_report.missing_fields

    def test_correct_query(self):
        action = GraphQLStageAction(host='a_host',
                                    uri='an_uri',
                                    query='a_query')

        assert action
        assert action.validation_report

    def test_correct_mutation(self):
        action = GraphQLStageAction(host='a_host',
                                    uri='an_uri',
                                    mutation='a_mutation')

        assert action
        assert action.validation_report

    def test_incorrect(self):
        action = GraphQLStageAction(host='a_host',
                                    uri='an_uri')

        assert not action
        assert not action.validation_report
        assert 'action.query' in action.validation_report.missing_fields
        assert 'action.mutation' in action.validation_report.missing_fields
