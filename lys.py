import datetime
import os

import boto3
from boto3.dynamodb.conditions import Key

import tweepy

consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('lys_events')

GENERIC_EVENT_STRING = "{} | {} - {} at {} CET. Watch live: {}"
DATETIME_CET_FORMAT = "%Y-%m-%dT%H:%M:%S"

flag_emojis = {
    "Andorra": "\U0001F1E6\U0001F1E9",
    "Albania": "\U0001F1E6\U0001F1F1",
    "Armenia": "\U0001F1E6\U0001F1F2",
    "Austria": "\U0001F1E6\U0001F1F9",
    "Australia": "\U0001F1E6\U0001F1FA",
    "Azerbaijan": "\U0001F1E6\U0001F1FF",
    "Bosnia and Herzegovina": "\U0001F1E7\U0001F1E6",
    "Belgium": "\U0001F1E7\U0001F1EA",
    "Bulgaria": "\U0001F1E7\U0001F1EC",
    "Belarus": "\U0001F1E7\U0001F1FE",
    "Switzerland": "\U0001F1E8\U0001F1ED",
    "Cyprus": "\U0001F1E8\U0001F1FE",
    "Czech Republic": "\U0001F1E8\U0001F1FF",
    "Germany": "\U0001F1E9\U0001F1EA",
    "Denmark": "\U0001F1E9\U0001F1F0",
    "Estonia": "\U0001F1EA\U0001F1EA",
    "Spain": "\U0001F1EA\U0001F1F8",
    "Finland": "\U0001F1EB\U0001F1EE",
    "France": "\U0001F1EB\U0001F1F7",
    "United Kingdom": "\U0001F1EC\U0001F1E7",
    "Georgia": "\U0001F1EC\U0001F1EA",
    "Greece": "\U0001F1EC\U0001F1F7",
    "Croatia": "\U0001F1ED\U0001F1F7",
    "Hungary": "\U0001F1ED\U0001F1FA",
    "Ireland": "\U0001F1EE\U0001F1EA",
    "Israel": "\U0001F1EE\U0001F1F1",
    "Iceland": "\U0001F1EE\U0001F1F8",
    "Italy": "\U0001F1EE\U0001F1F9",
    "Kazakhstan": "\U0001F1F0\U0001F1FF",
    "Lebanon": "\U0001F1F1\U0001F1E7",
    "Liechtenstein": "\U0001F1F1\U0001F1EE",
    "Lithuania": "\U0001F1F1\U0001F1F9",
    "Luxembourg": "\U0001F1F1\U0001F1FA",
    "Latvia": "\U0001F1F1\U0001F1FB",
    "Morocco": "\U0001F1F2\U0001F1E6",
    "Monaco": "\U0001F1F2\U0001F1E8",
    "Moldova": "\U0001F1F2\U0001F1E9",
    "Montenegro": "\U0001F1F2\U0001F1EA",
    "Malta": "\U0001F1F2\U0001F1F9",
    "Netherlands": "\U0001F1F3\U0001F1F1",
    "North Macedonia": "\U0001F1F2\U0001F1F0",
    "Norway": "\U0001F1F3\U0001F1F4",
    "Poland": "\U0001F1F5\U0001F1F1",
    "Portugal": "\U0001F1F5\U0001F1F9",
    "Romania": "\U0001F1F7\U0001F1F4",
    "Serbia": "\U0001F1F7\U0001F1F8",
    "Russia": "\U0001F1F7\U0001F1FA",
    "Sweden": "\U0001F1F8\U0001F1EA",
    "Slovenia": "\U0001F1F8\U0001F1EE",
    "Slovakia": "\U0001F1F8\U0001F1F0",
    "San Marino": "\U0001F1F8\U0001F1F2",
    "Turkey": "\U0001F1F9\U0001F1F7",
    "Ukraine": "\U0001F1FA\U0001F1E6",
    "Kosovo": "\U0001F1FD\U0001F1F0"
}


def generate_event_string(event, twitter_post):
    time = datetime.datetime.strptime(event['dateTimeCet'], DATETIME_CET_FORMAT).strftime("%H:%M")
    watchLink = ""
    try:
        watchLink = event['watchLink']
    except KeyError:
        watchLink = "(no watch link found)"
    return twitter_post + GENERIC_EVENT_STRING.format(event['country'], event['name'], event['stage'], time, watchLink)


def main(event, context):
    is_test = "isTest" in event
    today = datetime.datetime.now() + datetime.timedelta(hours=1)
    output = []

    if today.hour > 16:
        # weekly update
        if today.weekday == 6:
            tomorrow_morning = (today + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0)
            next_sunday_evening = (today + datetime.timedelta(days=7)).replace(hour=23, minute=59, second=59)

            events = table.scan(
                FilterExpression=Key('dateTimeCet').between(tomorrow_morning, next_sunday_evening)
            )['Items']

            if len(events) == 0:
                return

            # list of (weekday, country) tuples
            simplified_events = list(map(lambda e: (datetime.datetime.strptime(e['dateTimeCet'], DATETIME_CET_FORMAT).strftime("%A"), e['country'] + '*' if e['stage'] == "Final" else ''), events))
            # indicates if any event is a final
            includes_final = False

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
            twitter_post = "Coming up next week" + " (* = final)" if includes_final else "" + ":"
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

            if not is_test:
                api.update_status(twitter_post)

            output.append(twitter_post)
            return ouput
    # daily update
    else: 
        today_morning = today.strftime(DATETIME_CET_FORMAT)
        today_evening = today.replace(hour=23, minute=59, second=59).strftime(DATETIME_CET_FORMAT)

        events = table.scan(
            FilterExpression=Key('dateTimeCet').between(today_morning, today_evening)
        )['Items']

        if len(events) == 0:
            return

        if today.hour < 12:
            twitter_post = "TODAY: "
        else:
            twitter_post = "TONIGHT: "

        if len(events) == 1:
            event = events[0]
            twitter_post = generate_event_string(event, twitter_post)
            if not is_test:
                api.update_status(twitter_post)
            return {"output" : [twitter_post]}
        else:
            event_strings = []
            for event in events:
                event_string = generate_event_string(event, twitter_post)
                event_strings.append(event_string)

            twitter_post += str(len(events)) + " selection shows across Europe{}!".format(" and Australia" if any("Australia" == e['country'] for e in events) else "")
            output.append(twitter_post)
            if not is_test:
                status = api.update_status(twitter_post)

            for event_string in event_strings:
                output.append(event_string)
                if not is_test:
                    status = api.update_status(event_string, status.id_str)

        return output

