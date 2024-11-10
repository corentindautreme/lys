import unittest
import datetime

from unittest.mock import patch

from publisher.threads_weekly_publisher import ThreadsWeeklyPublisher
from client.mock_client import MockClient

class ThreadsWeeklyPublisherTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with patch('publisher.threads_weekly_publisher.ThreadsClient', new=MockClient):
            self.publisher = ThreadsWeeklyPublisher()


    def test_when_calling_weekly_publisher_should_generate_single_post_thread(self):
        events = [
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-02-02T20:00:00', 'watchLinks': [{'link': 'https://err.tv', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1 (part 2)', 'dateTimeCet': '2021-02-02T21:30:00', 'watchLinks': [{'link': 'https://err.tv', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-06T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-02-06T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}]}
        ]
        summary = self.publisher.publish(events, run_date=datetime.datetime(1970, 1, 1, 9, 0, 0, 0))
        
        expected_post = "\U0001F5D3 COMING UP NEXT WEEK (* = final):\n\n - Tuesday 02: \U0001F1EA\U0001F1EA\n - Saturday 06: \U0001F1F3\U0001F1F4*\U0001F1F8\U0001F1EA"
        
        self.assertEqual(len(summary), 1)
        self.assertEqual(summary[0], expected_post)

        published_posts = self.publisher.client.posts
        self.assertEqual(len(published_posts), 1)
        self.assertTrue(type(published_posts[0]) is str)
        self.assertEqual(published_posts[0], expected_post)
