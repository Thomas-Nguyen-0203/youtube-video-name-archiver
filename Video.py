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
	
	def __repr__(self) -> str:
		return self.name + "," + self.channel + "," + self.link

	def get_list(self) -> List[str]:
		return [self.name, self.channel, self.link, self.id]

	def __eq__(self, other: 'Video'):
		
		# Youtube video's ids are unique so comparing it should be the most 
		# logical way
		if not (isinstance(other, Video)):

			return False

		if (other.id == self.id):
			return True

		return False
		
