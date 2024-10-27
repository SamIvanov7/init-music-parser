import os
import time
import yt_dlp  # type: ignore
import pandas as pd  # type: ignore
import random
from typing import Optional, Dict, Any

class Downloader:
    def __init__(self, track_queue):
        self.track_queue = track_queue
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.source_dir = os.path.join(base_dir, '../source')
        self.directory = os.path.join(self.source_dir, 'playlists')
        self.cookies_file = os.path.join(base_dir, '../data/cookies.txt')

        # ensure directories exist
        os.makedirs(self.directory, exist_ok=True)

        # configure yt-dlp for searching
        self.ydl_search_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "cookiefile": self.cookies_file,
            "format": "bestaudio/best",
        }

        # configure yt-dlp for downloading
        self.ydl_download_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }],
            "keepvideo": False,
            "quiet": True,
            "cookiefile": self.cookies_file,
            "extract_flat": "in_playlist",
            "no_warnings": True,
            "ignoreerrors": True,
            "retries": 10,
            "fragment_retries": 10,
            "skip_unavailable_fragments": True,
        }

    def search_track(self, query: str, max_retries: int = 3) -> Optional[str]:
        """Search for a track on YouTube with retry logic."""
        for attempt in range(max_retries):
            try:
                with yt_dlp.YoutubeDL(self.ydl_search_opts) as ydl:
                    # search on youtube
                    search_query = f"ytsearch1:{query}"
                    result = ydl.extract_info(search_query, download=False)

                    if result and 'entries' in result and result['entries']:
                        video = result['entries'][0]
                        return f"https://youtube.com/watch?v={video['id']}"

            except Exception as e:
                print(f"Search attempt {attempt + 1} failed for '{query}': {str(e)}")
                if attempt < max_retries - 1:
                    # exponential backoff with jitter
                    sleep_time = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(sleep_time)
                continue

        return None

    def download_track(self, link: str, output_path: str, max_retries: int = 3) -> bool:
        """Download a track with retry logic."""
        opts = dict(self.ydl_download_opts)
        opts['outtmpl'] = output_path

        for attempt in range(max_retries):
            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([link])
                return True

            except Exception as e:
                print(f"Download attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    # exponential backoff with jitter
                    sleep_time = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(sleep_time)
                continue

        return False

    def download_tracks(self):
        """Main method to process and download tracks from playlists."""
        for filename in os.listdir(self.directory):
            if filename.startswith("tracklist_") and filename.endswith(".csv"):
                playlist_path = os.path.join(self.directory, filename)
                playlist_name = filename.replace(".csv", "")
                download_directory = os.path.join(self.source_dir, playlist_name)

                if not os.path.exists(download_directory):
                    os.makedirs(download_directory)

                playlist_df = pd.read_csv(playlist_path)

                for _, track in playlist_df.iterrows():
                    artist = track["artist"]
                    track_name = track["track"]
                    mp3_filename = f"{artist} - {track_name}.mp3"
                    mp3_filepath = os.path.join(download_directory, mp3_filename)

                    if os.path.exists(mp3_filepath):
                        continue

                    search_query = f"{artist} - {track_name}"

                    # add delay between tracks to avoid rate limiting
                    time.sleep(random.uniform(2, 5))

                    try:
                        # search for the track
                        video_url = self.search_track(search_query)
                        if not video_url:
                            print(f"Could not find track: {search_query}")
                            continue

                        # download the track
                        output_template = os.path.join(download_directory, "%(title)s.%(ext)s")
                        if self.download_track(video_url, output_template):
                            # find the downloaded file
                            downloaded_files = [f for f in os.listdir(download_directory)
                                             if f.endswith(".mp3") and f != mp3_filename]

                            if downloaded_files:
                                downloaded_file_path = os.path.join(download_directory, downloaded_files[0])
                                os.rename(downloaded_file_path, mp3_filepath)

                                track_info = {
                                    "file_path": mp3_filepath,
                                    "track_name": search_query
                                }
                                self.track_queue.put(track_info)
                            else:
                                print(f"Download succeeded but file not found for: {search_query}")
                        else:
                            print(f"Failed to download track: {search_query}")

                    except Exception as e:
                        print(f"Error processing track '{search_query}': {str(e)}")

    def run(self):
        """Entry point for the downloader."""
        self.download_tracks()
