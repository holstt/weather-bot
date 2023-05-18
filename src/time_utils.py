import logging
from datetime import date, datetime, time, timezone
from multiprocessing import Value
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)


# ALWAYS USE THIS FUNCTION TO GET THE CURRENT TIME
# Get _timezone-aware_ datetime object representing the current time in UTC
def utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def now(time_zone: ZoneInfo) -> datetime:
    return as_time_zone(utc_now(), time_zone)


def at_hour(hour: int, dt: datetime) -> datetime:
    return dt.replace(hour=hour, minute=0, second=0, microsecond=0)


# NB! If no tz info on dt, dt.astimezone() will assume dt is in local time...
# Therefore, do not not accept naive datetimes as input
def assert_timezone(dt: datetime):
    if dt.tzinfo is None:
        raise ValueError("Time zone must be set on the datetime object")


def as_time_zone(dt: datetime, zone_info: ZoneInfo):
    assert_timezone(dt)
    return dt.astimezone(zone_info)


def as_utc(dt: datetime):
    return as_time_zone(dt, ZoneInfo("UTC"))


# Parses the time string in the given time zone and converts it to UTC
def parse_time_str(time_str: str, time_zone: ZoneInfo) -> time:
    time_obj = time.fromisoformat(time_str)

    # Create a date in the specified time zone
    local_dt = datetime.now(tz=time_zone).replace(
        hour=time_obj.hour,
        minute=time_obj.minute,
        second=time_obj.second,
        microsecond=time_obj.microsecond,
    )

    # Convert the date to UTC and extract the time
    utc_dt = local_dt.astimezone(ZoneInfo("UTC"))
    return utc_dt.time()
