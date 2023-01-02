# External
import requests

# Python
from typing import *
import re
import sys
import pathlib
import json
import os

# Internal
from configuration import *
from Video import Video
from Playlist import Playlist

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

	# Check existence of both files.
	archive_file_name = pathlib.Path(output_file_path)
	archive_file_name = archive_file_name.expanduser()

	input_file = pathlib.Path(input_file_path)
	input_file = input_file.expanduser()

	if (input_file.samefile(archive_file_name)):
		err_print("Input file cannot be the same file as output file. Please recheck your arguments.")
		exit(1)

	stop = False

	# Warn the user of potential overwriting.
	if (archive_file_name.exists()):

		print(f"File with name {archive_file_name.name} already exists, Overwrite the file? y/n")
		stop = (input().lower() == "n")

	if (stop):
		print("The program will now exit...")
		exit()

	output_file_problem = True
	has_problem = False

	try:
		output_file = open(output_file_path, "w")

		output_file_problem = False

		playlists = input_file.open("r")

	except PermissionError:
		err_print("Please give me sufficient permission to open the files.")
		has_problem = True

	except FileNotFoundError:
		err_print("The input file does not exist, please recheck your input file.")
		has_problem = True

	except OSError:
		err_print("Something happened that made me unable to write to the output file")
		has_problem = True

	except Exception:
		err_print("Something really wrong happened and I could not tell what it is.")
		has_problem = True

	# Close output_file if the file having problem is the input file.
	if (has_problem):

		if not (output_file_problem):
			output_file.close()
			os.remove(output_file_path)

		exit(1)

	archive = {}

	none_of_the_links_work = False

	while True:

		line = playlists.readline()

		if not line:
			playlists.close()

			if (len(archive) == 0):
				none_of_the_links_work = True

			break

		url = line.strip()

		this_playlist = convert_playlist_url_to_playlist_obj(url)

		if not (this_playlist):
			continue

		archive[this_playlist.get_id()] = this_playlist.construct_json_obj()

	# I listen to songs that contain non-ascii characters a lot.
	if not (none_of_the_links_work):
		json.dump(archive, output_file, ensure_ascii=False, indent=4)
		output_file.close()

	else:
		output_file.close()
		os.remove(output_file_path)
	

def err_print(*args, **kwargs) -> None:
	'''
	This function is a wrapper for writing to stderr.

	Args:
		The parameters are like usual parameters of print()

	Returns:
		None
	
	It works like print() but instead of writing to stdout, it writes to 
	stderr.
	'''

	print(*args, **kwargs, file=sys.stderr)
	
def playlist_url_verifier(url: str) -> Union[str,None]:
	'''
	This function uses regular expression to verify whether the given URL is a 
	valid URL to a Youtube playlist.

	Args:
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

	Args:
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

	# The cost is prob sum floor(n_i/50) from i = 1 to n.
	# n_i denotes the size of playlist i.
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

if (__name__ == "__main__"):
	main()