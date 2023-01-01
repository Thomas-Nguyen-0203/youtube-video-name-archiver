import re
from typing import *

# This is an old key and it was already deprecated.
# You just need to generate your own key then substitute it in.
API_KEY: str = "AIzaSyB_5_NDZPeq7P3JbE0vUCt8UoXWBaBBEYo"

API_URL: str = "https://www.googleapis.com/youtube/v3/playlistItems"

_PLAYLIST_URL_REGEX_STR: str = "https://(?:www\\.)?youtube\\.com/playlist\\?list=([a-zA-Z0-9_\\-]+)"

PLAYLIST_REGEX: re = re.compile(_PLAYLIST_URL_REGEX_STR)
