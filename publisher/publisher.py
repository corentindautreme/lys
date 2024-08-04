from abc import ABC, abstractmethod

class Publisher(ABC):
    def __init__(self, client, generator):
        self.client = client
        self.generator = generator


    def set_client(self, client):
        self.client = client


    def publish_thread(self, thread):
        summary = []
        reply_post_id = parent_post_id = ""

        for post in thread:
            summary.append(post)
            try:
                (reply_post_id, parent_post_id) = self.client.publish(post, reply_post_id, parent_post_id)
            except PublishError as e:
                summary.append("Failed to publish " + post + " - " + str(e.errors))

        return summary


    def publish_daily_thread_for_events(self, events, is_morning):
        thread = generator.generate_thread(events, is_morning)
        return publish_thread(thread)
