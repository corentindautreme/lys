import unittest

from publisher.bluesky_daily_publisher import BlueskyDailyPublisher
from client.mock_client import MockClient

class BlueskyDailyPublisherTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.publisher = BlueskyDailyPublisher()
        self.publisher.client = MockClient()