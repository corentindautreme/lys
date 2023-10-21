import datetime
from operator import itemgetter as i
from functools import cmp_to_key
import json
import decimal
import re

DATETIME_CET_FORMAT = "%Y-%m-%dT%H:%M:%S"

flag_emojis = {
    "Andorra": "\U0001F1E6\U0001F1E9",
    "Albania": "\U0001F1E6\U0001F1F1",
    "Armenia": "\U0001F1E6\U0001F1F2",
    "Austria": "\U0001F1E6\U0001F1F9",
    "Australia": "\U0001F1E6\U0001F1FA",
    "Azerbaijan": "\U0001F1E6\U0001F1FF",
    "Bosnia and Herzegovina": "\U0001F1E7\U0001F1E6",
    "Belgium": "\U0001F1E7\U0001F1EA",
    "Bulgaria": "\U0001F1E7\U0001F1EC",
    "Belarus": "\U0001F1E7\U0001F1FE",
    "Switzerland": "\U0001F1E8\U0001F1ED",
    "Cyprus": "\U0001F1E8\U0001F1FE",
    "Czech Republic": "\U0001F1E8\U0001F1FF",
    "Germany": "\U0001F1E9\U0001F1EA",
    "Denmark": "\U0001F1E9\U0001F1F0",
    "Estonia": "\U0001F1EA\U0001F1EA",
    "Spain": "\U0001F1EA\U0001F1F8",
    "Finland": "\U0001F1EB\U0001F1EE",
    "France": "\U0001F1EB\U0001F1F7",
    "United Kingdom": "\U0001F1EC\U0001F1E7",
    "Georgia": "\U0001F1EC\U0001F1EA",
    "Greece": "\U0001F1EC\U0001F1F7",
    "Croatia": "\U0001F1ED\U0001F1F7",
    "Hungary": "\U0001F1ED\U0001F1FA",
    "Ireland": "\U0001F1EE\U0001F1EA",
    "Israel": "\U0001F1EE\U0001F1F1",
    "Iceland": "\U0001F1EE\U0001F1F8",
    "Italy": "\U0001F1EE\U0001F1F9",
    "Kazakhstan": "\U0001F1F0\U0001F1FF",
    "Lebanon": "\U0001F1F1\U0001F1E7",
    "Liechtenstein": "\U0001F1F1\U0001F1EE",
    "Lithuania": "\U0001F1F1\U0001F1F9",
    "Luxembourg": "\U0001F1F1\U0001F1FA",
    "Latvia": "\U0001F1F1\U0001F1FB",
    "Morocco": "\U0001F1F2\U0001F1E6",
    "Monaco": "\U0001F1F2\U0001F1E8",
    "Moldova": "\U0001F1F2\U0001F1E9",
    "Montenegro": "\U0001F1F2\U0001F1EA",
    "Malta": "\U0001F1F2\U0001F1F9",
    "Netherlands": "\U0001F1F3\U0001F1F1",
    "North Macedonia": "\U0001F1F2\U0001F1F0",
    "Norway": "\U0001F1F3\U0001F1F4",
    "Poland": "\U0001F1F5\U0001F1F1",
    "Portugal": "\U0001F1F5\U0001F1F9",
    "Romania": "\U0001F1F7\U0001F1F4",
    "Serbia": "\U0001F1F7\U0001F1F8",
    "Russia": "\U0001F1F7\U0001F1FA",
    "Sweden": "\U0001F1F8\U0001F1EA",
    "Slovenia": "\U0001F1F8\U0001F1EE",
    "Slovakia": "\U0001F1F8\U0001F1F0",
    "San Marino": "\U0001F1F8\U0001F1F2",
    "Turkey": "\U0001F1F9\U0001F1F7",
    "Ukraine": "\U0001F1FA\U0001F1E6",
    "Kosovo": "\U0001F1FD\U0001F1F0"
}

CASSETTE_EMOJI = "\U0001F4FC"
TROPHY_EMOJI = "\U0001F3C6"
CLOCK_EMOJI = "\U0001F553"
TV_EMOJI = "\U0001F4FA"
ALERT_EMOJI = "\U0001F6A8"

BLUESKY="bluesky"
TWITTER="twitter"


def get_short_url(url):
    link_text = re.sub(
        r'https?:\/\/(www\.)?',
        '',
        url
    )
    idx_slash = link_text.find("/")
    if idx_slash > -1:
        link_text = link_text[:idx_slash]
    return link_text


def get_watch_link_string(watch_link, country, shorten_urls=False):
    has_comment = False
    watch_link_string = get_short_url(watch_link['link']) if shorten_urls else watch_link['link']
    if "comment" in watch_link and watch_link['comment'] != "" and watch_link['comment'] != "Recommended link":
        watch_link_string += " (" + watch_link['comment'] + ")"
        has_comment = True

    additional_comments = []
    if "geoblocked" in watch_link and watch_link['geoblocked']:
        additional_comments.append("geoblocked")
    if "accountRequired" in watch_link and watch_link['accountRequired']:
        account_comment = "account required: see "
        account_help_link = "https://lyseurovision.github.io/help.html#account-" + country
        account_comment += get_short_url(account_help_link) if shorten_urls else account_help_link
        additional_comments.append(account_comment)
    if len(additional_comments) > 0:
        if not has_comment:
            watch_link_string += " "
        watch_link_string += "(" + ", ".join(additional_comments) + ")"

    return watch_link_string


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