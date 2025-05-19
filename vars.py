import os
from typing import List

API_ID = int(os.getenv("API_ID", "27339145"))
API_HASH = os.getenv("API_HASH", "e620f86919c34496729285dd2a6d35e6")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7579290702:AAHqYG6mrEN8Gnim6txjyAMo7GM8ynzl2SE")
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://starcinebot:mkooaa@werdeveloper.vxfam.mongodb.net/?retryWrites=true&w=majority&appName=werdeveloper")
DATABASE_CHANNEL_ID = int(os.getenv("DATABASE_CHANNEL_ID", "-1002474668306"))
ADMIN_ID = int(os.getenv("ADMIN_ID", "7025449786"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "dypixx")
FREE_LIMIT = int(os.getenv("FREE_LIMIT", "10"))
PRIME_LIMIT = int(os.getenv("PRIME_LIMIT", "40"))
IS_FSUB = bool(os.environ.get("FSUB", True))
AUTH_CHANNELS = list(map(int, os.environ.get("AUTH_CHANNEL", "-1002528152399").split()))
