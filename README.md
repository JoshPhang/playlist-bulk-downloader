# Playlist Bulk Downloader

This is a tool that helps bulk download _Spotify playlists_ and _Youtube Podcasts_

## Requirements

- Python

## Installation

1. Download the repository

```
git pull https://github.com/JoshPhang/playlist-bulk-downloader.git
```

2. Install required packages

```
pip install spotdl
```

```
spotdl --download-ffmpeg
```

- **Note** You may need to relaunch terminal or add the .spotdl folder to the environment variable PATH (Typically located in C:/Users/[user]/.spotdl)

## Add your playlists to playlists.txt

**See sample playlists.txt**

1. Add your desired download location to the first line
2. Add the name of the playlist, followed by the link of the Spotify playlist, separated by a single space

e.g.

```
PlaylistName https://open.spotify.com/playlist/playlistid
```

## Add your podcasts to podcasts.txt

**See sample podcasts.txt**

1. Add your desired download location to the first line
2. Add the name of the podcast, followed by the link of the YouTube podcast, separated by a single space

e.g.

```
PodcastName https://www.youtube.com/@ChannelName/videos
```

## Tune your settings in `playlist-updater.py`

- `generate_m3u8`: [Bool] - Generate a m3u8 file for playlist organization in jellyfin
- `download_playlists`: [Bool] - Enable downloading playlists from playlists.txt
- `download_podcasts`: [Bool] - Enable downloading podcasts from podcasts.txt
- `podcast_format`: ["mp4"/"mp3"] - Choose file format for podcasts
- `number_podcasts`: ["number"] - Choose how many episodes of each podcast to download

## Running the tool

1. Navigate to the folder containing `playlist-updated.py`
2. Execute the python script using

```
python playlist-updater.py
```

3. Find your downloaded files in your chosen location
