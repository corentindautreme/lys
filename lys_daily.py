import datetime
import os
import re

try:
    import boto3
    from boto3.dynamodb.conditions import Key
except ImportError:
    pass
    
from tweepy.errors import TweepyException, HTTPException
from common import create_tweepy_client, send_tweet, DATETIME_CET_FORMAT, flag_emojis, CASSETTE_EMOJI, TROPHY_EMOJI, CLOCK_EMOJI, TV_EMOJI

GENERIC_EVENT_STRING = "{}\n---------\n" + CASSETTE_EMOJI + " {}\n" + TROPHY_EMOJI + " {}\n" + CLOCK_EMOJI + " {} CET\n---------\n" + TV_EMOJI + " {}"

def generate_event_string(event, twitter_post):
    time = datetime.datetime.strptime(event['dateTimeCet'], DATETIME_CET_FORMAT).strftime("%H:%M")
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
        watch_link_string += "."
    except KeyError:
        pass
    if watch_link_string == "":    
        watch_link_string = "(no watch link found)"
    if event['country'] not in flag_emojis:
        output.append("WARNING: no emoji found for country " + country)
        country = event['country'].upper()
    else:
        country = flag_emojis[event['country']] + " " + event['country'].upper()
    return twitter_post + GENERIC_EVENT_STRING.format(country, event['name'], event['stage'], time, watch_link_string)


def generate_daily_tweet_thread(events, is_morning):
    twitter_post = ""

    if is_morning:
        twitter_post = "TODAY | "
    else:
        twitter_post = "TONIGHT | "

    multi_parter_regex = re.compile(r".*\(part [0-9]+\)")
    event_count = len(list(filter(lambda e: re.match(multi_parter_regex, e['stage']) is None, events)))

    if len(events) == 1:
        event = events[0]
        twitter_post = generate_event_string(event, twitter_post)
        return [twitter_post]
    else:
        tweets = []
        tweets.append(twitter_post + str(event_count) + " selection show{} across Europe{}!".format(
            "s" if event_count > 1 else "",
            " and Australia" if any("Australia" == e['country'] for e in events) else "")
        )

        for event in sorted(events, key=lambda e: (e['dateTimeCet'], e['country'])):
            event_string = generate_event_string(event, twitter_post)
            tweets.append(event_string)

        return tweets


def post_tweet(client, tweet, reply_tweet_id):
    try:
        response = send_tweet(client, tweet, reply_tweet_id)
        tweet_id = response.data['id']
        return (tweet_id, [])
    except HTTPException as e:
        return (None, e.api_errors)
    except TweepyException as e:
        return (None, [str(e)])


def send_errors_via_dm(errors, total_tweets, failed_tweets):
    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_SECRET']
    api = create_tweepy_client(consumer_key, consumer_secret, access_token, access_token_secret, twitter_api_version=1)
    target_user_id = 81432351
    message = "\U000026A0 Lys daily - {}/{} failed tweets: {}".format(failed_tweets, total_tweets, str(errors))
    api.send_direct_message(recipient_id=target_user_id, text=message)
    return


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

    today_morning = today.strftime(DATETIME_CET_FORMAT)
    today_evening = today.replace(hour=23, minute=59, second=59).strftime(DATETIME_CET_FORMAT)

    events = table.scan(
        FilterExpression=Key('dateTimeCet').between(today_morning, today_evening)
    )['Items']

    if len(events) == 0:
        return

    tweets = generate_daily_tweet_thread(events, is_morning=(today.hour < 12))

    errors = []
    failed_tweets = 0
    last_tweet_id = None

    output.append(tweets[0])
    if not is_test:
        (tweet_id, api_errors) = post_tweet(client, tweet=tweets[0], reply_tweet_id=None)
        if not tweet_id:
            errors.extend(api_errors)
            failed_tweets += 1
            output.append("Failed to tweet " + tweets[0] + " - " + str(api_errors))
        else:
            last_tweet_id = tweet_id

    for i in range(1,len(tweets)):
        output.append(tweets[i])
        if not is_test:
            (tweet_id, api_errors) = post_tweet(client, tweet=tweets[i], reply_tweet_id=last_tweet_id)
            if not tweet_id:
                errors.extend(api_errors)
                failed_tweets += 1
                output.append("Failed to tweet " + tweets[i] + " - " + str(api_errors))
            else:
                last_tweet_id = tweet_id

    if len(errors) > 0:
        send_errors_via_dm(errors, len(tweets), failed_tweets)

    return output
