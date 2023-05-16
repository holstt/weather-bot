# weather-bot

[![build](https://github.com/holstt/weather-bot/actions/workflows/build.yaml/badge.svg)](https://github.com/holstt/weather-bot/actions/workflows/build.yaml)

A simple Discord bot that tells you when it's going to rain in your location. With this bot, you'll never have to worry about getting caught in the rain without an umbrella! 🌧

<img src="docs/rainy_forecast_message.png" width=40%>

## Features

-   Reliable weather data from the [YR API](https://developer.yr.no/)
-   Weather updates for any location showing only rainy hours
-   Get notified about rainy weather forecast for today or tomorrow at a custom time every day (NOT IMPLEMENTED)

## Requirements

-   [Discord bot token](https://discord.com/developers/docs/intro)
-   [YR API key](https://developer.yr.no/)
-   If running locally: The Poetry package manager, see [installation instructions](https://python-poetry.org/docs/#installation)
-   If running with Docker: [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

**1. Clone the repository**:

```
git clone https://github.com/holstt/weather-bot.git
cd weather-bot
```

**2. Set up configuration**

The bot is configured using environment variables, which can be specified in a `.env` file or set directly in the environment.

`./example.env` provides an example of the required variables. Rename the file to `.env` and edit the values as needed:

```
# example.env
BOT_TOKEN=INSERT_BOT_TOKEN # Discord API token
DEV_CHANNEL_ID=1234578 # Channel to get notified when bot is online
LAT=11.11 # Default latitude
LON=11.11 # Default longitude
TIME_ZONE=Europe/Berlin # Time zone of guild
```

## Running Locally 💻

**3. Install the dependencies and create a virtual environment**

```
poetry install
```

**4. Activate the virtual environment**

```
poetry shell
```

**5. Run the bot**

```
python main.py
```

If you use a `.env` file to configure the environment, the program assumes it is named `.env` and located in the root of the project folder. Alternatively, you can provide a custom name/path for the environment file (e.g. if you create both a `dev.env` and `prod.env` file). Use `-e` to pass the path as an argument when running the bot:

```
python main.py -e path/to/my.env
```

## Running with Docker Compose 🐳

Using docker-compose is the easiest way to run the bot.

**3. From project root, navigate to the `./docker` folder**

```
cd docker
```

**4. Configure and run the Docker project**

`docker-compose.yml` expects the environment variables to be mounted from a file named `.env` in the root of the project folder. Set the `ENV_PATH` environment variable if you use a different name or location for the environment file. Then run:

```
docker-compose up -d
```

## Remarks

-   All requests to the YR API are cached with respect to their individual `Expire` response header to comply with the YR TOS. As such, muliple forecast requests for the same coordinate will only result in a single http request until the response expires (typically 0.5 hour it seems). The cache will be stored as a sqlite db at `./data/http_cache.sqlite`.

## Additional Information

This project uses [pre-commit](https://pre-commit.com/) to run git hooks. The hooks are defined in `.pre-commit-config.yaml` and can be installed by running:

```
pre-commit install
```
