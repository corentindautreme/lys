import os

import tweepy

from client.social_media_client import SocialMediaClient

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

	
	def __init__(self):
		self.x_api_version == int(os.environ['TWITTER_API_VERSION'])
		self.session = create_session()