import logging
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from tracemalloc import start
from zoneinfo import ZoneInfo

from src import time_utils

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Coordinates:
    lat: float
    lon: float


# Represents a forecast at a specific hour of the day
@dataclass(frozen=True)
class RainyForecastHour:
    time: datetime  # XXX: Time object?
    symbol_code: str
    precipitation_amount: float
    precipitation_amount_min: float | None
    precipitation_amount_max: float | None
    precipitation_probability: float | None


# Represents a period of time with rainy forecast
@dataclass(frozen=True)
class RainyForecastPeriod:
    updated_at: datetime
    coordinates: Coordinates
    forecast_hours: list[RainyForecastHour]


@dataclass(frozen=True)
class TimePeriod:
    start: datetime
    end: datetime

    @staticmethod
    def from_full_days(current_time: datetime, num_days: int = 1) -> "TimePeriod":
        time_utils.assert_timezone(current_time)
        current_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        return TimePeriod(
            start=current_time,
            # End of day is start of next day minus 1 microsecond
            end=current_time + timedelta(days=num_days, microseconds=-1),
        )

    def as_time_zone(self, time_zone: ZoneInfo) -> "TimePeriod":
        return TimePeriod(
            start=time_utils.as_time_zone(self.start, time_zone),
            end=time_utils.as_time_zone(self.end, time_zone),
        )

    def as_utc(self) -> "TimePeriod":
        return self.as_time_zone(ZoneInfo("UTC"))


@dataclass(frozen=True)
class RainyForecastPeriodQuery:
    time_period: TimePeriod
    coordinates: Coordinates
