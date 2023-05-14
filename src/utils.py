from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def to_local_time(dt: datetime, local_time_zone_key: str):
    return dt.astimezone(ZoneInfo(local_time_zone_key))


def to_utc(dt: datetime):
    return dt.astimezone(timezone.utc)
