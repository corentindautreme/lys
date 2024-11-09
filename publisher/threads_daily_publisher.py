from publisher.publisher import Publisher
from client.threads_client import ThreadsClient
from generator.daily_generator import DailyGenerator

class ThreadsDailyPublisher(Publisher):
    def __init__(self):
        super().__init__(ThreadsClient(), DailyGenerator())


    def get_log_header(self):
        return "daily|threads"
