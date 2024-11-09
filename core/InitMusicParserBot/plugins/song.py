import os
import time
import logging
from datetime import datetime, timedelta
from collections import deque
import requests
import yt_dlp
from pyrogram import filters, Client, idle
from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import MessageNotModified

# Environment variables
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")

# Rate limiter class
class RateLimiter:
    def __init__(self, max_requests=2, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()

    async def can_proceed(self):
        now = datetime.now()
        while self.requests and self.requests[0] < now - timedelta(seconds=self.time_window):
            self.requests.popleft()

        if len(self.requests) >= self.max_requests:
            return False

        self.requests.append(now)
        return True

rate_limiter = RateLimiter()

def get_cookies():
    if not os.path.exists('cookies.txt'):
        cookies = {
            'name': username,
            'value': password,
            'domain': '.youtube.com',
        }
        with open('cookies.txt', 'w') as f:
            f.write(f'youtube.com\tTRUE\t/\tTRUE\t{int(time.time()) + 31536000}\t{cookies["name"]}\t{cookies["value"]}')
    return 'cookies.txt'

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))

## Commands --------
@Client.on_message(filters.command(['start']))
async def start(client, message):
    await message.reply("This bot sends tracks to telegram",
                     reply_markup=InlineKeyboardMarkup(
                         [
                             [
                                 InlineKeyboardButton('Search Track', switch_inline_query_current_chat='')
                             ]
                         ]
                     ))

@Client.on_message(filters.command(['help']))
async def help(client, message):
    await message.reply("Help",
                     reply_markup=InlineKeyboardMarkup(
                         [
                             [
                                 InlineKeyboardButton('Developer', url='https://t.me/sabaney')
                             ]
                         ]
                     ))

@Client.on_message(filters.command(['about']))
async def about(client, message):
    await message.reply("About",
                     reply_markup=InlineKeyboardMarkup(
                         [
                             [
                                 InlineKeyboardButton('Search Inline', switch_inline_query_current_chat='')
                             ]
                         ]
                     ))

@Client.on_message(filters.text)
async def song_search(client, message):
    if not await rate_limiter.can_proceed():
        await message.reply("Please wait before making another request.")
        return

    query = message.text
    print(query)
    m = await message.reply('Searching...')

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }],
        "outtmpl": "%(title)s.%(ext)s",
        "postprocessor_args": [
            "-metadata", "title=%(title)s",
            "-metadata", "artist=MusicDownloadv2bot"
        ],
        "keepvideo": False,
        "cookiefile": ".cookies.txt",
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate",
        },
        "quiet": True,
        "no_warnings": True,
        "extract_flat": "in_playlist",
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": False,
        "retries": 5,
        "fragment_retries": 5,
        "skip_download": False,
        "sleep_interval": 5,
        "max_sleep_interval": 10,
        "sleep_interval_requests": 1,
        "max_sleep_interval_requests": 3,
        "rate_limit": "50K"
    }

    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count > 0:
                time.sleep(2)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1

        if not results:
            await m.edit('❎ No results found. Please try a different search term.')
            return

        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            performer = "InitTrackParserBot"
            views = results[0]["views"]
            thumb_name = f'thumb{message.id}.jpg'

            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(f"error in parsing search results: {str(e)}")
            await m.edit('Failed to process track information.')
            return

        try:
            await m.edit("Downloading track...")
        except MessageNotModified:
            pass

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                max_retries = 3
                retry_count = 0

                while retry_count < max_retries:
                    try:
                        info_dict = ydl.extract_info(link, download=False)
                        if info_dict.get('is_live'):
                            await m.edit('❌ Cannot download live streams.')
                            return

                        time.sleep(2)
                        info_dict = ydl.extract_info(link, download=True)
                        break

                    except yt_dlp.utils.ExtractorError as e:
                        if "Sign in to confirm you're not a bot" in str(e):
                            retry_count += 1
                            if retry_count >= max_retries:
                                await m.edit('❌ Failed due to YouTube restrictions. Please try again later.')
                                return
                            time.sleep(5 * retry_count)
                        else:
                            raise e

                audio_file = ydl.prepare_filename(info_dict).replace(info_dict['ext'], 'mp3')

                if not os.path.exists(audio_file):
                    await m.edit('Failed to download the audio file.')
                    return

                try:
                    await m.edit("Processing and uploading...")
                except MessageNotModified:
                    pass

                rep = (f'🎧 Title : [{title[:35]}]({link})\n⏳ Duration : {duration}\n👀 Views : {views}\n\n'
                    f'📮 By: {message.from_user.mention()}')

                secmul, dur, dur_arr = 1, 0, duration.split(':')
                for i in range(len(dur_arr) - 1, -1, -1):
                    dur += (int(dur_arr[i]) * secmul)
                    secmul *= 60

                time.sleep(2)
                await message.reply_audio(
                    audio_file,
                    caption=rep,
                    quote=False,
                    title=title,
                    duration=dur,
                    performer=performer,
                    thumb=thumb_name
                )

                await m.delete()

        except Exception as e:
            error_msg = str(e)
            print(f"error in download/upload process: {error_msg}")
            if "Sign in to confirm you're not a bot" in error_msg:
                await m.edit('❌ Download failed due to rate limiting. Please try again later.')
            else:
                await m.edit('❌ Download failed. Please try again later.')

    except Exception as e:
        print(f"general error: {str(e)}")
        await m.edit("❎ An error occurred while processing your request.")

    finally:
        try:
            if 'audio_file' in locals() and os.path.exists(audio_file):
                os.remove(audio_file)
            if os.path.exists(thumb_name):
                os.remove(thumb_name)
        except Exception as e:
            print(f"cleanup error: {str(e)}")