from datetime import datetime, timedelta, timezone
from glob import glob

import discord

from src.dto_yr_data_complete import Timesery
from src.models import WeatherForecast
from src.utils import to_local_time

RAIN_EMOJI = "🌧"
CLOUD_EMOJI = "☁"
SHOWER_EMOJI = "🚿"
UNKOWN_EMOJI = "❓"

# Create discord embed from weather data


def weather_forecast(forecast: WeatherForecast, time_zone: str) -> discord.Embed:
    updated_at_local = to_local_time(forecast.updated_at_utc, time_zone)
    forecast_message = None
    if len(forecast.rainy_forecasts) > 0:
        forecast_message = create_rainy_hours_message(
            forecast.rainy_forecasts, time_zone
        )
    else:
        forecast_message = "No rain 😎"

    embed = discord.Embed(
        title="Weather Forecast",
        description=f"**{'Tomorrow' if forecast.is_next_day_included else 'Today'}** {forecast.symbol_code_12_h}\n {forecast_message}",
        color=0x76CCFA,
    )
    embed.set_footer(
        text=f"Forecast updated at: {updated_at_local.strftime('%Y-%m-%d %H:%M:%S')}\nHH:mm min/med/max mm. (prob)"
    )
    return embed


def create_rainy_hours_message(rainy_forecasts: list[Timesery], time_zone: str):
    # Create message from filtered data
    seperation_line = "----------------------------\n"
    rainy_hours_message = seperation_line
    prev_hour: datetime | None = None
    for forecast in rainy_forecasts:
        next_hour_forecast = forecast.data.next_1__hours
        forecast_time_local = to_local_time(forecast.time, time_zone)
        forecast_time_formatted_str = forecast_time_local.strftime("%H:%M")

        # If this hour entry not immediatly after prev -> insert seperation line
        if prev_hour and ((prev_hour + timedelta(hours=1)) < forecast.time):
            rainy_hours_message += seperation_line

        prev_hour = forecast.time

        # Create hour entry line
        rainy_hours_message += f"**{forecast_time_formatted_str}** {next_hour_forecast.details.precipitation_amount_min}/{next_hour_forecast.details.precipitation_amount}/{next_hour_forecast.details.precipitation_amount_max} ({next_hour_forecast.details.probability_of_precipitation}%) - {next_hour_forecast.summary.symbol_code}  {rain_symbol_to_emoji(forecast.data.next_1__hours.summary.symbol_code)}\n"  # type: ignore
    return rainy_hours_message


def rain_symbol_to_emoji(rain_symbol: str):
    match rain_symbol:
        case "lightrain":
            return RAIN_EMOJI * 1
        case "rain":
            return RAIN_EMOJI * 2
        case "heavyrain":
            return RAIN_EMOJI * 3
        case _ if "cloud" in rain_symbol:
            return CLOUD_EMOJI
        case _ if "shower" in rain_symbol:
            return SHOWER_EMOJI
        case _:
            return UNKOWN_EMOJI
