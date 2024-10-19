import os
from core.track_names_parser import TrackNamesParser
from core.playlist_creator import PlaylistCreator

class Parser:
    def __init__(self):
        self.url = "https://www.junodownload.com/deep-house/charts/bestsellers/this-week/tracks/"
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.source_dir = os.path.join(base_dir, '../source')
        self.csv_file = os.path.join(self.source_dir, 'tracks.csv')

        os.makedirs(self.source_dir, exist_ok=True)

    def run_parser(self):
        parser = TrackNamesParser(self.url, self.csv_file)
        html_content = parser.fetch_webpage()
        if html_content:
            parser.parse_tracks(html_content)
            track_data = parser.extract_track_info()
            parser.save_to_csv(track_data)

    def create_playlists(self):
        input_file = self.csv_file
        playlists_dir = os.path.join(self.source_dir, 'playlists')

        creator = PlaylistCreator(input_file, playlists_dir)
        creator.create_playlist()

    def run(self):
        self.run_parser()
        self.create_playlists()
