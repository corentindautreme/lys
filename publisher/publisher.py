from abc import ABC, abstractmethod

from utils.time_utils import is_morning

class Publisher(ABC):
    def __init__(self, client, generator):
        self.client = client
        self.generator = generator


    def publish_thread(self, thread):
        summary = []
        reply_post_id = root_post_id = ""

        for post in thread:
            summary.append(post)
            try:
                (reply_post_id, root_post_id) = self.client.publish(post, reply_post_id, root_post_id)
            except PublishError as e:
                summary.append("Failed to publish " + post + " - " + str(e.errors))

        return summary


    def publish(self, events, run_date):
        is_morning = is_morning(run_date)
        thread = generator.generate_thread(events, is_morning)
        return publish_thread(thread)
