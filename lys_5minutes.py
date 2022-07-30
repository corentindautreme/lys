import datetime
import os

try:
    import boto3
    from boto3.dynamodb.conditions import Key
except ImportError:
    pass
    
from common import create_tweepy_client, send_tweet, DATETIME_CET_FORMAT, flag_emojis, ALERT_EMOJI


def generate_event_strings(events):
    event_strings = []
    for event in events:
        flag = (flag_emojis[event['country']] + " ") if event['country'] in flag_emojis else ""
        watch_link_string = ""
        try:
            watch_links = event['watchLinks']
            # tweeting only links that can be watched live
            for watch_link in list(filter(lambda wl: 'live' in wl and wl['live'], watch_links)):
                if watch_link_string != "":
                    watch_link_string += " OR "
                if "link" in watch_link:
                    watch_link_string += watch_link['link'] + ((" (" + watch_link['comment'] + ")") if "comment" in watch_link and watch_link['comment'] != "" and watch_link['comment'] != "Recommended link" else "")
                additional_comments = []
                if "geoblocked" in watch_link and watch_link['geoblocked']:
                    additional_comments.append("geoblocked")
                if "accountRequired" in watch_link and watch_link['accountRequired']:
                    additional_comments.append("account required: https://lyseurovision.github.io/help.html#account-" + event['country'])
                if len(additional_comments) > 0:
                    watch_link_string += " (" + ", ".join(additional_comments) + ")"
        except KeyError:
            pass
        if watch_link_string == "":    
            watch_link_string = "(no watch link found)"
        else:
            watch_link_string = "(" + watch_link_string + ")"
        event_string = "\n{}{} - {} {}".format(flag, event['name'], event['stage'], watch_link_string)
        event_strings.append(event_string)
    return event_strings

def build_tweets(event_strings):
    tweets = []
    tweet = ALERT_EMOJI + " 5 MINUTES REMINDER!"
    for string in event_strings:
        if len(tweet+string) < 260:
            tweet += "\n---------" + string
        else:
            tweets.append(tweet)
            tweet = string.lstrip('\n')
    if len(tweet) > 0:
        tweets.append(tweet)
    return tweets


def main(event, context):
    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_SECRET']

    client = create_tweepy_client(consumer_key, consumer_secret, access_token, access_token_secret)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('lys_events')

    is_test = "isTest" in event
    today = datetime.datetime.now() + datetime.timedelta(hours=1)
    output = []

    now = (today + datetime.timedelta(seconds=1)).strftime(DATETIME_CET_FORMAT)
    now_plus5min = (today + datetime.timedelta(minutes=5)).replace(second=0).strftime(DATETIME_CET_FORMAT)

    events = table.scan(
        FilterExpression=Key('dateTimeCet').between(now, now_plus5min)
    )['Items'] if not is_test else [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se'}]}]

    if len(events) == 0:
        return

    event_strings = generate_event_strings(events)
    tweets = build_tweets(event_strings)
    
    status = None
    if not is_test:
        status = send_tweet(client, tweet=tweets[0])
    output.append(tweets[0])

    for i in range(1,len(tweets)):
        if not is_test:
            status = send_tweet(client, tweet=tweets[i], reply_tweet_id=status.id_str)
        output.append(tweets[i])

    return output
