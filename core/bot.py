# core/bot.py
from pyrogram import Client, filters
import logging
from typing import Optional
import yt_dlp  # type: ignore
import os

# Initialize logger for this module
logger = logging.getLogger(__name__)

class Bot:
    def __init__(self, bot_token: str, api_id: int, api_hash: str, plugins: Optional[dict] = None):
        """
        Initialize the Bot with Pyrogram Client and register handlers.

        Args:
            bot_token (str): Telegram Bot API token.
            api_id (int): Telegram API ID.
            api_hash (str): Telegram API hash.
            plugins (dict, optional): Pyrogram plugins configuration.
        """
        self.bot = Client(
            "InitMusicParserBot",
            bot_token=bot_token,
            api_hash=api_hash,
            api_id=api_id,
            plugins=plugins or {}
        )
        self.add_handlers()

    def add_handlers(self):
        """Register message handlers for the bot."""

        @self.bot.on_message(filters.command("ping", prefixes="!"))
        async def ping(client, message):
            """Respond to the !ping command."""
            await message.reply("Pong!")
            logger.info(f"Responded to !ping from user {message.from_user.id}")

        # The following handlers have been moved to plugins for better modularity
        # If you prefer to keep them here, you can uncomment and adjust accordingly

        # @self.bot.on_message(filters.command("start"))
        # async def start(client, message):
        #     """Respond to the /start command."""
        #     logger.info(f"Received /start command from user {message.from_user.id}")
        #     await message.reply_text("Hello! I'm your Init Music Parser Bot.")

        # @self.bot.on_message(filters.command("download"))
        # async def download_video(client, message):
        #     """Handle the /download command to download YouTube videos."""
        #     # Implementation as shown earlier

        @self.bot.on_message(filters.channel)
        async def listen_channel(client, message):
            """Listen to all messages in the channel."""
            logger.info(f"New message in channel: {message.text}")

    def run(self):
        """Start the bot and idle."""
        logger.info("Starting bot...")
        self.bot.run()
