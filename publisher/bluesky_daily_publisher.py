from publisher.publisher import Publisher
from client.bluesky_client import BlueskyClient
from generator.daily_generator import DailyGenerator
from formatter.bluesky_formatter import BlueskyFormatter

class BlueskyDailyPublisher(Publisher):
    def __init__(self):
        super().__init__(BlueskyClient(), DailyGenerator(formatter=BlueskyFormatter(), shorten_urls=True))