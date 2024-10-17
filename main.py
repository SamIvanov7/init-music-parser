from core.track_names_parser import TrackNamesParser

def main():
    url = "https://www.junodownload.com/deep-house/charts/bestsellers/this-week/tracks/"
    csv_file = './source/tracks.csv'

    parser = TrackNamesParser(url, csv_file)

    html_content = parser.fetch_webpage()

    if html_content:
        parser.parse_tracks(html_content)

        track_data = parser.extract_track_info()

        parser.save_to_csv(track_data)

if __name__ == '__main__':
    main()
