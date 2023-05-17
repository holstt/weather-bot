import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path

import discord
from discord import TextChannel, app_commands
from dotenv import load_dotenv

import src.messages as messages
from src import config
from src.models import Coordinates, RainyForecastPeriodQuery, TimePeriod
from src.utils import to_local_time, to_utc
from src.weather_client import YrWeatherClient
from src.weather_service import WeatherService

app_config = config.load_config()

SYNC_SLASH_COMMANDS = False

# Set intents
intents = discord.Intents.default()
intents.message_content = True

# bot = commands.Bot(command_prefix='!', intents=intents)
_client = discord.Client(intents=intents)
tree = app_commands.CommandTree(_client)  # For slash commands


# TODO: Use cogs instead


@_client.event
async def on_ready():
    if SYNC_SLASH_COMMANDS:
        print("Syncing slash commands...")
        # await tree.sync() # This takes a while, as it syncs with all guilds
        # Sync with specified target guild to update slash commands instantly
        target_channel: discord.TextChannel = _client.get_channel(app_config.target_channel_id)  # type: ignore
        await tree.sync(guild=discord.Object(id=target_channel.guild.id))
        print("Slash commands synced")

    ready_msg = f"Bot is online ({_client.user})"
    dev_channel: TextChannel = _client.get_channel(app_config.dev_channel_id)  # type: ignore
    if not dev_channel:
        raise Exception(f"Dev channel not found (id: {app_config.dev_channel_id})")

    print(ready_msg)
    await dev_channel.send(ready_msg)
    # await send_rainy_forecast(dev_channel)


# Sends a rainy forecast (if any) to the target channel # TODO: Move resp. to other layer. Should be generic method that sends any embed to target channel
async def send_rainy_forecast(channel: discord.TextChannel):
    forecast, forecast_symbol = get_rainy_forecast()

    if forecast is None or forecast_symbol is None:
        return

    embed = messages.rainy_weather_forecast_daily(
        forecast, forecast_symbol, app_config.time_zone
    )
    await channel.send(embed=embed)
    print("Notification sent")


def get_rainy_forecast():
    client = YrWeatherClient()
    service = WeatherService(client)

    # Get start of day in local time
    local_start_of_day = to_local_time(datetime.utcnow(), app_config.time_zone).replace(
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
        coordinates=Coordinates(lat=app_config.lat, lon=app_config.lon),
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


def run():
    _client.run(app_config.bot_token, log_level=logging.INFO)
