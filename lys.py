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


def generate_event_string(event):
	time = datetime.datetime.strptime(event['dateTimeCet'], DATETIME_CET_FORMAT).strftime("%H:%M")
	return GENERIC_EVENT_STRING.format(event['country'], event['name'], event['stage'], time, event['watchLink'])


def main(event, context):
	today = datetime.datetime.now()
	today_morning = today.replace(hour=0, minute=0, second=0).strftime(DATETIME_CET_FORMAT)
	today_evening = today.replace(hour=23, minute=59, second=59).strftime(DATETIME_CET_FORMAT)

	events = table.scan(
	    FilterExpression=Key('dateTimeCet').between(today_morning, today_evening)
    )['Items']

	if len(events) == 0:
		return

	twitter_post = "TODAY: "

	if len(events) == 1:
		event = events[0]
		twitter_post += generate_event_string(event)
		api.update_status(twitter_post)
	else:
		event_strings = []
		for event in events:
			event_string = generate_event_string(event)
			event_strings.append(event_string)

		twitter_post += str(len(events)) + " selection shows across Europe!"
		status = api.update_status(twitter_post)

		for event_string in event_strings:
			status = api.update_status(event_string, status.id_str)

	return

