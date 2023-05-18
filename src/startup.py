import logging
import time

import colorlog

from src.config import AppConfig
from src.container import Container
from src.weather_client import YrWeatherClient
from src.weather_service import WeatherService


def resolve_deps(config: AppConfig) -> Container:
    weather_client = YrWeatherClient()
    weather_service = WeatherService(weather_client)
    return Container(weather_service, weather_client, config)


def setup_logging(log_level: int = logging.INFO):
    default_colored_log_format = "%(thin_white)s%(asctime)s %(log_color)s%(levelname)s%(reset)s  %(green)s%(name)s%(reset)s %(message)s"
    default_handler = _get_color_log_handler(default_colored_log_format)
    logging.basicConfig(
        level=log_level,
        handlers=[default_handler],
    )
    logging.Formatter.converter = time.gmtime  # Use UTC

    # Customize discord.py logger: Set different color of logger name
    discord_colored_log_format = "%(thin_white)s%(asctime)s %(log_color)s%(levelname)s%(reset)s  %(purple)s%(name)s%(reset)s %(message)s"
    discord_log_handler = _get_color_log_handler(discord_colored_log_format)
    discord_logger = logging.getLogger("discord")
    discord_logger.addHandler(discord_log_handler)
    discord_logger.propagate = False  # Do not propagate to root logger!


def _get_color_log_handler(fmt: str):
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            fmt=fmt,
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "bold_blue",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
    )
    return handler
