import datetime

DATETIME_CET_FORMAT = "%Y-%m-%dT%H:%M:%S"


def get_iso_timestamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def is_morning(run_date):
    return run_date.hour < 12


def get_morning_from_run_date(run_date):
    return run_date.strftime(DATETIME_CET_FORMAT)


def get_evening_from_run_date(run_date):
    return run_date.replace(hour=23, minute=59, second=59).strftime(DATETIME_CET_FORMAT)
