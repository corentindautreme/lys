import unittest

from lys_5minutes import build_bluesky_posts

class FiveMinutesBlueskyPostsGenerationTest(unittest.TestCase):
    def test_when_events_fit_in_one_post_then_should_generate_one_post(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}]
        (posts, posts_events) = build_bluesky_posts(events)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (svtplay.se)")
        self.assertEqual(len(posts_events), 1)
        self.assertEqual(len(posts_events[0]), 1)
        self.assertEqual(posts_events[0][0], events[0])


    def test_when_events_do_not_fit_in_one_post_then_should_generate_multiple_posts(self):
        events = [
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.no', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.ee', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Finland', 'name': 'Uuden Musiikin Kilpailu', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.fi', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Serbia', 'name': 'Beovizija', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.rs', 'comment': 'Recommended link', 'live': 1}]}
        ]
        (posts, posts_events) = build_bluesky_posts(events)
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0], "\U0001F6A8 5 MINUTES REMINDER! (thread \U00002B07\U0000FE0F)\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (svtplay.se)\n---------\n\U0001F1F3\U0001F1F4 Melodi Grand Prix - Final (somereallyreallyreallyreallylongurl.no)\n---------\n\U0001F1EA\U0001F1EA Eesti Laul - Final (somereallyreallyreallyreallylongurl.ee)")
        self.assertEqual(posts[1], "\U0001F6A8 5 MINUTES REMINDER! (cont.)\n---------\n\U0001F1EB\U0001F1EE Uuden Musiikin Kilpailu - Final (somereallyreallyreallyreallylongurl.fi)\n---------\n\U0001F1F7\U0001F1F8 Beovizija - Final (somereallyreallyreallyreallylongurl.rs)")
        self.assertEqual(len(posts_events), 2)
        # the first post should include the links of the first 3 events
        self.assertEqual(len(posts_events[0]), 3)
        # (which are the events at index 0, 1 and 2 in the events list)
        self.assertEqual(posts_events[0][0], events[0])
        self.assertEqual(posts_events[0][1], events[1])
        self.assertEqual(posts_events[0][2], events[2])
        # the second and final post should include the links of the last 2 events
        self.assertEqual(len(posts_events[1]), 2)
        # (which are the events at index 3 and 4 in the events list)
        self.assertEqual(posts_events[1][0], events[3])
        self.assertEqual(posts_events[1][1], events[4])


    def test_when_very_complicated_events_do_not_fit_in_one_post_then_should_generate_multiple_posts(self):
        events = [
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Best link every made out there!', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.no', 'comment': 'Next-best link every made out there!', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.ee', 'comment': 'Not the best link, but not the worst either!', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]},
            {'country': 'Finland', 'name': 'Uuden Musiikin Kilpailu', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.fi', 'comment': 'That link is pretty damn good!', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]},
            {'country': 'Serbia', 'name': 'Beovizija', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.rs', 'comment': 'Super mega ultra HD 16K very good link click it!', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]}
        ]
        (posts, posts_events) = build_bluesky_posts(events)
        self.assertEqual(len(posts), 5)
        self.assertEqual(posts[0], "\U0001F6A8 5 MINUTES REMINDER! (thread \U00002B07\U0000FE0F)\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (svtplay.se (Best link every made out there!)(geoblocked, account required: see lyseurovision.github.io))")
        self.assertEqual(posts[1], "\U0001F6A8 5 MINUTES REMINDER! (cont.)\n---------\n\U0001F1F3\U0001F1F4 Melodi Grand Prix - Final (somereallyreallyreallyreallylongurl.no (Next-best link every made out there!)(geoblocked, account required: see lyseurovision.github.io))")
        self.assertEqual(posts[2], "\U0001F6A8 5 MINUTES REMINDER! (cont.)\n---------\n\U0001F1EA\U0001F1EA Eesti Laul - Final (somereallyreallyreallyreallylongurl.ee (Not the best link, but not the worst either!)(geoblocked, account required: see lyseurovision.github.io))")
        self.assertEqual(posts[3], "\U0001F6A8 5 MINUTES REMINDER! (cont.)\n---------\n\U0001F1EB\U0001F1EE Uuden Musiikin Kilpailu - Final (somereallyreallyreallyreallylongurl.fi (That link is pretty damn good!)(geoblocked, account required: see lyseurovision.github.io))")
        self.assertEqual(posts[4], "\U0001F6A8 5 MINUTES REMINDER! (cont.)\n---------\n\U0001F1F7\U0001F1F8 Beovizija - Final (somereallyreallyreallyreallylongurl.rs (Super mega ultra HD 16K very good link click it!)(geoblocked, account required: see lyseurovision.github.io))")
        self.assertEqual(len(posts_events), 5)
        self.assertEqual(len(posts_events[0]), 1)
        self.assertEqual(len(posts_events[1]), 1)
        self.assertEqual(len(posts_events[2]), 1)
        self.assertEqual(len(posts_events[3]), 1)
        self.assertEqual(len(posts_events[4]), 1)
        self.assertEqual(posts_events[0][0], events[0])
        self.assertEqual(posts_events[1][0], events[1])
        self.assertEqual(posts_events[2][0], events[2])
        self.assertEqual(posts_events[3][0], events[3])
        self.assertEqual(posts_events[4][0], events[4])


    def test_when_one_event_with_multiple_links_should_generate_post_with_all_links_and_the_valid_comments(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'svtplay.se', 'comment': 'Recommended link', 'live': 1}, {'link': 'svtplay.se', 'comment': 'Another link', 'live': 1}]}]
        (posts, posts_events) = build_bluesky_posts(events)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (svtplay.se OR svtplay.se (Another link))")
        self.assertEqual(len(posts_events), 1)
        self.assertEqual(len(posts_events[0]), 1)
        self.assertEqual(posts_events[0][0], events[0])


    def test_when_one_event_with_multiple_links_should_generate_post_with_live_links_only(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'svtplay.se', 'comment': 'Recommended link', 'live': 1}, {'link': 'svtplay.se', 'comment': 'Another link', 'live': 0}]}]
        (posts, posts_events) = build_bluesky_posts(events)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (svtplay.se)")
        self.assertEqual(len(posts_events), 1)
        self.assertEqual(len(posts_events[0]), 1)
        self.assertEqual(posts_events[0][0], events[0])


    def test_when_one_event_contains_geoblocked_watch_links_should_add_geoblocked_comment_to_post(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'svtplay.se', 'comment': 'Recommended link', 'live': 1}, {'link': 'svtplay.se', 'comment': 'Another link', 'live': 1, 'geoblocked': 1}]}]
        (posts, posts_events) = build_bluesky_posts(events)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (svtplay.se OR svtplay.se (Another link)(geoblocked))")
        self.assertEqual(len(posts_events), 1)
        self.assertEqual(len(posts_events[0]), 1)
        self.assertEqual(posts_events[0][0], events[0])


    def test_when_one_event_contains_watch_link_that_requires_an_account_should_add_comment_to_post(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'svtplay.se', 'comment': 'Recommended link', 'live': 1}, {'link': 'svtplay.se', 'comment': 'Another link', 'live': 1, 'accountRequired': 1}]}]
        (posts, posts_events) = build_bluesky_posts(events)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (svtplay.se OR svtplay.se (Another link)(account required: see lyseurovision.github.io))")
        self.assertEqual(len(posts_events), 1)
        self.assertEqual(len(posts_events[0]), 1)
        self.assertEqual(posts_events[0][0], events[0])


    def test_when_one_event_contains_watch_link_that_requires_an_account_and_is_geoblocked_should_add_comment_to_post(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'svtplay.se', 'comment': 'Recommended link', 'live': 1}, {'link': 'svtplay.se', 'comment': 'Another link', 'live': 1, 'accountRequired': 1, 'geoblocked': 1}]}]
        (posts, posts_events) = build_bluesky_posts(events)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (svtplay.se OR svtplay.se (Another link)(geoblocked, account required: see lyseurovision.github.io))")
        self.assertEqual(len(posts_events), 1)
        self.assertEqual(len(posts_events[0]), 1)
        self.assertEqual(posts_events[0][0], events[0])

    # TODO add tests on the post objects (facets, etc.)
