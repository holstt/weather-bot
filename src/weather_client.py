from datetime import timedelta
from typing import Any

from requests_cache import CachedSession

from src.dto_yr_data_complete import data_complete_from_dict

# Fetches weather data from the YR API

# Create a new session with default values and cache
# Default to one hour expiration for all requests in this session.
# Enable cache control to automatically set expiration based on "Expired" response header (usally lt 0.5 hour)
client_session = CachedSession(
    expire_after=timedelta(hours=1),
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

    # Alt
    # if response.status_code != 200:
    #     raise Exception("")

    # print("Expires specs:")
    # print("created: " + str(response.created_at))
    # print("expires: " + str(response.expires))
    # print("is_expired: " + str(response.is_expired))

    # Check if cached response
    print(f"Response in cache: {str(response.from_cache)}")

    json: dict[str, Any] = response.json()
    data_complete = data_complete_from_dict(json)

    return data_complete
