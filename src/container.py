from typing import NamedTuple

from src.config import AppConfig
from src.weather_client import YrWeatherClient
from src.weather_service import WeatherService


# Service container
class Container(NamedTuple):
    weather_service: WeatherService
    weather_client: YrWeatherClient
    config: AppConfig
