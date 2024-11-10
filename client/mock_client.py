from client.social_media_client import SocialMediaClient

# a mock client used in dry-runs and tests
class MockClient(SocialMediaClient):
    def __init__(self):
        self.posts = []


    def init(self):
        return


    def create_session(self):
        return


    def publish(self, post, reply_post_id="", root_post_id=""):
        self.posts.append(post)
        return ("", "")
