'''
comparator.py: Compare 2 archives together to point out what has changed.

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
from io import UnsupportedOperation

# Internal
from Video import Video
from utilities import *
from PlaceHolder import PlaceHolder

class Comparator:
    
    def __init__(
        self, 
        old_archive_file_path, 
        new_archive_file_path, 
        output_file_path
    ) -> None:
        '''
        Good ol' constructor, can never go wrong.
        '''

        self.old_archive_file_path: pathlib.Path = pathlib.Path(
            old_archive_file_path
        ).expanduser()

        self.new_archive_file_path: pathlib.Path = pathlib.Path(
            new_archive_file_path
        ).expanduser()

        self.output_file_path: pathlib.Path = pathlib.Path(
            output_file_path
        ).expanduser()

        self.output_file = PlaceHolder.get_place_holder()

        self.no_output = True

        # JSON objects of old and new archive.
        self.old_archive: dict = None
        self.new_archive: dict = None

    def fetch_archives(self) -> None:
        '''
        This method will attempt to open the input files and retrieve the 
        JSON representation of both old and new archives.
        '''
        old_archive_file = input_file_opening(
            self.old_archive_file_path
        )

        new_archive_file = input_file_opening(
            self.new_archive_file_path
        )

        if (old_archive_file == PlaceHolder.get_place_holder() or 
            new_archive_file == PlaceHolder.get_place_holder()):

            exit(1)

        self.old_archive = convert_json_from_file_to_dict(
            old_archive_file
        )

        self.new_archive = convert_json_from_file_to_dict(
            new_archive_file
        )

        old_archive_file.close()
        new_archive_file.close()

        end_now = False

        if (self.old_archive == None or 
            not check_format_of_archive(self.old_archive)):

            err_print(f"File {self.old_archive_file_path.as_posix()} is not of correct format or is corrupted, please check it again.")

            end_now = True
        
        if (self.new_archive == None or 
            not check_format_of_archive(self.new_archive)):

            err_print(f"File {self.new_archive_file_path.as_posix()} is not of correct format or is corrupted, please check it again.")

            end_now = True

        if (end_now):
            exit(1)

    def main_work(self) -> None:
        '''
        The name is pretty much self-explanatory, the bulk work of the 
        comparator.
        '''
        pass
    
    def write_to_output(self) -> None:
        pass



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

def verify_json_format(to_be_verified: dict) -> bool:
    '''
    This function verifies whether the given dictionary is in a correct 
    format given by the JSON format of an archive.

    Params:
        dict which is the archive that is to be verified.

    Returns:
        True if the archive is of appropriate format, False otherwise. 
    '''
    # TODO
    pass

def convert_json_from_file_to_dict(file) -> dict:
    '''
    This function will convert the JSON object in the opened file into an 
    equivalent Python dictionary.

    Params:
        A file that is already opened for read.

    Returns:
        A dictionary if the file is the file is really JSON, None otherwise.
    '''
    try:
        equivalent_dictionary = json.load(file)
    
    except json.decoder.JSONDecodeError:
        return None

    return equivalent_dictionary

def check_format_of_video(video: dict) -> bool:
    '''
    This function checks whether the given dictionary is of correct format of 
    a video as defined in README.

    Params:
        dict which is the video.

    Returns:
        True if it is correct, false otherwise.
    ''' 

    if not (isinstance(video, dict)):
        return False

    if ("id" not in video or 
        "name" not in video or
        "channel" not in video or 
        "link" not in video):

        return False

    if (not isinstance(video["id"], str) or 
        not isinstance(video["name"], str) or 
        not isinstance(video["channel"], str) or 
        not isinstance(video["link"], str)):
        
        return False

    return True

def check_format_of_playlist(playlist: dict) -> bool:
    '''
    This function checks whether the given dictionary is of correct format of 
    a playlist as defined in README.

    Params:
        dict which is the playlist.

    Returns:
        True if it is correct, false otherwise.
    '''

    if (not isinstance(playlist, dict)):
        return False

    if ("id" not in playlist or 
        "videos" not in playlist or 
        "link" not in playlist):

        return False

    if (not isinstance(playlist["id"], str) or 
        not isinstance(playlist["videos"], dict) or 
        not isinstance(playlist["link"], str)):

        return False

    videos = playlist["videos"]

    for video_id in videos:
        
        if not (check_format_of_video(videos[video_id])):
            return False

    return True


def check_format_of_archive(archive: dict) -> bool:
    '''
    This function checks whether the given dictionary is of correct format of 
    an archive as defined in README.

    Params:
        dict which is the archive.

    Returns:
        True if it is correct, false otherwise.
    '''

    if not (isinstance(archive, dict)):
        return False

    for playlist_id in archive:

        if not (check_format_of_playlist(archive[playlist_id])):
            return False

    return True




    
        
def test():

    test_old_vid_set = json.load(open("old_vid_set_ex.json", "r"))
    test_new_vid_set = json.load(open("new_vid_set_ex.json", "r"))
    print(compare_video_set(test_old_vid_set, test_new_vid_set))
    pass


def main():

    if (len(sys.argv) != 4):
        err_print(
            "Usage: python3 comparator.py <old_archive> <new_archive> <output_file>"
        )

        exit(1)

    comparator: Comparator = Comparator(sys.argv[1], sys.argv[2], sys.argv[3])
    comparator.fetch_archives()

    # Record all the changes happened to mutual playlists. 
    changes: dict = {}

    # Iterate through the ids of the playlists in old archive.
    # for playlist_id in old_archive_json:

    #     if (playlist_id in new_archive_json):

    #         old_playlist = old_archive_json[playlist_id]["videos"]
    #         new_playlist = new_archive_json[playlist_id]["videos"]

    #         changes[playlist_id] = compare_video_set(
    #             old_playlist, new_playlist
    #         )

if (__name__ == "__main__"):
    main()
    # test()