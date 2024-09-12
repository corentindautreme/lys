import unittest

from publisher.bluesky_five_minute_publisher import BlueskyFiveMinutePublisher
from client.mock_client import MockClient

class BlueskyFiveMinutePublisherTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.publisher = BlueskyFiveMinutePublisher()
        self.publisher.client = MockClient()