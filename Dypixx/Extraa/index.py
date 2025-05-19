from pyrogram import Client, filters
from vars import DATABASE_CHANNEL_ID
from Database.maindb import mdb

@Client.on_message(filters.chat(DATABASE_CHANNEL_ID) & filters.video)
async def save_video(client, message):
    video_id = message.id
    video_duration = message.video.duration
    mdb.save_video_id(video_id, video_duration)
    print(f"Video saved successfully.\nVideo ID: {video_id}\nDuration: {video_duration} seconds")