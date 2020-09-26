import datetime
import os

try:
    import boto3
    from boto3.dynamodb.conditions import Key
except ImportError:
    pass

from common import flag_emojis, create_tweepy_api, send_tweet, DATETIME_CET_FORMAT

def generate_weekly_tweet_body(events):
    # list of (weekday, country) tuples
    simplified_events = list(map(lambda e: (datetime.datetime.strptime(e['dateTimeCet'], DATETIME_CET_FORMAT).strftime("%A"), e['country'] + ('*' if e['stage'] == "Final" else '')), events))
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
            calendar[day] = []
        calendar[day].append(country)

    # building and posting the tweet
    twitter_post = "\U0001F5D3 COMING UP NEXT WEEK" + (" (* = final)" if includes_final else "") + ":"
    for weekday in calendar.keys():
        # building flag emojis list
        flags = ""
        for c in calendar[weekday]:
            final = '*' in c
            country = c.replace('*', '')
            if country not in flag_emojis:
                output.append("WARNING: no emoji found for country " + country)
                flags += "(" + c + ")"
            else:
                flags += flag_emojis[country] + ('*' if final else '')
        twitter_post += "\n - {}: {}".format(weekday, flags)

    return twitter_post, output


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
    tomorrow_morning = (today + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0).strftime(DATETIME_CET_FORMAT)
    next_sunday_evening = (today + datetime.timedelta(days=7)).replace(hour=23, minute=59, second=59).strftime(DATETIME_CET_FORMAT)

    events = table.scan(
        FilterExpression=Key('dateTimeCet').between(tomorrow_morning, next_sunday_evening)
    )['Items'] if not is_test else [{'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLink': 'https://svtplay.se'}]

    if len(events) == 0:
        return

    (twitter_post, output) = generate_weekly_tweet_body(events)

    if not is_test:
        send_tweet(api, tweet=twitter_post)

    output.append(twitter_post)
    return output