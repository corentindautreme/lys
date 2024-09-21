from abc import ABC, abstractmethod

from utils.time_utils import is_morning
from client.publish_error import PublishError

class Publisher(ABC):
    def __init__(self, client, generator):
        self.client = client
        self.generator = generator


    @abstractmethod
    def get_log_header(self):
        pass


    def publish_thread(self, thread):
        summary = []
        summary.append(self.get_log_header())
        reply_post_id = root_post_id = ""

        for post in thread:
            summary.append(post)
            try:
                (reply_post_id, root_post_id) = self.client.publish(post, reply_post_id, root_post_id)
            except PublishError as e:
                summary.append("Failed to publish " + post + " - " + str(e.errors))

        return summary


    def publish(self, events, run_date):
        morning = is_morning(run_date)
        thread = self.generator.generate_thread(events, morning)
        return self.publish_thread(thread)
