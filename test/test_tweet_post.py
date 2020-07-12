import unittest
import os
import tweepy

from tweepy.error import TweepError

from lys import send_tweet

class TweetPostTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if 'TWITTER_CONSUMER_KEY' not in os.environ or 'TWITTER_CONSUMER_SECRET' not in os.environ or 'TWITTER_ACCESS_TOKEN' not in os.environ or 'TWITTER_ACCESS_SECRET' not in os.environ:
            assert False, "Missing Twitter auth config environment variables"

        consumer_key = os.environ['TWITTER_CONSUMER_KEY']
        consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
        access_token = os.environ['TWITTER_ACCESS_TOKEN']
        access_token_secret = os.environ['TWITTER_ACCESS_SECRET']

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        cls.tweepy_api = tweepy.API(auth)

    def test_when_calling_tweet_post_method_with_thread_should_send_tweet_thread_successfully(self):
        try:
            s1 = send_tweet(self.tweepy_api, tweet="Hello")
        except TweepError as e:
            self.fail("An exception was raised when sending the first tweet")
        try:
            s2 = send_tweet(self.tweepy_api, tweet="World", reply_status_id=s1.id_str)
        except TweepError as e:
            self.tweepy_api.destroy_status(s1.id_str)
            self.fail("An exception was raised when sending the second tweet")
        try:
            self.tweepy_api.destroy_status(s1.id_str)
            self.tweepy_api.destroy_status(s2.id_str)
        except TweepError as e:
            self.fail("An exception was raised when sending the first tweet")
