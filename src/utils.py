from datetime import timezone
from zoneinfo import ZoneInfo


def to_local_time(dt, local_time_zone):
    return dt.astimezone(ZoneInfo(local_time_zone))


def to_utc(dt):
    return dt.astimezone(timezone.utc)

