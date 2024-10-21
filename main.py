# main.py

import os
import sys
import logging
from core.bot import Bot

# Uncomment the following imports if you have these modules implemented and need to integrate them.
# from core.parser_module import Parser
# from core.downloader import Downloader
# from core.uploader import Uploader
# import threading
# from queue import Queue

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def validate_env_vars(env_vars):
    """
    Validate the presence and correctness of required environment variables.

    Parameters:
        env_vars (dict): Dictionary containing environment variables.

    Returns:
        dict: Validated and correctly typed environment variables.

    Exits:
        If any required environment variable is missing or invalid.
    """
    missing_vars = [var for var, value in env_vars.items() if not value]
    if missing_vars:
        logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
        sys.exit(1)

    try:
        env_vars['API_ID'] = int(env_vars['API_ID'])
    except ValueError:
        logger.error("API_ID must be an integer.")
        sys.exit(1)

    return env_vars

def main():
    """Main entry point for the application."""
    global logger
    logger = setup_logging()

    # Retrieve environment variables
    env_vars = {
        "BOT_TOKEN": os.environ.get("BOT_TOKEN"),
        "API_ID": os.environ.get("API_ID"),
        "API_HASH": os.environ.get("API_HASH"),
        "CHANNEL_ID": os.environ.get("CHANNEL_ID", "-1001549434173")  # Default channel ID
    }

    # Validate environment variables
    env_vars = validate_env_vars(env_vars)

    # Initialize the Bot
    plugins = {
        "root": "core/InitMusicParserBot/plugins"
    }

    bot = Bot(
        bot_token=env_vars["BOT_TOKEN"],
        api_id=env_vars["API_ID"],
        api_hash=env_vars["API_HASH"],
        plugins=plugins
    )

    # If you have additional components like Parser, Downloader, Uploader,
    # initialize and start them here. Ensure they run concurrently without blocking the bot.
    # Here's a basic example using threading:

    # Uncomment and adjust the following lines if you have these modules implemented.
    # track_queue = Queue()

    # parser = Parser()
    # downloader = Downloader(track_queue)
    # uploader = Uploader(track_queue, env_vars["CHANNEL_ID"])

    # parser_thread = threading.Thread(target=parser.run, daemon=True)
    # downloader_thread = threading.Thread(target=downloader.run, daemon=True)
    # uploader_thread = threading.Thread(target=uploader.run, daemon=True)

    # parser_thread.start()
    # downloader_thread.start()
    # uploader_thread.start()

    # Start the bot
    bot.run()

    # The bot.run() method is blocking. If you have non-daemon threads, ensure they are joined here.
    # parser_thread.join()
    # downloader_thread.join()
    # uploader_thread.join()

if __name__ == "__main__":
    main()
