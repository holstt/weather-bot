import logging

from src import config, startup
from src.bot import WeatherBot

logger = logging.getLogger(__name__)


def main():
    app_config = config.load_config()
    container = startup.resolve_deps(app_config)
    bot = WeatherBot(container)
    logger.info("Starting bot...")
    bot.run(app_config.bot_token, log_handler=None)


if __name__ == "__main__":
    startup.setup_logging()
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as e:
        logger.exception(
            f"Unhandled exception '{type(e).__name__}' caught in global exception handler: {e}. Program will exit."
        )
        raise e
