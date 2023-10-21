import datetime
import os

try:
    import boto3
    from boto3.dynamodb.conditions import Key
except ImportError:
    pass
    
from common import DATETIME_CET_FORMAT, flag_emojis, ALERT_EMOJI, DOWN_ARROW_EMOJI, BLUESKY, TWITTER, get_watch_link_string
from twitter_utils import create_tweepy_client, send_tweet


def generate_event_string(event, shorten_urls=False):
    flag = (flag_emojis[event['country']] + " ") if event['country'] in flag_emojis else ""
    watch_link_string = ""
    try:
        watch_links = event['watchLinks']
        # tweeting only links that can be watched live
        for watch_link in list(filter(lambda wl: 'live' in wl and wl['live'], watch_links)):
            if watch_link_string != "":
                watch_link_string += " OR "
            if "link" in watch_link:
                watch_link_string += get_watch_link_string(watch_link, event['country'], shorten_urls)
    except KeyError:
        pass
    if watch_link_string == "":    
        watch_link_string = "(no watch link found)"
    else:
        watch_link_string = "(" + watch_link_string + ")"
    event_string = "\n{}{} - {} {}".format(flag, event['name'], event['stage'], watch_link_string)
    return event_string


def generate_twitter_event_strings(events):
    event_strings = []
    for event in events:
        event_strings.append(generate_event_string(event))
    return event_strings


def generate_bluesky_event_string(event):
    return generate_event_string(event, shorten_urls=True)


def build_twitter_posts(event_strings):
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


def build_bluesky_posts(events):
    post_header = ALERT_EMOJI + " 5 MINUTES REMINDER!"
    posts = []
    event_idx = []
    is_thread=False
    tmp_post = ""
    post_events = []
    for idx, event in enumerate(events):
        event_string = generate_bluesky_event_string(event)
        # bluesky character limit = 300; leaving room for the header
        if len(tmp_post+event_string) < 260:
            # add the event string to the current post
            tmp_post += "\n---------" + event_string
            # flag the index of the event in the list as part of the current post
            post_events.append(idx)
        else:
            # we're ready to save the first post
            # add the header
            post = post_header
            # if we're here, we're about to create/continue a thread, because the next event doesn't fit in the current post
            if not is_thread:
                # if we haven't started a thread yet, this means this is the first post of the thread
                post += " (thread " + DOWN_ARROW_EMOJI + ")"
            else:
                # otherwise, we're just adding another post to the thread
                post += " (cont.)"
            is_thread = True
            # the post is complete, we save it and save the indices of the events that are part of it
            post += tmp_post
            posts.append(post)
            event_idx.append(post_events)
            # we reset the tmp post, and open it with the next event (the one we couldn't add to the previous post)
            tmp_post = "\n---------" + event_string
            post_events = [idx]
    # if we're out of events but still have event strings we haven't saved to a post, we do it now
    if len(tmp_post) > 0:
        post = post_header
        if is_thread:
            post += " (cont.)"
        post += tmp_post
        posts.append(post)
        event_idx.append(post_events)

    # finally, we return the complete list of posts, alongside the indices of the events that compose it
    return (posts, event_idx)


def generate_twitter_thread(events):
    event_strings = generate_twitter_event_strings(events)
    return build_twitter_posts(event_strings)


def generate_bluesky_thread(events):
    # TODO identify which post of the thread includes which event (to add right facets in right post)
    # TODO return a list of list, that includes for each post a list of the indexes of the events that are present in the post?
    # ex: posts = ["Post0=event 0, event 1", "Post1=event 2"], event_idx = [[0, 1], [2]]
    # => we can then iterate on each list of event_idx and generate the facets for each post individually
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
