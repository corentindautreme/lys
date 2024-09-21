import argparse
import datetime
import json

try:
    import boto3
    from boto3.dynamodb.conditions import Key
except ImportError:
    pass

from client.mock_client import MockClient

from publisher.bluesky_daily_publisher import BlueskyDailyPublisher
from publisher.bluesky_five_minute_publisher import BlueskyFiveMinutePublisher
from publisher.bluesky_weekly_publisher import BlueskyWeeklyPublisher

from publisher.x_daily_publisher import XDailyPublisher
from publisher.x_five_minute_publisher import XFiveMinutePublisher
from publisher.x_weekly_publisher import XWeeklyPublisher

from utils.time_utils import DATETIME_CET_FORMAT


def resolve_publisher(mode, target, dry_run=True):
    p = {
        "5min": {
            "twitter": XFiveMinutePublisher(),
            "bluesky": BlueskyFiveMinutePublisher()
        },
        "daily": {
            "twitter": XDailyPublisher(),
            "bluesky": BlueskyDailyPublisher()
        },
        "weekly": {
            "twitter": XWeeklyPublisher(),
            "bluesky": BlueskyWeeklyPublisher()
        }
    }
    try:
        publisher = p[mode][target]
        if dry_run:
            publisher.client = MockClient()
        return publisher
    except KeyError as e:
        raise RuntimeError("Cannot resolve publisher for mode={} and target={}".format(mode, target))


def main(event, context):
    output = []

    # settings
    dry_run = "dryRun" in event and event['dryRun'] == True
    target = event['target'] if "target" in event else None
    mode = event['mode'] if "mode" in event else None

    if target is None or mode is None:
        output = ["Error: Unable to do anything for mode={} and target={}".format(mode, target)]
        return output

    # override run date with value from the lambda event if present, otherwise default to now()
    run_date = datetime.datetime.strptime(event['runDate'], DATETIME_CET_FORMAT) if "runDate" in event else (datetime.datetime.now() + datetime.timedelta(hours=1))
    
    today = run_date

    today_morning = today.strftime(DATETIME_CET_FORMAT)
    today_evening = today.replace(hour=23, minute=59, second=59).strftime(DATETIME_CET_FORMAT)

    if dry_run and "events" in event:
        events = event['events']
    else:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('lys_events')

        events = table.scan(
            FilterExpression=Key('dateTimeCet').between(today_morning, today_evening)
        )['Items']

    if len(events) == 0:
        return

    publisher = resolve_publisher(mode, target, dry_run)
    return publisher.publish(events, run_date)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Launch Lys for the specified mode and target")
    parser.add_argument("--dry-run", dest="dry_run", help="Dry run (perform all actions, but the social media client is mocked). True by default", default=True)
    parser.add_argument("--mode", dest="mode", help="Mode (5min, daily, weekly)")
    parser.add_argument("--target", dest="target", help="Target (twitter, bluesky)")
    args = parser.parse_args()
    event = {
        "mode": args.mode,
        "target": args.target,
        "dryRun": args.dry_run
    }
    if args.dry_run:
        event['events'] = [
            {'country': 'Denmark', 'name': 'Dansk Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://dr.dk', 'comment': 'Recommended link', 'live': 1}]},
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}
        ]
    print(event)
    output = main(event, None)
    print(json.dumps(output, indent=4))