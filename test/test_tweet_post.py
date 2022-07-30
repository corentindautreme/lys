import unittest
import os
import tweepy

from tweepy.errors import TweepyException, HTTPException

from common import send_tweet, create_tweepy_client

class TweetPostTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if 'TWITTER_CONSUMER_KEY' not in os.environ or 'TWITTER_CONSUMER_SECRET' not in os.environ or 'TWITTER_ACCESS_TOKEN' not in os.environ or 'TWITTER_ACCESS_SECRET' not in os.environ:
            assert False, "Missing Twitter auth config environment variables"

        consumer_key = os.environ['TWITTER_CONSUMER_KEY']
        consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
        access_token = os.environ['TWITTER_ACCESS_TOKEN']
        access_token_secret = os.environ['TWITTER_ACCESS_SECRET']

        cls.tweepy_client = create_tweepy_client(consumer_key, consumer_secret, access_token, access_token_secret)

    def test_when_calling_tweet_post_method_with_thread_should_send_tweet_thread_successfully(self):
        try:
            t1_id = send_tweet(self.tweepy_client, tweet="Hello").data['id']
        except (TweepyException, HTTPException) as e:
            self.fail("An exception was raised when sending the first tweet")
        try:
            t2_id = send_tweet(self.tweepy_client, tweet="World", reply_tweet_id=t1_id).data['id']
        except (TweepyException, HTTPException) as e:
            self.tweepy_client.destroy_status(s1.id_str)
            self.fail("An exception was raised when sending the second tweet")
        try:
            self.tweepy_client.delete_tweet(t1_id)
            self.tweepy_client.delete_tweet(t2_id)
        except (TweepyException, HTTPException) as e:
            self.fail("An exception was raised when sending the first tweet")
