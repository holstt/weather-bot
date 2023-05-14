# XXX: Dataclass decorator?
from dataclasses import dataclass
from datetime import datetime

from src.dto_yr_data_complete import Timesery


class WeatherForecast:
    def __init__(
        self,
        rainy_forecasts: list[Timesery],
        includes_next_day: bool,
        symbol_code_12_h: str,
        updated_at_utc: datetime,
    ) -> None:
        self.rainy_forecasts = rainy_forecasts
        # Whether entries of the next day is included in the forecast
        self.is_next_day_included = includes_next_day
        # General symbol code for this day
        self.symbol_code_12_h = symbol_code_12_h
        self.updated_at_utc = updated_at_utc


@dataclass
class WeatherForecastQuery:
    lat: float
    lon: float
    should_include_next_day: bool
    next_day_summary_time_utc: datetime
    is_only_high_prob: bool = True
