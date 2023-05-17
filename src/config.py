from os import environ as env
from zoneinfo import ZoneInfo


class AppConfig:
    # Extract variables from environment.
    def __init__(self) -> None:
        self.BOT_TOKEN = env["BOT_TOKEN"]
        self.DEV_CHANNEL_ID = int(env["DEV_CHANNEL_ID"])
        self.TARGET_CHANNEL_ID = int(env["TARGET_CHANNEL_ID"])
        self.LAT = float(env["LAT"])
        self.LON = float(env["LON"])
        self.TIME_ZONE = ZoneInfo(env["TIME_ZONE"])
