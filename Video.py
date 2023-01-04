from typing import *

YOUTUBE_VIDEO_PREFIX = "youtube.com/watch?v="

class Video:
	def __init__(self, name: str, channel: str, id: str):
		self.name: str = name
		self.channel: str = channel
		self.id = id
		self.link: str = YOUTUBE_VIDEO_PREFIX + self.id

	@classmethod
	def initiate_video_from_json(cls, json_repr: Dict[str, str]) -> 'Video':
		'''
		This method takes the JSON representation of the Video object and turn 
		it into a Video object.

		Params:
			The dictionary which is the JSON representation of the video.

		Returns:
			The equivalent Video object.
		'''

		name = json_repr["name"]
		channel = json_repr["channel"]
		id = json_repr["id"]

		return Video(name, channel, id)

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

	def is_deleted(self) -> bool:
		'''
		This method checks whether this video is deleted (either 
		privatised by the uploader or nuked by Youtube)

		If a video is not available or deleted, the youtube API won't 
		return the uploader of the video, we can use this fact to determine whether the video is deleted/privatised.

		Returns:
			A boolean value indicating the current video is deleted or not.
		'''

		# This should be mentioned in archiver.py
		return (self.channel == "Unknown Channel")

	# For debugging purpose.
	def __repr__(self):
		return f"{self.name} {self.channel}"