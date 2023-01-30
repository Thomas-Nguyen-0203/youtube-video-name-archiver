'''
archiver.py: does the archiving of one or more Youtube playlists and save it 
as a JSON file.

Usage: python3 archiver.py <input_file> <output_file>
'''

# External
import requests

# Python
from typing import *
import re
import sys
import pathlib
import json
import os
import time

# Internal
from configuration import *
from Video import Video
from Playlist import Playlist
from utilities import *
from PlaceHolder import PlaceHolder

class Archiver:

	def __init__(self, input_file, output_file) -> None:
		'''
		A constructor, pretty self-explanatory so idk what to say.

		Also the constructor also calls open_files() which is somewhat 
		noteworthy.
		'''

		self.input_file_path: pathlib.Path = pathlib.Path(input_file).expanduser().resolve()
		self.input_file = PlaceHolder.get_place_holder()

		self.output_file_path: pathlib.Path = pathlib.Path(output_file).expanduser().resolve()
		
		self.output_file = PlaceHolder.get_place_holder()

		self.no_output: bool = True

		self.open_files()

	def open_files(self) -> None:
		'''
		This method opens the file descriptors to the file in the paths passed 
		through the constructor.

		it will handle some basic problems like (P means problem, R means 
		response): 

			P: The output file already exists which means there is a risk in 
			overwriting the original file.
			
			R: The program will inform the user then ask whether the user 
			wants this to happen, exit if not, continue otherwise.

			-------------------------------------------------------------------

			P: The output file is the same as input file which means once we 
			open the output file, the input file will be wiped of its original 
			content.
			
			R: The program will inform the user then exit if the output file 
			happens to be the same file as the input file.

			-------------------------------------------------------------------
			
			P: The input file does not exist.
			
			R: The program will inform the user then exit.

			-------------------------------------------------------------------

			P: The program does not have enough permission to open files.
			
			R: The program will inform the user then exit.

			-------------------------------------------------------------------
			
			P: Some unknown, unpredictable error occurs while opening files 
			(idk maybe a nearby nuclear plant melts down which somehow flips a 
			bit that makes the program unable to open the file)
			
			R: Maybe create a new issue on github ;)
		'''
		
		if (self.output_file_path.exists()):

			if (self.output_file_path.samefile(self.input_file_path)):
				err_print("Input file cannot be the same file as output file. Please recheck your arguments.")

				exit(1)

			overwrite_permission = False

			overwrite_permission = overwriting_file_warning(
				self.output_file_path.name
			)

			# Warn the user of potential overwriting.
			if not (overwrite_permission):

				# For fun only :)
				print("The program will now exit", end="", flush=True)
				time.sleep(0.5)
				print(".", end="", flush=True)
				time.sleep(0.5)
				print(".", end="", flush=True)
				time.sleep(0.5)
				print(".", end="", flush=True)
				time.sleep(0.5)
				print() 
				exit()

		self.input_file = input_file_opening(self.input_file_path)

		self.output_file = output_file_opening(self.output_file_path)

		if (self.output_file == PlaceHolder.get_place_holder() or 
			self.input_file == PlaceHolder.get_place_holder()):

			self.clean_up(1)

	def main_work(self):
		'''
		This method is where the Archiver does most of its work.
		'''

		playlists = {}
		archive = {
			"time": time.strftime(TIME_FORMAT_STR),
			"playlists": playlists
		}

		while True:
			line = self.input_file.readline()

			if not line:

				if (len(archive) != 0):
					self.no_output = False

				break

			url = line.strip()

			this_playlist = convert_playlist_url_to_playlist_obj(url)

			if not (this_playlist):
				continue

			playlists[this_playlist.get_id()] = this_playlist.construct_json_obj()

		if not (self.no_output):
			json.dump(archive, self.output_file, ensure_ascii=False, indent=4)

		self.clean_up(0)

	def clean_up(self, err_code: int) -> None:
		'''
		This method is supposed to be called whenever the program thinks it 
		should stop, it will close all opened file descriptors and remove the newly opened output file if there is no output from the program.
		'''
		self.input_file.close()
		self.output_file.close()

		if (self.no_output and 
			self.output_file_path.exists()):

			os.remove(self.output_file_path.name)
		
		exit(err_code)

# Helpful functions

def playlist_url_verifier(url: str) -> Union[str,None]:
	'''
	This function uses regular expression to verify whether the given URL is a 
	valid URL to a Youtube playlist.

	Params:
		url: the url to the playlist.

	Returns:
		A string which is the id of the playlist.

		None if the regular expression does not match.
	'''
	matched_id = PLAYLIST_REGEX.search(url)

	if not (matched_id):
		return None

	# Capture group 1 is the id of the playlist.
	return matched_id.group(1)

def convert_playlist_url_to_playlist_obj(url: str) -> Union[Playlist,None]:
	'''
	This function takes in an url to a Youtube playlist and attempt to convert 
	it to a playlist object.

	Params:
		url: the url to the playlist.

	Returns:
		A playlist object representing the playlist.

		None if the url is not valid.
	'''

	# Visit https://developers.google.com/youtube/v3/docs/playlistItems to 
	# understand what are the parameters.

	PARAMS: Dict[str,str] = {
		"part": "snippet",
		"maxResults": "50",
		"key": f"{API_KEY}",
		"fields": "nextPageToken,items(snippet(title,videoOwnerChannelTitle,resourceId/videoId))"
	}
	
	# Check if the url is a valid one using regex.
	playlist_id = playlist_url_verifier(url)

	if not (playlist_id):
		err_print(f"The url for the playlist ({url}) is invalid, please recheck it.")
		return None

	this_playlist = Playlist(playlist_id) 

	PARAMS["playlistId"] = playlist_id

	# Max size is 50 entries per call so we need to call it until we exhaust 
	# the playlist.

	# The cost is prob sum floor(N_i/50) from i = 1 to n.
	# N_i denotes the size of playlist i.
	# Assuming we have n playlists.

	while True:
		api_call = requests.get(API_URL, params=PARAMS)
		result_json = api_call.json()

		# Error in response means the id is not valid.
		if ("error" in result_json):

			code = result_json["error"]["code"]

			if (code == 400):
				err_print("Your API key is expired, please get a new one.")

			elif (code == 404):
				err_print(f"The url for the playlist ({url}) is invalid, please recheck it.")

			return None

		video_information_list = result_json["items"]

		for video in video_information_list:
			current_video = video["snippet"] 
			
			if ("videoOwnerChannelTitle" not in current_video):
				channel = "Unknown Channel"

			else:
				channel = current_video["videoOwnerChannelTitle"]
			
			video_object = Video(
				current_video["title"], 
				channel,
				current_video["resourceId"]["videoId"]
				)

			this_playlist.add_video(video_object)

		# Sign of playlist exhausted.
		if ("nextPageToken" not in result_json):
			break

		PARAMS["pageToken"] = result_json["nextPageToken"]

	return this_playlist

def main() -> None:
	
	if (len(sys.argv) != 3):

		err_print(
			"Usage: python3 archiver.py <input_file> <output_file>",
			"<input_file> should contain a valid <playlist_link> per line.",
			"<playlist_link> is in the form of \"https://www.youtube.com/playlist?list=<playlist_id>\"",
			"Also works for a video that is being watched from a playlist (ie, has a link of youtube.com/watch?v=<id>&list=<id>&ab_channel=<channel>",
			sep="\n\n"
		)

		exit(1)

	output_file_path = sys.argv[2]
	input_file_path = sys.argv[1]

	archiver = Archiver(input_file_path, output_file_path)

	archiver.main_work()

if (__name__ == "__main__"):
	main()