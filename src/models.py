import logging
from dataclasses import dataclass
from datetime import datetime

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


@dataclass(frozen=True)
class RainyForecastPeriodQuery:
    time_period: TimePeriod
    coordinates: Coordinates
