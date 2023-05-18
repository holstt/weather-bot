import logging

from src import config
from src.bot import WeatherBot
from src.config import AppConfig
from src.container import Container
from src.weather_client import YrWeatherClient
from src.weather_service import WeatherService


def resolve_deps(config: AppConfig) -> Container:
    weather_client = YrWeatherClient()
    weather_service = WeatherService(weather_client)
    return Container(weather_service, weather_client, config)


def main():
    app_config = config.load_config()
    container = resolve_deps(app_config)
    bot = WeatherBot(container)
    print("Starting bot...")
    bot.run(app_config.bot_token, log_level=logging.INFO)


if __name__ == "__main__":
    # utils.setup_logging()
    # utils.setup_logging(logging.DEBUG)
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        # logger.exception(f"Unhandled exception occurred: {e}")
        print(f"Unhandled exception occurred: {e}")
        raise e
