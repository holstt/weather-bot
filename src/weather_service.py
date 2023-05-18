from datetime import datetime, timedelta
from typing import Iterator

from src.dtos.yr_complete_response import (
    ForecastTimeStep,
    Next1_Hours,
    YrCompleteResponse,
)
from src.models import (
    Coordinates,
    RainyForecastHour,
    RainyForecastPeriod,
    RainyForecastPeriodQuery,
    TimePeriod,
)
from src.weather_client import YrWeatherClient

# TODO: Implement specification pattern for filtering forecasts
# class Specification(ABC):
#     @abstractmethod
#     def is_satisfied_by(self, forecast: ForecastTimeStep) -> bool:
#         pass

# class RainyForecastSpecification(Specification):
#     @override
#     def is_satisfied_by(self, forecast: ForecastTimeStep) -> bool:
#         return True


class WeatherService:
    def __init__(self, weather_client: YrWeatherClient) -> None:
        self._client = weather_client

    # Get forecast symbol code that represents the weather for the next 12 hours from a given time.
    def get_forecast_symbol_code(self, from_time: datetime, coordinates: Coordinates):
        print(f"Getting forecast symbol code for {coordinates} at {from_time}")
        json = self._client.get_complete_forecast(coordinates.lat, coordinates.lon)
        dto = YrCompleteResponse.from_dict(json)
        forecast = self._get_forecast_at_time(from_time, dto.properties.timeseries)
        return forecast.data.next_12__hours.summary.symbol_code  # type: ignore

    # Get forecast with rainy hours only
    def get_rainy_forecast(
        self, query: RainyForecastPeriodQuery
    ) -> RainyForecastPeriod | None:
        print(f"Getting rainy forecast for {query}")

        json = self._client.get_complete_forecast(
            query.coordinates.lat, query.coordinates.lon
        )
        dto = YrCompleteResponse.from_dict(json)

        # Convert to domain
        model = self._dto_to_model(query, dto)

        return model if model else None

    def _dto_to_model(
        self, query: RainyForecastPeriodQuery, weather_data: YrCompleteResponse
    ) -> RainyForecastPeriod | None:
        rainy_forecast_hours = self._get_rainy_forecast_hours(
            query.time_period, weather_data
        )
        if not rainy_forecast_hours:
            return None

        forecast_updated_at_utc = weather_data.properties.meta.updated_at

        return RainyForecastPeriod(
            forecast_updated_at_utc,
            query.coordinates,
            rainy_forecast_hours,
        )

    # Get rainy hours for a given time period
    def _get_rainy_forecast_hours(
        self, time_period: TimePeriod, weather_data: YrCompleteResponse
    ) -> list[RainyForecastHour] | None:
        rainy_forecasts: list[RainyForecastHour] = []
        for forecast_hour_dto in self._forecasts_within_period(
            weather_data,
            time_period,
        ):
            next_hour_forecast = forecast_hour_dto.data.next_1__hours
            if not (
                next_hour_forecast
                and self._is_rainy_forecast_estimated(next_hour_forecast)
            ):
                # Not a valid forecast, skip
                continue

            forecast_hour_model = RainyForecastHour(
                forecast_hour_dto.time,
                next_hour_forecast.summary.symbol_code,
                next_hour_forecast.details.precipitation_amount,  # type: ignore
                next_hour_forecast.details.precipitation_amount_min,
                next_hour_forecast.details.precipitation_amount_max,
                next_hour_forecast.details.probability_of_precipitation,
            )

            # Forecast is rainy, add to list
            rainy_forecasts.append(forecast_hour_model)

        if not rainy_forecasts:
            return None

        return rainy_forecasts

    def _get_forecast_at_time(
        self,
        time: datetime,
        forecasts: list[ForecastTimeStep],
    ):
        symbol_forecast = next(
            (forecast for forecast in forecasts if forecast.time >= time)
        )
        return symbol_forecast

    def _forecasts_within_period(
        self,
        weather_data: YrCompleteResponse,
        time_period: TimePeriod,
    ) -> Iterator[ForecastTimeStep]:
        print(
            f"Returning forecasts between period_start: {time_period.start}, and period_end: {time_period.end}"
        )
        for forecast_hour_entry in weather_data.properties.timeseries:
            if self._is_within_period(forecast_hour_entry, time_period):
                yield forecast_hour_entry

    def _is_within_period(
        self,
        forecast: ForecastTimeStep,
        time_period: TimePeriod,
    ) -> bool:
        return time_period.start <= forecast.time <= time_period.end

    # Returns too if there is a high probability of rain.
    def _is_rainy_forecast_high_prob(self, next_hour_forecast: Next1_Hours) -> bool:
        # XXX: Requires some testing.
        # XXX: Other possible values are "light_rain" and "heavy_rain" etc. Or set threshold for precipitation_amount?
        return "rain" in next_hour_forecast.summary.symbol_code

    # Returns true if there is a probability of rain in the best estimate
    def _is_rainy_forecast_estimated(self, next_hour_forecast: Next1_Hours) -> bool:
        # precipitation_amount represents the best estimate of the precipitation amount
        if (
            next_hour_forecast.details.precipitation_amount
        ):  # Can be None if not available
            return next_hour_forecast.details.precipitation_amount > 0
        return False

    # Returns true for any amount of rain, even if low probability
    def _is_rainy_forecast_any_amount(self, next_hour_forecast: Next1_Hours) -> bool:
        # precipitation_amount_max is not always available in the forecast, then use precipitation_amount instead
        # else we assume that the forecast is not rainy
        if (
            next_hour_forecast.details.precipitation_amount_max
        ):  # Can be None if not available
            return next_hour_forecast.details.precipitation_amount_max > 0
        if (
            next_hour_forecast.details.precipitation_amount
        ):  # Can be None if not available
            return next_hour_forecast.details.precipitation_amount > 0

        return False
