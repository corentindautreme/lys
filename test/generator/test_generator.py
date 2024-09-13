import unittest

from unittest.mock import patch

from generator.generator import Generator

class GeneratorTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with patch.multiple(Generator, __abstractmethods__=set()):
            self.generator = Generator()


    # TODO Add test cases for include_comments = false
    # Add test cases for generator.get_live_watch_links_string with include_comments=True/False + include_link_count != None down to 0
    def test_when_getting_watch_link_string_for_recommended_link_should_generate_string_without_comment(self):
        watch_link = {'link': 'https://svt.se/melodifestivalen', 'comment': 'Recommended link'}
        s = self.generator.get_single_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen")


    def test_when_getting_watch_link_string_for_link_without_comment_should_generate_string_without_comment(self):
        watch_link = {'link': 'https://svt.se/melodifestivalen'}
        s = self.generator.get_single_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen")


    def test_when_getting_watch_link_string_for_link_with_empty_comment_should_generate_string_without_comment(self):
        watch_link = {'link': 'https://svt.se/melodifestivalen', 'comment': ''}
        s = self.generator.get_single_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen")


    def test_when_getting_watch_link_string_for_link_with_comment_should_generate_string_with_comment(self):
        watch_link = {'link': 'https://svt.se/melodifestivalen', 'comment': 'English commentary'}
        s = self.generator.get_single_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen (English commentary)")


    def test_when_getting_watch_link_string_for_geoblocked_recommended_link_should_generate_string_with_geoblocked_comment(self):
        watch_link = {
            'link': 'https://svt.se/melodifestivalen',
            'comment': 'Recommended link',
            'geoblocked': 1
        }
        s = self.generator.get_single_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen (geoblocked)")


    def test_when_getting_watch_link_string_for_recommended_link_requiring_account_should_generate_string_with_account_required_comment(self):
        watch_link = {
            'link': 'https://svt.se/melodifestivalen',
            'comment': 'Recommended link',
            'accountRequired': 1
        }
        s = self.generator.get_single_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen (account required: see https://lyseurovision.github.io/help.html#account-Sweden)")


    def test_when_getting_watch_link_string_for_geoblocked_recommended_link_requiring_account_should_generate_string_with_geoblocked_and_account_required_comments(self):
        watch_link = {
            'link': 'https://svt.se/melodifestivalen',
            'comment': 'Recommended link',
            'accountRequired': 1,
            'geoblocked': 1
        }
        s = self.generator.get_single_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen (geoblocked, account required: see https://lyseurovision.github.io/help.html#account-Sweden)")


    def test_when_getting_watch_link_string_for_geoblocked_link_with_comment_should_generate_string_with_link_comment_and_geoblocked_comment(self):
        watch_link = {
            'link': 'https://svt.se/melodifestivalen',
            'comment': 'Swedish sign language',
            'geoblocked': 1
        }
        s = self.generator.get_single_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen (Swedish sign language)(geoblocked)")


    def test_when_getting_watch_link_string_for_link_with_comment_requiring_account_should_generate_string_with_link_and_account_required_comments(self):
        watch_link = {
            'link': 'https://svt.se/melodifestivalen',
            'comment': 'Finnish commentary',
            'accountRequired': 1
        }
        s = self.generator.get_single_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen (Finnish commentary)(account required: see https://lyseurovision.github.io/help.html#account-Sweden)")


    def test_when_getting_watch_link_string_for_geoblocked_link_with_comment_that_requires_account_should_generate_string_with_link_comment_and_geoblocked_and_account_required_comments(self):
        watch_link = {
            'link': 'https://svt.se/melodifestivalen',
            'comment': 'Swedish sign language',
            'accountRequired': 1,
            'geoblocked': 1
        }
        s = self.generator.get_single_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen (Swedish sign language)(geoblocked, account required: see https://lyseurovision.github.io/help.html#account-Sweden)")


    def test_when_getting_shortened_watch_link_string_for_recommended_link_should_generate_string_with_shortened_url(self):
        self.generator.shorten_urls = True
        watch_link = {'link': 'https://svt.se/melodifestivalen', 'comment': 'Recommended link'}
        s = self.generator.get_single_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "svt.se")
        self.generator.shorten_urls = False


    def test_when_getting_shortened_watch_link_string_for_link_with_comment_that_requires_account_should_generate_string_with_shortened_urls_and_comments(self):
        self.generator.shorten_urls = True
        watch_link = {
            'link': 'https://svt.se/melodifestivalen/live/english/123',
            'comment': 'English commentary',
            'accountRequired': 1
        }
        s = self.generator.get_single_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "svt.se (English commentary)(account required: see lyseurovision.github.io)")
        self.generator.shorten_urls = False


    def test_when_getting_shortened_watch_link_string_for_geoblocked_link_with_comment_that_requires_account_should_generate_string_with_shortened_urls_and_comments(self):
        self.generator.shorten_urls = True
        watch_link = {
            'link': 'https://svt.se/melodifestivalen/live/english/123',
            'comment': 'Swedish sign language',
            'accountRequired': 1,
            'geoblocked': 1
        }
        s = self.generator.get_single_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "svt.se (Swedish sign language)(geoblocked, account required: see lyseurovision.github.io)")
        self.generator.shorten_urls = False
