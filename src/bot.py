import argparse
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

import discord
from discord import TextChannel, app_commands
from dotenv import load_dotenv

import src.messages as messages
from src.config import AppConfig
from src.models import (
    Coordinates,
    RainyForecastPeriodQuery,
    RainyWeatherForecastQuery,
    TimePeriod,
)
from src.utils import to_local_time, to_utc
from src.weather_client import YrWeatherClient
from src.weather_service import WeatherService

# Not bot resp. XXX: Convert bot to class and pass config instance from main
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--env", required=False, help="Path of .env file", default=".env")
args = vars(ap.parse_args())

env_path = args["env"]
if not Path(env_path).exists():
    # print(f"WARNING: No .env file found (path was '{env_path}')")
    raise IOError(f"No .env file found (path was '{env_path}')")

# Load environment
load_dotenv(dotenv_path=args["env"])

config = AppConfig()


# XXX: Should be part of configuration
# Show next day instead of current after X (local time)
SHOW_TOMORROW_AFTER_HOUR_LOCAL = 20
MORNING_HOUR_LOCAL = 7

# Set intents
intents = discord.Intents.default()
intents.message_content = True

# bot = commands.Bot(command_prefix='!', intents=intents)
_client = discord.Client(intents=intents)
tree = app_commands.CommandTree(_client)  # For slash commands


# TODO: Use cogs instead


@_client.event
async def on_ready():
    print("Syncing slash commands...")
    # await tree.sync() # This takes a while, as it syncs with all guilds
    # Sync with specified target guild to update slash commands instantly
    target_channel: discord.TextChannel = _client.get_channel(config.TARGET_CHANNEL_ID)  # type: ignore
    await tree.sync(guild=discord.Object(id=target_channel.guild.id))
    print("Slash commands synced")

    ready_msg = f"Bot is online ({_client.user})"
    dev_channel: TextChannel = _client.get_channel(config.DEV_CHANNEL_ID)  # type: ignore
    if not dev_channel:
        raise Exception(f"Dev channel not found (id: {config.DEV_CHANNEL_ID})")

    print(ready_msg)
    await dev_channel.send(ready_msg)
    # await send_rainy_forecast(dev_channel)


# Sends a rainy forecast (if any) to the target channel # TODO: Move resp. to other layer. Should be generic method that sends any embed to target channel
async def send_rainy_forecast(channel: discord.TextChannel):
    forecast, forecast_symbol = get_rainy_forecast()

    if forecast is None or forecast_symbol is None:
        return

    embed = messages.rainy_weather_forecast_daily(
        forecast, forecast_symbol, config.TIME_ZONE
    )
    await channel.send(embed=embed)
    print("Notification sent")


def get_rainy_forecast():
    client = YrWeatherClient()
    service = WeatherService(client)

    # Get start of day in local time
    local_start_of_day = to_local_time(datetime.utcnow(), config.TIME_ZONE).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    local_start_of_day_tomorrow = local_start_of_day + timedelta(days=1)

    # Convert local day to utc period
    period_start = to_utc(local_start_of_day_tomorrow)
    period_end = period_start + timedelta(days=1)
    time_period = TimePeriod(start=period_start, end=period_end)

    print(f"Getting rainy forecast for UTC period: {time_period}")
    query = RainyForecastPeriodQuery(
        time_period=time_period,
        coordinates=Coordinates(lat=config.LAT, lon=config.LON),
    )
    forecast = service.get_rainy_forecast_new(query)

    if not forecast:
        print("No rainy forecast found for: " + str(local_start_of_day_tomorrow.date()))
        return None, None
    else:
        print("Rainy forecast found for: " + str(local_start_of_day_tomorrow.date()))
    forecast_symbol = service.get_forecast_symbol_code(
        from_time=local_start_of_day_tomorrow + timedelta(hours=8),
        coordinates=query.coordinates,
    )

    return forecast, forecast_symbol


class DiscordCommandException(Exception):
    pass


@tree.command(
    name="weather",
    description="Weather forecast showing only rainy hours",
    # Sync with specific guild to update slash commands instantly
    # guild=discord.Object(id=config.TARGET_GUILD_ID),
)
async def weather(
    interaction: discord.Interaction,
):
    current_time = datetime.now(tz=timezone.utc)
    query = create_weather_forecast_query(
        config.LAT, config.LON, False, current_time=current_time
    )
    client = YrWeatherClient()
    service = WeatherService(client)
    forecast = service.get_rainy_forecast(query)
    embed = messages.rainy_weather_forecast(forecast, config.TIME_ZONE)
    await interaction.response.send_message(embed=embed)


# # Temp. out of business
# @tree.command(
#     name="weather",
#     description="Weather forecast showing only rainy hours",
#     # Sync with specific guild to update slash commands instantly XXX: Fix, maybe only in dev?
#     # guild=discord.Object(id=config.TARGET_GUILD_ID),
# )
# async def weather(
#     interaction: discord.Interaction,
#     high_pred: bool = True,
#     lat: float = 0.0,
#     lon: float = 0.0,
# ):
#     # Handle if lat/long specified # XXX: Can we require none or both in discord command params?
#     if (not lat and lon) or (lat and not lon):
#         await interaction.response.send_message(
#             "Please specify both latitude and longitude"
#         )
#         return
#     # If none specified, use config
#     elif not lat and not lon:
#         lat = config.LAT
#         lon = config.LON

#     query = create_weather_forecast_query(high_pred, lat, lon)
#     client = WeatherClient()
#     service = WeatherService(client)
#     forecast = service.get_complete_forecast(query)
#     embed = messages.weather_forecast(forecast, config.TIME_ZONE)

#     await interaction.response.send_message(embed=embed)


# Creates weather forecast query from specified input
def create_weather_forecast_query(
    lat: float, lon: float, is_high_prob_required: bool, current_time: datetime
) -> RainyWeatherForecastQuery:
    include_next_day_from_time = get_next_day_time_if_needed(current_time)

    query = RainyWeatherForecastQuery(
        lat,
        lon,
        current_time,
        include_next_day_from_time,
        is_high_prob_required,
    )

    return query


def get_next_day_time_if_needed(current_time: datetime):
    current_time_local = to_local_time(current_time, config.TIME_ZONE)

    # If late, get entries for the next day also
    should_include_next_day = current_time_local.hour >= SHOW_TOMORROW_AFTER_HOUR_LOCAL
    print("Should include next day: " + str(should_include_next_day))
    if not should_include_next_day:
        return None

    include_next_day_from_time_local: datetime = (
        current_time_local + timedelta(days=1)
    ).replace(hour=MORNING_HOUR_LOCAL, minute=0, second=0, microsecond=0)
    include_next_day_from_time = to_utc(include_next_day_from_time_local)
    return include_next_day_from_time


def run():
    _client.run(config.BOT_TOKEN, log_level=logging.INFO)
