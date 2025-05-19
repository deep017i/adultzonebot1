from pyrogram import Client, filters
from pyrogram.types import *
import datetime, pytz
from vars import ADMIN_USERNAME

@Client.on_callback_query()
async def cb_handler(client, q : CallbackQuery):
    data = q.data

    if data == "disclaimer_bot":
        await q.edit_message_text(
            text = f"**>Disclaimer – 18+ Content 🔞**\n\n"
            "**This bot is intended strictly for adults aged 18 years or older. By using this bot, you confirm that you are of legal age in your country to view explicit adult content.**\n\n"
            "**Important:**\n"
            "**» This bot provides only consensual, legal adult videos including kiss and sex scenes.**\n"
            "**» All content is for personal entertainment only and should not be redistributed, shared with minors, or used for any illegal purpose.**\n"
            "**» If you are under 18 or find such content offensive, please do not use this bot.**\n"
            "**» The creators and operators of this bot do not take responsibility for any misuse or violation of local laws by users.**\n\n"
            "**Use responsibly and respect all applicable laws and guidelines.**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❓ Help", url="https://telegram.me/DypixxTech"),
                 InlineKeyboardButton("🤖 About", url="https://telegram.me/DypixxTech")],
                [InlineKeyboardButton("🏠 Home", url="https://telegram.me/DypixxTech")]]),
            disable_web_page_preview=True
        )

    elif data == "terms_bot":
        await q.edit_message_text(
            text=f"**📜 Terms and Conditions 📜**\n\n"
            "**» By using this bot, you agree that you are solely responsible for your actions.**\n"
            "**» The bot owner and developers hold no liability for any consequences arising from your use of this content.**\n"
            "**» You agree to comply with all local laws regarding adult content.**\n"
            "**» Misuse of this bot or sharing content with unauthorized persons is strictly prohibited.**\n\n"
            "**Please use this bot responsibly and at your own risk.**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❓ Help", url="https://telegram.me/DypixxTech"),
                 InlineKeyboardButton("🤖 About", url="https://telegram.me/DypixxTech")],
                [InlineKeyboardButton("🏠 Home", url="https://telegram.me/DypixxTech")]]),
            disable_web_page_preview=True
        )

    elif data == "help":
        await q.edit_message_text(
            text = f"**>How to Use the Bot ❓**\n\n"
            "**Use the following commands to interact with the bot:**\n\n"
            "**/getvideo - To get an 18+ video**\n"
            "**/myplan - Check your current daily limit and plan**\n"
            "**/plans - View all available premium plans**\n\n"
            "**⚠️ Note: This bot is for 18+ users only. Use it at your own responsibility.**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Home", url="https://telegram.me/DypixxTech"),
                 InlineKeyboardButton("🤖 About", url="https://telegram.me/DypixxTech")]]),
            disable_web_page_preview=True
        )

    elif data == "about":
        b = await client.get_me()
        await q.edit_message_text(
            text = f"**>📄 Bot Info 📄**\n\n" \
             "**About Bot**\n" \
             f"**» Bot Name - <a href='tg://user?id={b.id}'>{b.first_name}</a>**\n" \
             "**» Developer - <a href='https://t.me/Dypixx'>Dypixx</a>**\n" \
             "**» Updates - <a href='https://t.me/adulthub4all'>AdultHub4All</a>**\n\n" \
             "**>⚙️ Bot Setup Details**\n" \
             "**» Version - V0.1**\n" \
             "**» Language - <a href='https://www.python.org/download/releases/3.0/'>Python3</a>**\n" \
             "**» Library - <a href='https://docs.pyrogram.org/'>Pyrogram</a>**\n" \
             "**» Database - <a href='https://www.mongodb.com/'>MongoDB</a>**\n" \
             "**» Hosting - VPS**\n\n" \
             f"**⚠️ If you facing any error, Please Contact - <a href='https://t.me/{ADMIN_USERNAME}'>Support</a>**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Home", url="https://telegram.me/DypixxTech"),
                 InlineKeyboardButton("❓ Help", url="https://telegram.me/DypixxTech")]]),
            disable_web_page_preview=True
        )

    elif data == "home":
        full_name = q.from_user.first_name + (" " + q.from_user.last_name if q.from_user.last_name else "")
        h = datetime.now(pytz.timezone('Asia/Kolkata')).hour
        wish = "Good Morning" if 4 <= h < 12 else "Good Afternoon" if 12 <= h < 17 else "Good Evening" if 17 <= h < 20 else "Good Night"
        await q.edit_message_text(
            text=f"**👋 {full_name}, {wish}\n\nThis bot may contain 18+ content.\nPlease access it at your own risk.\nThe material may include explicit or graphic content that is not suitable for minors.\n\n🔞 If you’re under 18, please do not use this bot.**",
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("⚠️ Disclaimer", callback_data="disclaimer_bot"),
                  InlineKeyboardButton("📜 Terms", callback_data="terms_bot")],
                  [InlineKeyboardButton("❓ Help", callback_data="help"),
                   InlineKeyboardButton("🤖 About", callback_data="about")],
                   [InlineKeyboardButton("🔓 Close", callback_data="close")]])
            )

    elif data == "close":
        await q.answer("Thanks for closing ❤️", show_alert=True)
        await q.message.delete()
    