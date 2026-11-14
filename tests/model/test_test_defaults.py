from folker.model import Test as FolkerTest  # not `Test`: pytest would try to collect it


class TestTestDefaults:
    def test_default_foreach_is_empty(self):
        assert FolkerTest().foreach == {}

    # BUG-08: `foreach: dict = {}` was a shared default, so every Test built without a
    # foreach pointed at the same dict.
    def test_default_foreach_is_not_shared_between_tests(self):
        first = FolkerTest()
        second = FolkerTest()

        first.foreach['key'] = ['value']

        assert second.foreach == {}
        assert FolkerTest().foreach == {}

    def test_default_foreach_is_not_shared_when_empty_is_passed(self):
        first = FolkerTest(foreach={})
        second = FolkerTest(foreach={})

        first.foreach['key'] = ['value']

        assert second.foreach == {}

    def test_given_foreach_is_kept(self):
        foreach = {'key': ['value1', 'value2']}

        assert FolkerTest(foreach=foreach).foreach == {'key': ['value1', 'value2']}

    def test_default_tags_and_stages_are_not_shared_between_tests(self):
        first = FolkerTest()
        second = FolkerTest()

        first.tags.append('a_tag')
        first.stages.append('a_stage')

        assert second.tags == []
        assert second.stages == []
