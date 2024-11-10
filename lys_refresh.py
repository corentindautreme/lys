import json
import requests

from collections import ChainMap

try:
    import boto3
except ImportError:
    pass


def get_all_settings(dynamodb_client, keys):
    keys_list = list(map(lambda k: {'key': {'S': k}}, keys))
    settings_items = dynamodb_client.batch_get_item(
        RequestItems={
            'lys_settings': {
                'Keys': keys_list,
                'ProjectionExpression': '#key,lys_value',
                'ExpressionAttributeNames': {'#key': 'key'}
            }
        }
    )
    settings = dict(ChainMap(*list(map(lambda setting: {setting['key']['S']: setting['lys_value']['S']}, settings_items['Responses']['lys_settings']))))
    return settings


# update the passed key/lys_value pair in the lys_settings table
def write_setting(dynamodb_client, key, value):
    dynamodb_client.update_item(
        ExpressionAttributeNames={
            '#V': 'lys_value'
        },
        ExpressionAttributeValues={
            ':v': {
                'S': value
            }
        },
        Key={
            'key': {
                'S': key,
            }
        },
        ReturnValues='ALL_NEW',
        TableName='lys_settings',
        UpdateExpression='SET #V = :v',
    )


def refresh_threads_token(token):
    print("Refreshing token: ***" + token[-10:])
    token_response = requests.get("https://graph.threads.net/refresh_access_token?grant_type=th_refresh_token&access_token=" + token)
    token_response.raise_for_status()
    return token_response.json()['access_token']


def main(event=None, context=None):
    output = []

    dry_run = False
    client = boto3.client('dynamodb')

    # list all settings to read from the database in 'keys''
    settings = get_all_settings(client, keys=["threads_access_token"])
    
    # refresh Threads token
    token = settings['threads_access_token']
    if not dry_run:
        try:
            refreshed_token = refresh_threads_token(token)
            write_setting(client, 'threads_access_token', refreshed_token)
            output.append("OLD 'threads_access_token'=***" + token[-10:])
            output.append("NEW 'threads_access_token'=***" + refreshed_token[-10:])
        except HTTPError as e:
            status = e.response.status_code
            message = e.response.text
            output.append("ERROR - Unable to refresh Threads token, status is " + str(status) + ": " + message)
    else:
        output.append("DRY RUN - did not refresh or update 'threads_access_token'")

    return output


if __name__ == '__main__':
    output = main()
    print(output)