import unittest

from unittest.mock import patch, MagicMock

from utils import settings_utils
from utils.settings_utils import SettingsUtils

class SettingsUtilsTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings_utils = SettingsUtils()


    def test_when_all_requested_settings_are_in_cache_should_not_fetch_them_from_db(self):
        self.settings_utils.cached_settings = {
            'setting1': 'value',
            'setting2': 'value',
            'setting3': 'value'
        }
        settings = self.settings_utils.get_settings(['setting1', 'setting2'])
        self.assertTrue("setting1" in settings)
        self.assertTrue("setting2" in settings)
        self.assertEqual(settings['setting1'], "value")
        self.assertEqual(settings['setting2'], "value")
        self.settings_utils.cached_settings = {}


    @patch.object(settings_utils.SettingsUtils, 'load_settings_from_db')
    def test_when_some_requested_settings_are_not_in_cache_should_fetch_them_from_db(self, mock_load_settings_from_db):
        self.settings_utils.cached_settings = {
            'setting1': 'value'
        }
        mock_load_settings_from_db.return_value = {'setting2': 'value', 'setting3': 'value'}
        settings = self.settings_utils.get_settings(['setting1', 'setting2', 'setting3'])
        self.assertTrue("setting1" in settings)
        self.assertTrue("setting2" in settings)
        self.assertTrue("setting3" in settings)
        self.assertEqual(settings['setting1'], "value")
        self.assertEqual(settings['setting2'], "value")
        self.assertEqual(settings['setting3'], "value")
        self.settings_utils.cached_settings = {}