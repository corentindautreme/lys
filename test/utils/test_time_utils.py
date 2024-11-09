import datetime
import unittest

from utils.time_utils import resolve_range_from_run_date_and_mode

class TimeUtilsTest(unittest.TestCase):
    def test_when_getting_date_range_for_daily_mode_should_return_date_range_for_current_day(self):
        d = datetime.datetime(2022, 9, 1, 10, 0, 0)
        [start, end] = resolve_range_from_run_date_and_mode(d, "daily")
        self.assertEqual(start, datetime.datetime(2022, 9, 1, 10, 0, 0))
        self.assertEqual(end, datetime.datetime(2022, 9, 1, 23, 59, 59))


    def test_when_getting_date_range_for_weekly_mode_should_return_date_range_for_coming_calendar_week(self):
        d = datetime.datetime(2024, 11, 10, 16, 0, 0)
        [start, end] = resolve_range_from_run_date_and_mode(d, "weekly")
        self.assertEqual(start, datetime.datetime(2024, 11, 11, 0, 0, 0))
        self.assertEqual(end, datetime.datetime(2024, 11, 17, 23, 59, 59))


    def test_when_getting_date_range_for_5min_mode_should_return_date_range_for_next_five_minutes_ish(self):
        d = datetime.datetime(2024, 11, 10, 19, 55, 0)
        [start, end] = resolve_range_from_run_date_and_mode(d, "5min")
        self.assertEqual(start, datetime.datetime(2024, 11, 10, 19, 55, 1))
        self.assertEqual(end, datetime.datetime(2024, 11, 10, 20, 0, 0))


    def test_when_getting_date_range_for_unknown_mode_should_raise_exception(self):
        d = datetime.datetime(2024, 11, 10, 19, 55, 0)
        self.assertRaises(RuntimeError, resolve_range_from_run_date_and_mode, d, "bimonthly")