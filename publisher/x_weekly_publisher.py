from publisher.publisher import Publisher
from client.x_client import XClient
from generator.weekly_generator import WeeklyGenerator

class XWeeklyPublisher(Publisher):
    def __init__(self):
        super().__init__(XClient(), WeeklyGenerator())


    def get_log_header(self):
        return "weekly|twitter"
