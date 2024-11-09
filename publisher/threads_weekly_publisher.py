from publisher.publisher import Publisher
from client.threads_client import ThreadsClient
from generator.weekly_generator import WeeklyGenerator

class ThreadsWeeklyPublisher(Publisher):
    def __init__(self):
        super().__init__(ThreadsClient(), WeeklyGenerator())


    def get_log_header(self):
        return "weekly|threads"
