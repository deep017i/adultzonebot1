from pyrogram import Client, filters
from vars import ADMIN_ID, ADMIN_USERNAME, FREE_LIMIT, PRIME_LIMIT, IS_FSUB
from Database.maindb import mdb
from pyrogram.types import *
from Database.userdb import udb
from Dypixx.Extraa.fsub import get_fsub

PRIME_TXT = f"""<b>🔥 Upgrade Your Experience — Buy Now! 🔥

<blockquote>Free Users:</blockquote>

• {FREE_LIMIT} files per day
• Videos up to 5 minutes only
• No premium content access

<blockquote>Premium Users:</blockquote>

• {PRIME_LIMIT} files daily
• Unlimited video length
• Access to premium content

<blockquote>Affordable Subscription Plans:</blockquote>

» 1 Week — ₹10
» 15 Days — ₹18
» 1 Month — ₹50

💬 Contact @{ADMIN_USERNAME} to upgrade your plan</b>"""

@Client.on_message(filters.command("plans") & filters.private)
async def remove_prime(client, message):
    if await udb.is_user_banned(message.from_user.id):
        await message.reply("**🚫 You are banned from using this bot**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Support 🧑‍💻", url=f"https://t.me/{ADMIN_USERNAME}")]]))
        return
    if IS_FSUB and not await get_fsub(client, message):return
    await message.reply_text(PRIME_TXT, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔓 Close", callback_data="https://telegram.me/DypixxTech")]]))

@Client.on_message(filters.command("myplan") & filters.private)
async def my_plan(client, message):
    if await udb.is_user_banned(message.from_user.id):
        await message.reply("**🚫 You are banned from using this bot**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Support 🧑‍💻", url=f"https://t.me/{ADMIN_USERNAME}")]]))
        return
    if IS_FSUB and not await get_fsub(client, message):return
    user_id = message.from_user.id
    user = mdb.get_user(user_id)
    mdb.check_prime_expiry(user_id)
    user = mdb.get_user(user_id)
    plan = user.get("plan", "free")
    daily_count = user.get("daily_count", 0)
    daily_limit = user.get("daily_limit", FREE_LIMIT)
    prime_expiry = user.get("prime_expiry")
    status_text = "**>Plan Details**\n\n"
    status_text += f"**User: {message.from_user.mention}**\n"
    status_text += f"**User id: {user_id}**\n"
    status_text += f"**User Plan: {plan.capitalize()}**\n"
    status_text += f"**Daily Limit: {daily_limit}**\n"
    status_text += f"**Today used: {daily_count}/{daily_limit}**\n"
    status_text += f"**Total Remaining: {daily_limit - daily_count}**\n\n"
    if plan == "prime" and prime_expiry:
        status_text += f"**Expiry Date: {prime_expiry.strftime('%d:%m:%Y')}**"
    if daily_count >= daily_limit and plan == "free":
         status_text += "\n**>⚠️ You’ve reached your daily limit. Consider upgrading to the Prime Plan to enjoy more limits!**"

    await message.reply_text(status_text)

@Client.on_message(filters.command("add") & filters.private)
async def add_prime(client, message):
    if message.from_user.id != ADMIN_ID:
        message.delete()
        await message.reply_text("**🚫 You’re not authorized to use this command...**")
        return
    
    if len(message.command) != 4 or message.command[2] not in ("-m", "-d"):
        await message.reply_text("**Usage: /add <user_id> -m / -d <duration>\n\n-m = month\n-d = day**")
        return
    
    i = int(message.command[1])
    duration_str = f"{message.command[2]} {message.command[3]}"
    mdb.add_prime_user(i, duration_str)
    await message.reply_text(f"**✅ User {i} has been successfully added to the Prime Plan for {duration_str}.**")
    await client.send_message(chat_id=i, text="**🎉 Hey!\n\nYou’ve been upgraded to a Premier user.\nCheck your plan by using /myplan**")

@Client.on_message(filters.command("removeprime") & filters.private)
async def remove_prime(client, message):
    if message.from_user.id != ADMIN_ID:
        message.delete()
        await message.reply_text("**🚫 You’re not authorized to use this command...**")
        return
    if len(message.command) != 2:
        await message.reply_text("**Usage: /remove <user_id>**")
        return
    
    k = int(message.command[1])
    mdb.remove_prime_user(k)
    await message.reply_text(f"**User {k} has been removed from the Prime Plan**")
    await client.send_message(chat_id=k, text="**👋 Hey!\n\nYour premium access has been removed by the admin.\nIf you have any questions, feel free to reach out!**",
                              reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Admin Support 🧑‍💻", url=f"https://telegram.me/{ADMIN_USERNAME}")]]))