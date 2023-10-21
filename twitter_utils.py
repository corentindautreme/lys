import tweepy

def send_tweet(tweepy_client, tweet, reply_tweet_id=""):
    if not reply_tweet_id:
        return tweepy_client.create_tweet(text=tweet)
    return tweepy_client.create_tweet(text=tweet, in_reply_to_tweet_id=reply_tweet_id)

def create_tweepy_client(consumer_key, consumer_secret, access_token, access_token_secret, twitter_api_version):
    if twitter_api_version == 2:
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