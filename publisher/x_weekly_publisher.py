from publisher.publisher import Publisher
from client.x_client import XClient
from generator.weekly_generator import WeeklyGenerator
from formatter.default_formatter import DefaultFormatter

class XWeeklyPublisher(Publisher):
    def __init__(self):
        super().__init__(XClient(), WeeklyGenerator(formatter=DefaultFormatter()))