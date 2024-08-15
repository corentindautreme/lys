from publisher.publisher import Publisher
from client.bluesky_client import BlueskyClient
from generator.five_minute_generator import FiveMinuteGenerator
from formatter.bluesky_formatter import BlueskyFormatter

class BlueskyFiveMinutePublisher(Publisher):
    def __init__(self):
        super().__init__(BlueskyClient(), FiveMinuteGenerator(formatter=BlueskyFormatter(), shorten_urls=True))