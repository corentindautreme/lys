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


    def test_when_getting_watch_link_string_for_link_without_including_comments_should_generate_string_without_comment(self):
        watch_link = {'link': 'https://svt.se/melodifestivalen', 'comment': 'English commentary'}
        s = self.generator.get_single_watch_link_string(watch_link, country="Sweden", include_comments=False)
        self.assertEqual(s, "https://svt.se/melodifestivalen")


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
    

    def test_when_getting_watch_links_string_for_all_live_links_in_event_should_include_all_links_and_comments(self):
        event = {
            "dateTimeCet": "2024-03-09T20:00:00",
            "country": "Sweden",
            "name": "Melodifestivalen",
            "stage": "Final",
            "watchLinks": [
                {
                    "accountRequired": 0,
                    "castable": 1,
                    "channel": "SVT1",
                    "comment": "Recommended link",
                    "geoblocked": 0,
                    "link": "https://www.svtplay.se/video/jw2BJEy/melodifestivalen/final",
                    "live": 1,
                    "replayable": 1
                },
                {
                    "accountRequired": 0,
                    "castable": 1,
                    "channel": "SVT1",
                    "comment": "English commentary",
                    "geoblocked": 0,
                    "link": "https://www.svtplay.se/video/jQ72NXZ/melodifestivalen/melodifestivalen-2024-the-final",
                    "live": 1,
                    "replayable": 1
                },
                {
                    "accountRequired": 0,
                    "castable": 1,
                    "channel": "SVT1",
                    "geoblocked": 0,
                    "link": "https://www.svtplay.se/melodifestivalen",
                    "live": 1,
                    "replayable": 0
                },
                {
                    "accountRequired": 0,
                    "castable": 1,
                    "channel": "SVT1",
                    "geoblocked": 0,
                    "link": "https://www.svtplay.se/melodifestivalen/replay",
                    "live": 0,
                    "replayable": 1
                }
            ]
        }
        s = self.generator.get_live_watch_links_string(event)
        self.assertEqual(s, "https://www.svtplay.se/video/jw2BJEy/melodifestivalen/final OR https://www.svtplay.se/video/jQ72NXZ/melodifestivalen/melodifestivalen-2024-the-final (English commentary) OR https://www.svtplay.se/melodifestivalen")
    

    def test_when_getting_watch_links_string_for_all_live_links_in_event_without_comments_should_include_all_links_without_comments(self):
        event = {
            "dateTimeCet": "2024-03-09T20:00:00",
            "country": "Sweden",
            "name": "Melodifestivalen",
            "stage": "Final",
            "watchLinks": [
                {
                    "accountRequired": 0,
                    "castable": 1,
                    "channel": "SVT1",
                    "comment": "Recommended link",
                    "geoblocked": 0,
                    "link": "https://www.svtplay.se/video/jw2BJEy/melodifestivalen/final",
                    "live": 1,
                    "replayable": 1
                },
                {
                    "accountRequired": 0,
                    "castable": 1,
                    "channel": "SVT1",
                    "comment": "English commentary",
                    "geoblocked": 0,
                    "link": "https://www.svtplay.se/video/jQ72NXZ/melodifestivalen/melodifestivalen-2024-the-final",
                    "live": 1,
                    "replayable": 1
                },
                {
                    "accountRequired": 0,
                    "castable": 1,
                    "channel": "SVT1",
                    "geoblocked": 0,
                    "link": "https://www.svtplay.se/melodifestivalen",
                    "live": 1,
                    "replayable": 0
                },
                {
                    "accountRequired": 0,
                    "castable": 1,
                    "channel": "SVT1",
                    "geoblocked": 0,
                    "link": "https://www.svtplay.se/melodifestivalen/replay",
                    "live": 0,
                    "replayable": 1
                }
            ]
        }
        s = self.generator.get_live_watch_links_string(event, include_comments=False)
        self.assertEqual(s, "https://www.svtplay.se/video/jw2BJEy/melodifestivalen/final OR https://www.svtplay.se/video/jQ72NXZ/melodifestivalen/melodifestivalen-2024-the-final OR https://www.svtplay.se/melodifestivalen")
    

    def test_when_getting_watch_links_string_for_the_2_first_live_links_in_event_without_comments_should_include_2_links_without_comments(self):
        event = {
            "dateTimeCet": "2024-03-09T20:00:00",
            "country": "Sweden",
            "name": "Melodifestivalen",
            "stage": "Final",
            "watchLinks": [
                {
                    "accountRequired": 0,
                    "castable": 1,
                    "channel": "SVT1",
                    "comment": "Recommended link",
                    "geoblocked": 0,
                    "link": "https://www.svtplay.se/video/jw2BJEy/melodifestivalen/final",
                    "live": 1,
                    "replayable": 1
                },
                {
                    "accountRequired": 0,
                    "castable": 1,
                    "channel": "SVT1",
                    "comment": "English commentary",
                    "geoblocked": 0,
                    "link": "https://www.svtplay.se/video/jQ72NXZ/melodifestivalen/melodifestivalen-2024-the-final",
                    "live": 1,
                    "replayable": 1
                },
                {
                    "accountRequired": 0,
                    "castable": 1,
                    "channel": "SVT1",
                    "geoblocked": 0,
                    "link": "https://www.svtplay.se/melodifestivalen",
                    "live": 1,
                    "replayable": 0
                },
                {
                    "accountRequired": 0,
                    "castable": 1,
                    "channel": "SVT1",
                    "geoblocked": 0,
                    "link": "https://www.svtplay.se/melodifestivalen/replay",
                    "live": 0,
                    "replayable": 1
                }
            ]
        }
        s = self.generator.get_live_watch_links_string(event, include_comments=False, include_link_count=2)
        self.assertEqual(s, "https://www.svtplay.se/video/jw2BJEy/melodifestivalen/final OR https://www.svtplay.se/video/jQ72NXZ/melodifestivalen/melodifestivalen-2024-the-final")
    

    def test_when_getting_watch_links_string_for_0_live_link_in_event_should_not_include_any_link(self):
        event = {
            "dateTimeCet": "2024-03-09T20:00:00",
            "country": "Sweden",
            "name": "Melodifestivalen",
            "stage": "Final",
            "watchLinks": [
                {
                    "accountRequired": 0,
                    "castable": 1,
                    "channel": "SVT1",
                    "comment": "Recommended link",
                    "geoblocked": 0,
                    "link": "https://www.svtplay.se/video/jw2BJEy/melodifestivalen/final",
                    "live": 1,
                    "replayable": 1
                },
                {
                    "accountRequired": 0,
                    "castable": 1,
                    "channel": "SVT1",
                    "comment": "English commentary",
                    "geoblocked": 0,
                    "link": "https://www.svtplay.se/video/jQ72NXZ/melodifestivalen/melodifestivalen-2024-the-final",
                    "live": 1,
                    "replayable": 1
                },
                {
                    "accountRequired": 0,
                    "castable": 1,
                    "channel": "SVT1",
                    "geoblocked": 0,
                    "link": "https://www.svtplay.se/melodifestivalen",
                    "live": 1,
                    "replayable": 0
                },
                {
                    "accountRequired": 0,
                    "castable": 1,
                    "channel": "SVT1",
                    "geoblocked": 0,
                    "link": "https://www.svtplay.se/melodifestivalen/replay",
                    "live": 0,
                    "replayable": 1
                }
            ]
        }
        s = self.generator.get_live_watch_links_string(event, include_link_count=0)
        self.assertEqual(s, "")
