import argparse
import json
import datetime

class MockLambdaClient():
    def invoke(self):
        return

try:
    import boto3
    from boto3.dynamodb.conditions import Key
    lambda_client = boto3.client("lambda")
except ImportError:
    lambda_client = MockLambdaClient()
    pass

from utils.time_utils import DATETIME_CET_FORMAT, resolve_range_from_run_date_and_mode, is_within_national_final_season
from utils.extraction_utils import DecimalEncoder


def trigger_lys_lambda(mode, target, events):
    output = ["Triggering Lys for mode={} and target={}".format(mode, target)]

    try:
        response = lambda_client.invoke(
            FunctionName='Lys',
            InvocationType='Event',
            Payload=json.dumps({"mode": mode, "target": target, "events": events}, cls=DecimalEncoder)
        )
        output.append("Triggered Lys with status={} ({}, {})".format(response['StatusCode'], mode, target))
    except Error as e:
        output.append("Error: Unable to trigger Lys for mode={} and target={} - error is: {}".format(mode, target, str(e)))

    return output


def main(event, context):
    # settings
    dry_run = "dryRun" in event and event['dryRun'] == True
    targets = event['targets'] if "targets" in event else ["threads", "bluesky", "twitter"]
    mode = event['mode'] if "mode" in event else None

    if mode is None:
        print("Error: mode is not provided - unable to trigger anything")
        return ["Error: mode is not provided - unable to trigger anything"]

    output = ["{}|trigger".format(mode)]

    # override run date with value from the lambda event if present, otherwise default to now()
    run_date = datetime.datetime.strptime(event['runDate'], DATETIME_CET_FORMAT) if "runDate" in event else (datetime.datetime.now() + datetime.timedelta(hours=1))
    
    today = run_date

    if "events" in event:
        events = event['events']
    else:
        if not is_within_national_final_season(today):
            output.append("Run date {} is without NF season range - exiting".format(today.strftime(DATETIME_CET_FORMAT)))

            for l in output:
                print(l)
            return output

        try:
            event_date_range = resolve_range_from_run_date_and_mode(run_date, mode)
        except RuntimeError as e:
            output.append("Error: Unable to resolve date range for run with mode={} - error is: {}".format(mode, str(e)))

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

    output.append("Loaded {} event(s)".format(len(events)))

    output += map(lambda e: json.dumps(e, cls=DecimalEncoder), events)

    # trigger lambdas
    if dry_run:
        output.append("Dry-run - skipping the triggering of lambdas")
    else:
        for target in targets:
            output += trigger_lys_lambda(mode, target, events)

    for l in output:
        print(l)
        
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Trigger Lys for the specified mode")
    parser.add_argument("--dry-run", dest="dry_run", help="Dry run (performs checks and loads events, but does not trigger lambdas). True by default", default=True)
    parser.add_argument("--run-date", dest="run_date", help="Override the run date (yyyy-MM-ddTHH:mm:SS)")
    parser.add_argument("--events", dest="events", help="Manual list of events, as a JSON string")
    parser.add_argument("--mode", dest="mode", help="Mode (5min, daily, weekly)")
    parser.add_argument("--targets", dest="targets", help="(optional) Desired targets (twitter, bluesky, threads)")
    args = parser.parse_args()
    
    event = {
        "mode": args.mode,
        "dryRun": args.dry_run
    }
    if args.run_date is not None:
        event['runDate'] = args.run_date
    if args.events is not None:
        event['events'] = json.loads(args.events)
    if args.targets is not None:
        event['targets'] = args.targets.split(',')
    print(event)
    output = main(event, None)
    print(json.dumps(output, indent=4))