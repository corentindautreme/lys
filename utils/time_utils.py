import datetime

DATETIME_CET_FORMAT = "%Y-%m-%dT%H:%M:%S"


def event_timestamp_string_to_datetime(timestamp_str):
    return datetime.datetime.strptime(timestamp_str, DATETIME_CET_FORMAT)


def extract_time_from_timestamp_string(timestamp_str):
    return event_timestamp_string_to_datetime(timestamp_str).strftime("%H:%M")


def extract_weekday_and_day_from_timestamp_string(timestamp_str):
    return event_timestamp_string_to_datetime(timestamp_str).strftime("%A %d")


def get_iso_timestamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def is_morning(run_date):
    return run_date.hour < 12


def get_morning_from_run_date(run_date):
    return run_date.strftime(DATETIME_CET_FORMAT)


def get_evening_from_run_date(run_date):
    return run_date.replace(hour=23, minute=59, second=59).strftime(DATETIME_CET_FORMAT)


def resolve_range_from_run_date_and_mode(run_date, mode):
    if mode == "daily":
        today_morning = run_date
        today_evening = run_date.replace(hour=23, minute=59, second=59)
        return (today_morning, today_evening)
    elif mode == "5min":
        now = (run_date + datetime.timedelta(seconds=1))
        now_plus5min = (run_date + datetime.timedelta(minutes=5)).replace(second=0)
        return (now, now_plus5min)
    elif mode == "weekly":
        tomorrow_morning = (run_date + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0)
        next_sunday_evening = (run_date + datetime.timedelta(days=7)).replace(hour=23, minute=59, second=59)
        return (tomorrow_morning, next_sunday_evening)
    else:
        raise RuntimeError("Unknown mode=" + mode)

