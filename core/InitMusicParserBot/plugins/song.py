import os
import time
import logging
import requests
import yt_dlp  # type: ignore
from pyrogram import filters, Client, idle
from youtube_search import YoutubeSearch  # type: ignore
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import MessageNotModified

username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")

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

@Client.on_message(filters.text) # type: ignore
async def song_search(client, message):
    query = message.text
    print(query)
    m = await message.reply('Searching...') # type: ignore

    # enhanced yt-dlp options with better error handling and rate limiting
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
        "cookiefile": "data/cookies.txt",
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": False,
        "retries": 5,
        "fragment_retries": 5,
        "skip_download": False,
        "sleep_interval": 5,
        "max_sleep_interval": 10,
        "sleep_interval_requests": 1,
        "max_sleep_interval_requests": 3
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

            # download thumbnail
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(f"error in parsing search results: {str(e)}")
            await m.edit('Failed to process track information.')
            return

        # update status message
        try:
            await m.edit("`Downloading track...`")
        except MessageNotModified:
            pass

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # first try to extract info without downloading
                try:
                    info_dict = ydl.extract_info(link, download=False)
                    time.sleep(2)
                    if info_dict.get('is_live'):
                        await m.edit('❌ Cannot download live streams.')
                        return
                except Exception as e:
                    print(f"info extraction error: {str(e)}")
                    if "Sign in to confirm your age" in str(e):
                        await m.edit('❌ Age-restricted content cannot be downloaded.')
                        return
                    elif "Sign in to confirm you're not a bot" in str(e):
                        # retry with additional delay
                        time.sleep(5)

                # proceed with download
                info_dict = ydl.extract_info(link, download=True)
                time.sleep(2)
                audio_file = ydl.prepare_filename(info_dict).replace(info_dict['ext'], 'mp3')

                if not os.path.exists(audio_file):
                    await m.edit('Failed to download the audio file.')
                    return

                # update status message
                try:
                    await m.edit("`Processing and uploading...`")
                except MessageNotModified:
                    pass

                # prepare caption
                rep = (f'🎧 Title : [{title[:35]}]({link})\n⏳ Duration : `{duration}`\n👀 Views : `{views}`\n\n'
                    f'📮 By: {message.from_user.mention()}')

                # calculate duration in seconds
                secmul, dur, dur_arr = 1, 0, duration.split(':')
                for i in range(len(dur_arr) - 1, -1, -1):
                    dur += (int(dur_arr[i]) * secmul)
                    secmul *= 60

                # send the audio file
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
        # cleanup files
        try:
            if 'audio_file' in locals() and os.path.exists(audio_file):
                os.remove(audio_file)
            if os.path.exists(thumb_name):
                os.remove(thumb_name)
        except Exception as e:
            print(f"cleanup error: {str(e)}")
