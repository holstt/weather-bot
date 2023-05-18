import logging
from datetime import datetime, time, timezone
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)


def to_local_time(dt: datetime, zone_info: ZoneInfo):
    return dt.astimezone(zone_info)


def to_utc(dt: datetime):
    return dt.astimezone(timezone.utc)


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
