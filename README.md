# youtube-video-name-archiver

## Introduction
Don't you hate it when you are vibing with your crazily cool youtube music playlist (which may or may not contain bunch of niche songs that is reposted from Nico Nico Douga) 
that you have been building up for 5 years but then one day, the warning: "unavailable videos are hidden" shows up? Or when you just revisit a playlist that you created a decade ago,
only for it to be filled with "Unavailable video" or "Deleted video"? 

This program aims to archive the title, id and the name of channel that uploaded the video for all videos within a playlist.
It uses the Youtube API's to retrieve all the required information.

This project was initiated to help me in understanding API's.

Also, I made this project using python version 3.8.10 but I think any version of Python > 3.5 should work.

## Prerequisites
- requests module (Latest release)
- A Google API key
- Python interpreter (v3.8 was used to make this program but should work for all Python > 3.5)

## Usage
### Archiver
To use the archiver, you need to create an input file which contains valid URL's to one or more Youtube playlists (URL's of the form `https://www.youtube.com/playlist?list=<playlist_id>`).

__Note:__ This program also works with URL of a video inside the playlist (ie videos with URL of the form: `https://www.youtube.com/watch?v=<video_id>&list=<playlist_id>`)

An example of a valid input file and its output can be found in example folder.

Then in order to run the program you just need to run

```
python3 archiver.py <name_of_input_file> <name_of_output_file>
```

And the program will produce its output and write to the file with name given by <name_of_output_file>

Since this program lets the user name its own output, I will not enforce any naming rules to the output file, however, since the output is in JSON syntax, a file extension of `.json` is advised.


### Comparator
To use the comparator, you have to have 2 archives (not necessarily different but comparing the same archive to itself is kinda against the point of a comparator), the 2 archives need not to contain the same playlists because the comparator will find all mutual playlists between the 2 archives and compare them.

Its purpose is to compare between the same set of playlists at 2 different points in time (old archive and new archive) and find out what have happened to all the playlists after that time period. The comparator will make a list of added videos, removed videos and videos that changed (going from private to non-private, going from normal to deleted and vice-versa) for each mutual playlist and log that to the output file indicated by the user.

In order to run the comparator, you need to run the command

```
python3 comparator.py <old_archive> <new_archive> <output_file>
```

Example input-output will be included **soon**!!!

## Side Information

### JSON-representation of various objects (relevant to the program and how it will output information)

#### JSON-representation of a video

```python
video = {
	"id": str,
	"name": str,
	"channel": str,
	"link": str
}
```

#### JSON-representation of a playlist

```python
playlist = {
	"id": str,
	"videos": {
		video_id: video
	},
	"link": str
}
```

#### JSON-representation of an archive

```python
archive = {
	playlist_id : playlist
}
```

__Note__: an archive may have one or more playlists.

The use of a dictionary instead of an array will help a lot with speed once we are comparing 2 archives and 2 playlists.

### Cost per run
Since I chose 50 videos per call (the maximum number), the expected cost per run is:
$$\sum_{i = 1}^n \left\lceil\frac{N_i}{50}\right\rceil \text{quota}$$ 
for: 
- $n$ the number of playlists of the input
- $N_i$ the number of videos in the $i^{th}$ playlist