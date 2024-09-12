import unittest
import datetime

from unittest.mock import patch, MagicMock

from publisher.bluesky_daily_publisher import BlueskyDailyPublisher
from client.mock_client import MockClient

class BlueskyDailyPublisherTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.publisher = BlueskyDailyPublisher()
        self.publisher.client = MockClient()
    
    def test_when_calling_daily_publisher_with_one_event_should_generate_and_publish_single_post_thread(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}]
        
        mock_requests_resp = MagicMock(text="""
            <meta property="og:title" content="MOCK_TITLE"/>
            <meta property="og:description" content="MOCK_DESCRIPTION"/>
        """)
        with patch.object(requests, 'get', return_value=mock_requests_resp) as mock_req:
            summary = self.publisher.publish(events, run_date=datetime.datetime(1970, 1, 1, 9, 0, 0, 0))
        
        expected_post = "TONIGHT | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Final\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://svtplay.se."
        self.assertEqual(len(summary), 1)
        self.assertEqual(summary[0], expected_post)
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

        self.assertTrue(type(post['embed']) is dict)
        self.assertEqual(post['embed']['$type'], "app.bsky.embed.external")
        self.assertEqual(post['embed']['external']['uri'], "https://svtplay.se")
        self.assertEqual(post['embed']['external']['title'], "MOCK_TITLE")
        self.assertEqual(post['embed']['external']['description'], "MOCK_DESCRIPTION")


    def test_when_calling_daily_publisher_with_multiple_events_should_generate_and_publish_multi_post_thread(self):
        events = [
            {'country': 'Australia', 'name': 'Australia Decides', 'stage': 'Final', 'dateTimeCet': '2021-02-13T10:30:00', 'watchLinks': [{'link': 'https://facebook.com', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Heat 5', 'dateTimeCet': '2021-02-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 2', 'dateTimeCet': '2021-02-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}
        ]

        mock_requests_resp = MagicMock(text="""
            <meta property="og:title" content="MOCK_TITLE"/>
            <meta property="og:description" content="MOCK_DESCRIPTION"/>
        """)
        with patch.object(requests, 'get', return_value=mock_requests_resp) as mock_req:
            summary = self.publisher.publish(events, run_date=datetime.datetime(1970, 1, 1, 16, 0, 0, 0))

        self.assertEqual(len(summary), 4)
        self.assertEqual(summary[0], "TODAY | 3 selection shows across Europe and Australia! (thread \U00002B07\U0000FE0F)")
        self.assertEqual(summary[1], "TODAY | \U0001F1E6\U0001F1FA AUSTRALIA\n---------\n\U0001F4FC Australia Decides\n\U0001F3C6 Final\n\U0001F553 10:30 CET\n---------\n\U0001F4FA https://facebook.com.")
        self.assertEqual(summary[2], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Heat 5\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp.")
        self.assertEqual(summary[3], "TODAY | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Heat 2\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://svtplay.se.")
        
        published_posts = self.publisher.client.posts
        self.assertEqual(len(published_posts), 4)
        
        self.assertEqual(published_posts[0]['text'], "TODAY | 3 selection shows across Europe and Australia! (thread \U00002B07\U0000FE0F)")
        post = published_posts[0]
        self.assertTrue("facets" not in post)
        self.assertTrue("embed" not in post)

        self.assertEqual(published_posts[1]['text'], "TODAY | \U0001F1E6\U0001F1FA AUSTRALIA\n---------\n\U0001F4FC Australia Decides\n\U0001F3C6 Final\n\U0001F553 10:30 CET\n---------\n\U0001F4FA https://facebook.com.")
        post = published_posts[1]
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
        self.assertEqual(feature['uri'], "https://facebook.com")

        self.assertTrue(type(post['embed']) is dict)
        self.assertEqual(post['embed']['$type'], "app.bsky.embed.external")
        self.assertEqual(post['embed']['external']['uri'], "https://facebook.com")
        self.assertEqual(post['embed']['external']['title'], "MOCK_TITLE")
        self.assertEqual(post['embed']['external']['description'], "MOCK_DESCRIPTION")

        self.assertEqual(published_posts[2]['text'], "TODAY | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Heat 5\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp.")
        post = published_posts[2]
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
        self.assertEqual(feature['uri'], "https://nrk.no/mgp")

        self.assertTrue(type(post['embed']) is dict)
        self.assertEqual(post['embed']['$type'], "app.bsky.embed.external")
        self.assertEqual(post['embed']['external']['uri'], "https://nrk.no/mgp")
        self.assertEqual(post['embed']['external']['title'], "MOCK_TITLE")
        self.assertEqual(post['embed']['external']['description'], "MOCK_DESCRIPTION")

        self.assertEqual(published_posts[3]['text'], "TODAY | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Heat 2\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://svtplay.se.")
        post = published_posts[3]
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

        self.assertTrue(type(post['embed']) is dict)
        self.assertEqual(post['embed']['$type'], "app.bsky.embed.external")
        self.assertEqual(post['embed']['external']['uri'], "https://svtplay.se")
        self.assertEqual(post['embed']['external']['title'], "MOCK_TITLE")
        self.assertEqual(post['embed']['external']['description'], "MOCK_DESCRIPTION")
