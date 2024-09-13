import unittest

from generator.five_minute_generator import FiveMinuteGenerator

class FiveMinuteGeneratorGeneratorTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generator = FiveMinuteGenerator(formatter=None)
        self.maxDiff = 1000


    def test_when_events_fit_in_one_post_then_should_generate_one_post(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}]
        posts = self.generator.generate_thread(events)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se)")


    def test_when_events_do_not_fit_in_one_post_then_should_generate_multiple_posts(self):
        events = [
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.no', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.ee', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Finland', 'name': 'Uuden Musiikin Kilpailu', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.fi', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Serbia', 'name': 'Beovizija', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.rs', 'comment': 'Recommended link', 'live': 1}]}
        ]
        self.generator.thread_indicator = True
        posts = self.generator.generate_thread(events)
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0], "\U0001F6A8 5 MINUTES REMINDER! (thread \U00002B07\U0000FE0F)\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se)\n---------\n\U0001F1F3\U0001F1F4 Melodi Grand Prix - Final (https://somereallyreallyreallyreallylongurl.no)\n---------\n\U0001F1EA\U0001F1EA Eesti Laul - Final (https://somereallyreallyreallyreallylongurl.ee)")
        self.assertEqual(posts[1], "\U0001F6A8 5 MINUTES REMINDER! (cont.)\n---------\n\U0001F1EB\U0001F1EE Uuden Musiikin Kilpailu - Final (https://somereallyreallyreallyreallylongurl.fi)\n---------\n\U0001F1F7\U0001F1F8 Beovizija - Final (https://somereallyreallyreallyreallylongurl.rs)")
        self.generator.thread_indicator = False


    def test_when_watch_links_would_result_in_a_too_long_string_then_should_shorten_the_event_string_and_generate_a_valid_thread_anyway(self):
        events = [
            {
                "id": 283,
                "dateTimeCet": "2024-03-09T20:00:00",
                "country": "Sweden",
                "endDateTimeCet": "2024-03-09T22:00:00",
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
                        "replayable": 1
                    }
                ]
            },
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.no', 'comment': 'Recommended link', 'live': 1}]},
        ]
        self.generator.post_char_limit = 245
        event_string = self.generator.generate_event_string(events[0])
        self.assertTrue(self.generator.is_post_too_long(event_string))
        shorter_event_string = self.generator.generate_shorter_event_string(events[0])
        # in this case, we expect comments and the last link to be excluded from the final event string
        self.assertEqual(shorter_event_string, "\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://www.svtplay.se/video/jw2BJEy/melodifestivalen/final OR https://www.svtplay.se/video/jQ72NXZ/melodifestivalen/melodifestivalen-2024-the-final)")
        
        posts = self.generator.generate_thread(events)
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://www.svtplay.se/video/jw2BJEy/melodifestivalen/final OR https://www.svtplay.se/video/jQ72NXZ/melodifestivalen/melodifestivalen-2024-the-final)")
        self.assertEqual(posts[1], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F3\U0001F1F4 Melodi Grand Prix - Final (https://somereallyreallyreallyreallylongurl.no)")
        self.generator.post_char_limit = 260


    def test_when_all_watch_links_are_too_long_and_none_can_be_included_in_the_post_then_should_not_include_any_link_or_mention_of_missing_links(self):
        events = [
            {
                'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00',
                'watchLinks': [
                    {'link': 'https://svtplaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaay.se', 'comment': 'Best link every made out there!', 'live': 1, 'accountRequired': 1, 'geoblocked': 1},
                    {'link': 'https://svtplaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaay.se', 'comment': 'Best link every made out there!', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}
                ]
            },
        ]
        posts = self.generator.generate_thread(events)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final ")


    def test_when_very_complicated_events_do_not_fit_in_one_post_then_should_generate_multiple_posts(self):
        events = [
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Best link every made out there!', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.no', 'comment': 'Next-best link every made out there!', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.ee', 'comment': 'Not the best link, but not the worst either!', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]},
            {'country': 'Finland', 'name': 'Uuden Musiikin Kilpailu', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.fi', 'comment': 'That link is pretty damn good!', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]},
            {'country': 'Serbia', 'name': 'Beovizija', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.rs', 'comment': 'Super mega ultra HD 16K very good link click it!', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]}
        ]
        posts = self.generator.generate_thread(events)
        self.assertEqual(len(posts), 5)
        self.assertEqual(posts[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se (Best link every made out there!)(geoblocked, account required: see https://lyseurovision.github.io/help.html#account-Sweden))")
        self.assertEqual(posts[1], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F3\U0001F1F4 Melodi Grand Prix - Final (https://somereallyreallyreallyreallylongurl.no (Next-best link every made out there!)(geoblocked, account required: see https://lyseurovision.github.io/help.html#account-Norway))")
        self.assertEqual(posts[2], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1EA\U0001F1EA Eesti Laul - Final (https://somereallyreallyreallyreallylongurl.ee (Not the best link, but not the worst either!)(geoblocked, account required: see https://lyseurovision.github.io/help.html#account-Estonia))")
        self.assertEqual(posts[3], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1EB\U0001F1EE Uuden Musiikin Kilpailu - Final (https://somereallyreallyreallyreallylongurl.fi (That link is pretty damn good!)(geoblocked, account required: see https://lyseurovision.github.io/help.html#account-Finland))")
        self.assertEqual(posts[4], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F7\U0001F1F8 Beovizija - Final (https://somereallyreallyreallyreallylongurl.rs (Super mega ultra HD 16K very good link click it!)(geoblocked, account required: see https://lyseurovision.github.io/help.html#account-Serbia))")


    def test_when_one_event_with_multiple_links_should_generate_post_with_all_links_and_the_valid_comments(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://svtplay.se', 'comment': 'Another link', 'live': 1}]}]
        posts = self.generator.generate_thread(events)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se OR https://svtplay.se (Another link))")


    def test_when_one_event_with_multiple_links_should_generate_post_with_live_links_only(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://svtplay.se', 'comment': 'Another link', 'live': 0}]}]
        posts = self.generator.generate_thread(events)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se)")


    def test_when_one_event_contains_geoblocked_watch_links_should_add_geoblocked_comment_to_post(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://svtplay.se', 'comment': 'Another link', 'live': 1, 'geoblocked': 1}]}]
        posts = self.generator.generate_thread(events)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se OR https://svtplay.se (Another link)(geoblocked))")


    def test_when_one_event_contains_watch_link_that_requires_an_account_should_add_comment_to_post(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://svtplay.se', 'comment': 'Another link', 'live': 1, 'accountRequired': 1}]}]
        posts = self.generator.generate_thread(events)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se OR https://svtplay.se (Another link)(account required: see https://lyseurovision.github.io/help.html#account-Sweden))")


    def test_when_one_event_contains_watch_link_that_requires_an_account_and_is_geoblocked_should_add_comment_to_post(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://svtplay.se', 'comment': 'Another link', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]}]
        posts = self.generator.generate_thread(events)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se OR https://svtplay.se (Another link)(geoblocked, account required: see https://lyseurovision.github.io/help.html#account-Sweden))")
