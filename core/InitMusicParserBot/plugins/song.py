import os
import time
import logging
import requests
import yt_dlp  # type: ignore
from pyrogram import filters, Client, idle
from youtube_search import YoutubeSearch  # type: ignore
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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

    # yt-dlp options for downloading as MP3
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",  # Set bitrate for the MP3
        }],
        "outtmpl": "%(title)s.%(ext)s",  # Output file template
        "postprocessor_args": [
            "-metadata", "title=%(title)s",
            "-metadata", "artist=MusicDownloadv2bot"
        ],  # Add metadata to MP3
        "keepvideo": False  # Do not keep the WebM or M4A after conversion
    }

    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count > 0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
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
            print(e)
            await m.edit('Track not found.')
            return
    except Exception as e:
        await m.edit("❎ Found no results.\n\nEg.`Faded`")
        print(str(e))
        return

    await m.edit("`Uploading track...`")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # using yt-dlp for MP3 conversion
            info_dict = ydl.extract_info(link, download=True)  # Download the video/audio
            audio_file = ydl.prepare_filename(info_dict).replace(info_dict['ext'], 'mp3')  # Get the correct MP3 filename

        rep = (f'🎧 Title : [{title[:35]}]({link})\n⏳ Duration : `{duration}`\n👀 Views : `{views}`\n\n'
               f'📮 By: {message.from_user.mention()}')

        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60

        # Send the MP3 file to Telegram
        await message.reply_audio(audio_file, caption=rep, quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)

        await m.delete()
    except Exception as e:
        await m.edit('Failed\n\n`Try again...`')
        print(e)

    try:
        # Clean up files
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
