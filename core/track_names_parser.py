import os
import requests
from bs4 import BeautifulSoup
import csv
import logging
from dotenv import load_dotenv

load_dotenv()

logging_enabled = os.getenv('LOGGING_ENABLED', 'True').lower() == 'true'

if logging_enabled:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.CRITICAL)


class TrackNamesParser:
    def __init__(self, url: str, csv_file: str):
        self.url = url
        self.csv_file = csv_file
        self.tracks: list = []

    def fetch_webpage(self):
        logging.info(f"Sending GET request to {self.url}")
        response = requests.get(self.url)

        if response.status_code == 200:
            logging.info("Successfully fetched the webpage")
            return response.content
        else:
            logging.error(f"Failed to fetch the webpage. Status code: {response.status_code}")
            return None

    def parse_tracks(self, html_content: str):
        soup = BeautifulSoup(html_content, 'html.parser')
        tracks = soup.find_all('div', class_='jd-listing-item-track')

        if not tracks:
            logging.error("No tracks found on the page. The structure may have changed or the data is missing.")
            return []

        logging.debug(f"Found {len(tracks)} tracks on the page")
        self.tracks = tracks[:16]
        logging.debug(f"Processing {len(self.tracks)} tracks")

    def extract_track_info(self):
        extracted_tracks = []

        for index, track in enumerate(self.tracks, start=1):
            artist = track.select_one('.juno-artist a')
            artist = artist.get_text(strip=True) if artist else ''
            if not artist:
                logging.warning(f"Artist not found for track {index}")

            title = track.select_one('a.juno-title')
            title = title.get_text(strip=True) if title else ''
            if not title:
                logging.warning(f"Track title not found for track {index}")

            label = track.select_one('.lit-label-genre a')
            label = label.get_text(strip=True) if label else ''
            if not label:
                logging.warning(f"Label not found for track {index}")

            duration_bpm_text = track.select_one('.lit-date-length-tempo')
            if duration_bpm_text:
                duration_bpm_text = duration_bpm_text.get_text(strip=True)
                duration, bpm = duration_bpm_text.split(' / ') if ' / ' in duration_bpm_text else (duration_bpm_text, '')
            else:
                duration, bpm = '', ''
                logging.warning(f"Duration or BPM not found for track {index}")

            extracted_tracks.append([f"{index:02}", artist, title, label, duration, bpm])

        return extracted_tracks

    def save_to_csv(self, data):
        file_exists = os.path.isfile(self.csv_file)
        mode = 'a' if file_exists else 'w'

        with open(self.csv_file, mode=mode, newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            if not file_exists:
                logging.debug("Writing headers to the CSV file")
                writer.writerow(["Index", "Artist", "Track", "Label", "Duration", "BPM"])

            for track in data:
                logging.debug(f"Writing track {track[0]} to the CSV file")
                writer.writerow(track)

        logging.info(f"Data saved in {self.csv_file}")
