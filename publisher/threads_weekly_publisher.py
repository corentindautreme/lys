from publisher.publisher import Publisher
from client.threads_client import ThreadsClient
from generator.weekly_generator import WeeklyGenerator
from formatter.threads_formatter import ThreadsFormatter

class ThreadsWeeklyPublisher(Publisher):
    def __init__(self):
        super().__init__(ThreadsClient(), WeeklyGenerator(formatter=ThreadsFormatter()))


    def get_log_header(self):
        return "weekly|threads"
