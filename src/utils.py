from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def to_local_time(dt: datetime, zone_info: ZoneInfo):
    return dt.astimezone(zone_info)


def to_utc(dt: datetime):
    return dt.astimezone(timezone.utc)
