from folker.module.rest.action import RestStageAction, RestMethod


class TestRestActionEnrichment:
    def test_enrich_empty_get(self):
        original = RestStageAction(method=RestMethod.GET.name)
        enrichment = RestStageAction(method=RestMethod.GET.name,
                                     host='a_host')

        enriched = original + enrichment

        assert enriched.method == RestMethod.GET
        assert enriched.host == 'a_host'

    def test_enrich_override_host(self):
        original = RestStageAction(method=RestMethod.GET.name,
                                   host='a_host')
        enrichment = RestStageAction(method=RestMethod.GET.name,
                                     host='another_host')

        enriched = original + enrichment

        assert enriched.method == RestMethod.GET
        assert enriched.host == 'another_host'

    def test_enrich_set_uri(self):
        original = RestStageAction(method=RestMethod.GET.name,
                                   host='a_host')
        enrichment = RestStageAction(method=RestMethod.GET.name,
                                     uri='an_uri')

        enriched = original + enrichment

        assert enriched.method == RestMethod.GET
        assert enriched.host == 'a_host'
        assert enriched.uri == 'an_uri'

    def test_enrich_override_uri(self):
        original = RestStageAction(method=RestMethod.GET.name,
                                   host='a_host',
                                   uri='an_uri')
        enrichment = RestStageAction(method=RestMethod.GET.name,
                                     uri='another_uri')

        enriched = original + enrichment

        assert enriched.method == RestMethod.GET
        assert enriched.host == 'a_host'
        assert enriched.uri == 'another_uri'

    def test_enrich_set_headers(self):
        original = RestStageAction(method=RestMethod.GET.name,
                                   host='a_host')
        enrichment = RestStageAction(method=RestMethod.GET.name,
                                     headers={'a_key': 'a_value'})

        enriched = original + enrichment

        assert enriched.method == RestMethod.GET
        assert enriched.host == 'a_host'
        assert enriched.headers == {'a_key': 'a_value'}

    def test_enrich_override_headers(self):
        original = RestStageAction(method=RestMethod.GET.name,
                                   host='a_host',
                                   headers={'a_key': 'a_value'})
        enrichment = RestStageAction(method=RestMethod.GET.name,
                                     headers={'another_key': 'another_value'})

        enriched = original + enrichment

        assert enriched.method == RestMethod.GET
        assert enriched.host == 'a_host'
        assert enriched.headers == {'a_key': 'a_value',
                                    'another_key': 'another_value'}

    def test_enrich_override_duplicated_headers(self):
        original = RestStageAction(method=RestMethod.GET.name,
                                   host='a_host',
                                   headers={'a_key': 'a_value', 'another_key': 'another_value'})
        enrichment = RestStageAction(method=RestMethod.GET.name,
                                     headers={'a_key': 'a_value',
                                              'and_another_key': 'and_another_value'})

        enriched = original + enrichment

        assert enriched.method == RestMethod.GET
        assert enriched.host == 'a_host'
        assert enriched.headers == {'a_key': 'a_value',
                                    'another_key': 'another_value',
                                    'and_another_key': 'and_another_value'}

    def test_enrich_set_parameters(self):
        original = RestStageAction(method=RestMethod.GET.name,
                                   host='a_host')
        enrichment = RestStageAction(method=RestMethod.GET.name,
                                     params={'a_key': 'a_value'})

        enriched = original + enrichment

        assert enriched.method == RestMethod.GET
        assert enriched.host == 'a_host'
        assert enriched.params == {'a_key': 'a_value'}

    def test_enrich_override_parameters(self):
        original = RestStageAction(method=RestMethod.GET.name,
                                   host='a_host',
                                   params={'a_key': 'a_value'})
        enrichment = RestStageAction(method=RestMethod.GET.name,
                                     params={'another_key': 'another_value'})

        enriched = original + enrichment

        assert enriched.method == RestMethod.GET
        assert enriched.host == 'a_host'
        assert enriched.params == {'a_key': 'a_value',
                                   'another_key': 'another_value'}

    def test_enrich_override_duplicated_parameters(self):
        original = RestStageAction(method=RestMethod.GET.name,
                                   host='a_host',
                                   params={'a_key': 'a_value', 'another_key': 'another_value'})
        enrichment = RestStageAction(method=RestMethod.GET.name,
                                     params={'a_key': 'a_value',
                                             'and_another_key': 'and_another_value'})

        enriched = original + enrichment

        assert enriched.method == RestMethod.GET
        assert enriched.host == 'a_host'
        assert enriched.params == {'a_key': 'a_value',
                                   'another_key': 'another_value',
                                   'and_another_key': 'and_another_value'}

    def test_enrich_set_body(self):
        original = RestStageAction(method=RestMethod.GET.name,
                                   host='a_host')
        enrichment = RestStageAction(method=RestMethod.GET.name,
                                     body='a_body')

        enriched = original + enrichment

        assert enriched.method == RestMethod.GET
        assert enriched.host == 'a_host'
        assert enriched.body == 'a_body'

    def test_enrich_override_body(self):
        original = RestStageAction(method=RestMethod.GET.name,
                                   host='a_host',
                                   body='a_body')
        enrichment = RestStageAction(method=RestMethod.GET.name,
                                     body='another_body')

        enriched = original + enrichment

        assert enriched.method == RestMethod.GET
        assert enriched.host == 'a_host'
        assert enriched.body == 'another_body'

    def test_enrich_set_data(self):
        original = RestStageAction(method=RestMethod.GET.name,
                                   host='a_host')
        enrichment = RestStageAction(method=RestMethod.GET.name,
                                     data='some_data')

        enriched = original + enrichment

        assert enriched.method == RestMethod.GET
        assert enriched.host == 'a_host'
        assert enriched.data == 'some_data'

    def test_enrich_override_data(self):
        original = RestStageAction(method=RestMethod.GET.name,
                                   host='a_host',
                                   data='some_data')
        enrichment = RestStageAction(method=RestMethod.GET.name,
                                     data='another_data')

        enriched = original + enrichment

        assert enriched.method == RestMethod.GET
        assert enriched.host == 'a_host'
        assert enriched.data == 'another_data'

    def test_enrich_set_json_body(self):
        original = RestStageAction(method=RestMethod.GET.name,
                                   host='a_host')
        enrichment = RestStageAction(method=RestMethod.GET.name,
                                     json={'a_key': 'a_value'})

        enriched = original + enrichment

        assert enriched.method == RestMethod.GET
        assert enriched.host == 'a_host'
        assert enriched.body_json == {'a_key': 'a_value'}

    def test_enrich_override_json_body(self):
        original = RestStageAction(method=RestMethod.GET.name,
                                   host='a_host',
                                   json={'a_key': 'a_value'})
        enrichment = RestStageAction(method=RestMethod.GET.name,
                                     json={'another_key': 'another_value'})

        enriched = original + enrichment

        assert enriched.method == RestMethod.GET
        assert enriched.host == 'a_host'
        assert enriched.body_json == {'a_key': 'a_value',
                                      'another_key': 'another_value'}

    def test_enrich_override_duplicated_json_body(self):
        original = RestStageAction(method=RestMethod.GET.name,
                                   host='a_host',
                                   json={'a_key': 'a_value', 'another_key': 'another_value'})
        enrichment = RestStageAction(method=RestMethod.GET.name,
                                     json={'a_key': 'a_value',
                                           'and_another_key': 'and_another_value'})

        enriched = original + enrichment

        assert enriched.method == RestMethod.GET
        assert enriched.host == 'a_host'
        assert enriched.body_json == {'a_key': 'a_value',
                                      'another_key': 'another_value',
                                      'and_another_key': 'and_another_value'}

    def test_enrich_deep_merge_json_body(self):
        original = RestStageAction(method=RestMethod.GET.name,
                                   host='a_host',
                                   json={'key_1': {'key_1_1': 'value_1_1'}})
        enrichment = RestStageAction(method=RestMethod.GET.name,
                                     json={'key_1': {'key_1_2': 'value_1_2'}})

        enriched = original + enrichment

        assert enriched.method == RestMethod.GET
        assert enriched.host == 'a_host'
        assert enriched.body_json == {'key_1': {'key_1_1': 'value_1_1',
                                                'key_1_2': 'value_1_2'}}
