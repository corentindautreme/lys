import tweepy
import datetime
from operator import itemgetter as i
from functools import cmp_to_key

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

# tweepy

def send_tweet(tweepy_api, tweet, reply_status_id=""):
    if not reply_status_id:
        return tweepy_api.update_status(tweet)
    return tweepy_api.update_status(tweet, reply_status_id)

def create_tweepy_api(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

def get_current_season_range_for_date(date):
    if date.month > 3:
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
