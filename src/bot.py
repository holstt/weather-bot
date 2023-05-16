import argparse
import logging
from datetime import datetime, timedelta, timezone
from os import environ as env
from pathlib import Path

import discord
from discord import app_commands
from dotenv import load_dotenv

import src.messages as messages
import src.weather_service as weather_service
from src.config import AppConfig
from src.models import WeatherForecastQuery
from src.utils import to_local_time, to_utc

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
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)  # For slash commands


# Subscribe to events


@client.event
async def on_ready():
    await tree.sync()
    # Sync with specified target guild to update slash commands instantly XXX: Fix, maybe only in dev?
    # await tree.sync(guild=discord.Object(id=config.TARGET_GUILD_ID))
    ready_msg = f"Bot is online ({client.user})"
    channel = client.get_channel(config.DEV_CHANNEL_ID)
    if not channel:
        raise Exception(f"Dev channel not found (id: {config.DEV_CHANNEL_ID})")

    await channel.send(ready_msg)  # type: ignore

    # query = create_query(True, config.LAT, config.LON)
    # forecast = weather_service.get_forecast(query)
    # embed = messages.weather_forecast(
    #     forecast, config.TIME_ZONE)
    # await channel.send(embed=embed)


# @client.event
# async def on_message(message):
#     # Ignore own messages.
#     if message.author == client.user:
#         return

#     await client.process_commands(message)


# Commands  # XXX: Skal i sin egen fil, cogs?


# Command for weather forecast
@tree.command(
    name="weather",
    description="Weather forecast showing only rainy hours",
    # Sync with specific guild to update slash commands instantly XXX: Fix, maybe only in dev?
    # guild=discord.Object(id=config.TARGET_GUILD_ID),
)
async def weather(
    interaction: discord.Interaction,
    high_pred: bool = True,
    lat: float = 0.0,
    lon: float = 0.0,
):
    # Handle if lat/long specified # XXX: Har discord.py ikke bedre løsning på optional params?
    if (not lat and lon) or (lat and not lon):
        await interaction.response.send_message(
            "Please specify both latitude and longitude"
        )
        return
    # If none specified, use config
    elif not lat and not lon:
        lat = config.LAT
        lon = config.LON

    query = create_weather_forecast_query(high_pred, lat, lon)
    forecast = weather_service.get_forecast(query)
    embed = messages.weather_forecast(forecast, config.TIME_ZONE)

    # Handle if lat/lon NOT specified
    # Use coords from config file

    # elif bool(os.environ.get('DB_ENABLED')):
    #     # Look up in db
    #     _
    #     # Set up a default location using 'weather setup' or specify coordinates as parameters e.g. 54.33 66.33
    #     await ctx.send('Not implemented...')

    await interaction.response.send_message(embed=embed)


# Creates weather forecast query from specified input


def create_weather_forecast_query(is_only_high_prob: bool, lat: float, lon: float):
    current_time_utc = datetime.now(timezone.utc)
    current_time_local = to_local_time(current_time_utc, config.TIME_ZONE)
    should_include_next_day = current_time_local.hour >= SHOW_TOMORROW_AFTER_HOUR_LOCAL

    print("Should include next day: " + str(should_include_next_day))

    next_day_summary_time_local: datetime = (
        current_time_local + timedelta(days=1)
    ).replace(hour=MORNING_HOUR_LOCAL, minute=0, second=0, microsecond=0)
    print("get tomorrow local: " + str(next_day_summary_time_local))
    next_day_summary_time_utc = to_utc(next_day_summary_time_local)
    print("get tomorrow utc: " + str(next_day_summary_time_utc))

    query = WeatherForecastQuery(
        lat, lon, should_include_next_day, next_day_summary_time_utc, is_only_high_prob
    )

    return query


def run():
    client.run(config.BOT_TOKEN, log_level=logging.INFO)
