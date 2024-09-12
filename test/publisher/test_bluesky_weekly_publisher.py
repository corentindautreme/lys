import unittest

from publisher.bluesky_weekly_publisher import BlueskyWeeklyPublisher
from client.mock_client import MockClient

class BlueskyWeeklyPublisherTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.publisher = BlueskyWeeklyPublisher()
        self.publisher.client = MockClient()