from pyrogram.client import Client
from vars import *
import time

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Adultzonebot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=200,
            plugins={"root": "Dypixx"},
            sleep_threshold=15,
        )
        self.START_TIME = None

    async def start(self):
        self.START_TIME = time.time()
        await super().start()
        me = await self.get_me()
        print("""
██████  ██    ██ ██████  ██ ██   ██ ██   ██     ████████ ███████  ██████ ██   ██ 
██   ██  ██  ██  ██   ██ ██  ██ ██   ██ ██         ██    ██      ██      ██   ██ 
██   ██   ████   ██████  ██   ███     ███          ██    █████   ██      ███████ 
██   ██    ██    ██      ██  ██ ██   ██ ██         ██    ██      ██      ██   ██ 
██████     ██    ██      ██ ██   ██ ██   ██        ██    ███████  ██████ ██   ██""")
        print(f"\n{me.first_name} is started...")

    async def stop(self, *args):
        await super().stop()
        me = await self.get_me()
        print(f"{me.first_name} is stopped...")

bot = Bot()
bot.run()