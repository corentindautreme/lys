import boto3
from boto3.dynamodb.conditions import Key
import datetime
import json
import os

from utils.extraction_utils import get_current_season_range_for_date, multikeysort, DecimalEncoder
from utils.time_utils import DATETIME_CET_FORMAT

if __name__ == '__main__':
  dynamo_client = boto3.resource(
      'dynamodb',
      aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
      aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
  )
  events_table = dynamo_client.Table('lys_events_archive')
  countries_table = dynamo_client.Table('lys_ref_country')

  countries = {c['country']:c for c in countries_table.scan()['Items']}

  date_from = datetime.datetime(2023, 9, 1, 0, 0, 0).strftime(DATETIME_CET_FORMAT)
  date_to = datetime.datetime(2024, 3, 31, 23, 59, 59).strftime(DATETIME_CET_FORMAT)

  events = events_table.scan(
          FilterExpression=Key('dateTimeCet').between(date_from, date_to)
      )['Items']

  sorted_events = multikeysort(events, ['dateTimeCet', 'country'])

  # print("\n".join(list(map(lambda e: "{} | {} - {}".format(e['country'], e['name'], e['stage']), sorted_events))))

  # uncomment below for legacy watch links format (single watchLink string)

  # for event in sorted_events:
  #   event['watchLinks'] = []
  #   for link_str in list(filter(lambda s: '/' in s and 'no link found' not in s, event['watchLink'].split(" OR "))):
  #     event['watchLinks'].append({
  #        "accountRequired": 1 if 'account required' in event['watchLink'] else 0,
  #        "channel": countries[event['country']]['defaultChannel'] if 'defaultChannel' in countries[event['country']] else '',
  #        "link": link_str
  #     })
  #   del event['watchLink']


  # if you want to print something specific:

  # for event in sorted_events:
  #   if event['country'] == 'San Marino':
  #       print(event['stage'] + ": " + event['watchLinks'][1]['link'])

  print(json.dumps(sorted_events, cls=DecimalEncoder, indent=4))