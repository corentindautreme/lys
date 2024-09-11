import datetime

DATETIME_CET_FORMAT = "%Y-%m-%dT%H:%M:%S"


def event_timestamp_string_to_datetime(timestamp_str):
    return datetime.datetime.strptime(timestamp_str, DATETIME_CET_FORMAT)


def extract_time_from_timestamp_string(timestamp_str):
    return event_timestamp_string_to_datetime(timestamp_str).strftime("%H:%M")


def extract_weekday_and_day_from_timestamp_string(timestamp_str):
    return event_timestamp_string_to_datetime(timestamp_str).strftime("%A %d")


def get_timestamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def is_morning(run_date):
    return run_date.hour < 12


def get_morning_from_run_date(run_date):
    return run_date.strftime(DATETIME_CET_FORMAT)


def get_evening_from_run_date(run_date):
    return run_date.replace(hour=23, minute=59, second=59).strftime(DATETIME_CET_FORMAT)
