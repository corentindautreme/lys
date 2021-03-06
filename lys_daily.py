import datetime
import os

try:
    import boto3
    from boto3.dynamodb.conditions import Key
except ImportError:
    pass
    
from common import create_tweepy_api, send_tweet, DATETIME_CET_FORMAT, flag_emojis

GENERIC_EVENT_STRING = "{} | {} - {} at {} CET. Watch live: {}"

def generate_event_string(event, twitter_post):
    time = datetime.datetime.strptime(event['dateTimeCet'], DATETIME_CET_FORMAT).strftime("%H:%M")
    watchLink = ""
    try:
        watchLink = event['watchLink']
    except KeyError:
        watchLink = "(no watch link found)"
    if event['country'] not in flag_emojis:
        output.append("WARNING: no emoji found for country " + country)
        country = event['country']
    else:
        country = flag_emojis[event['country']] + " " + event['country']
    return twitter_post + GENERIC_EVENT_STRING.format(country, event['name'], event['stage'], time, watchLink)


def generate_daily_tweet_thread(events, is_morning):
    twitter_post = ""

    if is_morning:
        twitter_post = "TODAY: "
    else:
        twitter_post = "TONIGHT: "

    if len(events) == 1:
        event = events[0]
        twitter_post = generate_event_string(event, twitter_post)
        return [twitter_post]
    else:
        tweets = []
        tweets.append(twitter_post + str(len(events)) + " selection shows across Europe{}!".format(" and Australia" if any("Australia" == e['country'] for e in events) else ""))

        for event in sorted(events, key=lambda e: (e['dateTimeCet'], e['country'])):
            event_string = generate_event_string(event, twitter_post)
            tweets.append(event_string)

        return tweets


def main(event, context):
    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_SECRET']

    api = create_tweepy_api(consumer_key, consumer_secret, access_token, access_token_secret)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('lys_events')

    is_test = "isTest" in event
    today = datetime.datetime.now() + datetime.timedelta(hours=1)
    output = []

    today_morning = today.strftime(DATETIME_CET_FORMAT)
    today_evening = today.replace(hour=23, minute=59, second=59).strftime(DATETIME_CET_FORMAT)

    events = table.scan(
        FilterExpression=Key('dateTimeCet').between(today_morning, today_evening)
    )['Items']

    if len(events) == 0:
        return

    tweets = generate_daily_tweet_thread(events, is_morning=(today.hour < 12))

    status = None
    if not is_test:
        status = send_tweet(api, tweet=tweets[0])
    output.append(tweets[0])

    for i in range(1,len(tweets)):
        if not is_test:
            status = send_tweet(api, tweet=tweets[i], reply_status_id=status.id_str)
        output.append(tweets[i])

    return output
