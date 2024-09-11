import unittest
import re
import datetime
import requests

from bs4 import BeautifulSoup
from unittest.mock import patch, MagicMock

from formatter.bluesky_formatter import BlueskyFormatter

class BlueskyFormatterTest(unittest.TestCase):
    # below matches YYYY-MM-DD'T'HH:mm:SS.SSSSSS'Z'
    ISO_TIMESTAMP_PATTERN = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}Z")
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formatter = BlueskyFormatter()
        self.maxDiff = 1000


    def is_dt_not_older_than(self, dt, minutes=None, seconds=None):
        now = datetime.datetime.now(datetime.timezone.utc)
        if minutes is not None:
            return dt >= now - datetime.timedelta(minutes=minutes)
        return dt >= now - datetime.timedelta(seconds=seconds)


    def test_when_formatting_post_with_no_event_should_generate_post_without_facets_nor_link_card(self):
        post_string = "\U0001F5D3 COMING UP NEXT WEEK:\n\n - Saturday 06: \U0001F1F8\U0001F1EA"
        post = self.formatter.format_post(post_string)
        self.assertTrue(type(post) is dict)
        self.assertEqual(post['text'], post_string)
        self.assertEqual(post['$type'], "app.bsky.feed.post")
        self.assertEqual(post['langs'], ["en-US"])
        self.assertTrue("facets" not in post)
        self.assertTrue("embed" not in post)
        self.assertTrue(self.ISO_TIMESTAMP_PATTERN.match(post['createdAt']))
        post_datetime = datetime.datetime.fromisoformat(post['createdAt'].replace("Z", "+00:00"))
        # verify that the attached datetime is in the past (and reasonably close to now)
        self.assertTrue(self.is_dt_not_older_than(post_datetime, seconds=2))


    def test_when_formatting_post_with_event_and_link_card_enabled_should_generate_post_with_facets_and_link_card(self):
        self.formatter.include_link_card = True

        events = [
            {'country': 'Sweden', 'name': 'Melodifestivalen', 'stage': 'Heat 2', 'dateTimeCet': '2021-02-13T20:00:00', 'watchLinks': [{'link': 'https://svtplay.se', 'comment': 'Recommended link', 'live': 1}]}
        ]
        post_string = "TODAY | \U0001F1F8\U0001F1EA SWEDEN\n---------\n\U0001F4FC Melodifestivalen\n\U0001F3C6 Heat 2\n\U0001F553 20:00 CET\n---------\n\U0001F4FA https://svtplay.se."
        
        mock_requests_resp = MagicMock(text="<>")
        with patch.object(BeautifulSoup, 'find', side_effect=[{"content": "MOCK_TITLE"}, {"content": "MOCK_DESCR"}]) as mock_bs, patch.object(requests, 'get', return_value=mock_requests_resp) as mock_req:
            post = self.formatter.format_post(post_string, events)

        self.assertTrue(type(post) is dict)
        self.assertEqual(post['text'], post_string)
        self.assertEqual(post['$type'], "app.bsky.feed.post")
        self.assertEqual(post['langs'], ["en-US"])
        self.assertTrue(self.ISO_TIMESTAMP_PATTERN.match(post['createdAt']))
        post_datetime = datetime.datetime.fromisoformat(post['createdAt'].replace("Z", "+00:00"))
        # verify that the attached datetime is in the past (and reasonably close to now)
        self.assertTrue(self.is_dt_not_older_than(post_datetime, seconds=2))

        self.assertTrue(type(post['facets']) is list)

        self.assertTrue(type(post['embed']) is dict)
        self.assertEqual(post['embed']['$type'], "app.bsky.embed.external")
        self.assertEqual(post['embed']['external']['uri'], "https://svtplay.se")
        self.assertEqual(post['embed']['external']['title'], "MOCK_TITLE")
        self.assertEqual(post['embed']['external']['description'], "MOCK_DESCRIPTION")

        self.formatter.include_link_card = False
