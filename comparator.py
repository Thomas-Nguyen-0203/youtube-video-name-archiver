'''
comparator.py: Compare 2 archives together to notice what has changed.

Note that comparator.py only compares mutual playlists within the 2 archives, 
which means if 2 archives have no mutual playlist, it will not report anything.

Usage: python3 comparator.py <old_archive> <new_archive> <output_file>
'''
# Python
import json
import sys
import pathlib
import os
from typing import *

# Internal
from Video import Video

def main():

    if (len(sys.argv) != 4):
        err_print(
            "Usage: python3 comparator.py <old_archive> <new_archive> <output_file>"
        )

        exit(1)

    old_archive_path = pathlib.Path(sys.argv[1])
    old_archive_path = old_archive_path.expanduser()

    new_archive_path = pathlib.Path(sys.argv[2])
    new_archive_path = new_archive_path.expanduser()

    output_file = pathlib.Path(sys.argv[3])
    output_file = output_file.expanduser()

    if (output_file.exists()):
        print(f"File with name {output_file.name} already exists, Overwrite the file? y/n")
        stop = (input().strip().lower() == "n")

    if (stop):
        print("The program will now exit...")
        exit()

    if (old_archive_path.samefile(output_file) or
        new_archive_path.samefile(output_file)):

        err_print("Any of the input files cannot be the same one as output file, please recheck your arguments")

        exit(1)

    opened_files = []
    has_problem = False

    try:
        old_archive = old_archive_path.open("r")
        opened_files.append(old_archive)

        new_archive = new_archive_path.open("r")
        opened_files.append(new_archive)

        output = output_file.open("w")

    except PermissionError:
        err_print("Please give me sufficient permission to open the files.")
        has_problem = True

    except FileNotFoundError:
        err_print("The input file(s) may not exist, please recheck your files.")
        has_problem = True

    except Exception:
        err_print("Something happened that prevented me from reading the files.")
        has_problem = True

    if (has_problem):
        for file in opened_files:
            file.close()

        exit(1)

    old_archive_problem = True
    try:
        old_archive_json = json.load(old_archive)
        old_archive_problem = False

        new_archive_json = json.load(new_archive)

    except json.decoder.JSONDecodeError:
        
        problem = (
            old_archive_path.name if (old_archive_problem) 
            else new_archive_path.name)

        err_print(f"The archive in {problem} is not valid, please recheck it")

        output.close()
        old_archive.close()
        new_archive.close()

        os.remove(output_file.name)
        exit(1)

    # Record all the changes happened to mutual playlists. 
    changes: Dict[str, Tuple[Union[List[Video], List[List[Video]]]]] = {}

    # Iterate through the ids of the playlists in old archive.
    for playlist_id in old_archive_json:

        if (playlist_id in new_archive_json):

            old_playlist = old_archive_json[playlist_id]["videos"]
            new_playlist = new_archive_json[playlist_id]["videos"]

            changes[playlist_id] = compare_video_set(
                old_playlist, new_playlist
            )



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

def compare_video_set(
    old_video_set: Dict[str, Dict[str, str]], 
    new_video_set: Dict[str, Dict[str, str]]
) -> Tuple[Union[List[Video], List[List[Video]]]]:
    '''
    This function takes in 2 videos attributes of a playlist then find the differences between them.

    Params:
        videos attribute of the first playlist.
        videos attribute of the second playlist.

    Returns:
        A tuple of 3 lists:
            - The first list contains the videos added.
            - The second list contains the videos removed.
            - The third list contains the videos that changed 
            (ie privatised then unprivatised and vice versa)
    '''

    added: List[Video] = []
    changed: List[Video] = []

    # This is the odd one out because if a video is changed, we want to know 
    # it before and after being changed, unlike removed and added where we 
    # only need to know the video at 1 timestamp only.
    removed: List[List[Video]] = []

    # Iterate through the keys which are the id of the videos.
    old_videos_id: str = list(old_video_set.keys())

    while len(old_videos_id) > 0:

        current_video_id = old_videos_id[0]

        current_video = Video.initiate_video_from_json(
            old_video_set[current_video_id]
        )

        # If the video in old playlist is not there anymore in the new 
        # playlist then that means that video was removed.

        if (current_video_id not in new_video_set):
            removed.append(current_video)

        # We can't check for added videos yet, however we can check for 
        # changed videos.
        else:
            new_current_video = Video.initiate_video_from_json(
                new_video_set[current_video_id]
            )

            # The idea is that we want to remove the videos we have been 
            # through.
            new_video_set.pop(current_video_id)

            # Is this readable at all lol.
            video_changed = (
                (current_video.is_deleted() and 
                not new_current_video.is_deleted()) or 

                (not current_video.is_deleted() and
                new_current_video.is_deleted())
            )

            if (video_changed):
                changed.append([current_video, new_current_video])

        old_videos_id.pop(0)

    # After exhausting the old version of the playlist, check for all newly 
    # added videos.

    for video in new_video_set:
        added.append(Video.initiate_video_from_json(
            new_video_set[video]
        ))

    return added, removed, changed
        
def test():

    test_old_vid_set = json.load(open("old_vid_set_ex.json", "r"))
    test_new_vid_set = json.load(open("new_vid_set_ex.json", "r"))
    print(compare_video_set(test_old_vid_set, test_new_vid_set))
    pass


if (__name__ == "__main__"):
    # main()
    test()