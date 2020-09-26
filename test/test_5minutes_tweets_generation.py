import unittest

from lys_5minutes import generate_event_strings, build_tweets

class FiveMinutesTweetsGenerationTest(unittest.TestCase):
    def test_when_events_fit_in_one_tweet_then_should_generate_one_tweet(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLink': 'https://svtplay.se'}]
        event_strings = generate_event_strings(events)
        tweets = build_tweets(event_strings)
        self.assertTrue(len(tweets) == 1)
        self.assertTrue(tweets[0] == "\U0001F6A8 5 MINUTES REMINDER!\n\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se)")


    def test_when_events_do_not_fit_in_one_tweet_then_should_generate_multiple_tweet(self):
        events = [
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLink': 'https://svtplay.se'},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLink': 'https://somereallyreallyreallyreallylongurl.no'},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLink': 'https://somereallyreallyreallyreallylongurl.ee'},
            {'country': 'Finland', 'name': 'Uuden Musiikin Kilpailu', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLink': 'https://somereallyreallyreallyreallylongurl.fi'},
            {'country': 'Serbia', 'name': 'Beovizija', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLink': 'https://somereallyreallyreallyreallylongurl.rs'}
        ]
        event_strings = generate_event_strings(events)
        tweets = build_tweets(event_strings)
        self.assertTrue(len(tweets) == 2)
        self.assertTrue(tweets[0] == "\U0001F6A8 5 MINUTES REMINDER!\n\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se)\n\U0001F1F3\U0001F1F4 Melodi Grand Prix - Final (https://somereallyreallyreallyreallylongurl.no)\n\U0001F1EA\U0001F1EA Eesti Laul - Final (https://somereallyreallyreallyreallylongurl.ee)")
        self.assertTrue(tweets[1] == "\U0001F1EB\U0001F1EE Uuden Musiikin Kilpailu - Final (https://somereallyreallyreallyreallylongurl.fi)\n\U0001F1F7\U0001F1F8 Beovizija - Final (https://somereallyreallyreallyreallylongurl.rs)")
