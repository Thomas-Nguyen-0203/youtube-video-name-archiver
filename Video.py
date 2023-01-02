from typing import *

YOUTUBE_VIDEO_PREFIX = "youtube.com/watch?v="

class Video:
	def __init__(self, name: str, channel: str, id: str):
		self.name: str = name
		self.channel: str = channel
		self.id = id
		self.link: str = YOUTUBE_VIDEO_PREFIX + self.id

	def get_name(self) -> str:
		return self.name

	def get_channel(self) -> str:
		return self.channel

	def get_link(self) -> str:
		return self.link

	def get_id(self) -> str:
		return self.id

	def construct_json_obj(self):
		'''
        This method constructs the dictionary which is the representation of 
        the video and return it.

		As noted in README, the JSON representation of a video is of the form

		{
			"id": str.
			"name": str,
			"channel": str
			"link": str
		}

        Returns:
            The dictionary representation of the JSON object of the video.
        '''
		json_obj = {
			"id": self.id,
			"name": self.name,
			"channel": self.channel,
			"link": self.link,
		}

		return json_obj
