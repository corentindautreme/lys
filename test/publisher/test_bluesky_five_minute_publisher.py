import unittest
import datetime

from unittest.mock import patch

from publisher.bluesky_five_minute_publisher import BlueskyFiveMinutePublisher
from client.mock_client import MockClient

class BlueskyFiveMinutePublisherTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with patch('publisher.bluesky_five_minute_publisher.BlueskyClient', new=MockClient):
            self.publisher = BlueskyFiveMinutePublisher()
    

    def test_when_calling_five_minute_publisher_with_one_event_should_generate_and_publish_single_post_thread(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}]
        summary = self.publisher.publish(events, run_date=datetime.datetime(1970, 1, 1, 9, 0, 0, 0))

        self.assertEqual(summary[0], "5min|bluesky")
        summary = summary[1:]

        expected_post = "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (svtplay.se)"

        self.assertEqual(len(summary), 1)
        self.assertEqual(summary[0]['text'], expected_post)

        published_posts = self.publisher.client.posts
        self.assertEqual(len(published_posts), 1)
        self.assertTrue(type(published_posts[0]) is dict)
        self.assertEqual(published_posts[0]['text'], expected_post)
        post = published_posts[0]
        self.assertTrue(type(post['facets']) is list)
        self.assertEqual(len(post['facets']), 1)
        facet = post['facets'][0]
        self.assertTrue(type(facet['index']) is dict)
        self.assertTrue("byteStart" in facet['index'])
        self.assertTrue("byteEnd" in facet['index'])
        self.assertTrue(type(facet['features']) is list)
        self.assertEqual(len(facet['features']), 1)
        feature = facet['features'][0]
        self.assertEqual(feature['$type'], "app.bsky.richtext.facet#link")
        self.assertEqual(feature['uri'], "https://svtplay.se")

        self.assertTrue("embed" not in post)
    

    def test_when_calling_five_minute_publisher_with_multiple_events_should_generate_and_publish_multi_post_thread(self):
        events = [
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.no', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.ee', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Finland', 'name': 'Uuden Musiikin Kilpailu', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.fi', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Serbia', 'name': 'Beovizija', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.rs', 'comment': 'Recommended link', 'live': 1}]}
        ]
        summary = self.publisher.publish(events, run_date=datetime.datetime(1970, 1, 1, 19, 55, 0, 0))

        self.assertEqual(summary[0], "5min|bluesky")
        summary = summary[1:]

        self.assertEqual(len(summary), 2)
        self.assertEqual(summary[0]['text'], "\U0001F6A8 5 MINUTES REMINDER! (thread \U00002B07\U0000FE0F)\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (svtplay.se)\n---------\n\U0001F1F3\U0001F1F4 Melodi Grand Prix - Final (somereallyreallyreallyreallylongurl.no)\n---------\n\U0001F1EA\U0001F1EA Eesti Laul - Final (somereallyreallyreallyreallylongurl.ee)")
        self.assertEqual(summary[1]['text'], "\U0001F6A8 5 MINUTES REMINDER! (cont.)\n---------\n\U0001F1EB\U0001F1EE Uuden Musiikin Kilpailu - Final (somereallyreallyreallyreallylongurl.fi)\n---------\n\U0001F1F7\U0001F1F8 Beovizija - Final (somereallyreallyreallyreallylongurl.rs)")

        published_posts = self.publisher.client.posts
        self.assertEqual(len(published_posts), 2)
        
        self.assertEqual(published_posts[0]['text'], "\U0001F6A8 5 MINUTES REMINDER! (thread \U00002B07\U0000FE0F)\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (svtplay.se)\n---------\n\U0001F1F3\U0001F1F4 Melodi Grand Prix - Final (somereallyreallyreallyreallylongurl.no)\n---------\n\U0001F1EA\U0001F1EA Eesti Laul - Final (somereallyreallyreallyreallylongurl.ee)")
        post = published_posts[0]
        self.assertTrue(type(post['facets']) is list)
        self.assertEqual(len(post['facets']), 3)
        facet = post['facets'][0]
        self.assertTrue(type(facet['index']) is dict)
        self.assertTrue("byteStart" in facet['index'])
        self.assertTrue("byteEnd" in facet['index'])
        self.assertTrue(type(facet['features']) is list)
        self.assertEqual(len(facet['features']), 1)
        feature = facet['features'][0]
        self.assertEqual(feature['$type'], "app.bsky.richtext.facet#link")
        self.assertEqual(feature['uri'], "https://svtplay.se")
        facet = post['facets'][1]
        self.assertTrue(type(facet['index']) is dict)
        self.assertTrue("byteStart" in facet['index'])
        self.assertTrue("byteEnd" in facet['index'])
        self.assertTrue(type(facet['features']) is list)
        self.assertEqual(len(facet['features']), 1)
        feature = facet['features'][0]
        self.assertEqual(feature['$type'], "app.bsky.richtext.facet#link")
        self.assertEqual(feature['uri'], "https://somereallyreallyreallyreallylongurl.no")
        facet = post['facets'][2]
        self.assertTrue(type(facet['index']) is dict)
        self.assertTrue("byteStart" in facet['index'])
        self.assertTrue("byteEnd" in facet['index'])
        self.assertTrue(type(facet['features']) is list)
        self.assertEqual(len(facet['features']), 1)
        feature = facet['features'][0]
        self.assertEqual(feature['$type'], "app.bsky.richtext.facet#link")
        self.assertEqual(feature['uri'], "https://somereallyreallyreallyreallylongurl.ee")

        self.assertTrue("embed" not in post)

        self.assertEqual(published_posts[1]['text'], "\U0001F6A8 5 MINUTES REMINDER! (cont.)\n---------\n\U0001F1EB\U0001F1EE Uuden Musiikin Kilpailu - Final (somereallyreallyreallyreallylongurl.fi)\n---------\n\U0001F1F7\U0001F1F8 Beovizija - Final (somereallyreallyreallyreallylongurl.rs)")
        post = published_posts[1]
        self.assertTrue(type(post['facets']) is list)
        self.assertEqual(len(post['facets']), 2)
        facet = post['facets'][0]
        self.assertTrue(type(facet['index']) is dict)
        self.assertTrue("byteStart" in facet['index'])
        self.assertTrue("byteEnd" in facet['index'])
        self.assertTrue(type(facet['features']) is list)
        self.assertEqual(len(facet['features']), 1)
        feature = facet['features'][0]
        self.assertEqual(feature['$type'], "app.bsky.richtext.facet#link")
        self.assertEqual(feature['uri'], "https://somereallyreallyreallyreallylongurl.fi")
        facet = post['facets'][1]
        self.assertTrue(type(facet['index']) is dict)
        self.assertTrue("byteStart" in facet['index'])
        self.assertTrue("byteEnd" in facet['index'])
        self.assertTrue(type(facet['features']) is list)
        self.assertEqual(len(facet['features']), 1)
        feature = facet['features'][0]
        self.assertEqual(feature['$type'], "app.bsky.richtext.facet#link")
        self.assertEqual(feature['uri'], "https://somereallyreallyreallyreallylongurl.rs")

        self.assertTrue("embed" not in post)
