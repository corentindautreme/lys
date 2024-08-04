from publisher.publisher import Publisher
from client.x_client import XClient
from generator.daily_generator import DailyGenerator
from formatter.default_formatter import DefaultFormatter

class XDailyPublisher(Publisher):
    def __init__(self):
        super().__init__(XClient(), DailyGenerator(formatter=DefaultFormatter()))