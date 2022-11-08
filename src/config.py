from os import environ as env


class AppConfig:
    def __init__(self) -> None:
        self.ENV = env.get('WB_ENVIRONMENT')
        self.BOT_TOKEN = env.get('BOT_TOKEN')
        self.DEV_CHANNEL_ID = int(env.get('DEV_CHANNEL_ID'))
        self.DEV_GUILD_ID = int(env.get('DEV_GUILD_ID'))
        self.TARGET_GUILD_ID = int(env.get('TARGET_GUILD_ID'))
        self.LAT = float(env.get('LAT'))
        self.LON = float(env.get('LON'))
        self.TIME_ZONE = env.get('TIME_ZONE')
