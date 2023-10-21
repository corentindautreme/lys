import datetime
import os

try:
    import boto3
    from boto3.dynamodb.conditions import Key
except ImportError:
    pass
    
from common import DATETIME_CET_FORMAT, flag_emojis, ALERT_EMOJI, BLUESKY, TWITTER, get_watch_link_string
from twitter_utils import create_tweepy_client, send_tweet


def generate_twitter_event_strings(events):
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


def generate_twitter_thread(events):
    event_strings = generate_twitter_event_strings(events)
    return build_tweets(event_strings)


def generate_bluesky_thread(events):
    # TODO identify which post of the thread includes which event (to add right facets in right post)
    # TODO return a list of list, that includes for each post a list of the indexes of the links that are present in the post?
    # ex: posts = ["Post0=link 0, link 1", "Post1=link 2"], links_idx = [[0, 1], [2]]
    # => we can then iterate on each list of links_idx and generate the facets for each post individually
    return []


def generate_thread(events, target):
    posts = []
    if target == TWITTER:
        posts = generate_twitter_thread(events)
    elif target == BLUESKY:
        posts = generate_bluesky_thread(events)
    else:
        raise ValueError("Unknown target '" + str(target) + "'")
    return posts


def post_to_twitter(tweets, is_test=True):
    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_SECRET']

    client = create_tweepy_client(consumer_key, consumer_secret, access_token, access_token_secret, twitter_api_version=2)

    output = []

    status = None
    if not is_test:
        status = send_tweet(client, tweet=tweets[0])
    output.append(tweets[0])

    for i in range(1,len(tweets)):
        if not is_test:
            status = send_tweet(client, tweet=tweets[i], reply_tweet_id=status.id_str)
        output.append(tweets[i])

    return output


def post_to_bluesky(posts, is_test=True):
    output = []
    return output


def post_to_target(posts, target, is_test=True):
    if target == TWITTER:
        output = post_to_twitter(posts, is_test)
    elif target == BLUESKY:
        output = post_to_bluesky(posts, is_test)
    else:
        raise ValueError("Unknown target '" + str(target) + "'")
    return output


def main(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('lys_events')

    is_test = "isTest" in event
    # override run date with value from the lambda event if present, otherwise default to now()
    run_date = datetime.datetime.strptime(event['runDate'], DATETIME_CET_FORMAT) if "runDate" in event else (datetime.datetime.now() + datetime.timedelta(hours=1))
    today = run_date
    output = []

    now = (today + datetime.timedelta(seconds=1)).strftime(DATETIME_CET_FORMAT)
    now_plus5min = (today + datetime.timedelta(minutes=5)).replace(second=0).strftime(DATETIME_CET_FORMAT)

    events = table.scan(
        FilterExpression=Key('dateTimeCet').between(now, now_plus5min)
    )['Items']

    if len(events) == 0:
        return

    target = event['target'] if "target" in event else None

    posts = []
    try:
        posts = generate_thread(events, target)
    except ValueError as e:
        output = ["Error: Unable to generate posts from events - " + str(e)]
        return output

    if len(posts) == 0:
        return ["Error: Lys was unable to generate any post from " + str(len(events)) + " events"]

    try:
        output = post_to_target(posts, target, is_test)
    except ValueError as e:
        output = ["Error: Unable to generate posts from events - " + str(e)]

    return output
