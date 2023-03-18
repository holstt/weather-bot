from os import environ as env


class AppConfig:
    # Extract variables from environment.
    def __init__(self) -> None:
        self.ENV = env.get('WB_ENVIRONMENT')
        self.BOT_TOKEN = env.get('BOT_TOKEN')
        self.DEV_CHANNEL_ID = int(env['DEV_CHANNEL_ID'])
        self.DEV_GUILD_ID = int(env['DEV_GUILD_ID'])
        self.TARGET_GUILD_ID = int(env['TARGET_GUILD_ID'])
        self.LAT = float(env['LAT'])
        self.LON = float(env['LON'])
        self.TIME_ZONE = env['TIME_ZONE']
