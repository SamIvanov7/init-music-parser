import pandas as pd  # type: ignore
import os
from datetime import datetime

class PlaylistCreator:
    def __init__(self, input_file, directory='source/playlists/'):
        self.input_file = input_file
        self.directory = directory
        self.tracks_df = None
        self.ensure_directory_exists()
        self.ensure_initial_playlist_file()

    def ensure_directory_exists(self):
        """Ensure the directory for tracklists exists."""
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def ensure_initial_playlist_file(self):
        """Create an initial empty playlist file if no files exist in the directory."""
        if not any(fname.startswith("tracklist_") and fname.endswith(".csv") for fname in os.listdir(self.directory)):
            # Create an empty playlist CSV with necessary fields
            empty_df = pd.DataFrame(columns=["track_id", "rating_in_top_50", "artist", "track", "label", "duration", "bpm"])
            empty_filename = os.path.join(self.directory, "tracklist_initial.csv")
            empty_df.to_csv(empty_filename, index=False)
            print(f"Initial empty playlist file created: {empty_filename}")

    def load_tracks(self):
        """Load the main tracks file and sort tracks by rating."""
        try:
            self.tracks_df = pd.read_csv(self.input_file)
            self.tracks_df = self.tracks_df.sort_values(by='rating_in_top_50', ascending=True)
        except Exception as e:
            print(f"Error reading {self.input_file}: {e}")
            self.tracks_df = pd.DataFrame()  # Empty DataFrame if file loading fails

    def load_existing_playlists(self):
        """Load all existing tracklists to identify tracks already used."""
        existing_tracks = set()
        for filename in os.listdir(self.directory):
            if filename.startswith("tracklist_") and filename.endswith(".csv"):
                try:
                    df = pd.read_csv(os.path.join(self.directory, filename))
                    existing_tracks.update(df['track_id'])
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
        return existing_tracks

    def filter_available_tracks(self, existing_tracks, start_rating, end_rating):
        """Filter out tracks that are already used in existing playlists and within the given rating range."""
        if self.tracks_df is not None:
            available_tracks = self.tracks_df[
                (~self.tracks_df['track_id'].isin(existing_tracks)) &
                (self.tracks_df['rating_in_top_50'] >= start_rating) &
                (self.tracks_df['rating_in_top_50'] <= end_rating)
            ]
            return available_tracks
        return pd.DataFrame()

    def create_playlist(self):
        """Create a new playlist with 16 unique tracks."""
        # Load the tracks
        self.load_tracks()

        # Load existing tracklists to avoid repeating tracks
        existing_tracks = self.load_existing_playlists()

        # Determine the current range of ratings for the new playlist
        existing_ratings = self.tracks_df[self.tracks_df['track_id'].isin(existing_tracks)]['rating_in_top_50']
        if not existing_ratings.empty:
            start_rating = existing_ratings.max() + 1
        else:
            start_rating = 1

        end_rating = start_rating + 15

        # Filter available tracks within the determined rating range
        available_tracks = self.filter_available_tracks(existing_tracks, start_rating, end_rating)

        # Check if there are enough tracks to create a playlist
        if len(available_tracks) < 16:
            print("Not enough unique tracks available to create a new playlist.")
            return

        # Select the top 16 tracks for the new playlist
        new_playlist = available_tracks.head(16)

        # Generate filename for the new playlist
        current_date = datetime.now().strftime('%Y-%m-%d')
        new_filename = f"tracklist_{current_date}.csv"

        # Save the new playlist to a CSV file
        new_playlist.to_csv(os.path.join(self.directory, new_filename), index=False)
        print(f"New playlist saved as {os.path.join(self.directory, new_filename)}")


