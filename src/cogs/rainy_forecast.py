import logging
from datetime import timedelta

import discord
from discord import app_commands
from discord.ext import commands, tasks

import src.discord_messages as discord_messages
from src import config, time_utils
from src.bot import WeatherBot
from src.models import Coordinates, RainyForecastPeriodQuery, TimePeriod

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
    @app_commands.guilds(discord.Object(id=config.app_config.target_guild_id))
    async def rain_check(self, interaction: discord.Interaction) -> None:
        forecast, forecast_symbol = self._get_rainy_forecast_tomorrow()

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
    @tasks.loop(time=config.app_config.notify_time)
    async def rain_check_loop(self):
        # Sends a rainy forecast (if any) to the target channel
        logger.info("Executing daily rain check...")
        forecast, forecast_symbol = self._get_rainy_forecast_tomorrow()
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

    def get_user_current_time(self):
        return time_utils.now(self.bot.config.time_zone)

    def _get_rainy_forecast_tomorrow(self):
        user_current_time = self.get_user_current_time()
        time_period = TimePeriod.from_full_days(
            current_time=user_current_time + timedelta(days=1), num_days=1
        )
        time_period = time_period.as_utc()

        query = RainyForecastPeriodQuery(
            time_period=time_period,
            coordinates=Coordinates(lat=self.bot.config.lat, lon=self.bot.config.lon),
        )
        forecast = self.bot.container.weather_service.get_rainy_forecast(query)

        if not forecast:
            return None, None

        symbol_time = time_utils.as_utc(
            time_utils.at_hour(8, user_current_time)
        ) + timedelta(days=1)

        # Get forecast symbol as of 8am tomorrow (user time) to best describe the weather of the day
        forecast_symbol = self.bot.container.weather_service.get_forecast_symbol_code(
            from_time=symbol_time,
            coordinates=query.coordinates,
        )

        return forecast, forecast_symbol


async def setup(bot: WeatherBot):
    await bot.add_cog(RainyForecast(bot))
