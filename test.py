#!/usr/bin/env python
import time

from requests_cache import CachedSession
# import requests_cache

import logging

logging.basicConfig(level='DEBUG')


# Old

# # Calculate individual cache expiration for this URL
# date_header_val = response.headers["Date"]  # Time of request
# request_dt = dparser.parse(date_header_val)
# print("Cached request was sent at: " + str(request_dt))

# # expires_header_val = response.headers["Expires"]
# # expires_dt = dparser.parse(expires_header_val)
# expires_dt = datetime.now(timezone.utc)
# expires_dt = expires_dt + timedelta(seconds=20)
# print("Cached request expiration is at: " + str(expires_dt))

# total_cache_time = expires_dt - request_dt
# print("Total cache time: " + str(total_cache_time))

# if(total_cache_time.total_seconds() >= 0):

#     # Handle negative edge case
#     if(total_cache_time.total_seconds() < 0):
#         total_cache_time = 0  # 0 = no cache

#     # Set cache expiration
#     client_session.urls_expire_after.update(
#         {response.url: total_cache_time.total_seconds()})
