import unittest
import datetime

from common import get_current_season_range_for_date, get_watch_link_string

class CommonTest(unittest.TestCase):
    def test_when_getting_current_season_range_for_date_in_february_then_should_return_year_n_minus_one_season_start(self):
        d = datetime.datetime(2022, 2, 15, 0, 0, 0)
        [start, end] = get_current_season_range_for_date(d)
        self.assertEqual(start, datetime.datetime(2021, 9, 1, 0, 0, 0))
        self.assertEqual(end, datetime.datetime(2022, 3, 31, 23, 59, 59))


    def test_when_getting_current_season_range_for_date_in_july_then_should_return_year_n_minus_one_season_start(self):
        d = datetime.datetime(2022, 7, 15, 0, 0, 0)
        [start, end] = get_current_season_range_for_date(d)
        self.assertEqual(start, datetime.datetime(2021, 9, 1, 0, 0, 0))
        self.assertEqual(end, datetime.datetime(2022, 3, 31, 23, 59, 59))


    def test_when_getting_current_season_range_for_date_in_november_then_should_return_current_year_season_start(self):
        d = datetime.datetime(2022, 11, 15, 0, 0, 0)
        [start, end] = get_current_season_range_for_date(d)
        self.assertEqual(start, datetime.datetime(2022, 9, 1, 0, 0, 0))
        self.assertEqual(end, datetime.datetime(2023, 3, 31, 23, 59, 59))


    def test_when_getting_current_season_range_for_date_on_september_1_then_should_return_current_year_season_start(self):
        d = datetime.datetime(2022, 9, 1, 0, 0, 0)
        [start, end] = get_current_season_range_for_date(d)
        self.assertEqual(start, datetime.datetime(2022, 9, 1, 0, 0, 0))
        self.assertEqual(end, datetime.datetime(2023, 3, 31, 23, 59, 59))


    def test_when_getting_current_season_range_for_date_on_august_31_then_should_return_year_n_minus_one_season_start(self):
        d = datetime.datetime(2022, 8, 31, 0, 0, 0)
        [start, end] = get_current_season_range_for_date(d)
        self.assertEqual(start, datetime.datetime(2021, 9, 1, 0, 0, 0))
        self.assertEqual(end, datetime.datetime(2022, 3, 31, 23, 59, 59))


    def test_when_getting_watch_link_string_for_recommended_link_should_generate_string_without_comment(self):
        watch_link = {'link': 'https://svt.se/melodifestivalen', 'comment': 'Recommended link'}
        s = get_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen")


    def test_when_getting_watch_link_string_for_link_without_comment_should_generate_string_without_comment(self):
        watch_link = {'link': 'https://svt.se/melodifestivalen'}
        s = get_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen")


    def test_when_getting_watch_link_string_for_link_with_empty_comment_should_generate_string_without_comment(self):
        watch_link = {'link': 'https://svt.se/melodifestivalen', 'comment': ''}
        s = get_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen")


    def test_when_getting_watch_link_string_for_link_with_comment_should_generate_string_with_comment(self):
        watch_link = {'link': 'https://svt.se/melodifestivalen', 'comment': 'English commentary'}
        s = get_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen (English commentary)")


    def test_when_getting_watch_link_string_for_geoblocked_recommended_link_should_generate_string_with_geoblocked_comment(self):
        watch_link = {
            'link': 'https://svt.se/melodifestivalen',
            'comment': 'Recommended link',
            'geoblocked': 1
        }
        s = get_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen (geoblocked)")


    def test_when_getting_watch_link_string_for_recommended_link_requiring_account_should_generate_string_with_account_required_comment(self):
        watch_link = {
            'link': 'https://svt.se/melodifestivalen',
            'comment': 'Recommended link',
            'accountRequired': 1
        }
        s = get_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen (account required: see https://lyseurovision.github.io/help.html#account-Sweden)")


    def test_when_getting_watch_link_string_for_geoblocked_recommended_link_requiring_account_should_generate_string_with_geoblocked_and_account_required_comments(self):
        watch_link = {
            'link': 'https://svt.se/melodifestivalen',
            'comment': 'Recommended link',
            'accountRequired': 1,
            'geoblocked': 1
        }
        s = get_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen (geoblocked, account required: see https://lyseurovision.github.io/help.html#account-Sweden)")


    def test_when_getting_watch_link_string_for_geoblocked_link_with_comment_should_generate_string_with_link_comment_and_geoblocked_comment(self):
        watch_link = {
            'link': 'https://svt.se/melodifestivalen',
            'comment': 'Swedish sign language',
            'geoblocked': 1
        }
        s = get_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen (Swedish sign language)(geoblocked)")


    def test_when_getting_watch_link_string_for_link_with_comment_requiring_account_should_generate_string_with_link_and_account_required_comments(self):
        watch_link = {
            'link': 'https://svt.se/melodifestivalen',
            'comment': 'Finnish commentary',
            'accountRequired': 1
        }
        s = get_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen (Finnish commentary)(account required: see https://lyseurovision.github.io/help.html#account-Sweden)")


    def test_when_getting_watch_link_string_for_geoblocked_link_with_comment_that_requires_account_should_generate_string_with_link_comment_and_geoblocked_and_account_required_comments(self):
        watch_link = {
            'link': 'https://svt.se/melodifestivalen',
            'comment': 'Swedish sign language',
            'accountRequired': 1,
            'geoblocked': 1
        }
        s = get_watch_link_string(watch_link, country="Sweden")
        self.assertEqual(s, "https://svt.se/melodifestivalen (Swedish sign language)(geoblocked, account required: see https://lyseurovision.github.io/help.html#account-Sweden)")


    def test_when_getting_shortened_watch_link_string_for_recommended_link_should_generate_string_with_shortened_url(self):
        watch_link = {'link': 'https://svt.se/melodifestivalen', 'comment': 'Recommended link'}
        s = get_watch_link_string(watch_link, country="Sweden", shorten_urls=True)
        self.assertEqual(s, "svt.se")


    def test_when_getting_shortened_watch_link_string_for_link_with_comment_that_requires_account_should_generate_string_with_shortened_urls_and_comments(self):
        watch_link = {
            'link': 'https://svt.se/melodifestivalen/live/english/123',
            'comment': 'English commentary',
            'accountRequired': 1
        }
        s = get_watch_link_string(watch_link, country="Sweden", shorten_urls=True)
        self.assertEqual(s, "svt.se (English commentary)(account required: see lyseurovision.github.io)")


    def test_when_getting_shortened_watch_link_string_for_geoblocked_link_with_comment_that_requires_account_should_generate_string_with_shortened_urls_and_comments(self):
        watch_link = {
            'link': 'https://svt.se/melodifestivalen/live/english/123',
            'comment': 'Swedish sign language',
            'accountRequired': 1,
            'geoblocked': 1
        }
        s = get_watch_link_string(watch_link, country="Sweden", shorten_urls=True)
        self.assertEqual(s, "svt.se (Swedish sign language)(geoblocked, account required: see lyseurovision.github.io)")
