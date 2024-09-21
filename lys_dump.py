import datetime
import requests
import json
import os
import base64

try:
    import boto3
    from boto3.dynamodb.conditions import Key
except ImportError:
    pass

from urllib3.exceptions import InsecureRequestWarning

from utils.extraction_utils import get_current_season_range_for_date, multikeysort, DecimalEncoder
from utils.time_utils import DATETIME_CET_FORMAT

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def dump_calendar_to_github():
    GITHUB_API_BASE = "https://api.github.com"

    username = os.environ['GITHUB_USERNAME']
    pat = os.environ['GITHUB_PAT']

    auth_header = base64.b64encode(str.encode(username + ":" + pat)).decode("ascii")

    with open('/tmp/lys_dump.json', 'r') as f:
        dump = f.read()

    response = requests.get(GITHUB_API_BASE + "/repos/lyseurovision/lys.github.io/branches/main", headers={'Authorization': 'Basic ' + auth_header}, verify=False)
    last_commit_sha = response.json()['commit']['sha']

    response = requests.post(GITHUB_API_BASE + "/repos/lyseurovision/lys.github.io/git/blobs", headers={'Authorization': 'Basic ' + auth_header}, json={'content': dump, 'encoding': 'utf-8'}, verify=False)
    utf8_blob_sha = response.json()['sha']

    data = {
        'base_tree': last_commit_sha,
        'tree': [
            {
                'path': 'lys_dump.json',
                'mode': '100644',
                'type': 'blob',
                'sha': utf8_blob_sha
            }
        ]
    }
    response = requests.post(GITHUB_API_BASE + "/repos/lyseurovision/lys.github.io/git/trees", headers={'Authorization': 'Basic ' + auth_header}, json=data, verify=False)
    tree_sha = response.json()['sha']

    data = {
        'message': 'Lys calendar dump',
        'author': {
            'name': 'Lys dump lambda',
            'email': 'noreply@lys.githib.io'
        },
        'parents': [
            last_commit_sha
        ],
        'tree': tree_sha
    }
    response = requests.post(GITHUB_API_BASE + "/repos/lyseurovision/lys.github.io/git/commits", headers={'Authorization': 'Basic ' + auth_header}, json=data, verify=False)
    new_commit_sha = response.json()['sha']

    data = {
        'ref': 'refs/heads/main',
        'sha': new_commit_sha
    }
    response = requests.post(GITHUB_API_BASE + "/repos/lyseurovision/lys.github.io/git/refs/heads/main", headers={'Authorization': 'Basic ' + auth_header}, json=data, verify=False)


def main(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('lys_events')

    today = datetime.datetime.now()
    (season_start, season_end) = get_current_season_range_for_date(today)
    season_start_str = season_start.strftime(DATETIME_CET_FORMAT)
    season_end_str = season_end.strftime(DATETIME_CET_FORMAT)

    events = table.scan(
        FilterExpression=Key('dateTimeCet').between(season_start_str, season_end_str)
    )['Items']
    sorted_events = multikeysort(events, ['dateTimeCet', 'country'])

    latest_dump = requests.get('https://raw.githubusercontent.com/LysEurovision/lys.github.io/main/lys_dump.json', verify=False).json()
    
    if json.dumps(latest_dump) == json.dumps(sorted_events, cls=DecimalEncoder):
        print("No diff between latest dump and current event list - nothing to do")
        return "No diff between latest dump and current event list - nothing to do"

    with open('/tmp/lys_dump.json', 'w') as f:
        f.write(json.dumps(sorted_events, cls=DecimalEncoder))

    dump_calendar_to_github()
    print("Dumped calendar to Github for season range " + season_start_str[:10] + " - " + season_end_str[:10])
    return "Dumped calendar to Github for season range " + season_start_str[:10] + " - " + season_end_str[:10]


if __name__ == '__main__':
    main(event={}, context={})