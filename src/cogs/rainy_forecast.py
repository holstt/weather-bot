import logging
from datetime import datetime, timedelta

import discord
from discord import app_commands
from discord.ext import commands, tasks

import src.discord_messages as discord_messages
from src import config
from src.bot import WeatherBot
from src.models import Coordinates, RainyForecastPeriodQuery, TimePeriod
from src.time_utils import to_local_time, to_utc

logger = logging.getLogger(__name__)


class RainyForecast(commands.Cog):
    def __init__(self, bot: WeatherBot):
        self.bot = bot
        logger.info(
            f"Scheduling rain check. Will check for rainy forecast (tomorrow), every day at {self.bot.config.notify_time} UTC"
        )
        self.rain_check_loop.start()

    # Manually check for rain tomorrow
    @app_commands.command(
        description="Checks if it's going to rain tomorrow",
        name="rain_check",
    )
    @app_commands.guilds(discord.Object(id=config.get_guild_id()))
    async def rain_check(self, interaction: discord.Interaction) -> None:
        forecast, forecast_symbol = self._get_rainy_forecast()

        if not forecast or not forecast_symbol:
            await interaction.response.send_message(
                "No rain in forecast for tomorrow 😎"
            )
            return

        embed = discord_messages.rainy_weather_forecast_tomorrow(
            forecast, forecast_symbol, self.bot.container.config.time_zone
        )

        await interaction.response.send_message(embed=embed)

    def cog_unload(self):
        self.rain_check_loop.cancel()
        return super().cog_unload()

    # Daily rain check
    # @tasks.loop(seconds=5)
    @tasks.loop(time=config.get_notify_time())
    async def rain_check_loop(self):
        # Sends a rainy forecast (if any) to the target channel
        logger.info("Executing daily rain check...")
        forecast, forecast_symbol = self._get_rainy_forecast()
        if forecast is None or forecast_symbol is None:
            return
        embed = discord_messages.rainy_weather_forecast_tomorrow(
            forecast, forecast_symbol, self.bot.container.config.time_zone
        )
        if self.bot.target_channel is None:
            return  # XXX: Unexpected
        await self.bot.target_channel.send(embed=embed)
        logger.info("Notification sent")

    @rain_check_loop.before_loop
    async def before_rain_check_loop(self):
        logger.info("Rain check loop waiting for bot to be ready...")
        await self.bot.wait_until_ready()

    def _get_rainy_forecast(self):
        # Get start of day in local time
        local_start_of_day = to_local_time(
            datetime.utcnow(), self.bot.config.time_zone
        ).replace(hour=0, minute=0, second=0, microsecond=0)
        local_start_of_day_tomorrow = local_start_of_day + timedelta(days=1)

        # Convert local day to utc period
        period_start = to_utc(local_start_of_day_tomorrow)
        period_end = period_start + timedelta(days=1)
        time_period = TimePeriod(start=period_start, end=period_end)

        logger.info(f"Getting rainy forecast for UTC period: {time_period}")
        query = RainyForecastPeriodQuery(
            time_period=time_period,
            coordinates=Coordinates(lat=self.bot.config.lat, lon=self.bot.config.lon),
        )
        forecast = self.bot.container.weather_service.get_rainy_forecast(query)

        if not forecast:
            logger.info(
                "No rainy forecast found for: "
                + str(local_start_of_day_tomorrow.date())
            )
            return None, None
        else:
            logger.info(
                "Rainy forecast found for: " + str(local_start_of_day_tomorrow.date())
            )
        forecast_symbol = self.bot.container.weather_service.get_forecast_symbol_code(
            from_time=local_start_of_day_tomorrow + timedelta(hours=8),
            coordinates=query.coordinates,
        )

        return forecast, forecast_symbol


async def setup(bot: WeatherBot):
    await bot.add_cog(RainyForecast(bot))
