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
import time
import datetime

# Internal
from Video import Video
from configuration import YOUTUBE_PLAYLIST_PREFIX,TIME_FORMAT_STR
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
        ).expanduser().resolve()

        self.new_archive_file_path: pathlib.Path = pathlib.Path(
            new_archive_file_path
        ).expanduser().resolve()

        self.output_file_path: pathlib.Path = pathlib.Path(
            output_file_path
        ).expanduser().resolve()

        self.output_file = PlaceHolder.get_place_holder()

        self.no_output = True

        # JSON objects of old and new archive playlists.
        self.old_archive_playlists: dict = None
        self.old_archive_date: time.struct_time = None
    
        self.new_archive_playlists: dict = None
        self.new_archive_date: time.struct_time = None

        # This variable record all the changes happening between mutual 
        # playlists.
        self.changes: dict = {}

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

            old_archive_file.close()
            new_archive_file.close()

            exit(1)

        old_archive = convert_json_from_file_to_dict(
            old_archive_file
        )

        new_archive = convert_json_from_file_to_dict(
            new_archive_file
        )

        old_archive_file.close()
        new_archive_file.close()

        end_now = False

        if (old_archive == None or 
            not check_format_of_archive(old_archive)):

            err_print(f"File {self.old_archive_file_path.as_posix()} is not of correct format or is corrupted, please check it again.")

            end_now = True
        
        if (new_archive == None or 
            not check_format_of_archive(new_archive)):

            err_print(f"File {self.new_archive_file_path.as_posix()} is not of correct format or is corrupted, please check it again.")

            end_now = True

        if (end_now):
            exit(1)

        self.old_archive_playlists = old_archive["playlists"]
        self.old_archive_date = parse_time(old_archive["time"])

        self.new_archive_playlists = new_archive["playlists"]
        self.new_archive_date = parse_time(new_archive["time"])

    def open_output_file(self) -> None:
        '''
        This method will attempt to test whether the output file can be 
        correctly opened by the program so that the user does not have to waste their time waiting for the program to complete before being notified that the output file path is faulty. 
        '''

        if (self.output_file_path.exists()):

            overwrite_permission = overwriting_file_warning(
                self.output_file_path.name
            )

            if not (overwrite_permission):
            
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


        
        self.output_file = output_file_opening(self.output_file_path)

        if (self.output_file == PlaceHolder.get_place_holder()):
            exit(1)
            
    def main_work(self) -> None:
        '''
        The name is pretty much self-explanatory, the bulk work of the 
        comparator.
        '''
        
        for playlist_id in self.old_archive_playlists:

            if (playlist_id in self.new_archive_playlists):

                old_playlist = self.old_archive_playlists[playlist_id]["videos"]
                new_playlist = self.new_archive_playlists[playlist_id]["videos"]

                self.changes[playlist_id] = compare_video_set(
                    old_playlist, new_playlist
                )
    
    def write_to_output(self) -> None:
        '''
        This method logs the findings to output file for each mutual playlist 
        between the 2 archives.
        '''
        if (len(self.changes) != 0):

            time_apart = get_time_apart(
                self.old_archive_date,
                self.new_archive_date
            )

            self.output_file.write(f"Reporting the changes of the mutual playlists between the 2 archives after {time_apart[0]} days, {time_apart[1]} hours, {time_apart[2]} minutes, {time_apart[3]} seconds\n\n")


        for main_loop_index, mutual_playlist_id in enumerate(self.changes):

            this_playlist_changes: tuple = self.changes[mutual_playlist_id]

            if (check_changes_empty(this_playlist_changes)):
                self.output_file.write(f"0 changes for playlist with id {mutual_playlist_id} ({YOUTUBE_PLAYLIST_PREFIX}{mutual_playlist_id}) \n\n")
                continue

            self.output_file.write(f"The changes in playlist with id {mutual_playlist_id} ({YOUTUBE_PLAYLIST_PREFIX}{mutual_playlist_id}):\n\n")

            added_videos: list = this_playlist_changes[0]

            self.output_file.write(f"Added ({len(added_videos)} video(s) added):\n")

            if (len(added_videos) == 0):
                self.output_file.write("None\n\n")

            else:
                for index, video in enumerate(added_videos):

                    self.output_file.write(f"+ \"{video.get_name()}\" by channel \"{video.get_channel()}\"")

                    if (index != len(added_videos) - 1):
                        
                        self.output_file.write("\n")
                    else:
                        self.output_file.write("\n\n")

            removed_videos: list = this_playlist_changes[1]

            self.output_file.write(f"Removed ({len(removed_videos)} video(s) removed):\n")

            if (len(removed_videos) == 0):
                self.output_file.write("None\n\n")
            
            else:
                for index, video in enumerate(removed_videos):

                    self.output_file.write(f"- \"{video.get_name()}\" by channel \"{video.get_channel()}\"")

                    if (index != len(removed_videos) - 1):
                        self.output_file.write("\n")

                    else:
                        self.output_file.write("\n\n")

            changed_videos: list = this_playlist_changes[2]

            self.output_file.write(f"Changed ({len(changed_videos)} video(s) changed):\n")            

            if (len(changed_videos) == 0):
                
                if (main_loop_index != len(self.changes) - 1):
                    self.output_file.write("None\n\n" + "-"*156 + "\n\n")
                else:
                    self.output_file.write("None")
            
            else: 
                for index, videos in enumerate(changed_videos):
                    old_video: Video = videos[0]
                    new_video: Video = videos[1]

                    if (old_video.is_deleted()):
                        self.output_file.write(f"{old_video.get_name()} --> \"{new_video.get_name()}\" by channel \"{new_video.get_channel()}\"")

                    else:
                        self.output_file.write(f"\"{old_video.get_name()}\" by \"{old_video.get_channel()}\" --> {new_video.get_name()}")

                    if (index != len(changed_videos) - 1):
                        self.output_file.write("\n")

                    else:
                        if (main_loop_index != len(self.changes) - 1):
                            self.output_file.write("\n\n" + "-"*156 + "\n\n")

        self.output_file.close()
         
def compare_video_set(
    old_video_set: Dict[str, Dict[str, str]], 
    new_video_set: Dict[str, Dict[str, str]]
) -> tuple:
    '''
    This function takes in 2 videos attributes of a playlist then find the 
    differences between them.

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

def check_changes_empty(changes: tuple) -> bool:
    '''
    This function checks whether the result given by the function 
    compare_video_set is empty or not (ie there is no change in the mutual playlist between the two archives)

    Params:
        tuple which is the same tuple returned by the function \
        compare_video_set.

    Returns:
        True if it is empty (no change), False otherwise.
    '''

    for i in changes:
        if len(i) != 0:
            return False

    return True

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

    if ("time" not in archive or
        "playlists" not in archive):

        return False

    if (not isinstance(archive["time"], str) or 
        not isinstance(archive["playlists"], dict)):

        return False

    if (not check_time_format(archive["time"])):
        return False

    playlists = archive["playlists"]

    for playlist_id in playlists:

        if not (check_format_of_playlist(playlists[playlist_id])):
            return False

    return True

def check_time_format(time_str: str) -> bool:
    '''
    This function checks whether the time string of the archive is of correct 
    format.

    Params:
        str which is the time string.

    Returns:
        True if correct, False otherwise.
    '''

    try:
        time.strptime(time_str, TIME_FORMAT_STR)
    except ValueError:
        return False

    return True

def parse_time(time_str: str) -> time.struct_time:
    '''
    This function will parse the time string of the correct format into the 
    equivalent struct_time object.

    Params:
        str which is the time string of the correct format.

    Returns:
        The equivalent struct_time object.
    '''

    return time.strptime(time_str, TIME_FORMAT_STR)

def get_time_apart(
    time1: time.struct_time,
    time2: time.struct_time
) -> Tuple[int, int, int, int]:
    '''
    This function will calculate the number of days, hours, minutes and seconds apart between the 2 time 
    stamps. It will return the absolute difference so the order of the 
    parameters does not matter.

    Params:
        2 struct_time objects which represent the 2 different timestamps

    Returns
        A tuple of the format (days, hours, minutes, seconds) which represents 
        the difference between the 2 timestamps.
    '''

    datetime1 = datetime.datetime(
        year=time1.tm_year,
        month=time1.tm_mon,
        day=time1.tm_mday,
        hour=time1.tm_hour,
        minute=time1.tm_min,
        second=time1.tm_sec
    )

    datetime2 = datetime.datetime(
        year=time2.tm_year,
        month=time2.tm_mon,
        day=time2.tm_mday,
        hour=time2.tm_hour,
        minute=time2.tm_min,
        second=time2.tm_sec
    )

    time_apart: datetime.timedelta = abs(datetime1 - datetime2)

    days_apart: int = time_apart.days

    seconds_apart: int = time_apart.seconds

    hours_apart: int = seconds_apart//3600
    seconds_apart -= 3600*hours_apart

    minutes_apart: int = seconds_apart//60
    seconds_apart -= 60*minutes_apart

    return (days_apart, hours_apart, minutes_apart, seconds_apart)

def main():

    if (len(sys.argv) != 4):
        err_print(
            "Usage: python3 comparator.py <old_archive> <new_archive> <output_file>"
        )

        exit(1)

    comparator: Comparator = Comparator(sys.argv[1], sys.argv[2], sys.argv[3])
    comparator.fetch_archives()
    comparator.open_output_file()
    comparator.main_work()
    comparator.write_to_output()

if (__name__ == "__main__"):
    main()