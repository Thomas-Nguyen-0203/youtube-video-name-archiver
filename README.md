# youtube-video-name-archiver
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

## JSON-representation of various objects

JSON-representation of a video

```python
video = {
	"id": str,
	"name": str,
	"channel": str,
	"link": str
}
```

JSON-representation of a playlist

```python
playlist = {
	"id": str,
	"videos": {
		video_id: video
	},
	"link": str
}
```

JSON-representation of an archive

```python
archive = {
	playlist_id : playlist
}
```

__Note__: an archive may have one or more playlists.

The use of a dictionary instead of an array will help a lot with speed once we are comparing 2 archives and 2 playlists.