from publisher.publisher import Publisher
from client.bluesky_client import BlueskyClient
from generator.weekly_generator import WeeklyGenerator
from formatter.bluesky_formatter import BlueskyFormatter

class BlueskyWeeklyPublisher(Publisher):
    def __init__(self):
        super().__init__(BlueskyClient(), WeeklyGenerator(formatter=BlueskyFormatter()))