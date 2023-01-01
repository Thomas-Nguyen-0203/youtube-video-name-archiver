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

        Returns:
            The dictionary representation of the JSON.
        '''

        result = {
            "id": self.id, 
            "link": self.link, 
            "videos": {x.get_id() : x.construct_json_obj() for x in self.videos}
            }

        return result

    def __repr__(self):
        return str(self.construct_json_obj())


def test():
    file = open("test.json", "w")

    songa = Video("Electrical Surfin", "Tokino Sora", "01")
    songb = Video("Caramel Devil", "Yozora Mel", "02")
    songc = Video("Linger Ringer", "Momosuzu Nene", "3")
    
    playlist = Playlist("0")

    playlist.add_video(songa)
    playlist.add_video(songb)
    playlist.add_video(songc)

    json.dump(playlist.construct_json_obj(), file)
    file.close()

if __name__ == "__main__":
    test()