import requests
import os

from client.social_media_client import SocialMediaClient

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

	
	def __init__(self):
		self.session = create_session()