import unittest
import datetime

from unittest.mock import patch

from publisher.threads_five_minute_publisher import ThreadsFiveMinutePublisher
from client.mock_client import MockClient

class ThreadsFiveMinutePublisherTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with patch('publisher.threads_five_minute_publisher.ThreadsClient', new=MockClient):
            self.publisher = ThreadsFiveMinutePublisher()
    

    def test_when_calling_five_minute_publisher_with_one_event_should_generate_and_publish_single_post_thread(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}]
        summary = self.publisher.publish(events, run_date=datetime.datetime(1970, 1, 1, 9, 0, 0, 0))

        ethreadspected_post = "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se)"

        self.assertEqual(len(summary), 1)
        self.assertEqual(summary[0], ethreadspected_post)

        published_posts = self.publisher.client.posts
        self.assertEqual(len(published_posts), 1)
        self.assertTrue(type(published_posts[0]) is str)
        self.assertEqual(published_posts[0], ethreadspected_post)
    

    def test_when_calling_five_minute_publisher_with_multiple_events_should_generate_and_publish_multi_post_thread(self):
        events = [
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Norway', 'name': 'Melodi Grand Prithreads', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylikereallyreallyreallyreallylongurl.no', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurlbutlikereallyreallyreallylong.ee', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Finland', 'name': 'Uuden Musiikin Kilpailu', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.fi', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Serbia', 'name': 'Beovizija', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.rs', 'comment': 'Recommended link', 'live': 1}]}
        ]
        summary = self.publisher.publish(events, run_date=datetime.datetime(1970, 1, 1, 19, 55, 0, 0))

        self.assertEqual(len(summary), 2)
        self.assertEqual(summary[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se)\n---------\n\U0001F1F3\U0001F1F4 Melodi Grand Prithreads - Final (https://somereallyreallyreallyreallylikereallyreallyreallyreallylongurl.no)\n---------\n\U0001F1EA\U0001F1EA Eesti Laul - Final (https://somereallyreallyreallyreallylongurlbutlikereallyreallyreallylong.ee)\n---------\n\U0001F1EB\U0001F1EE Uuden Musiikin Kilpailu - Final (https://somereallyreallyreallyreallylongurl.fi)")
        self.assertEqual(summary[1], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F7\U0001F1F8 Beovizija - Final (https://somereallyreallyreallyreallylongurl.rs)")

        published_posts = self.publisher.client.posts
        self.assertEqual(len(published_posts), 2)
        
        self.assertTrue(type(published_posts[0]) is str)
        self.assertEqual(published_posts[0], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se)\n---------\n\U0001F1F3\U0001F1F4 Melodi Grand Prithreads - Final (https://somereallyreallyreallyreallylikereallyreallyreallyreallylongurl.no)\n---------\n\U0001F1EA\U0001F1EA Eesti Laul - Final (https://somereallyreallyreallyreallylongurlbutlikereallyreallyreallylong.ee)\n---------\n\U0001F1EB\U0001F1EE Uuden Musiikin Kilpailu - Final (https://somereallyreallyreallyreallylongurl.fi)")
        self.assertTrue(type(published_posts[1]) is str)
        self.assertEqual(published_posts[1], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F7\U0001F1F8 Beovizija - Final (https://somereallyreallyreallyreallylongurl.rs)")
