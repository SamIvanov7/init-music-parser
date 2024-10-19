import os
import time
import yt_dlp  # type: ignore
import pandas as pd  # type: ignore
from youtube_search import YoutubeSearch  # type: ignore

class Downloader:
    def __init__(self, track_queue):
        self.track_queue = track_queue
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.source_dir = os.path.join(base_dir, '../source')
        self.directory = os.path.join(self.source_dir, 'playlists')

        os.makedirs(self.directory, exist_ok=True)

    def download_tracks(self):
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

                    try:
                        time.sleep(10)
                        search_results = YoutubeSearch(search_query, max_results=1).to_dict()
                        if not search_results:
                            continue

                        link = f"https://youtube.com{search_results[0]['url_suffix']}"

                        ydl_opts = {
                            "format": "bestaudio/best",
                            "postprocessors": [{
                                "key": "FFmpegExtractAudio",
                                "preferredcodec": "mp3",
                                "preferredquality": "320",
                            }],
                            "outtmpl": os.path.join(download_directory, "%(title)s.%(ext)s"),
                            "keepvideo": False,
                            "quiet": True
                        }

                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([link])

                        downloaded_files = os.listdir(download_directory)
                        downloaded_mp3 = [f for f in downloaded_files if f.endswith(".mp3")]

                        if downloaded_mp3:
                            downloaded_file_path = os.path.join(download_directory, downloaded_mp3[0])
                            os.rename(downloaded_file_path, mp3_filepath)

                            track_info = {
                                "file_path": mp3_filepath,
                                "track_name": search_query
                            }
                            self.track_queue.put(track_info)

                    except Exception as e:
                        print(f"Failed to download track '{search_query}'. Error: {e}")

    def run(self):
        self.download_tracks()
