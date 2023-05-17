from dataclasses import dataclass
from datetime import datetime

from src.dtos.yr_complete_response import ForecastTimeStep


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


# TODO: Consider classes below belonging to old version of message
@dataclass(frozen=True)
class RainyForecastPeriodQuery:
    time_period: TimePeriod
    coordinates: Coordinates


# A weather forecast containing only rainy hours
@dataclass
class RainyWeatherForecast:
    forecast_hours: list[ForecastTimeStep]
    # Whether entries of the next day is included in the forecast
    is_next_day_included: bool
    # General symbol code for this weather forecast
    forecast_symbol: str
    updated_at_utc: datetime


@dataclass
class RainyWeatherForecastQuery:
    lat: float
    lon: float
    period_start: datetime
    # Whether and from which time the next day should be included
    include_next_day_from_time: datetime | None  # XXX: Make more generic
    # Whether only forecasts with high probability of rain should be included
    is_high_prob_required: bool = True
