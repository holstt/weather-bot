import argparse
import logging
from datetime import time
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from pydantic import BaseSettings, Field, validator  # type: ignore

from src import time_utils

logger = logging.getLogger(__name__)

_guild_id = None
_notify_time = None


# Global variables which should be accessible from cogs
def get_guild_id():
    if _guild_id is None:
        raise Exception("Guild ID not set")
    return _guild_id


def get_notify_time():
    if _notify_time is None:
        raise Exception("Notify time not set")
    return _notify_time


class AppConfig(BaseSettings):
    bot_token: str = Field(..., env="BOT_TOKEN")
    dev_channel_id: int = Field(..., env="DEV_CHANNEL_ID")
    target_channel_id: int = Field(..., env="TARGET_CHANNEL_ID")
    target_guild_id: int = Field(..., env="TARGET_GUILD_ID")
    lat: float = Field(..., env="LAT")
    lon: float = Field(..., env="LON")
    time_zone: ZoneInfo = Field(..., env="TIME_ZONE")
    notify_time: time = Field(..., env="NOTIFY_TIME_OF_DAY")

    @validator("time_zone", pre=True)
    def parse_timezone(cls, value: str):
        return ZoneInfo(value)

    @validator("notify_time", pre=True)
    def parse_notify_time(cls, value: str, values: dict[str, Any]):
        return time_utils.parse_time_str(value, values["time_zone"])


def load_config() -> AppConfig:
    logger.info("Loading config...")
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-e", "--env", required=False, help="Path of .env file", default=".env"
    )
    args = vars(ap.parse_args())

    env_path = Path(args["env"]).absolute()
    if Path(env_path).exists():
        logger.info(f"env file found: '{env_path}'")
        # Load into environment
        load_dotenv(dotenv_path=env_path)
    else:
        # Assume set in environment
        logger.info(
            f"No env file found at '{env_path}'. Assuming environment variables are set."
        )

    config = AppConfig()  # type: ignore

    # Set guild id for all to access when command syncing
    global _guild_id
    global _notify_time
    _guild_id = config.target_guild_id
    _notify_time = config.notify_time
    return config
