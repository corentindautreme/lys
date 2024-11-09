try:
    import boto3
except ImportError:
    pass

from collections import ChainMap

class SettingsUtils:
    def get_db_client(self):
        try:
            return boto3.client('dynamodb')
        except NameError:
            return None


    def __init__(self):
        self.cached_settings = {}
        self.db_client = self.get_db_client()


    def load_settings_from_db(self, keys):
        if len(keys) == 0:
            return {}

        keys_list = list(map(lambda k: {'key': {'S': k}}, keys))
        settings_items = self.db_client.batch_get_item(
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


    def get_settings(self, keys):
        settings = {}
        loaded_settings = {}
        keys_to_load_from_db = []
        
        for key in keys:
            if key in self.cached_settings:
                settings[key] = self.cached_settings[key]
            else:
                keys_to_load_from_db.append(key)

        if len(keys_to_load_from_db) > 0:
            loaded_settings = self.load_settings_from_db(keys_to_load_from_db)
            self.cached_settings = {**self.cached_settings, **loaded_settings}

        return {k: self.cached_settings[k] for k in keys}