from unittest import TestCase


class TestParseTitle(TestCase):
    def test_parse_title_without_space(self):
        from common import parse_title

        result = parse_title('title[eBook]')

        self.assertEquals('title', result)

    def test_parse_title_with_space(self):
        from common import parse_title

        result = parse_title('title [eBook]')

        self.assertEqual('title', result)

    def test_parse_title_repeated_match(self):
        from common import parse_title

        result = parse_title('title [eBook] [eBook]')

        self.assertEqual('title', result)

    def test_parse_title_repeated_match_without_space_between(self):
        from common import parse_title

        result = parse_title('title [eBook][eBook]')

        self.assertEqual('title', result)


class TestBuildHeaders(TestCase):
    def test_build_headers(self):
        from common import build_headers

        result = build_headers('referer', 'user-agent')
        target = {'Referer': 'referer', 'User-Agent': 'user-agent'}

        self.assertDictEqual(target, result)
