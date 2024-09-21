import boto3
from boto3.dynamodb.conditions import Key
import datetime
import json
import os

from utils.extraction_utils import DecimalEncoder
from utils.time_utils import DATETIME_CET_FORMAT

if __name__ == '__main__':
  dynamo_client = boto3.resource(
      'dynamodb',
      aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
      aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
  )
  events_archive_table = dynamo_client.Table('lys_events_archive')
  events_table = dynamo_client.Table('lys_events')
  countries_table = dynamo_client.Table('lys_ref_country')

  countries = {c['country']:c for c in countries_table.scan()['Items']}

  date_from = datetime.datetime(2023, 9, 1, 0, 0, 0).strftime(DATETIME_CET_FORMAT)
  date_to = datetime.datetime(2024, 3, 31, 23, 59, 59).strftime(DATETIME_CET_FORMAT)

  events = events_table.scan(
          FilterExpression=Key('dateTimeCet').between(date_from, date_to)
      )['Items']
  event_ids = set(map(lambda e: e['id'], events))

  archived_events = events_archive_table.scan(
          FilterExpression=Key('dateTimeCet').between(date_from, date_to)
      )['Items']
  archived_ids = set(map(lambda e: e['id'], archived_events))

  # missing_event_ids_in_archive = list(event_ids - archived_ids)
  # print(missing_event_ids_in_archive)

  # for event_id in missing_event_ids_in_archive:
  #   event = list(filter(lambda e: e['id'] == event_id, events))[0]
  #   print(json.dumps(event, cls=DecimalEncoder, indent=4))
  #   events_archive_table.put_item(Item=event)

  # for event in events:
  #   events_archive_table.put_item(Item=event)

  # for event in events:
  #   events_table.delete_item(Key={'id': event['id'], 'dateTimeCet': event['dateTimeCet']})
