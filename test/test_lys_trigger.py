import unittest
import datetime
import requests

from unittest.mock import patch, MagicMock

from lys_trigger import main, lambda_client

class LysTriggerTest(unittest.TestCase):
    def test_when_running_the_trigger_with_no_mode_should_return_output_with_error_message_only(self):
        event = {
            "events": [
                {
                    'country': 'Sweden',
                    'name': 'Melodifestivalen',
                    'stage': 'Final',
                    'dateTimeCet': '2021-03-13T20:00:00',
                    'watchLinks': [
                        {
                            'link': 'https://svtplay.se',
                            'comment': 'Recommended link',
                            'live': 1
                        }
                    ]
                }
            ],
            "dryRun": True,
            "targets": ["threads", "bluesky", "twitter"],
            "runDate": "2021-03-13T16:00:00"
        }
        output = main(event=event, context=None)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0], "Error: mode is not provided - unable to trigger anything")


    def test_when_running_trigger_for_targets_in_dry_mode_should_not_trigger_any_lambda(self):
        event = {
            "events": [
                {
                    'country': 'Sweden',
                    'name': 'Melodifestivalen',
                    'stage': 'Final',
                    'dateTimeCet': '2021-03-13T20:00:00',
                    'watchLinks': [
                        {
                            'link': 'https://svtplay.se',
                            'comment': 'Recommended link',
                            'live': 1
                        }
                    ]
                }
            ],
            "mode": "daily",
            "dryRun": True,
            "targets": ["threads", "bluesky", "twitter"],
            "runDate": "2021-03-13T16:00:00"
        }
        output = main(event=event, context=None)
        self.assertEqual(len(output), 4)
        self.assertEqual(output[0], "daily")
        self.assertEqual(output[1], "Loaded 1 event(s)")
        self.assertEqual(output[2], "{\"country\": \"Sweden\", \"name\": \"Melodifestivalen\", \"stage\": \"Final\", \"dateTimeCet\": \"2021-03-13T20:00:00\", \"watchLinks\": [{\"link\": \"https://svtplay.se\", \"comment\": \"Recommended link\", \"live\": 1}]}")
        self.assertEqual(output[3], "Dry-run - skipping the triggering of lambdas")


    def test_if_should_fetch_events_from_database_but_running_outside_of_nf_season_range_should_exit_without_triggering_any_lambda(self):
        event = {
            "mode": "daily",
            "dryRun": False,
            "targets": ["threads", "bluesky", "twitter"],
            "runDate": "2025-08-01T16:00:00"
        }
        output = main(event=event, context=None)
        self.assertEqual(len(output), 2)
        self.assertEqual(output[0], "daily")
        self.assertEqual(output[1], "Run date 2025-08-01T16:00:00 is without NF season range - exiting")


    def test_when_running_trigger_outside_of_dry_run_should_trigger_lambdas_for_each_target(self):
        event = {
            "events": [
                {
                    'country': 'Sweden',
                    'name': 'Melodifestivalen',
                    'stage': 'Final',
                    'dateTimeCet': '2021-03-13T20:00:00',
                    'watchLinks': [
                        {
                            'link': 'https://svtplay.se',
                            'comment': 'Recommended link',
                            'live': 1
                        }
                    ]
                }
            ],
            "mode": "daily",
            "targets": ["threads", "bluesky"],
            "runDate": "2021-03-13T16:00:00"
        }
        mock_trigger_resp = MagicMock(return_value={'StatusCode': 202})
        with patch.object(lambda_client, 'invoke', return_value=mock_trigger_resp) as mock_req:
            output = main(event=event, context=None)
        self.assertEqual(len(output), 7)
        self.assertEqual(output[0], "daily")
        self.assertEqual(output[1], "Loaded 1 event(s)")
        self.assertEqual(output[2], "{\"country\": \"Sweden\", \"name\": \"Melodifestivalen\", \"stage\": \"Final\", \"dateTimeCet\": \"2021-03-13T20:00:00\", \"watchLinks\": [{\"link\": \"https://svtplay.se\", \"comment\": \"Recommended link\", \"live\": 1}]}")
        self.assertEqual(output[3], "Triggering Lys for mode=daily and target=threads")
        self.assertTrue(output[4].startswith("Triggered Lys with status="))
        self.assertTrue(output[4].endswith(" (daily, threads)"))
