import logging
from typing import Any

from requests_cache import CachedSession

logger = logging.getLogger(__name__)


# Fetches weather data from the YR API (https://developer.yr.no/featured-products/forecast/)
# - From YR: "Full weather forecast for one location, that is, a forecast with several parameters for a nine-day period.""
# - Forecasts in one hour intervals starting from latest update time (usually every hour) in UTC
# - Each datapoint contains "instant" weather metrics about the weather for that hour
# - Each datapoint also contains 1, 6 and 12 hour summary data from the perspective of that hour. Includes symbol code, precipitation etc
class YrWeatherClient:
    BASE_URL = "https://api.met.no/weatherapi/locationforecast/2.0/"
    CACHE_PATH = "./data/http_cache.sqlite"

    def __init__(self) -> None:
        # Create a cached session
        # Enable cache control to automatically set expiration based on "Expired" response header (usally lt 0.5 hour for YR)
        # This caches all requests for the same weather location
        self.session = CachedSession(
            cache_control=True,
            cache_name=self.CACHE_PATH,
        )
        # Identification required by YR
        self.session.headers = {"User-Agent": "WeatherBot/0.1"}

    def get_complete_forecast(self, lat: float, lon: float) -> dict[str, Any]:
        # data_endpoint = "compact"
        DATA_ENDPOINT = "complete"  # Endpoint providing most details
        url = self.BASE_URL + DATA_ENDPOINT
        location_query = {"lat": lat, "lon": lon}

        response = self.session.get(url, params=location_query)  # type: ignore
        response.raise_for_status()

        logger.info(f"YR API response retrieved from cache: {response.from_cache}")

        # Get json and convert to DTO
        json: dict[str, Any] = response.json()
        return json
