# core/bot.py
from pyrogram import Client, filters, idle

class Bot:
    def __init__(self, bot_token, api_id, api_hash, plugins=None):
        self.bot = Client(
            "InitMusicParserBot",
            bot_token=bot_token,
            api_hash=api_hash,
            api_id=api_id,
            plugins=plugins
        )
        self.add_handlers()

    def add_handlers(self):
        @self.bot.on_message(filters.command("ping", prefixes="!") & filters.channel)
        async def ping(client, message):
            await message.reply("Pong!")

        @self.bot.on_message(filters.channel)
        async def listen_channel(client, message):
            print(f"New message in channel: {message.text}")

    def start(self):
        self.bot.start()

    def idle(self):
        idle()

    def run(self):
        self.start()
        print("Bot is running...")
        self.idle()
