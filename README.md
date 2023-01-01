# youtube-video-name-archiver
A personal project that is used to help me identify what is the name of the Youtube video that was deleted.

It uses the Youtube API to retrieve the names of all the videos inside the link of the playlist provided.

This project was initiated so that it could help me in understanding the use of API and for my personal learning mainly.

This project depends on the external module requests so you need to install it to use this program.

Also, I made this project using python version 3.8.10 but I think any version of Python > 3.5 should work.

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

The use of a dictionary instead of an array will help a lot with speed once we are comparing 2 archives.
