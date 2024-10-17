
# Init Music Parser

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)

## Installation

### Prerequisites
- Python version 3.11.10
- `pip` for managing Python packages
- A virtual environment (recommended)
- `python-dotenv` for environment variable management

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/SamIvanov7/init-music-parser.git
   cd init-music-parser
   ```

2. Install dependencies using `pipenv`:
   ```bash
   pipenv install
   ```

3. Create a `.env` file:
   ```bash
   touch .env
   ```

   Add the following content to the `.env` file:
   ```
   LOGGING_ENABLED=True
   ```

4. Activate the virtual environment:
   ```bash
   pipenv shell
   ```

---

## Usage

2. Run the main script to parse the track names:
   ```bash
   python main.py
   ```

   If you want to disable logging (e.g., for production or cleaner output), update the `.env` file:
   ```bash
   LOGGING_ENABLED=False
   ```

   This will turn off logging during execution.

---

## Environment Variables

You can configure logging behavior using environment variables. The `.env` file controls whether logging is enabled or disabled.

- **LOGGING_ENABLED**: Set to `True` to enable logging (default). Set to `False` to disable logging.

Example `.env` file:
```
LOGGING_ENABLED=True
```

---

## Project Structure

```
📦init-music-parser
 ┣ 📂core
 ┃ ┣ 📜__init__.py               # Core logic for parsing track names
 ┃ ┗ 📜track_names_parser.py      # Main parser for track names
 ┣ 📂source
 ┃ ┗ 📜tracks.csv                # CSV file with track names
 ┣ 📜.env                        # Environment variable settings
 ┣ 📜.gitignore                  # Files to ignore in version control
 ┣ 📜Pipfile                     # Pipenv configuration for dependencies
 ┣ 📜Pipfile.lock                # Pipenv lock file
 ┣ 📜README.md                   # Project documentation
 ┣ 📜main.py                     # Main script to run the parser
 ┣ 📜readme                      # Additional documentation (if needed)
 ┗ 📜requirements.txt            # Project dependencies for pip (alternative to Pipfile)
```

### Key Files:
- `core/track_names_parser.py`: This file contains the logic for fetching the webpage, parsing the track names, and saving them to a CSV file.
- `source/tracks.csv`: Your input CSV file where track names are stored.
- `main.py`: The entry point for executing the track name parsing functionality.

---

## Dependencies

The project uses the following Python libraries, as defined in the `Pipfile`:

- `requests`: For handling HTTP requests.
- `beautifulsoup4`: For web scraping and HTML parsing.
- `aioslsk`: For asynchronous operations related to downloading or scraping (depends on implementation).
- `python-dotenv`: For loading environment variables from a `.env` file.

To install dependencies, use `pipenv install` as described in the [Installation](#installation) section.
