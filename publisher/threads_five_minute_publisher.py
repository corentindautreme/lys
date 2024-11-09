from publisher.publisher import Publisher
from client.threads_client import ThreadsClient
from generator.five_minute_generator import FiveMinuteGenerator

class ThreadsFiveMinutePublisher(Publisher):
    def __init__(self):
        super().__init__(ThreadsClient(), FiveMinuteGenerator(post_char_limit=450))


    def get_log_header(self):
        return "5min|threads"
