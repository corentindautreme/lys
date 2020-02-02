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
	today_morning = today.strftime(DATETIME_CET_FORMAT)
	today_evening = today.replace(hour=23, minute=59, second=59).strftime(DATETIME_CET_FORMAT)
	output = []

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

