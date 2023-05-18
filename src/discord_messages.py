import logging
from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

import discord
import geopy  # type: ignore
from geopy.geocoders import Nominatim  # type: ignore

from src import time_utils
from src.models import RainyForecastHour, RainyForecastPeriod

logger = logging.getLogger(__name__)

# Messages converting model -> discord embed

RAIN_EMOJI = "🌧"
CLOUD_EMOJI = "☁"
SHOWER_EMOJI = "🚿"
UNKOWN_EMOJI = "❓"


# Returns rainy forecast embed
def rainy_weather_forecast_tomorrow(
    forecast: RainyForecastPeriod, forecast_symbol: str, user_time_zone: ZoneInfo
) -> discord.Embed:
    if not forecast.forecast_hours:
        return discord.Embed(
            title="Weather Forecast",
            description="No rain 😎",
            color=0x76CCFA,
        )

    geolocator = Nominatim(user_agent="weather-bot")
    location: geopy.Location = geolocator.reverse(f"{forecast.coordinates.lat}, {forecast.coordinates.lon}")  # type: ignore
    city: str = _extract_city(location) or "Unknown"

    updated_at_local = time_utils.to_local_time(forecast.updated_at, user_time_zone)

    weather_code_line = f"**Summary:** {forecast_symbol}\n"
    forecast_message = _create_rainy_hours_message_simple(
        forecast.forecast_hours, user_time_zone
    )
    location_line = f"Location: {city} ({forecast.coordinates.lat:.2f}, {forecast.coordinates.lon:.2f})\n"
    updated_line = f"Updated: {updated_at_local.strftime('%Y-%m-%d %H:%M:%S')}\n"

    title = f"Rain tomorrow! ☔"
    description = weather_code_line + forecast_message
    footer = location_line + updated_line

    embed = discord.Embed(
        title=title,
        description=description,
        color=0x76CCFA,
    )
    embed.set_footer(text=footer)
    return embed


# Given a Geopy Location object, attempt to extract the city or the closest equivalent.
def _extract_city(location: geopy.Location) -> str | None:
    # Order of preference for the city name
    city_keys = ["city", "town", "village", "hamlet", "suburb", "county", "state"]

    # Get the raw OSM data
    osm_data: dict[str, Any] = location.raw  # type: ignore

    # Check for the city name in the OSM data
    for key in city_keys:
        if key in osm_data["address"]:
            return osm_data["address"][key]  # type: ignore
    # If no city name was found, return None
    return None


def _create_rainy_hours_message_simple(
    forecast_hours: list[RainyForecastHour], user_time_zone: ZoneInfo
):
    # Create message from filtered data
    seperation_line = "------------------------------------\n"
    rainy_hours_message = seperation_line
    prev_hour: datetime | None = None
    for forecast_hour in forecast_hours:
        forecast_time_local = time_utils.to_local_time(
            forecast_hour.time, user_time_zone
        )
        forecast_time_formatted_str = forecast_time_local.strftime("%H:%M")

        # If this hour entry not immediatly after prev -> insert seperation line
        if prev_hour and ((prev_hour + timedelta(hours=1)) < forecast_hour.time):
            rainy_hours_message += seperation_line

        prev_hour = forecast_hour.time

        # Omit for now to keep message simple
        # precipitation_amount_elem = (
        #     f"{forecast_hour.precipitation_amount_min}-{forecast_hour.precipitation_amount_max}"
        #     if forecast_hour.precipitation_amount_max
        #     else forecast_hour.precipitation_amount
        # )
        precipitation_amount_elem = forecast_hour.precipitation_amount

        rainy_hours_message += f"**{forecast_time_formatted_str}**"
        rainy_hours_message += f" - "
        # rainy_hours_message += f" {precipation_probability_elem}" # Omit for now to keep message simple
        rainy_hours_message += f" "
        rainy_hours_message += f"{precipitation_amount_elem} mm."
        rainy_hours_message += " "
        rainy_hours_message += f"{forecast_hour.symbol_code}"
        rainy_hours_message += " "
        rainy_hours_message += f"{_rain_symbol_to_emoji(forecast_hour.symbol_code)}"
        rainy_hours_message += "\n"

    return rainy_hours_message


def _rain_symbol_to_emoji(rain_symbol: str):
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
