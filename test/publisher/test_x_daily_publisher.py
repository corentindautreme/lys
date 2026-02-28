import unittest
import datetime

from unittest.mock import patch

from publisher.x_daily_publisher import XDailyPublisher
from client.mock_client import MockClient

class XDailyPublisherTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with patch('publisher.x_daily_publisher.XClient', new=MockClient):
            self.publisher = XDailyPublisher()
    
    def test_when_calling_daily_publisher_with_one_event_should_generate_and_publish_single_post_thread(self):
        events = [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}]
        
        summary = self.publisher.publish(events, run_date=datetime.datetime(1970, 1, 1, 9, 0, 0, 0))
        
        expected_post = "TODAY | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Final\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://svtplay.se."
        self.assertEqual(len(summary), 1)
        self.assertEqual(summary[0], expected_post)

        published_posts = self.publisher.client.posts
        self.assertEqual(len(published_posts), 1)
        self.assertTrue(type(published_posts[0]) is str)
        self.assertEqual(published_posts[0], expected_post)


    def test_when_calling_daily_publisher_with_multiple_events_should_generate_and_publish_multi_post_thread(self):
        events = [
            {'country': 'Australia', 'name': 'Australia Decides', 'stage': 'Final', 'dateTimeCet': '2021-02-13T10:30:00', 'watchLinks': [{'link': 'https://facebook.com', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Heat 5', 'dateTimeCet': '2021-02-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 2', 'dateTimeCet': '2021-02-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Serbia', 'name': 'Pesma za Evroviziju', 'stage': 'Final', 'dateTimeCet': '2021-02-13T21:00:00', 'watchLinks': [{'link': 'https://youtu.be/@pesmaevroviziju', 'comment': 'Recommended link', 'live': 1}]}
        ]

        summary = self.publisher.publish(events, run_date=datetime.datetime(1970, 1, 1, 16, 0, 0, 0))

        self.assertEqual(len(summary), 5)
        self.assertEqual(summary[0], "TONIGHT | 4 selection shows across Europe and Australia! (thread \U00002B07\U0000FE0F)")
        self.assertEqual(summary[1], "TONIGHT | \U0001F1E6\U0001F1FA AUSTRALIA\n---------\n\U0001F4FC Australia Decides\n\U0001F3C6 Final\n\U0001F553 10:30 CET\n---------\n\U0001F4FA https://facebook.com.")
        self.assertEqual(summary[2], "TONIGHT | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Heat 5\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp.")
        self.assertEqual(summary[3], "TONIGHT | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Heat 2\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://svtplay.se.")
        self.assertEqual(summary[4], "TONIGHT | \U0001F1F7\U0001F1F8 SERBIA\n---------\n\U0001F4FC Pesma za Evroviziju\n\U0001F3C6 Final\n\U0001F553 21:00 CET\n---------\n\U0001F4FA https://youtu.be/%40pesmaevroviziju.")
        
        published_posts = self.publisher.client.posts
        self.assertEqual(len(published_posts), 5)
        self.assertEqual(published_posts[0], "TONIGHT | 4 selection shows across Europe and Australia! (thread \U00002B07\U0000FE0F)")
        self.assertEqual(published_posts[1], "TONIGHT | \U0001F1E6\U0001F1FA AUSTRALIA\n---------\n\U0001F4FC Australia Decides\n\U0001F3C6 Final\n\U0001F553 10:30 CET\n---------\n\U0001F4FA https://facebook.com.")
        self.assertEqual(published_posts[2], "TONIGHT | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Heat 5\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp.")
        self.assertEqual(published_posts[3], "TONIGHT | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Heat 2\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://svtplay.se.")
        self.assertEqual(published_posts[4], "TONIGHT | \U0001F1F7\U0001F1F8 SERBIA\n---------\n\U0001F4FC Pesma za Evroviziju\n\U0001F3C6 Final\n\U0001F553 21:00 CET\n---------\n\U0001F4FA https://youtu.be/%40pesmaevroviziju.")
        