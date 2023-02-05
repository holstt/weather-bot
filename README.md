

# weather-bot
[![deploy](https://github.com/roedebaron/weather-bot/actions/workflows/deploy.yaml/badge.svg)](https://github.com/roedebaron/weather-bot/actions/workflows/deploy.yaml)

A simple Discord bot that tells you when it's going to rain in your location. With this bot, you'll never have to worry about getting caught in the rain without an umbrella! 🌧

<img src="doc/rainy_forecast_message.png" width=40%>

## Features
- Reliable weather data from the [YR API](https://developer.yr.no/)
- Weather updates for any location showing only rainy hours
- Get notified about rainy weather forecast for today or tomorrow at a custom time every day (NOT IMPLEMENTED)

## Prerequisites
- [Discord API token](https://discord.com/developers/docs/intro)
- [YR API key](https://developer.yr.no/)

## Local setup with Anaconda

#### 1. Create environment and install dependencies

```
conda create --name weatherbot --file requirements.txt python=3.10
conda activate weatherbot
```


#### 2. Configuration 

Add the relevant information to the `./example.env` file and rename it to `.env`:
```
# example.env
BOT_TOKEN=INSERT_BOT_TOKEN # Discord API token
DEV_CHANNEL_ID=1234578 # Channel to get notified when bot is online
LAT=11.11 # Default latitude
LON=11.11 # Default longitude
TIME_ZONE=Europe/Berlin # Time zone of guild
```
**Please note**
 - You can also use a custom name for the environment file (e.g. if you create both a `dev.env` or `prod.env` file). For a custom named and/or custom path of the .env file, the path should be given as argument when running the bot using the `-e` option e.g. `-e dev.env`
- See [Using a database](using-a-database-not-implemented) for using a database to store a default coordinate for each guild

#### 3. Run the bot

```
python main.py 
python main.py -e dev.env # With custom named .env file
```

## Running with Docker Compose

Using docker-compose is the easiest way to run the bot. Files for running the bot with docker-compose is placed in the `/docker` folder which includes a Dockerfile as well as docker-compose files. 

You can rename the image in `docker-compose.yml` to a custom name or a name that links the image to your own Docker Hub repository if you wish to use the CI/CD pipeline (see below)

The environment file is not copied into the docker image but mounted into the container at run time. As such, it must exist at the path specified under `volumes` in `docker-compose.prod.yml` (for production) and `docker-compose.override.yml` (for development). 
- Please note, that in `docker-compose.prod.yml` the path can also be specified by setting the $ENV_PATH environment variable (this option is used in the CI/CD pipeline)


```
cd docker

# Run in Development
docker-compose up --build

# Run in Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```

## Running the CI/CD pipeline

For the pipeline to work, you must create a Docker Hub account.

The Github Actions CI/CD pipeline deploys the bot on your server automatically every time a commit is made to the `main` branch. Please inspect `.github/workflows/deploy.yaml` for the required environment variables that should be set up in your Github repository as well as the assumptions made about the file structure of the repository and the remote server. 

## Using a database (NOT IMPLEMENTED)

Instead of using static coordinates, it is possible to store a default location for each guild in a database. Add the database credentials in the `.env` file and remember to set `DB_ENABLED=TRUE`.

## Remarks

- All requests to the YR API are cached with respect to their individual `Expire` response header to comply with the YR TOS. As such, muliple forecast requests for the same coordinate will only result in a single http request until the response expires (typically 0.5 hour it seems). The cache will be stored as a sqlite db and placed in the root folder.
