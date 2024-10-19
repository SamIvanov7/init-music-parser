import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

import threading
from queue import Queue
from core.bot import Bot
from core.parser_module import Parser
from core.downloader import Downloader
from core.uploader import Uploader

if __name__ == '__main__':
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN")
    API_ID = int(os.environ.get("API_ID", "YOUR_API_ID"))
    API_HASH = os.environ.get("API_HASH", "YOUR_API_HASH")
    CHANNEL_ID = "-1001549434173"

    track_queue = Queue() # type: ignore

    parser = Parser()
    downloader = Downloader(track_queue)
    uploader = Uploader(track_queue, CHANNEL_ID)

    plugins = dict(
        root="core/InitMusicParserBot/plugins"
    )
    bot = Bot(BOT_TOKEN, API_ID, API_HASH, plugins)

    parser_thread = threading.Thread(target=parser.run)
    parser_thread.start()
    parser_thread.join()
    downloader_thread = threading.Thread(target=downloader.run)
    downloader_thread.start()

    bot.start()

    uploader.run(bot.bot)

    print("Bot is running...")
    bot.idle()

    downloader_thread.join()
