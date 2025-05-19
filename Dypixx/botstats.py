from pyrogram import *
from vars import ADMIN_ID
from Database.maindb import mdb
from Database.userdb import udb
from bot import bot
import time
from pyrogram.types import *

def get_readable_time(seconds: int) -> str:
    time_data = []
    for unit, div in [("d", 86400), ("h", 3600), ("m", 60), ("s", 1)]:
        value, seconds = divmod(seconds, div)
        if value > 0 or unit == "s":
            time_data.append(f"{int(value)}{unit}")
    return " ".join(time_data)

@Client.on_message(filters.command("stats") & filters.private)
async def stats_command(client, message):
    if message.from_user.id != ADMIN_ID:
        await message.delete()
        await message.reply_text("**🚫 You’re not authorized to use this command...**")
        return
    
    video_count = await mdb.get_video_count()
    total_users = await udb.get_all_users()
    active_today = await udb.get_active_users_today()
    bot_uptime = int(time.time() - bot.START_TIME)
    uptime = get_readable_time(bot_uptime)

    STATS = "**>🤖 Bot Statistics**\n\n"
    STATS += f"Total Users: {len(total_users)}\n"
    STATS += f"Active Users: {active_today}\n"
    STATS += f"Total Files in DB: {video_count}\n"
    STATS += f"BOT Uptime: {uptime}\n"

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Refresh ♻️", callback_data="refresh_stats")]]
    )
    await message.reply_text(STATS, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("refresh_stats"))
async def refresh_stats_callback(client, callback_query):
    video_count = await mdb.get_video_count()
    total_users = await udb.get_all_users()
    active_today = await udb.get_active_users_today()
    bot_uptime = int(time.time() - bot.START_TIME)
    uptime = get_readable_time(bot_uptime)

    STATS = "**>🤖 Bot Statistics (Updated)**\n\n"
    STATS += f"Total Users: {len(total_users)}\n"
    STATS += f"Active Users: {active_today}\n"
    STATS += f"Total Files in DB: {video_count}\n"
    STATS += f"BOT Uptime: {uptime}\n"

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Refresh ♻️", callback_data="refresh_stats")]]
    )

    await callback_query.message.edit_text(STATS, reply_markup=keyboard)
