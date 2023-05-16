from datetime import timedelta
from typing import Any

from requests_cache import CachedSession

from src.dtos.yr_complete_response import YrCompleteResponse

# Fetches weather data from the YR API
# - Full weather forecast for one location, that is, a forecast with several parameters for a nine-day period.
# - Forecasts in one hour intervals from latest update time (usually every hour) in UTC to 9 days ahead.
# - Each datapoint contains "instant" weather metrics about the weather for that hour
# - Each datapoint also contains 1, 6 and 12 hour summary data from the perspective of that hour. Includes symbol code, precipitation,


# Create a new session with default values and cache
# Default to one hour expiration for all requests in this session.
# Enable cache control to automatically set expiration based on "Expired" response header (usally lt 0.5 hour)
client_session = CachedSession(
    expire_after=timedelta(hours=1),  # XXX: Redundant?
    cache_control=True,
    cache_name="./data/http_cache.sqlite",
)


# Identification required by YR
client_session.headers = {"User-Agent": "WeatherBot/0.1"}

print("Default cache expiration: " + str(client_session.expire_after))  # type: ignore


def get_forecast(lat: float, lon: float):
    # data_endpoint = "compact"
    data_endpoint = "complete"  # Endpoint providing most details
    query = {"lat": lat, "lon": lon}
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/{data_endpoint}"

    response = client_session.get(url, params=query)  # type: ignore
    # Throw if not success. # XXX Hvad medtages i exception, response?
    response.raise_for_status()

    # Whether this request was retrieved from cache
    print(f"Response retrieved from cache: {response.from_cache}")

    # Get json and convert to DTO
    json: dict[str, Any] = response.json()
    dto = YrCompleteResponse.from_dict(json)

    return dto
