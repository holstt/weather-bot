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
    RainyWeatherForecast,
    RainyWeatherForecastQuery,
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

    # Retrieves a rainy forecast using the new models
    def get_rainy_forecast_new(
        self, query: RainyForecastPeriodQuery
    ) -> RainyForecastPeriod | None:
        json = self._client.get_complete_forecast(
            query.coordinates.lat, query.coordinates.lon
        )
        dto = YrCompleteResponse.from_dict(json)

        # Convert to domain
        model = self._dto_to_new_model(query, dto)

        return model if model else None

    def _dto_to_new_model(
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

    # Retrieves a rainy forecast.
    def get_rainy_forecast(
        self, query: RainyWeatherForecastQuery
    ) -> RainyWeatherForecast:
        json = self._client.get_complete_forecast(query.lat, query.lon)
        dto = YrCompleteResponse.from_dict(json)

        # Convert to domain
        model = self._dto_to_model(dto, query)
        return model

    def _dto_to_model(
        self, weather_data: YrCompleteResponse, query: RainyWeatherForecastQuery
    ) -> RainyWeatherForecast:
        period_start_time = query.period_start
        period_end_time = self._get_end_time(
            period_start_time, has_next_day=bool(query.include_next_day_from_time)
        )
        time_period = TimePeriod(period_start_time, period_end_time)

        forecast_symbol = self._get_forecast_symbol(
            weather_data.properties.timeseries,
            after_time=query.include_next_day_from_time,
        )

        rainy_forecasts = self._get_rainy_forecasts(
            weather_data, query.is_high_prob_required, time_period
        )
        forecast_updated_at_utc = weather_data.properties.meta.updated_at

        return RainyWeatherForecast(
            rainy_forecasts,
            query.include_next_day_from_time is not None,
            forecast_symbol,
            forecast_updated_at_utc,
        )

    def _get_end_time(self, period_start_time: datetime, has_next_day: bool):
        # Default to end of day
        period_end_time = period_start_time.replace(hour=23, minute=59, second=59)
        if has_next_day:
            # Bump end time to tomorrow
            period_end_time = period_end_time + timedelta(days=1)
        return period_end_time

    def _get_forecast_symbol(
        self,
        forecast_time_steps: list[ForecastTimeStep],
        after_time: datetime | None = None,
    ):
        # Find the forecast entry that should be used to determine the general forecast symbol
        symbol_forecast = forecast_time_steps[0]
        if after_time:
            symbol_forecast = self._get_forecast_at_time(
                after_time,
                forecast_time_steps,
            )

        # TODO: Handle if no 12h symbol exists
        forecast_symbol = symbol_forecast.data.next_12__hours.summary.symbol_code  # type: ignore
        return forecast_symbol

    def _get_forecast_at_time(
        self,
        time: datetime,
        forecasts: list[ForecastTimeStep],
    ):
        symbol_forecast = next(
            (forecast for forecast in forecasts if forecast.time >= time)
        )
        return symbol_forecast

    def _get_rainy_forecasts(
        self,
        weather_data: YrCompleteResponse,
        is_high_prob_required: bool,
        time_period: TimePeriod,
    ) -> list[ForecastTimeStep]:
        rainy_forecasts: list[ForecastTimeStep] = []
        for forecast_hour_entry in self._forecasts_within_period(
            weather_data, time_period
        ):
            next_hour_forecast = forecast_hour_entry.data.next_1__hours
            if not (
                next_hour_forecast
                and self._is_rainy_forecast_estimated(next_hour_forecast)
            ):
                # Not a valid forecast, skip
                continue

            # If high probability of rain is required, only include forecasts with rain symbol
            if is_high_prob_required and not self._is_rainy_forecast_high_prob(
                next_hour_forecast
            ):
                # Not rainy enough, skip
                continue

            # Forecast is rainy, add to list
            rainy_forecasts.append(forecast_hour_entry)
        return rainy_forecasts

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
