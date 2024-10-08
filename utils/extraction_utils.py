import datetime
import json
import decimal

from operator import itemgetter as i
from functools import cmp_to_key


def get_current_season_range_for_date(date):
    if date.month > 8:
        season_start = datetime.datetime(date.year, 9, 1, 0, 0, 0)
        season_end = datetime.datetime(date.year + 1, 3, 31, 23, 59, 59)
        return (season_start, season_end)
    elif date.month >= 1:
        season_start = datetime.datetime(date.year - 1, 9, 1, 0, 0, 0)
        season_end = datetime.datetime(date.year, 3, 31, 23, 59, 59)
        return (season_start, season_end)


def cmp(x, y):
    """
    Replacement for built-in function cmp that was removed in Python 3

    Compare the two objects x and y and return an integer according to
    the outcome. The return value is negative if x < y, zero if x == y
    and strictly positive if x > y.

    https://portingguide.readthedocs.io/en/latest/comparisons.html#the-cmp-function
    """

    return (x > y) - (x < y)


def multikeysort(items, columns):
    comparers = [
        ((i(col[1:].strip()), -1) if col.startswith('-') else (i(col.strip()), 1))
        for col in columns
    ]
    def comparer(left, right):
        comparer_iter = (
            cmp(fn(left), fn(right)) * mult
            for fn, mult in comparers
        )
        return next((result for result in comparer_iter if result), 0)
    return sorted(items, key=cmp_to_key(comparer))


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)