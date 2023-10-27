import datetime
import os
import re

try:
    import boto3
    from boto3.dynamodb.conditions import Key
except ImportError:
    pass
    
from tweepy.errors import TweepyException, HTTPException
from common import DATETIME_CET_FORMAT, flag_emojis, CASSETTE_EMOJI, TROPHY_EMOJI, CLOCK_EMOJI, TV_EMOJI, DOWN_ARROW_EMOJI, BLUESKY, TWITTER, get_watch_link_string, get_first_watch_link
from twitter_utils import create_tweepy_client, send_tweet
from bluesky_utils import get_session, get_facets_for_event_links_in_string, generate_post, publish_post

GENERIC_EVENT_STRING = "{}\n---------\n" + CASSETTE_EMOJI + " {}\n" + TROPHY_EMOJI + " {}\n" + CLOCK_EMOJI + " {} CET\n---------\n" + TV_EMOJI + " {}"

def generate_event_string(event, post, shorten_urls=False):
    time = datetime.datetime.strptime(event['dateTimeCet'], DATETIME_CET_FORMAT).strftime("%H:%M")
    watch_link_string = ""
    try:
        watch_links = event['watchLinks']
        # tweeting only links that can be watched live
        for watch_link in list(filter(lambda wl: 'live' in wl and wl['live'], watch_links)):
            if watch_link_string != "":
                watch_link_string += " OR "
            if "link" in watch_link:
                watch_link_string += get_watch_link_string(watch_link, event['country'], shorten_urls)
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
    return post + GENERIC_EVENT_STRING.format(country, event['name'], event['stage'], time, watch_link_string)


def generate_daily_thread_posts(events, is_morning, shorten_urls=False):
    post = ""

    if is_morning:
        post = "TODAY | "
    else:
        post = "TONIGHT | "

    multi_parter_regex = re.compile(r".*\(part [0-9]+\)")
    event_count = len(list(filter(lambda e: re.match(multi_parter_regex, e['stage']) is None, events)))

    if len(events) == 1:
        event = events[0]
        post = generate_event_string(event, post, shorten_urls)
        return [post]
    else:
        posts = []
        posts.append((post + str(event_count) + " selection show{} across Europe{}! (thread " + DOWN_ARROW_EMOJI + ")").format(
            "s" if event_count > 1 else "",
            " and Australia" if any("Australia" == e['country'] for e in events) else "")
        )

        for event in events:
            event_string = generate_event_string(event, post, shorten_urls)
            posts.append(event_string)

        return posts


def generate_daily_twitter_thread(events, is_morning):
    return generate_daily_thread_posts(events, is_morning)


def generate_daily_bluesky_thread(events, is_morning):
    post_bodies = generate_daily_thread_posts(events, is_morning, shorten_urls=True)
    posts = []
    # pad the event by one so that we can reference them by idx in the following loop
    if len(post_bodies) > 1:
        events.insert(0, {})
        
    for idx, body in enumerate(post_bodies):
        facets = []
        first_link = None
        # only include facets if the post contains an event (to avoid searching facets for the initial post of a thread)
        if "CET" in body:
            event = events[idx]
            # extract link facets from post
            facets = get_facets_for_event_links_in_string([event], body)
            first_link = get_first_watch_link(event)
        posts.append(generate_post(body, facets, include_card=first_link is not None, url_for_card=first_link))
    return posts


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


def generate_thread(events, is_morning, target):
    posts = []
    if target == TWITTER:
        posts = generate_daily_thread_posts(events, is_morning)
    elif target == BLUESKY:
        posts = generate_daily_bluesky_thread(events, is_morning)
    else:
        raise ValueError("Unknown target '" + str(target) + "'")
    return posts


def post_to_twitter(tweets, is_test=True):
    output = []
    errors = []
    failed_tweets = 0
    last_tweet_id = None

    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_SECRET']
    client = create_tweepy_client(consumer_key, consumer_secret, access_token, access_token_secret, twitter_api_version=2)

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

    return output


def post_to_bluesky(posts, is_test=True):
    output = []
    session = get_session()

    # publish the first post of the thread
    if not is_test:
        parent = root = publish_post(session, posts[0])
    output.append(posts[0]['text'])

    for post in posts[1:]:
        if not is_test:
            post['reply'] = {
                "root": root,
                "parent": parent
            }
            parent = publish_post(session, post)
        output.append(post['text'])

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

    today_morning = today.strftime(DATETIME_CET_FORMAT)
    today_evening = today.replace(hour=23, minute=59, second=59).strftime(DATETIME_CET_FORMAT)

    events = table.scan(
        FilterExpression=Key('dateTimeCet').between(today_morning, today_evening)
    )['Items']

    if len(events) == 0:
        return

    target = event['target'] if "target" in event else None

    posts = []
    try:
        posts = generate_thread(sorted(events, key=lambda e: (e['dateTimeCet'], e['country'])), is_morning=(today.hour < 12), target=target)
    except ValueError as e:
        output = ["Error: Unable to generate post(s) from events - " + str(e)]
        return output

    if len(posts) == 0:
        return ["Error: Lys was unable to generate any post from " + str(len(events)) + " events"]

    try:
        output = post_to_target(posts, target=target, is_test=is_test)
    except ValueError as e:
        output = ["Error: Unable to send post(s) to target - " + str(e)]

    return output
