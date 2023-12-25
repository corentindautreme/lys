import boto3
from boto3.dynamodb.conditions import Key
import datetime
import json
import decimal
from operator import itemgetter as i
from functools import cmp_to_key
import os

DATETIME_CET_FORMAT = "%Y-%m-%dT%H:%M:%S"

def cmp(x, y):
    """
    Replacement for built-in function cmp that was removed in Python 3

    Compare the two objects x and y and return an integer according to
    the outcome. The return value is negative if x < y, zero if x == y
    and strictly positive if x > y.

    https://portingguide.readthedocs.io/en/latest/comparisons.html#the-cmp-function
    """

    return (x > y) - (x < y)

def multikeysort(items, columns):
    comparers = [
        ((i(col[1:].strip()), -1) if col.startswith('-') else (i(col.strip()), 1))
        for col in columns
    ]
    def comparer(left, right):
        comparer_iter = (
            cmp(fn(left), fn(right)) * mult
            for fn, mult in comparers
        )
        return next((result for result in comparer_iter if result), 0)
    return sorted(items, key=cmp_to_key(comparer))

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)


if __name__ == '__main__':
  dynamo_client = boto3.resource(
      'dynamodb',
      aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
      aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
  )
  events_table = dynamo_client.Table('lys_events_archive')
  countries_table = dynamo_client.Table('lys_ref_country')

  countries = {c['country']:c for c in countries_table.scan()['Items']}

  date_from = datetime.datetime(2022, 9, 1, 0, 0, 0).strftime(DATETIME_CET_FORMAT)
  date_to = datetime.datetime(2023, 3, 31, 23, 59, 59).strftime(DATETIME_CET_FORMAT)

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