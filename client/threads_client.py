import os
import requests

from requests.exceptions import HTTPError
from urllib.parse import quote

from client.social_media_client import SocialMediaClient
from client.publish_error import PublishError
from utils.settings_utils import SettingsUtils

class ThreadsClient(SocialMediaClient):
    def __init__(self):
        self.settings_utils = SettingsUtils()
        self.user_id = os.environ['THREADS_USER_ID']
        self.token = None


    def create_session(self):
        if 'THREADS_ACCESS_TOKEN' in os.environ:
            self.token = os.environ['THREADS_ACCESS_TOKEN']
        else:
            self.token = self.settings_utils.get_settings(["threads_access_token"])['threads_access_token']


    def publish(self, post, reply_post_id="", root_post_id=""):
        if self.token is None:
            self.create_session()

        formatted_post = quote(post)
        create_post_url = "https://graph.threads.net/v1.0/{user_id}/threads?media_type=TEXT&text={post}&access_token={token}".format(user_id=self.user_id, post=formatted_post, token=self.token)
        if reply_post_id != "":
            create_post_url += "&reply_to_id=" + reply_post_id

        try:
            create_response = requests.post(create_post_url)
            create_response.raise_for_status()
        except HTTPError as e:
            status = e.response.status_code
            message = e.response.text
            raise PublishError("Unable to create post on Thread - status is " + status, message)

        creation_id = create_response.json()['id']
        publish_post_url = "https://graph.threads.net/v1.0/{user_id}/threads_publish?creation_id={creation_id}&access_token={token}".format(user_id=self.user_id, creation_id=creation_id, token=self.token)

        try:
            publish_response = requests.post(publish_post_url)
            publish_response.raise_for_status()
        except HTTPError as e:
            status = e.response.status_code
            message = e.response.text
            raise PublishError("Unable to publish created post to Thread - status is " + status, message)

        # save the "id" (a json in this case) of the published post for the next post to be a reply to it 
        new_reply_post_id = publish_response.json()['id']
        # if we have no root, this is the first post => this post becomes the root
        new_root_post_id = new_reply_post_id if root_post_id == "" else root_post_id
        
        return (new_reply_post_id, new_root_post_id)
