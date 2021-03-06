import unittest

from lys_daily import generate_daily_tweet_thread

class DailyTweetsGenerationTest(unittest.TestCase):
    def test_when_one_event_then_should_generate_one_tweet(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLink': 'https://svtplay.se'}]
        tweets = generate_daily_tweet_thread(events, is_morning=False)
        self.assertTrue(len(tweets) == 1)
        self.assertTrue(tweets[0] == "TONIGHT: \U0001F1F8\U0001F1EA Sweden | Melodifestivalen - Final at 20:00 CET. Watch live: https://svtplay.se")


    def test_when_2_events_then_should_generate_3_tweets(self):
        events = [
            {'country': 'Denmark', 'name': 'Dansk Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLink': 'https://tv.dr.dk'},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLink': 'https://svtplay.se'}
        ]
        tweets = generate_daily_tweet_thread(events, is_morning=True)
        self.assertTrue(len(tweets) == 3)
        self.assertTrue(tweets[0] == "TODAY: 2 selection shows across Europe!")
        self.assertTrue(tweets[1] == "TODAY: \U0001F1E9\U0001F1F0 Denmark | Dansk Melodi Grand Prix - Final at 20:00 CET. Watch live: https://tv.dr.dk")
        self.assertTrue(tweets[2] == "TODAY: \U0001F1F8\U0001F1EA Sweden | Melodifestivalen - Final at 20:00 CET. Watch live: https://svtplay.se")


    def test_when_multiple_events_and_1_Australian_event_then_should_mention_Australia_in_first_tweet(self):
        events = [
            {'country': 'Australia', 'name': 'Australia Decides', 'stage': 'Final', 'dateTimeCet': '2021-02-13T10:30:00', 'watchLink': 'https://facebook.com'},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Heat 5', 'dateTimeCet': '2021-02-13T19:50:00', 'watchLink': 'https://nrk.no/mgp'},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 2', 'dateTimeCet': '2021-02-13T20:00:00', 'watchLink': 'https://svtplay.se'}
        ]
        tweets = generate_daily_tweet_thread(events, is_morning=True)
        self.assertTrue(len(tweets) == 4)
        self.assertTrue(tweets[0] == "TODAY: 3 selection shows across Europe and Australia!")
        self.assertTrue(tweets[1] == "TODAY: \U0001F1E6\U0001F1FA Australia | Australia Decides - Final at 10:30 CET. Watch live: https://facebook.com")
        self.assertTrue(tweets[2] == "TODAY: \U0001F1F3\U0001F1F4 Norway | Melodi Grand Prix - Heat 5 at 19:50 CET. Watch live: https://nrk.no/mgp")
        self.assertTrue(tweets[3] == "TODAY: \U0001F1F8\U0001F1EA Sweden | Melodifestivalen - Heat 2 at 20:00 CET. Watch live: https://svtplay.se")

    def test_when_multiple_events_then_should_sort_tweets_by_start_time_and_country(self):
        events = [
            {'country': 'Denmark', 'name': 'Dansk Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:05:00', 'watchLink': 'https://tv.dr.dk'},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLink': 'https://svtplay.se'},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T19:50:00', 'watchLink': 'https://nrk.no/mgp'}
        ]
        tweets = generate_daily_tweet_thread(events, is_morning=True)
        self.assertTrue(len(tweets) == 4)
        self.assertTrue(tweets[0] == "TODAY: 3 selection shows across Europe!")
        self.assertTrue(tweets[1] == "TODAY: \U0001F1F3\U0001F1F4 Norway | Melodi Grand Prix - Final at 19:50 CET. Watch live: https://nrk.no/mgp")
        self.assertTrue(tweets[2] == "TODAY: \U0001F1F8\U0001F1EA Sweden | Melodifestivalen - Final at 20:00 CET. Watch live: https://svtplay.se")
        self.assertTrue(tweets[3] == "TODAY: \U0001F1E9\U0001F1F0 Denmark | Dansk Melodi Grand Prix - Final at 20:05 CET. Watch live: https://tv.dr.dk")
