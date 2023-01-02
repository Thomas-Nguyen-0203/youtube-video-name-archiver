from typing import *
from Video import Video
import json

YOUTUBE_PLAYLIST_PREFIX = "https://www.youtube.com/playlist?list="

class Playlist:

    def __init__(self, id: str):
        self.videos: List[Video] = []
        self.id: str = id
        self.link: str = YOUTUBE_PLAYLIST_PREFIX + self.id

    def get_id(self) -> str:
        return self.id

    def add_video(self, video: Video) -> None:
        self.videos.append(video)

    def construct_json_obj(self) -> dict:
        '''
        This method constructs the dictionary which is the representation of 
        the playlist and return it.

        As noted in README, the JSON representation of a playlist is of the 
        form:

        {
            "id": str,
            "name": str
            "videos": {
                video_id: video
            }
            "link": str
        }

        Returns:
            The dictionary representation of the JSON.
        '''

        result = {
            "id": self.id, 
            "link": self.link, 
            "videos": {x.get_id() : x.construct_json_obj() for x in self.videos}
            }

        return result
