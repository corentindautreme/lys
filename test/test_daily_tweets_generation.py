import unittest

from lys_daily import generate_daily_tweet_thread

class DailyTweetsGenerationTest(unittest.TestCase):
    def test_when_one_event_then_should_generate_one_tweet(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}]
        tweets = generate_daily_tweet_thread(events, is_morning=False)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "TONIGHT: \U0001F1F8\U0001F1EA Sweden | Melodifestivalen - Final at 20:00 CET. Watch live: https://svtplay.se")


    def test_when_2_events_then_should_generate_3_tweets(self):
        events = [
            {'country': 'Denmark', 'name': 'Dansk Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://tv.dr.dk', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}
        ]
        tweets = generate_daily_tweet_thread(events, is_morning=True)
        self.assertEqual(len(tweets), 3)
        self.assertEqual(tweets[0], "TODAY: 2 selection shows across Europe!")
        self.assertEqual(tweets[1], "TODAY: \U0001F1E9\U0001F1F0 Denmark | Dansk Melodi Grand Prix - Final at 20:00 CET. Watch live: https://tv.dr.dk")
        self.assertEqual(tweets[2], "TODAY: \U0001F1F8\U0001F1EA Sweden | Melodifestivalen - Final at 20:00 CET. Watch live: https://svtplay.se")


    def test_when_multiple_events_and_1_Australian_event_then_should_mention_Australia_in_first_tweet(self):
        events = [
            {'country': 'Australia', 'name': 'Australia Decides', 'stage': 'Final', 'dateTimeCet': '2021-02-13T10:30:00', 'watchLinks': [{'link': 'https://facebook.com', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Heat 5', 'dateTimeCet': '2021-02-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 2', 'dateTimeCet': '2021-02-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}
        ]
        tweets = generate_daily_tweet_thread(events, is_morning=True)
        self.assertEqual(len(tweets), 4)
        self.assertEqual(tweets[0], "TODAY: 3 selection shows across Europe and Australia!")
        self.assertEqual(tweets[1], "TODAY: \U0001F1E6\U0001F1FA Australia | Australia Decides - Final at 10:30 CET. Watch live: https://facebook.com")
        self.assertEqual(tweets[2], "TODAY: \U0001F1F3\U0001F1F4 Norway | Melodi Grand Prix - Heat 5 at 19:50 CET. Watch live: https://nrk.no/mgp")
        self.assertEqual(tweets[3], "TODAY: \U0001F1F8\U0001F1EA Sweden | Melodifestivalen - Heat 2 at 20:00 CET. Watch live: https://svtplay.se")

    def test_when_multiple_events_then_should_sort_tweets_by_start_time_and_country(self):
        events = [
            {'country': 'Denmark', 'name': 'Dansk Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:05:00', 'watchLinks': [{'link': 'https://tv.dr.dk', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}]}
        ]
        tweets = generate_daily_tweet_thread(events, is_morning=True)
        self.assertEqual(len(tweets), 4)
        self.assertEqual(tweets[0], "TODAY: 3 selection shows across Europe!")
        self.assertEqual(tweets[1], "TODAY: \U0001F1F3\U0001F1F4 Norway | Melodi Grand Prix - Final at 19:50 CET. Watch live: https://nrk.no/mgp")
        self.assertEqual(tweets[2], "TODAY: \U0001F1F8\U0001F1EA Sweden | Melodifestivalen - Final at 20:00 CET. Watch live: https://svtplay.se")
        self.assertEqual(tweets[3], "TODAY: \U0001F1E9\U0001F1F0 Denmark | Dansk Melodi Grand Prix - Final at 20:05 CET. Watch live: https://tv.dr.dk")

    def test_when_events_include_multi_parter_then_should_count_the_multi_parter_as_only_one_event_in_the_initial_tweet(self):
        events = [
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-03-13T18:30:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1 (part 2)', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]}
        ]
        tweets = generate_daily_tweet_thread(events, is_morning=True)
        self.assertEqual(len(tweets), 4)
        self.assertEqual(tweets[0], "TODAY: 2 selection shows across Europe!")

    def test_when_events_only_contains_a_multi_parter_show_then_should_count_the_multi_parter_show_as_only_one_event_in_the_initial_tweet(self):
        events = [
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-03-13T18:30:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1 (part 2)', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]}
        ]
        tweets = generate_daily_tweet_thread(events, is_morning=True)
        self.assertEqual(len(tweets), 3)
        self.assertEqual(tweets[0], "TODAY: 1 selection show across Europe!")

    def test_when_event_contains_multiple_watch_links_should_generate_one_tweet_that_includes_all_links_and_comments(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'A first link', 'live': 1}, {'link': 'https://tv.nrk.no', 'comment': 'Another link', 'live': 1}]}
        ]
        tweets = generate_daily_tweet_thread(events, is_morning=True)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "TODAY: \U0001F1F3\U0001F1F4 Norway | Melodi Grand Prix - Heat 1 at 19:50 CET. Watch live: https://nrk.no/mgp (A first link) OR https://tv.nrk.no (Another link)")

    def test_when_event_contains_multiple_watch_links_should_generate_one_tweet_that_includes_all_links_and_valid_comments(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://tv.nrk.no', 'comment': 'Another link', 'live': 1}]}
        ]
        tweets = generate_daily_tweet_thread(events, is_morning=True)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "TODAY: \U0001F1F3\U0001F1F4 Norway | Melodi Grand Prix - Heat 1 at 19:50 CET. Watch live: https://nrk.no/mgp OR https://tv.nrk.no (Another link)")


    def test_when_2_events_contain_multiple_watch_links_should_generate_3_tweet_that_includes_all_links_and_valid_comments(self):
        events = [
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se/melodifestivalen', 'comment': '', 'live': 1}]},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://tv.nrk.no', 'live': 1}]}
        ]
        tweets = generate_daily_tweet_thread(events, is_morning=True)
        self.assertEqual(len(tweets), 3)
        self.assertEqual(tweets[1], "TODAY: \U0001F1F3\U0001F1F4 Norway | Melodi Grand Prix - Final at 19:50 CET. Watch live: https://nrk.no/mgp OR https://tv.nrk.no")
        self.assertEqual(tweets[2], "TODAY: \U0001F1F8\U0001F1EA Sweden | Melodifestivalen - Final at 20:00 CET. Watch live: https://svtplay.se/melodifestivalen")


    def test_when_one_event_contains_multiple_watch_links_should_generate_tweet_that_includes_live_links_only(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://tv.nrk.no', 'live': 0}]}
        ]
        tweets = generate_daily_tweet_thread(events, is_morning=True)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "TODAY: \U0001F1F3\U0001F1F4 Norway | Melodi Grand Prix - Final at 19:50 CET. Watch live: https://nrk.no/mgp")


    def test_when_one_event_contains_geoblocked_watch_links_should_add_geoblocked_comment_to_tweet(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://tv.nrk.no', 'live': 1, 'geoblocked': 1}]}
        ]
        tweets = generate_daily_tweet_thread(events, is_morning=True)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "TODAY: \U0001F1F3\U0001F1F4 Norway | Melodi Grand Prix - Final at 19:50 CET. Watch live: https://nrk.no/mgp OR https://tv.nrk.no (geoblocked)")


    def test_when_one_event_contains_watch_link_that_requires_an_account_should_add_comment_to_tweet(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://tv.nrk.no', 'live': 1, 'accountRequired': 1}]}
        ]
        tweets = generate_daily_tweet_thread(events, is_morning=True)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "TODAY: \U0001F1F3\U0001F1F4 Norway | Melodi Grand Prix - Final at 19:50 CET. Watch live: https://nrk.no/mgp OR https://tv.nrk.no (account required)")


    def test_when_one_event_contains_watch_link_that_requires_an_account_and_is_geoblocked_should_add_comment_to_tweet(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://tv.nrk.no', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]}
        ]
        tweets = generate_daily_tweet_thread(events, is_morning=True)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "TODAY: \U0001F1F3\U0001F1F4 Norway | Melodi Grand Prix - Final at 19:50 CET. Watch live: https://nrk.no/mgp OR https://tv.nrk.no (geoblocked, account required)")
