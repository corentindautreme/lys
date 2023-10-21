import unittest

from lys_5minutes import generate_twitter_event_strings, build_tweets

class FiveMinutesTweetsGenerationTest(unittest.TestCase):
    def test_when_events_fit_in_one_tweet_then_should_generate_one_tweet(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}]
        event_strings = generate_twitter_event_strings(events)
        tweets = build_tweets(event_strings)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se)")


    def test_when_events_do_not_fit_in_one_tweet_then_should_generate_multiple_tweets(self):
        events = [
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.no', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.ee', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Finland', 'name': 'Uuden Musiikin Kilpailu', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.fi', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Serbia', 'name': 'Beovizija', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.rs', 'comment': 'Recommended link', 'live': 1}]}
        ]
        event_strings = generate_twitter_event_strings(events)
        tweets = build_tweets(event_strings)
        self.assertEqual(len(tweets), 2)
        self.assertEqual(tweets[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se)\n---------\n\U0001F1F3\U0001F1F4 Melodi Grand Prix - Final (https://somereallyreallyreallyreallylongurl.no)\n---------\n\U0001F1EA\U0001F1EA Eesti Laul - Final (https://somereallyreallyreallyreallylongurl.ee)")
        self.assertEqual(tweets[1], "\U0001F1EB\U0001F1EE Uuden Musiikin Kilpailu - Final (https://somereallyreallyreallyreallylongurl.fi)\n---------\n\U0001F1F7\U0001F1F8 Beovizija - Final (https://somereallyreallyreallyreallylongurl.rs)")

    def test_when_very_complicated_events_do_not_fit_in_one_tweet_then_should_generate_multiple_tweets(self):
        events = [
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Best link every made out there!', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.no', 'comment': 'Next-best link every made out there!', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.ee', 'comment': 'Not the best link, but not the worst either!', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]},
            {'country': 'Finland', 'name': 'Uuden Musiikin Kilpailu', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.fi', 'comment': 'That link is pretty damn good!', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]},
            {'country': 'Serbia', 'name': 'Beovizija', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.rs', 'comment': 'Super mega ultra HD 16K very good link click it!', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]}
        ]
        event_strings = generate_twitter_event_strings(events)
        tweets = build_tweets(event_strings)
        self.assertEqual(len(tweets), 5)
        self.assertEqual(tweets[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se (Best link every made out there!) (geoblocked, account required: https://lyseurovision.github.io/help.html#account-Sweden))")
        self.assertEqual(tweets[1], "\U0001F1F3\U0001F1F4 Melodi Grand Prix - Final (https://somereallyreallyreallyreallylongurl.no (Next-best link every made out there!) (geoblocked, account required: https://lyseurovision.github.io/help.html#account-Norway))")
        self.assertEqual(tweets[2], "\U0001F1EA\U0001F1EA Eesti Laul - Final (https://somereallyreallyreallyreallylongurl.ee (Not the best link, but not the worst either!) (geoblocked, account required: https://lyseurovision.github.io/help.html#account-Estonia))")
        self.assertEqual(tweets[3], "\U0001F1EB\U0001F1EE Uuden Musiikin Kilpailu - Final (https://somereallyreallyreallyreallylongurl.fi (That link is pretty damn good!) (geoblocked, account required: https://lyseurovision.github.io/help.html#account-Finland))")
        self.assertEqual(tweets[4], "\U0001F1F7\U0001F1F8 Beovizija - Final (https://somereallyreallyreallyreallylongurl.rs (Super mega ultra HD 16K very good link click it!) (geoblocked, account required: https://lyseurovision.github.io/help.html#account-Serbia))")

    def test_when_one_event_with_multiple_links_should_generate_tweet_with_all_links_and_the_valid_comments(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://svtplay.se', 'comment': 'Another link', 'live': 1}]}]
        event_strings = generate_twitter_event_strings(events)
        tweets = build_tweets(event_strings)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se OR https://svtplay.se (Another link))")

    def test_when_one_event_with_multiple_links_should_generate_tweet_with_live_links_only(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://svtplay.se', 'comment': 'Another link', 'live': 0}]}]
        event_strings = generate_twitter_event_strings(events)
        tweets = build_tweets(event_strings)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se)")

    def test_when_one_event_contains_geoblocked_watch_links_should_add_geoblocked_comment_to_tweet(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://svtplay.se', 'comment': 'Another link', 'live': 1, 'geoblocked': 1}]}]
        event_strings = generate_twitter_event_strings(events)
        tweets = build_tweets(event_strings)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se OR https://svtplay.se (Another link) (geoblocked))")

    def test_when_one_event_contains_watch_link_that_requires_an_account_should_add_comment_to_tweet(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://svtplay.se', 'comment': 'Another link', 'live': 1, 'accountRequired': 1}]}]
        event_strings = generate_twitter_event_strings(events)
        tweets = build_tweets(event_strings)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se OR https://svtplay.se (Another link) (account required: https://lyseurovision.github.io/help.html#account-Sweden))")

    def test_when_one_event_contains_watch_link_that_requires_an_account_and_is_geoblocked_should_add_comment_to_tweet(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://svtplay.se', 'comment': 'Another link', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]}]
        event_strings = generate_twitter_event_strings(events)
        tweets = build_tweets(event_strings)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se OR https://svtplay.se (Another link) (geoblocked, account required: https://lyseurovision.github.io/help.html#account-Sweden))")
