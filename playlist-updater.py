'''
PLAYLIST UPDATER SETTINGS
generate_m3u8: [Bool] - Generate a m3u8 file for playlist organization in jellyfin
download_playlists: [Bool] - Enable downloading playlists from playlists.txt
download_podcasts: [Bool] - Enable downloading podcasts from podcasts.txt
podcast_format: ["mp4"/"mp3"] - Choose file format for podcasts
number_podcasts: ["number"] - Choose how many episodes of each podcast to download
'''
generate_m3u8 = True
download_playlists = True
download_podcasts = True
podcast_format = "mp3"
number_podcasts = "10"


'''
DO NOT EDIT CODE BELOW HERE
'''

import subprocess
import os
import shutil

def update_playlist(playlist_url, download_dir):
    if generate_m3u8:
        proc = subprocess.Popen([
                                    "spotdl", playlist_url,
                                    "--output", download_dir,
                                    "--yt-dlp-args", "--sleep-requests 1.5 --min-sleep-interval 1 --max-sleep-interval 10",
                                    "--m3u",
                                ])
    else:
        proc = subprocess.Popen([
                                    "spotdl", playlist_url,
                                    "--output", download_dir,
                                    "--yt-dlp-args", "--sleep-requests 1.5 --min-sleep-interval 1 --max-sleep-interval 10",
                                ])
    proc.wait()  # Wait for the download to complete
    # Move the .m3u file to the download directory
    for file in os.listdir('.'):
        if file.endswith('.m3u8'):
            # Change absolute file path to relative file path for Jellyfin
            with open(file, "r", encoding="utf8") as f:
                newPath=f.read().replace(download_dir, "")

            with open(file, "w", encoding="utf8") as f:
                f.write(newPath)
            shutil.move(file, os.path.join(download_dir, file))
    

def update_podcasts(podcast_url, download_dir, podcast_name):
    if generate_m3u8:
        proc = subprocess.Popen([
                                    "yt-dlp", podcast_url,
                                    "-t", podcast_format,
                                    "--paths", download_dir,
                                    "--match-filter", 'original_url!*=/shorts/',
                                    "--output", "%(channel)s " + "[" + "%(id)s" + "]",
                                    "--playlist-end", "10",
                                    "--cookies-from-browser", "chrome",
                                    "--sleep-requests", "1.5",
                                    "--min-sleep-interval", "1",
                                    "--max-sleep-interval", "10",
                                    "--parse-metadata", "title:%(title)s", "--embed-metadata",
                                    "--embed-thumbnail", "-f", "bestaudio", "-x", "--audio-format", "mp3", "--audio-quality", "320k",
                                    "--print-to-file", "#EXTINF:%(duration)s,%(upload_date>%d/%m/%Y)s %(title)s", f"{podcast_name}.m3u8",
                                    "--print-to-file", "%(channel)s " + "[" + "%(id)s" + "]" + "." + podcast_format, f"{podcast_name}.m3u8"
                                ])
    else:
        proc = subprocess.Popen([
                                    "yt-dlp", podcast_url,
                                    "-t", podcast_format,
                                    "--paths", download_dir,
                                    "--playlist-end", "10",
                                    "--cookies-from-browser", "chrome",
                                    "--sleep-requests", "1.5",
                                    "--min-sleep-interval", "1",
                                    "--max-sleep-interval", "10",
                                    "--parse-metadata", "title:%(title)s", "--write-thumbnail", "--embed-metadata",
                                    "--embed-thumbnail", "-f", "bestaudio", "-x", "--audio-format", "mp3", "--audio-quality", "320k",
                                ])
    proc.wait()  # Wait for the download to complete
    for file in os.listdir(download_dir):
        if file.endswith('.m3u8'):
            # Change absolute file path to relative file path for Jellyfin
            shutil.move(download_dir+"\\"+file, os.path.join(download_dir, file))

if __name__ == "__main__":
    '''
    READ PLAYLISTS
    '''
    if download_playlists:
        file_path = "playlists.txt"
        with open(file_path, "r") as f:
            lines = f.readlines()
            
        if not lines:
            raise ValueError("playlists.txt is empty. Please specify the download directory on the first line.")
        download_dir = lines[0].strip()

        for pl in lines[1:]:
            url = pl.strip().split(" ")[1]
            update_playlist(url, download_dir)

    '''
    DOWNLOAD PODCASTS
    '''
    if download_podcasts:
        file_path = "podcasts.txt"
        with open(file_path, "r") as f:
            lines = f.readlines()
            
        if not lines:
            raise ValueError("podcasts.txt is empty. Please specify the download directory on the first line.")
        download_dir = lines[0].strip()

        # Reset podcast playlist to prevent overlapping
        for file in os.listdir(download_dir):
            if file.endswith('.m3u8'):
                os.remove(os.path.join(download_dir, file))

        for pl in lines[1:]:
            podcast_name = pl.strip().split(" ")[0]
            url = pl.strip().split(" ")[1]
            update_podcasts(url, download_dir, podcast_name)

    

