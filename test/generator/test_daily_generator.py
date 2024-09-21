import unittest

from generator.daily_generator import DailyGenerator

class DailyGeneratorTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generator = DailyGenerator(formatter=None)


    def test_when_zero_or_one_event_in_list_should_not_generate_header(self):
        events = []
        self.assertEqual(self.generator.has_header(events), False)
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-02-06T19:50:00', 'watchLink': 'https://nrk.no/mgp'}
        ]
        self.assertEqual(self.generator.has_header(events), False)


    def test_when_more_than_one_event_in_list_should_generate_header(self):
        events = [
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-06T20:00:00', 'watchLink': 'https://svtplay.se'},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-02-06T19:50:00', 'watchLink': 'https://nrk.no/mgp'}
        ]
        self.assertEqual(self.generator.has_header(events), True)


    def test_when_more_than_one_event_in_list_should_generate_header(self):
        events = [
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-06T20:00:00', 'watchLink': 'https://svtplay.se'},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-02-06T19:50:00', 'watchLink': 'https://nrk.no/mgp'}
        ]
        self.assertEqual(self.generator.has_header(events), True)
        header = self.generator.generate_header(events, is_morning=False)
        self.assertEqual(header, "TONIGHT | 2 selection shows across Europe! (thread \U00002B07\U0000FE0F)")


    def test_when_multiple_events_and_1_Australian_event_then_should_mention_Australia_in_header(self):
        events = [
            {'country': 'Australia', 'name': 'Australia Decides', 'stage': 'Final', 'dateTimeCet': '2021-02-13T10:30:00', 'watchLinks': [{'link': 'https://facebook.com', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Heat 5', 'dateTimeCet': '2021-02-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 2', 'dateTimeCet': '2021-02-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}
        ]
        self.assertEqual(self.generator.has_header(events), True)
        header = self.generator.generate_header(events, is_morning=True)
        self.assertEqual(header, "TODAY | 3 selection shows across Europe and Australia! (thread \U00002B07\U0000FE0F)")


    def test_when_events_include_multi_parter_then_should_count_the_multi_parter_as_only_one_event_in_header(self):
        events = [
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-03-13T18:30:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1 (part 2)', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]}
        ]
        self.assertEqual(self.generator.has_header(events), True)
        header = self.generator.generate_header(events, is_morning=True)
        self.assertEqual(header, "TODAY | 2 selection shows across Europe! (thread \U00002B07\U0000FE0F)")


    def test_when_events_only_contains_a_multi_parter_show_then_should_count_the_multi_parter_show_as_only_one_event_in_the_header(self):
        events = [
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-03-13T18:30:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1 (part 2)', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]}
        ]
        self.assertEqual(self.generator.has_header(events), True)
        header = self.generator.generate_header(events, is_morning=False)
        self.assertEqual(header, "TONIGHT | 1 selection show across Europe! (thread \U00002B07\U0000FE0F)")


    def test_when_one_event_then_should_generate_one_post(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}]
        posts = self.generator.generate_thread(events, is_morning=False)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "TONIGHT | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Final\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://svtplay.se.")


    def test_when_2_events_then_should_generate_3_posts(self):
        events = [
            {'country': 'Denmark', 'name': 'Dansk Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://tv.dr.dk', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}
        ]
        posts = self.generator.generate_thread(events, is_morning=True)
        self.assertEqual(len(posts), 3)
        self.assertEqual(posts[0], "TODAY | 2 selection shows across Europe! (thread \U00002B07\U0000FE0F)")
        self.assertEqual(posts[1], "TODAY | \U0001F1E9\U0001F1F0 DENMARK\n---------\n\U0001F4FC Dansk Melodi Grand Prix\n\U0001F3C6 Final\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://tv.dr.dk.")
        self.assertEqual(posts[2], "TODAY | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Final\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://svtplay.se.")


    def test_when_multiple_events_and_1_Australian_event_then_should_mention_Australia_in_first_post(self):
        events = [
            {'country': 'Australia', 'name': 'Australia Decides', 'stage': 'Final', 'dateTimeCet': '2021-02-13T10:30:00', 'watchLinks': [{'link': 'https://facebook.com', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Heat 5', 'dateTimeCet': '2021-02-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 2', 'dateTimeCet': '2021-02-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}
        ]
        posts = self.generator.generate_thread(events, is_morning=True)
        self.assertEqual(len(posts), 4)
        self.assertEqual(posts[0], "TODAY | 3 selection shows across Europe and Australia! (thread \U00002B07\U0000FE0F)")
        self.assertEqual(posts[1], "TODAY | \U0001F1E6\U0001F1FA AUSTRALIA\n---------\n\U0001F4FC Australia Decides\n\U0001F3C6 Final\n\U0001F553 10:30 CET\n---------\n\U0001F4FA https://facebook.com.")
        self.assertEqual(posts[2], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Heat 5\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp.")
        self.assertEqual(posts[3], "TODAY | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Heat 2\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://svtplay.se.")


    def test_when_multiple_events_then_should_sort_posts_by_start_time_and_country(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Denmark', 'name': 'Dansk Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:05:00', 'watchLinks': [{'link': 'https://tv.dr.dk', 'comment': 'Recommended link', 'live': 1}]},
        ]
        posts = self.generator.generate_thread(events, is_morning=True)
        self.assertEqual(len(posts), 4)
        self.assertEqual(posts[0], "TODAY | 3 selection shows across Europe! (thread \U00002B07\U0000FE0F)")
        self.assertEqual(posts[1], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Final\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp.")
        self.assertEqual(posts[2], "TODAY | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Final\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://svtplay.se.")
        self.assertEqual(posts[3], "TODAY | \U0001F1E9\U0001F1F0 DENMARK\n---------\n\U0001F4FC Dansk Melodi Grand Prix\n\U0001F3C6 Final\n\U0001F553 20:05 CET\n---------\n\U0001F4FA https://tv.dr.dk.")


    def test_when_events_include_multi_parter_then_should_count_the_multi_parter_as_only_one_event_in_the_initial_post(self):
        events = [
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-03-13T18:30:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1 (part 2)', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]}
        ]
        posts = self.generator.generate_thread(events, is_morning=True)
        self.assertEqual(len(posts), 4)
        self.assertEqual(posts[0], "TODAY | 2 selection shows across Europe! (thread \U00002B07\U0000FE0F)")


    def test_when_events_only_contains_a_multi_parter_show_then_should_count_the_multi_parter_show_as_only_one_event_in_the_initial_post(self):
        events = [
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-03-13T18:30:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1 (part 2)', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://etv.err.ee/', 'comment': 'Recommended link', 'live': 1}]}
        ]
        posts = self.generator.generate_thread(events, is_morning=True)
        self.assertEqual(len(posts), 3)
        self.assertEqual(posts[0], "TODAY | 1 selection show across Europe! (thread \U00002B07\U0000FE0F)")


    def test_when_event_contains_multiple_watch_links_should_generate_one_post_that_includes_all_links_and_comments(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'A first link', 'live': 1}, {'link': 'https://tv.nrk.no', 'comment': 'Another link', 'live': 1}]}
        ]
        posts = self.generator.generate_thread(events, is_morning=True)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Heat 1\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp (A first link) OR https://tv.nrk.no (Another link).")


    def test_when_event_contains_multiple_watch_links_should_generate_one_post_that_includes_all_links_and_valid_comments(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://tv.nrk.no', 'comment': 'Another link', 'live': 1}]}
        ]
        posts = self.generator.generate_thread(events, is_morning=True)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Heat 1\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp OR https://tv.nrk.no (Another link).")


    def test_when_2_events_contain_multiple_watch_links_should_generate_3_post_that_includes_all_links_and_valid_comments(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://tv.nrk.no', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se/melodifestivalen', 'comment': '', 'live': 1}]}
        ]
        posts = self.generator.generate_thread(events, is_morning=True)
        self.assertEqual(len(posts), 3)
        self.assertEqual(posts[1], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Final\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp OR https://tv.nrk.no.")
        self.assertEqual(posts[2], "TODAY | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Final\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://svtplay.se/melodifestivalen.")


    def test_when_one_event_contains_multiple_watch_links_should_generate_post_that_includes_live_links_only(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://tv.nrk.no', 'live': 0}]}
        ]
        posts = self.generator.generate_thread(events, is_morning=True)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Final\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp.")


    def test_when_one_event_contains_geoblocked_watch_links_should_add_geoblocked_comment_to_post(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://tv.nrk.no', 'live': 1, 'geoblocked': 1}]}
        ]
        self.generator.shorten_urls = True
        posts = self.generator.generate_thread(events, is_morning=True)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Final\n\U0001F553 19:50 CET\n---------\n\U0001F4FA nrk.no OR tv.nrk.no (geoblocked).")


    def test_when_one_event_contains_watch_link_that_requires_an_account_should_add_comment_to_post(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://tv.nrk.no', 'live': 1, 'accountRequired': 1}]}
        ]
        posts = self.generator.generate_thread(events, is_morning=True)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Final\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp OR https://tv.nrk.no (account required: see https://lyseurovision.github.io/help.html#account-Norway).")


    def test_when_one_event_contains_watch_link_that_requires_an_account_and_is_geoblocked_should_add_comment_to_post(self):
        events = [
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}, {'link': 'https://tv.nrk.no', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]}
        ]
        self.generator.shorten_urls = True
        posts = self.generator.generate_thread(events, is_morning=True)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Final\n\U0001F553 19:50 CET\n---------\n\U0001F4FA nrk.no OR tv.nrk.no (geoblocked, account required: see lyseurovision.github.io).")