import unittest
import datetime
import requests

from unittest.mock import patch, MagicMock

from lys import main

class LysTest(unittest.TestCase):
    def test_when_running_lys_with_no_mode_should_return_output_with_error_message_only(self):
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
            "target": "twitter"
        }
        output = main(event=event, context=None)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0], "Error: Unable to do anything for mode=None and target=twitter")


    def test_when_running_lys_with_any_mode_and_no_target_should_return_output_with_error_message_only(self):
        event = {
            "mode": "daily",
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
            "dryRun": True
        }
        output = main(event=event, context=None)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0], "Error: Unable to do anything for mode=daily and target=None")


    def test_when_running_lys_with_unknown_mode_should_fail_at_date_range_resolution_and_return_output_with_error_message_only(self):
        event = {
            "mode": "yearly",
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
            "target": "threads"
        }
        output = main(event=event, context=None)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0], "Error: Unable to resolve date range for run with mode=yearly and target=threads - error is: Unknown mode=yearly")


    def test_when_running_lys_with_mode_5min_and_no_event_should_return_output_with_log_header_only(self):
        event = {
            "mode": "5min",
            "events": [],
            "dryRun": True,
            "target": "bluesky"
        }
        output = main(event=event, context=None)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0], "5min|bluesky")

        
    def test_when_running_lys_with_mode_daily_and_no_event_should_return_output_with_log_header_only(self):
        event = {
            "mode": "daily",
            "events": [],
            "dryRun": True,
            "target": "twitter"
        }
        output = main(event=event, context=None)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0], "daily|twitter")

        
    def test_when_running_lys_with_mode_weekly_and_no_event_should_return_output_with_log_header_only(self):
        event = {
            "mode": "weekly",
            "events": [],
            "dryRun": True,
            "target": "twitter"
        }
        output = main(event=event, context=None)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0], "weekly|twitter")

        
    def test_when_running_lys_with_mode_daily_target_twitter_should_return_output_with_log_header_and_published_posts(self):
        event = {
            "mode": "daily",
            "events": [
                {'country': 'Australia', 'name': 'Australia Decides', 'stage': 'Final', 'dateTimeCet': '2021-02-13T10:30:00', 'watchLinks': [{'link': 'https://facebook.com', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Heat 5', 'dateTimeCet': '2021-02-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 2', 'dateTimeCet': '2021-02-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}
            ],
            "dryRun": True,
            "target": "twitter",
            "runDate": "2020-01-01T16:00:00"
        }
        output = main(event=event, context=None)
        self.assertEqual(len(output), 5)
        self.assertEqual(output[0], "daily|twitter")
        self.assertEqual(output[1], "TONIGHT | 3 selection shows across Europe and Australia! (thread \U00002B07\U0000FE0F)")
        self.assertEqual(output[2], "TONIGHT | \U0001F1E6\U0001F1FA AUSTRALIA\n---------\n\U0001F4FC Australia Decides\n\U0001F3C6 Final\n\U0001F553 10:30 CET\n---------\n\U0001F4FA https://facebook.com.")
        self.assertEqual(output[3], "TONIGHT | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Heat 5\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp.")
        self.assertEqual(output[4], "TONIGHT | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Heat 2\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://svtplay.se.")

        
    def test_when_running_lys_with_mode_weekly_target_twitter_should_return_output_with_log_header_and_published_post(self):
        event = {
            "mode": "weekly",
            "events": [
                {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-02-02T20:00:00', 'watchLinks': [{'link': 'https://err.tv', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1 (part 2)', 'dateTimeCet': '2021-02-02T21:30:00', 'watchLinks': [{'link': 'https://err.tv', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-06T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-02-06T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}]}
            ],
            "dryRun": True,
            "target": "twitter"
        }
        output = main(event=event, context=None)
        self.assertEqual(len(output), 2)
        self.assertEqual(output[0], "weekly|twitter")
        self.assertEqual(output[1], "\U0001F5D3 COMING UP NEXT WEEK (* = final):\n\n - Tuesday 02: \U0001F1EA\U0001F1EA\n - Saturday 06: \U0001F1F3\U0001F1F4*\U0001F1F8\U0001F1EA")
        

    def test_when_running_lys_with_mode_5min_target_twitter_should_return_output_with_log_header_and_published_posts(self):
        event = {
            "mode": "5min",
            "events": [
                {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.no', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.ee', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Finland', 'name': 'Uuden Musiikin Kilpailu', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.fi', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Serbia', 'name': 'Beovizija', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.rs', 'comment': 'Recommended link', 'live': 1}]}
            ],
            "dryRun": True,
            "target": "twitter"
        }
        output = main(event=event, context=None)
        self.assertEqual(len(output), 4)
        self.assertEqual(output[0], "5min|twitter")
        self.assertEqual(output[1], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se)\n---------\n\U0001F1F3\U0001F1F4 Melodi Grand Prix - Final (https://somereallyreallyreallyreallylongurl.no)")
        self.assertEqual(output[2], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1EA\U0001F1EA Eesti Laul - Final (https://somereallyreallyreallyreallylongurl.ee)\n---------\n\U0001F1EB\U0001F1EE Uuden Musiikin Kilpailu - Final (https://somereallyreallyreallyreallylongurl.fi)")
        self.assertEqual(output[3], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F7\U0001F1F8 Beovizija - Final (https://somereallyreallyreallyreallylongurl.rs)")

        
    def test_when_running_lys_with_mode_daily_target_threads_should_return_output_with_log_header_and_published_posts(self):
        event = {
            "mode": "daily",
            "events": [
                {'country': 'Australia', 'name': 'Australia Decides', 'stage': 'Final', 'dateTimeCet': '2021-02-13T10:30:00', 'watchLinks': [{'link': 'https://facebook.com', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Heat 5', 'dateTimeCet': '2021-02-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 2', 'dateTimeCet': '2021-02-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}
            ],
            "dryRun": True,
            "target": "threads",
            "runDate": "2020-01-01T16:00:00"
        }
        output = main(event=event, context=None)
        self.assertEqual(len(output), 5)
        self.assertEqual(output[0], "daily|threads")
        self.assertEqual(output[1], "TONIGHT | 3 selection shows across Europe and Australia! (thread \U00002B07\U0000FE0F)")
        self.assertEqual(output[2], "TONIGHT | \U0001F1E6\U0001F1FA AUSTRALIA\n---------\n\U0001F4FC Australia Decides\n\U0001F3C6 Final\n\U0001F553 10:30 CET\n---------\n\U0001F4FA https://facebook.com.")
        self.assertEqual(output[3], "TONIGHT | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Heat 5\n\U0001F553 19:50 CET\n---------\n\U0001F4FA https://nrk.no/mgp.")
        self.assertEqual(output[4], "TONIGHT | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Heat 2\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://svtplay.se.")

        
    def test_when_running_lys_with_mode_weekly_target_threads_should_return_output_with_log_header_and_published_post(self):
        event = {
            "mode": "weekly",
            "events": [
                {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-02-02T20:00:00', 'watchLinks': [{'link': 'https://err.tv', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1 (part 2)', 'dateTimeCet': '2021-02-02T21:30:00', 'watchLinks': [{'link': 'https://err.tv', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-06T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-02-06T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}]}
            ],
            "dryRun": True,
            "target": "threads"
        }
        output = main(event=event, context=None)
        self.assertEqual(len(output), 2)
        self.assertEqual(output[0], "weekly|threads")
        self.assertEqual(output[1], "\U0001F5D3 COMING UP NEXT WEEK (* = final):\n\n - Tuesday 02: \U0001F1EA\U0001F1EA\n - Saturday 06: \U0001F1F3\U0001F1F4*\U0001F1F8\U0001F1EA")
        

    def test_when_running_lys_with_mode_5min_target_threads_should_return_output_with_log_header_and_published_posts(self):
        event = {
            "mode": "5min",
            "events": [
                {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylikereallyreallyreallyreallylongurl.no', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurlbutlikereallyreallyreallylong.ee', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Finland', 'name': 'Uuden Musiikin Kilpailu', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.fi', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Serbia', 'name': 'Beovizija', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.rs', 'comment': 'Recommended link', 'live': 1}]}
            ],
            "dryRun": True,
            "target": "threads"
        }
        output = main(event=event, context=None)
        self.assertEqual(len(output), 3)
        self.assertEqual(output[0], "5min|threads")
        self.assertEqual(output[1], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (https://svtplay.se)\n---------\n\U0001F1F3\U0001F1F4 Melodi Grand Prix - Final (https://somereallyreallyreallyreallylikereallyreallyreallyreallylongurl.no)\n---------\n\U0001F1EA\U0001F1EA Eesti Laul - Final (https://somereallyreallyreallyreallylongurlbutlikereallyreallyreallylong.ee)\n---------\n\U0001F1EB\U0001F1EE Uuden Musiikin Kilpailu - Final (https://somereallyreallyreallyreallylongurl.fi)")
        self.assertEqual(output[2], "\U0001F6A8 5 MINUTES REMINDER!\n---------\n\U0001F1F7\U0001F1F8 Beovizija - Final (https://somereallyreallyreallyreallylongurl.rs)")

        
    def test_when_running_lys_with_mode_daily_target_bluesky_should_return_output_with_log_header_and_published_posts(self):
        event = {
            "mode": "daily",
            "events": [
                {'country': 'Australia', 'name': 'Australia Decides', 'stage': 'Final', 'dateTimeCet': '2021-02-13T10:30:00', 'watchLinks': [{'link': 'https://facebook.com', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Heat 5', 'dateTimeCet': '2021-02-13T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 2', 'dateTimeCet': '2021-02-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}
            ],
            "dryRun": True,
            "target": "bluesky",
            "runDate": "2020-01-01T16:00:00"
        }

        mock_requests_resp = MagicMock(text="""
            <meta property="og:title" content="MOCK_TITLE"/>
            <meta property="og:description" content="MOCK_DESCRIPTION"/>
        """)
        with patch.object(requests, 'get', return_value=mock_requests_resp) as mock_req:
            output = main(event=event, context=None)

        self.assertEqual(len(output), 5)
        self.assertEqual(output[0], "daily|bluesky")
        self.assertTrue(type(output[1]) is dict)
        self.assertEqual(output[1]['text'], "TONIGHT | 3 selection shows across Europe and Australia! (thread \U00002B07\U0000FE0F)")
        self.assertTrue(type(output[2]) is dict)
        self.assertEqual(output[2]['text'], "TONIGHT | \U0001F1E6\U0001F1FA AUSTRALIA\n---------\n\U0001F4FC Australia Decides\n\U0001F3C6 Final\n\U0001F553 10:30 CET\n---------\n\U0001F4FA facebook.com.")
        self.assertTrue(type(output[3]) is dict)
        self.assertEqual(output[3]['text'], "TONIGHT | \U0001F1F3\U0001F1F4 NORWAY\n---------\n\U0001F4FC Melodi Grand Prix\n\U0001F3C6 Heat 5\n\U0001F553 19:50 CET\n---------\n\U0001F4FA nrk.no.")
        self.assertTrue(type(output[4]) is dict)
        self.assertEqual(output[4]['text'], "TONIGHT | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Heat 2\n\U0001F553 20:00 CET\n---------\n\U0001F4FA svtplay.se.")
        
        
    def test_when_running_lys_with_mode_weekly_target_bluesky_should_return_output_with_log_header_and_published_post(self):
        event = {
            "mode": "weekly",
            "events": [
                {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1', 'dateTimeCet': '2021-02-02T20:00:00', 'watchLinks': [{'link': 'https://err.tv', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Semi-final 1 (part 2)', 'dateTimeCet': '2021-02-02T21:30:00', 'watchLinks': [{'link': 'https://err.tv', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 1', 'dateTimeCet': '2021-02-06T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-02-06T19:50:00', 'watchLinks': [{'link': 'https://nrk.no/mgp', 'comment': 'Recommended link', 'live': 1}]}
            ],
            "dryRun": True,
            "target": "bluesky"
        }
        output = main(event=event, context=None)
        self.assertEqual(len(output), 2)
        self.assertEqual(output[0], "weekly|bluesky")
        self.assertTrue(type(output[1]) is dict)
        self.assertEqual(output[1]['text'], "\U0001F5D3 COMING UP NEXT WEEK (* = final):\n\n - Tuesday 02: \U0001F1EA\U0001F1EA\n - Saturday 06: \U0001F1F3\U0001F1F4*\U0001F1F8\U0001F1EA")
        

    def test_when_running_lys_with_mode_5min_target_bluesky_should_return_output_with_log_header_and_published_posts(self):
        event = {
            "mode": "5min",
            "events": [
                {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Norway', 'name': 'Melodi Grand Prix', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.no', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Estonia', 'name': 'Eesti Laul', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.ee', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Finland', 'name': 'Uuden Musiikin Kilpailu', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.fi', 'comment': 'Recommended link', 'live': 1}]},
                {'country': 'Serbia', 'name': 'Beovizija', 'stage': 'Final', 'dateTimeCet': '2021-03-13T20:00:00', 'watchLinks': [{'link': 'https://somereallyreallyreallyreallylongurl.rs', 'comment': 'Recommended link', 'live': 1}]}
            ],
            "dryRun": True,
            "target": "bluesky"
        }
        output = main(event=event, context=None)
        self.assertEqual(len(output), 3)
        self.assertEqual(output[0], "5min|bluesky")
        self.assertTrue(type(output[1]) is dict)
        self.assertEqual(output[1]['text'], "\U0001F6A8 5 MINUTES REMINDER! (thread \U00002B07\U0000FE0F)\n---------\n\U0001F1F8\U0001F1EA Melodifestivalen - Final (svtplay.se)\n---------\n\U0001F1F3\U0001F1F4 Melodi Grand Prix - Final (somereallyreallyreallyreallylongurl.no)\n---------\n\U0001F1EA\U0001F1EA Eesti Laul - Final (somereallyreallyreallyreallylongurl.ee)")
        self.assertTrue(type(output[2]) is dict)
        self.assertEqual(output[2]['text'], "\U0001F6A8 5 MINUTES REMINDER! (cont.)\n---------\n\U0001F1EB\U0001F1EE Uuden Musiikin Kilpailu - Final (somereallyreallyreallyreallylongurl.fi)\n---------\n\U0001F1F7\U0001F1F8 Beovizija - Final (somereallyreallyreallyreallylongurl.rs)")
