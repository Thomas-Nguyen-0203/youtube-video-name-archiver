import requests
import csv
from typing import *
import re
import sys
import os
import pathlib

from configuration import *
from Video import Video

def main() -> None:
	
	if (len(sys.argv) < 2):

		err_print(
			"Usage: python3 main.py <playlists_link> ... <csv_file_name>",
			"<playlist_link> is in the form of \"https://www.youtube.com/playlist?list=<playlist_id>\"",
			sep="\n\n"
		)

		exit(1)

	csv_file_name = pathlib.Path(sys.argv[-1])
	csv_file_name = csv_file_name.expanduser()

	stop = False

	if (csv_file_name.exists()):

		print(f"File with name {sys.argv[-1]} already exists, Overwrite the file? y/n")
		stop = (input().lower() == "n")

	if (stop):
		print("The program will now exit...")
		exit()

	try:
		output_file = open(sys.argv[-1], "w")

	except PermissionError:
		err_print("Please give me sufficient permission to open the file.")
		exit(1)

	except OSError:
		err_print("Something happened that made me unable to write to the output file")
		exit(1)

	except Exception:
		err_print("Something really wrong happened and I could not tell what it is.")
		exit(1)

	output_file.close()
		
	pass 

def err_print(*args, **kwargs) -> None:
	'''
	This function is a wrapper for writing to stderr.

	Args:
		The parameters are like usual parameters of print()

	Returns:
		None
	
	It works like print() but instead of writing to stdout, it writes to stderr.
	'''

	print(*args, **kwargs, file=sys.stderr)
	
def playlist_url_verifier(url: str) -> Union[str,None]:
	'''
	This function uses regular expression to verify whether the given URL is a valid URL to a Youtube playlist.

	Args:
		url: the url to the playlist.

	Returns:
		A string which is the id of the playlist.

		None if the regular expression does not match.
	'''

	pass

if (__name__ == "__main__"):
	main()