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

from publisher.threads_daily_publisher import ThreadsDailyPublisher
from publisher.threads_five_minute_publisher import ThreadsFiveMinutePublisher
from publisher.threads_weekly_publisher import ThreadsWeeklyPublisher

from utils.time_utils import DATETIME_CET_FORMAT, resolve_range_from_run_date_and_mode, is_within_national_final_season


def resolve_publisher(mode, target, dry_run=True):
    p = {
        "5min": {
            "twitter": XFiveMinutePublisher(),
            "bluesky": BlueskyFiveMinutePublisher(),
            "threads": ThreadsFiveMinutePublisher()
        },
        "daily": {
            "twitter": XDailyPublisher(),
            "bluesky": BlueskyDailyPublisher(),
            "threads": ThreadsDailyPublisher()
        },
        "weekly": {
            "twitter": XWeeklyPublisher(),
            "bluesky": BlueskyWeeklyPublisher(),
            "threads": ThreadsWeeklyPublisher()
        }
    }
    try:
        publisher = p[mode][target]
        if dry_run:
            publisher.client = MockClient()

        # init the publisher and its components before using it - this allows to initialize API clients, fetch config... only when needed
        publisher.init()
        
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

    try:
        publisher = resolve_publisher(mode, target, dry_run)
    except RuntimeError as e:
        output = ["Error: Unable to resolve a publisher - error is: " + str(e)]
        return output

    # override run date with value from the lambda event if present, otherwise default to now()
    run_date = datetime.datetime.strptime(event['runDate'], DATETIME_CET_FORMAT) if "runDate" in event else (datetime.datetime.now() + datetime.timedelta(hours=1))
    
    today = run_date

    # in the normal flow, the trigger passes the events to this lambda
    if "events" in event:
        events = event['events']
    else:
        # if no event was passed to the lambda, fetch them from the database
        if not is_within_national_final_season(today):
            output = ["Run date {} is without NF season range - exiting".format(today.strftime(DATETIME_CET_FORMAT))]

            for l in output:
                print(l)
            return output

        try:
            event_date_range = resolve_range_from_run_date_and_mode(run_date, mode)
        except RuntimeError as e:
            output = ["Error: Unable to resolve date range for run with mode={} and target={} - error is: {}".format(mode, target, str(e))]

            for l in output:
                print(l)
            return output

        events_start_date = event_date_range[0].strftime(DATETIME_CET_FORMAT)
        events_end_date = event_date_range[1].strftime(DATETIME_CET_FORMAT)

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('lys_events')

        events = table.scan(
            FilterExpression=Key('dateTimeCet').between(events_start_date, events_end_date)
        )['Items']

    print(publisher.get_log_header())
    output = []

    if len(events) > 0:
        output += publisher.publish(events, run_date)

    for l in output:
        print(l)
        
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Launch Lys for the specified mode and target")
    parser.add_argument("--dry-run", dest="dry_run", help="Dry run (perform all actions, but the social media client is mocked). Injects mocked events. True by default", default=True)
    parser.add_argument("--mode", dest="mode", help="Mode (5min, daily, weekly)")
    parser.add_argument("--target", dest="target", help="Target (twitter, bluesky, threads)")
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