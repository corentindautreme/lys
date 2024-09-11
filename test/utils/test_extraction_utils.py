import datetime
import unittest

from utils.extraction_utils import get_current_season_range_for_date

class ExtractionUtilsTest(unittest.TestCase):
    def test_when_getting_current_season_range_for_date_on_august_31_then_should_return_year_n_minus_one_season_start(self):
        d = datetime.datetime(2022, 8, 31, 0, 0, 0)
        [start, end] = get_current_season_range_for_date(d)
        self.assertEqual(start, datetime.datetime(2021, 9, 1, 0, 0, 0))
        self.assertEqual(end, datetime.datetime(2022, 3, 31, 23, 59, 59))

        
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
