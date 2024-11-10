import os
import requests

from requests.exceptions import HTTPError

from client.social_media_client import SocialMediaClient
from client.publish_error import PublishError

class BlueskyClient(SocialMediaClient):
    def create_session(self):
        BLUESKY_ACCOUNT_HANDLE=os.environ['BLUESKY_ACCOUNT_HANDLE']
        BLUESKY_ACCOUNT_APP_PASSWORD=os.environ['BLUESKY_ACCOUNT_APP_PASSWORD']

        # json with accessJwt and refreshJwt
        response = requests.post(
            "https://bsky.social/xrpc/com.atproto.server.createSession",
            json={"identifier": BLUESKY_ACCOUNT_HANDLE, "password": BLUESKY_ACCOUNT_APP_PASSWORD},
        )
        response.raise_for_status()
        return response.json()

    
    def init(self):
        self.session = self.create_session()


    def publish_post(self, post):
        try:
            resp = requests.post(
                "https://bsky.social/xrpc/com.atproto.repo.createRecord",
                headers={"Authorization": "Bearer " + self.session["accessJwt"]},
                json={
                    "repo": self.session["did"],
                    "collection": "app.bsky.feed.post",
                    "record": post
                }
            )
            resp.raise_for_status()
            return resp.json()
        except HTTPError as e:
            status = e.response.status_code
            message = e.response.text
            raise PublishError("Unable to publish post to Bluesky - status is " + status, message)


    def publish(self, post, reply_post_id="", root_post_id=""):
        if reply_post_id != "" and root_post_id != "":
            post['reply'] = {
                "root": root_post_id,
                "parent": reply_post_id
            }

        # save the "id" (a json in this case) of the published post for the next post to be a reply to it 
        new_reply_post_id = self.publish_post(post)
        # if we have no root, this is the first post => this post becomes the root
        new_root_post_id = new_reply_post_id if root_post_id == "" else root_post_id
        
        return (new_reply_post_id, new_root_post_id)
