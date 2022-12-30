import typing

YOUTUBE_VIDEO_PREFIX = "youtube.com/watch?v="

class Video:
	def __init__(self, name: str, channel: str, id: str):
		self.name: str = name
		self.channel: str = channel
		self.link: str = YOUTUBE_VIDEO_PREFIX + id

	def get_name(self) -> str:
		return self.name

	def get_channel(self) -> str:
		return self.channel

	def get_link(self) -> str:
		return self.link
	
	def __repr__(self) -> str:
		return self.name + "," + self.channel + "," + self.link
