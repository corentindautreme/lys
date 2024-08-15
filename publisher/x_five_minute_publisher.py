from publisher.publisher import Publisher
from client.x_client import XClient
from generator.five_minute_generator import FiveMinuteGenerator

class XFiveMinutePublisher(Publisher):
    def __init__(self):
        super().__init__(XClient(), FiveMinuteGenerator())