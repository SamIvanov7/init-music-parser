# # core/uploader.py
# import asyncio
# import time
# from pyrogram.errors import PeerIdInvalid, ChatWriteForbidden

# class Uploader:
#     def __init__(self, track_queue, channel_id):
#         # Ensure channel_id is properly formatted
#         if channel_id.startswith('@'):
#             self.channel_id = channel_id  # Username of the channel
#         else:
#             try:
#                 self.channel_id = int(channel_id)
#             except ValueError:
#                 raise ValueError("Invalid CHANNEL_ID. It should be an integer ID or a channel username starting with '@'.")

#         self.track_queue = track_queue

#     async def send_tracks_to_channel(self, bot):
#         while True:
#             # Get track info from the queue in a non-blocking way
#             track_info = await asyncio.get_event_loop().run_in_executor(None, self.track_queue.get)
#             if track_info is None:
#                 break

#             try:
#                 await asyncio.sleep(10)  # Sleep for 10 seconds before sending each track
#                 file_path = track_info["file_path"]
#                 track_name = track_info["track_name"]

#                 caption = f"🎵 Now Playing: {track_name}"
#                 print(f"Attempting to send '{track_name}' to channel: {self.channel_id}")

#                 await bot.send_audio(chat_id=self.channel_id, audio=file_path, caption=caption)

#                 print(f"Successfully sent '{track_name}' to the channel.")
#             except PeerIdInvalid:
#                 print(f"Failed to send '{track_name}' to the channel. Error: PeerIdInvalid - The bot may not have access to the channel. Ensure the bot is added to the channel and has the necessary permissions.")
#                 # Optionally, you can break the loop here if the bot cannot access the channel
#                 break
#             except ChatWriteForbidden:
#                 print(f"Failed to send '{track_name}' to the channel. Error: ChatWriteForbidden - The bot doesn't have permission to send messages to this chat.")
#                 # Optionally, you can break the loop here if the bot cannot write to the channel
#                 break
#             except Exception as e:
#                 print(f"Failed to send '{track_name}' to the channel. Error: {e}")
#             finally:
#                 self.track_queue.task_done()

#     def run(self, bot):
#         # Schedule the coroutine in the bot's event loop
#         bot.loop.create_task(self.send_tracks_to_channel(bot))
