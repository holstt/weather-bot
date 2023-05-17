import argparse
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from pydantic import BaseSettings, Field, validator  # type: ignore


class AppConfig(BaseSettings):
    bot_token: str = Field(..., env="BOT_TOKEN")
    dev_channel_id: int = Field(..., env="DEV_CHANNEL_ID")
    target_channel_id: int = Field(..., env="TARGET_CHANNEL_ID")
    lat: float = Field(..., env="LAT")
    lon: float = Field(..., env="LON")
    time_zone: ZoneInfo = Field(..., env="TIME_ZONE")

    @validator("time_zone", pre=True)
    def parse_timezone(cls, value: str):
        return ZoneInfo(value)


def load_config() -> AppConfig:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-e", "--env", required=False, help="Path of .env file", default=".env"
    )
    args = vars(ap.parse_args())

    env_path = Path(args["env"]).absolute()
    if Path(env_path).exists():
        print(f"env file found: '{env_path}'")
        # Load into environment
        load_dotenv(dotenv_path=env_path)
    else:
        # Assume set in environment
        print(
            f"No env file found at '{env_path}'. Assuming environment variables are set."
        )

    config = AppConfig()  # type: ignore
    return config
