import datetime
import os

try:
    import boto3
    from boto3.dynamodb.conditions import Key
except ImportError:
    pass

from common import flag_emojis, DATETIME_CET_FORMAT, BLUESKY, TWITTER
from twitter_utils import create_tweepy_client, send_tweet

def generate_weekly_post(events):
    # list of (weekday, country) tuples
    simplified_events = list(map(lambda e: (datetime.datetime.strptime(e['dateTimeCet'], DATETIME_CET_FORMAT).strftime("%A %d"), e['country'] + ('*' if "Final" in e['stage'] else '')), events))
    # indicates if any event is a final
    includes_final = False
    output = []

    # weekday -> [country] map
    calendar = {}
    for event in simplified_events:
        day = event[0]
        country = event[1]
        if '*' in country:
            includes_final = True
        if day not in calendar:
            calendar[day] = set()
        calendar[day].add(country)

    # building and posting the tweet
    post = "\U0001F5D3 COMING UP NEXT WEEK" + (" (* = final)" if includes_final else "") + ":\n"
    for weekday in calendar.keys():
        # building flag emojis list
        flags = ""
        for c in sorted(list(calendar[weekday])):
            final = '*' in c
            country = c.replace('*', '')
            if country not in flag_emojis:
                output.append("WARNING: no emoji found for country " + country)
                flags += "(" + c + ")"
            else:
                flags += flag_emojis[country] + ('*' if final else '')
        post += "\n - {}: {}".format(weekday, flags)

    return post, output


def post_to_twitter(twitter_post):
    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_SECRET']

    client = create_tweepy_client(consumer_key, consumer_secret, access_token, access_token_secret, twitter_api_version=2)
    send_tweet(client, tweet=twitter_post)


def post_to_bluesky():
    pass


def post_to_target(post, target):
    if target == TWITTER:
        post_to_twitter(post)
    elif target == BLUESKY:
        post_to_bluesky(post)
    else:
        raise ValueError("Unknown target '" + str(target) + "'")


def main(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('lys_events')

    is_test = "isTest" in event
    # override run date with value from the lambda event if present, otherwise default to now()
    run_date = datetime.datetime.strptime(event['runDate'], DATETIME_CET_FORMAT) if "runDate" in event else (datetime.datetime.now() + datetime.timedelta(hours=1))
    today = run_date
    tomorrow_morning = (today + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0).strftime(DATETIME_CET_FORMAT)
    next_sunday_evening = (today + datetime.timedelta(days=7)).replace(hour=23, minute=59, second=59).strftime(DATETIME_CET_FORMAT)

    events = table.scan(
        FilterExpression=Key('dateTimeCet').between(tomorrow_morning, next_sunday_evening)
    )['Items']

    if len(events) == 0:
        return

    events = sorted(events, key=lambda e: e['dateTimeCet'])

    (post, output) = generate_weekly_post(events)
    target = event['target'] if "target" in event else None
    if not is_test:
        try:
            post_to_target(post, target)
        except ValueError as e:
            output = ["Unable to post to target - " + str(e)]
            return output

    output.append(post)
    return output
