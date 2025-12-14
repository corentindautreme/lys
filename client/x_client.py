import os

import tweepy

from tweepy.errors import TweepyException, HTTPException

from client.social_media_client import SocialMediaClient
from client.publish_error import PublishError

class XClient(SocialMediaClient):
    def create_session(self):
        consumer_key = os.environ['TWITTER_CONSUMER_KEY']
        consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
        access_token = os.environ['TWITTER_ACCESS_TOKEN']
        access_token_secret = os.environ['TWITTER_ACCESS_SECRET']

        if self.x_api_version == 2:
            return tweepy.Client(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
            )
        else:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)
            return api


    def init(self):
        self.x_api_version = int(os.environ['TWITTER_API_VERSION'])
        self.session = self.create_session()


    def publish(self, post, reply_post_id="", root_post_id=""):
        try:
            if not reply_post_id:
                response = self.session.create_tweet(text=post)
            else:
                response = self.session.create_tweet(text=post, in_reply_to_tweet_id=reply_post_id)
            return (response.data['id'], "")
        except HTTPException as e:
            print(e)
            raise PublishError("Unable to publish post to X", e.api_errors)
        except TweepyException as e:
            print(e)
            raise PublishError("Unable to publish post to X", [str(e)])