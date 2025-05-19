from pyrogram import Client, filters
from pyrogram.types import *
from vars import *
from Database.maindb import mdb
from Database.userdb import udb
from datetime import datetime
import pytz
from Dypixx.Extraa.fsub import get_fsub

@Client.on_message(filters.command("getvideo") & filters.private)
async def send_video(client, message):
    if await udb.is_user_banned(message.from_user.id):
        await message.reply("**🚫 You are banned from using this bot**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Support 🧑‍💻", url=f"https://t.me/{ADMIN_USERNAME}")]]))
        return
    if IS_FSUB and not await get_fsub(client, message):return
    user_id = message.from_user.id
    user = mdb.get_user(user_id)
    mdb.check_prime_expiry(user_id)
    user = mdb.get_user(user_id)
    daily_count = user.get("daily_count", 0)
    daily_limit = user.get("daily_limit", FREE_LIMIT)
    plan = user.get("plan", "free")
    if daily_count < daily_limit:
        video_data = mdb.get_random_video_id(user_id)

        if video_data is not None:
            try:
                video_id = video_data["video_id"]
                caption_text = "Here is your video!"
                await client.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=DATABASE_CHANNEL_ID,
                    message_id=video_id,
                    caption=caption_text)
                await mdb.increment_daily_count(user_id)
                await mdb.add_sent_video(user_id, video_id)
                await udb.update_user_activity(user_id)
            except Exception as e:
                print(f"Error sending video {video_id}: {e}")
                await message.reply_text("**⚠️ An error occurred on the backend.\n\nPlease try again by sending the /getvideo command.**")
                mdb.remove_sent_video(user_id, video_id)
        else:
            await message.reply_text("**✅ You’ve watched all available videos!\n\n>Please check back in a few hours or days for new uploads.**")
    else:
        await message.reply_text(f"**🚫 You've reached your daily limit of {daily_limit} videos.**")


@Client.on_message(filters.command("deleteall") & filters.private)
async def delete_all_videos_command(client, message):
    if message.from_user.id != ADMIN_ID:
        await message.delete()
        await message.reply_text("**🚫 You’re not authorized to use this command...**")
        return
    mdb.delete_all_videos()
    await message.reply_text("**⚠️ All videos have been deleted from the database**")

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    if await udb.is_user_banned(message.from_user.id):
        await message.reply("**🚫 You are banned from using this bot**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Support 🧑‍💻", url=f"https://t.me/{ADMIN_USERNAME}")]]))
        return
    if IS_FSUB and not await get_fsub(client, message):return
    if await udb.get_user(message.from_user.id) is None:
        await udb.addUser(message.from_user.id, message.from_user.first_name)
    full_name = message.from_user.first_name + (" " + message.from_user.last_name if message.from_user.last_name else "")
    h = datetime.now(pytz.timezone('Asia/Kolkata')).hour
    wish = "Good Morning" if 4 <= h < 12 else "Good Afternoon" if 12 <= h < 17 else "Good Evening" if 17 <= h < 20 else "Good Night"
    await message.reply_text(f"**👋 {full_name}, {wish}\n\nThis bot may contain 18+ content.\nPlease access it at your own risk.\nThe material may include explicit or graphic content that is not suitable for minors.\n\n🔞 If you’re under 18, please do not use this bot.**",
                             reply_markup = InlineKeyboardMarkup(
                                 [[InlineKeyboardButton("⚠️ Disclaimer", callback_data="disclaimer_bot"),
                                   InlineKeyboardButton("📜 Terms", callback_data="terms_bot")],
                                   [InlineKeyboardButton("❓ Help", callback_data="help"),
                                    InlineKeyboardButton("🤖 About", callback_data="about")],
                                    [InlineKeyboardButton("🔓 Close", callback_data="close")]])
                            )