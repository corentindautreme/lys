import unittest

from lys_daily import generate_daily_thread_posts, generate_thread, post_to_target

class DailyPostsGenerationTest(unittest.TestCase):
    def test_when_one_event_then_should_generate_one_tweet(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}]
        tweets = generate_daily_thread_posts(events, is_morning=False)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "TONIGHT | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Final\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://svtplay.se.")


    def test_when_2_events_then_should_generate_3_tweets(self):
        events = [
            {'country': 'Denmark', 'name': 'Dansk Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://tv.dr.dk', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}
        ]
        tweets = generate_daily_thread_posts(events, is_morning=True)
        self.assertEqual(len(tweets), 3)
        self.assertEqual(tweets[0], "TODAY | 2 selection shows across Europe! (thread \U00002B07\U0000FE0F)")
        self.assertEqual(tweets[1], "TODAY | \U0001F1E9\U0001F1F0 DENMARK\n---------\n\U0001F4FC Dansk Melodi Grand Prix\n\U0001F3C6 Final\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://tv.dr.dk.")
        self.assertEqual(tweets[2], "TODAY | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Final\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://svtplay.se.")


    def test_when_multiple_events_and_1_Australian_event_then_should_mention_Australia_in_first_tweet(self):
        events = [
            {'country': 'Australia', 'name': 'Australia Decides', 'stage': 'Final', 'dateTimeCet': '2021-02-13T10:30:00', 'watchLinks': [{'link': 'https://facebook.com', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Heat 5', 'dateTimeCet': '2021-02-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 2', 'dateTimeCet': '2021-02-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}
        ]
        tweets = generate_daily_thread_posts(events, is_morning=True)
        self.assertEqual(len(tweets), 4)
        self.assertEqual(tweets[0], "TODAY | 3 selection shows across Europe and Australia! (thread \U00002B07\U0000FE0F)")
        self.assertEqual(tweets[1], "TODAY | \U0001F1E6\U0001F1FA AUSTRALIA\n---------\n\U0001F4FC Australia Decides\n\U0001F3C6 Final\n\U0001F553 10:30 CET\n---------\n\U0001F4FA https://facebook.com.")
        self.assertEqual(tweets[2], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Heat 5\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp.")
        self.assertEqual(tweets[3], "TODAY | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Heat 2\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://svtplay.se.")

    def test_when_multiple_events_then_should_sort_tweets_by_start_time_and_country(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Denmark', 'name': 'Dansk Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:05:00', 'watchLinks': [{'link': 'https://tv.dr.dk', 'comment': 'Recommended link', 'live': 1}]},
        ]
        tweets = generate_daily_thread_posts(events, is_morning=True)
        self.assertEqual(len(tweets), 4)
        self.assertEqual(tweets[0], "TODAY | 3 selection shows across Europe! (thread \U00002B07\U0000FE0F)")
        self.assertEqual(tweets[1], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Final\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp.")
        self.assertEqual(tweets[2], "TODAY | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Final\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://svtplay.se.")
        self.assertEqual(tweets[3], "TODAY | \U0001F1E9\U0001F1F0 DENMARK\n---------\n\U0001F4FC Dansk Melodi Grand Prix\n\U0001F3C6 Final\n\U0001F553 20:05 CET\n---------\n\U0001F4FA https://tv.dr.dk.")

    def test_when_events_include_multi_parter_then_should_count_the_multi_parter_as_only_one_event_in_the_initial_tweet(self):
        events = [
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-03-13T18:30:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1 (part 2)', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]}
        ]
        tweets = generate_daily_thread_posts(events, is_morning=True)
        self.assertEqual(len(tweets), 4)
        self.assertEqual(tweets[0], "TODAY | 2 selection shows across Europe! (thread \U00002B07\U0000FE0F)")

    def test_when_events_only_contains_a_multi_parter_show_then_should_count_the_multi_parter_show_as_only_one_event_in_the_initial_tweet(self):
        events = [
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-03-13T18:30:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1 (part 2)', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]}
        ]
        tweets = generate_daily_thread_posts(events, is_morning=True)
        self.assertEqual(len(tweets), 3)
        self.assertEqual(tweets[0], "TODAY | 1 selection show across Europe! (thread \U00002B07\U0000FE0F)")

    def test_when_event_contains_multiple_watch_links_should_generate_one_tweet_that_includes_all_links_and_comments(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'A first link', 'live': 1}, {'link': 'https://tv.nrk.no', 'comment': 'Another link', 'live': 1}]}
        ]
        tweets = generate_daily_thread_posts(events, is_morning=True)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Heat 1\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp (A first link) OR https://tv.nrk.no (Another link).")

    def test_when_event_contains_multiple_watch_links_should_generate_one_tweet_that_includes_all_links_and_valid_comments(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://tv.nrk.no', 'comment': 'Another link', 'live': 1}]}
        ]
        tweets = generate_daily_thread_posts(events, is_morning=True)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Heat 1\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp OR https://tv.nrk.no (Another link).")


    def test_when_2_events_contain_multiple_watch_links_should_generate_3_tweet_that_includes_all_links_and_valid_comments(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://tv.nrk.no', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se/melodifestivalen', 'comment': '', 'live': 1}]}
        ]
        tweets = generate_daily_thread_posts(events, is_morning=True)
        self.assertEqual(len(tweets), 3)
        self.assertEqual(tweets[1], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Final\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp OR https://tv.nrk.no.")
        self.assertEqual(tweets[2], "TODAY | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Final\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://svtplay.se/melodifestivalen.")


    def test_when_one_event_contains_multiple_watch_links_should_generate_tweet_that_includes_live_links_only(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://tv.nrk.no', 'live': 0}]}
        ]
        tweets = generate_daily_thread_posts(events, is_morning=True)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Final\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp.")


    def test_when_one_event_contains_geoblocked_watch_links_should_add_geoblocked_comment_to_tweet(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://tv.nrk.no', 'live': 1, 'geoblocked': 1}]}
        ]
        tweets = generate_daily_thread_posts(events, is_morning=True, shorten_urls=True)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Final\n\U0001F553 19:50 CET\n---------\n\U0001F4FA nrk.no OR tv.nrk.no (geoblocked).")


    def test_when_one_event_contains_watch_link_that_requires_an_account_should_add_comment_to_tweet(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://tv.nrk.no', 'live': 1, 'accountRequired': 1}]}
        ]
        tweets = generate_daily_thread_posts(events, is_morning=True)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Final\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp OR https://tv.nrk.no (account required: see https://lyseurovision.github.io/help.html#account-Norway).")


    def test_when_one_event_contains_watch_link_that_requires_an_account_and_is_geoblocked_should_add_comment_to_tweet(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://tv.nrk.no', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]}
        ]
        tweets = generate_daily_thread_posts(events, is_morning=True, shorten_urls=True)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Final\n\U0001F553 19:50 CET\n---------\n\U0001F4FA nrk.no OR tv.nrk.no (geoblocked, account required: see lyseurovision.github.io).")


    def test_when_generating_posts_for_none_target_should_raise_value_error(self):
        e = None
        try:
            generate_thread(events=[], is_morning=False, target=None)
        except ValueError as err:
            e = err
        self.assertIsNotNone(e)
        self.assertEqual(str(e), "Unknown target 'None'")


    def test_when_generating_posts_for_unknown_target_should_raise_value_error(self):
        e = None
        try:
            generate_thread(events=[], is_morning=False, target="facebook")
        except ValueError as err:
            e = err
        self.assertIsNotNone(e)
        self.assertEqual(str(e), "Unknown target 'facebook'")

    def test_when_posting_to_none_target_should_raise_value_error(self):
        e = None
        try:
            post_to_target(posts=[], target=None)
        except ValueError as err:
            e = err
        self.assertIsNotNone(e)
        self.assertEqual(str(e), "Unknown target 'None'")

    def test_when_posting_to_unknown_target_should_raise_value_error(self):
        e = None
        try:
            post_to_target(posts=[], target='instagram')
        except ValueError as err:
            e = err
        self.assertIsNotNone(e)
        self.assertEqual(str(e), "Unknown target 'instagram'")

