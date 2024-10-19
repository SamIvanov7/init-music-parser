
# Init Music Parser

A Telegram bot that parses music tracks from JunoDownload charts, downloads them from YouTube, and uploads them to a Telegram channel.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Notes](#notes)

---

## Features

- Parses music track names from the JunoDownload Deep House charts.
- Creates playlists based on the parsed tracks.
- Downloads tracks from YouTube as MP3 files.
- Uploads tracks to a specified Telegram channel with metadata including thumbnails, duration, and views.
- Supports inline search functionality and song requests via Telegram bot.

---

## Installation

### Prerequisites

- **Python** version 3.11.10 or higher
- **pip** for managing Python packages
- A **virtual environment** (recommended)
- **FFmpeg** installed on your system (required by `yt-dlp` for audio conversion)
- **python-dotenv** for environment variable management
- A **Telegram Bot Token** (from [BotFather](https://t.me/BotFather))
- **Telegram API ID** and **API Hash** (from [my.telegram.org](https://my.telegram.org))
- A **Telegram Channel ID** where the bot will upload tracks

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SamIvanov7/init-music-parser.git
   cd init-music-parser
   ```

2. **Install dependencies:**

   Using **pipenv**:
   ```bash
   pipenv install
   ```

   Or using **pip** and `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file:**
   ```bash
   touch .env
   ```

   Add the following content to the `.env` file:
   ```
   BOT_TOKEN=your_bot_token
   API_ID=your_api_id
   API_HASH=your_api_hash
   CHANNEL_ID=your_channel_id
   LOGGING_ENABLED=True
   ```

   Replace `your_bot_token`, `your_api_id`, `your_api_hash`, and `your_channel_id` with your actual Telegram bot token, API ID, API Hash, and the ID or username of your Telegram channel.

4. **Activate the virtual environment:**

   Using **pipenv**:
   ```bash
   pipenv shell
   ```

5. **Ensure FFmpeg is installed:**

   - **macOS** (using Homebrew):
     ```bash
     brew install ffmpeg
     ```

   - **Ubuntu/Debian**:
     ```bash
     sudo apt-get install ffmpeg
     ```

   - **Windows**:
     Download FFmpeg from the [official website](https://ffmpeg.org/download.html) and add it to your system PATH.

---

## Usage

1. **Run the main script:**
   ```bash
   python main.py
   ```

2. **Interact with the bot:**

   - **Start the bot** by sending `/start` in your Telegram bot chat.
   - **Use inline search** by typing your bot's username in any chat followed by a song name.
   - The bot will automatically parse the latest tracks, download them, and upload them to your specified channel.

3. **Disable logging (optional):**

   If you want to disable logging (e.g., for production or cleaner output), update the `.env` file:
   ```
   LOGGING_ENABLED=False
   ```

---

## Environment Variables

Configure the bot and logging behavior using the `.env` file.

- **BOT_TOKEN**: Your Telegram bot token obtained from [BotFather](https://t.me/BotFather).
- **API_ID**: Your Telegram API ID obtained from [my.telegram.org](https://my.telegram.org).
- **API_HASH**: Your Telegram API Hash obtained from [my.telegram.org](https://my.telegram.org).
- **CHANNEL_ID**: The ID or username of the Telegram channel where the bot will upload tracks. If using a channel ID, it should be in the format `-1001234567890`. If using a username, prefix it with `@`, e.g., `@your_channel_username`.
- **LOGGING_ENABLED**: Set to `True` to enable logging (default). Set to `False` to disable logging.

Example `.env` file:
```
BOT_TOKEN=123456789:ABCDEF_GHIJKLMNOPQRSTUVWXYZ
API_ID=123456
API_HASH=abcdef1234567890abcdef1234567890
CHANNEL_ID=-1001234567890
LOGGING_ENABLED=True
```

---

## Project Structure

```
📦 init-music-parser
├── 📂 core
│   ├── 📂 InitMusicParserBot
│   │   ├── 📂 plugins
│   │   │   ├── __init__.py
│   │   │   ├── inline.py          # Handles inline queries
│   │   │   └── song.py            # Handles song requests
│   │   └── __init__.py
│   ├── __init__.py
│   ├── bot.py                     # Bot initialization and handlers
│   ├── downloader.py              # Downloads tracks from YouTube
│   ├── parser_module.py           # Parses track names and creates playlists
│   ├── playlist_creator.py        # Creates playlists from parsed tracks
│   ├── track_names_parser.py      # Parses track names from the website
│   └── uploader.py                # Uploads tracks to Telegram channel
├── 📂 source
│   ├── 📂 playlists
│   │   ├── tracklist_YYYY-MM-DD.csv   # Generated playlists
│   ├── 📂 tracklist_YYYY-MM-DD        # Downloaded tracks for the date
│   └── tracks.csv                     # CSV file with parsed track names
├── .env                           # Environment variable settings
├── .gitignore                     # Files to ignore in version control
├── Pipfile                        # Pipenv configuration for dependencies
├── Pipfile.lock                   # Pipenv lock file
├── README.md                      # Project documentation
├── main.py                        # Main script to run the bot
├── requirements.txt               # Project dependencies for pip
└── tree.txt                       # File tree of the project
```

### Key Files

- **`main.py`**: The entry point for executing the bot.
- **`core/bot.py`**: Initializes the bot and sets up message handlers.
- **`core/parser_module.py`**: Contains classes to parse track names and create playlists.
- **`core/downloader.py`**: Downloads tracks from YouTube based on the playlists.
- **`core/uploader.py`**: Uploads the downloaded tracks to the Telegram channel.
- **`core/InitMusicParserBot/plugins/inline.py`**: Handles inline queries for song search.
- **`core/InitMusicParserBot/plugins/song.py`**: Handles song requests via messages.

---

## Dependencies

The project uses the following Python libraries:

- **[pyrogram](https://docs.pyrogram.org/)**: For interacting with the Telegram API.
- **[requests](https://docs.python-requests.org/)**: For handling HTTP requests.
- **[beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)**: For web scraping and HTML parsing.
- **[pandas](https://pandas.pydata.org/)**: For data manipulation and CSV handling.
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)**: For downloading and converting videos from YouTube.
- **[youtube-search-python](https://pypi.org/project/youtube-search-python/)**: For searching YouTube videos.
- **[python-dotenv](https://saurabh-kumar.com/python-dotenv/)**: For loading environment variables from a `.env` file.
- **[asyncio](https://docs.python.org/3/library/asyncio.html)**: For asynchronous programming.
- **[aiohttp](https://docs.aiohttp.org/)**: For asynchronous HTTP requests (if used in the code).
- **FFmpeg** (external dependency): Required by `yt-dlp` for audio conversion.

To install dependencies, use `pipenv install` as described in the [Installation](#installation) section, or:

```bash
pip install -r requirements.txt
```

---

## Notes

- **Bot Permissions**: Ensure that the bot is added to your Telegram channel and has the necessary permissions to send messages. For private channels, the bot must be a member.
- **Channel ID Format**: If using a channel ID, make sure it starts with `-100`. For example: `-1001234567890`.
- **First Run**: When running the bot for the first time, it will parse the latest tracks from JunoDownload, download them, and upload them to your channel.
- **API Terms of Service**: Be mindful of YouTube's and Telegram's API terms of service when downloading and sharing content.
- **Logging**: Adjust the `LOGGING_ENABLED` variable in the `.env` file to control logging verbosity.

---

Feel free to contribute to this project or report any issues you encounter. Happy parsing and sharing music!
