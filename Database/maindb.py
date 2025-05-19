from pymongo import MongoClient
from vars import *
from datetime import datetime, timedelta
import pytz

IST = pytz.timezone('Asia/Kolkata')

class Database:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client["adultzonebot"]
        self.video_collection = self.db["videos"]
        self.user_collection = self.db["users"]

    def save_video_id(self, video_id: int, duration: int):
        if not self.video_collection.find_one({"video_id": video_id}):
            self.video_collection.insert_one({"video_id": video_id, "duration": duration})

    def get_random_video_id(self, user_id: int):
        user_data = self.get_user(user_id)
        sent_videos_list = user_data.get("sent_videos", [])
        sent_video_ids = [entry["video_id"] for entry in sent_videos_list if "video_id" in entry]
        user_plan = user_data.get("plan", "free")
        duration_filter = {}
        if user_plan == "free":
            duration_filter = {"duration": {"$lt": 300}}
        elif user_plan == "prime":
            duration_filter = {"duration": {"$gte": 300}}
        available_videos = list(self.video_collection.find({"$and": [{"video_id": {"$nin": sent_video_ids}}, duration_filter]}))
        if not available_videos:
            return None
        import random
        random_video = random.choice(available_videos) 
        return random_video

    def get_user(self, user_id: int):
        user = self.user_collection.find_one({"_id": user_id})
        if not user:
            default_user = {
                "_id": user_id,
                "plan": "free",
                "daily_count": 0,
                "daily_limit": FREE_LIMIT,
                "last_request_date": datetime.now(IST),
                "sent_videos": [],
                "prime_expiry": None
            }
            self.user_collection.insert_one(default_user)
            return default_user
        return user

    def update_user(self, user_id: int, update_data: dict):
        self.user_collection.update_one({"_id": user_id}, {"$set": update_data})

    def increment_daily_count(self, user_id: int):
        user = self.get_user(user_id)
        today = datetime.now(IST)
        if user.get("last_request_date") is None or user.get("last_request_date").date() != today.date():
            self.update_user(user_id, {"daily_count": 1, "last_request_date": today})
            return 1
        else:
            new_count = user.get("daily_count", 0) + 1
            self.update_user(user_id, {"daily_count": new_count})
            return new_count

    def add_sent_video(self, user_id: int, video_id: int):
        sent_entry = {"video_id": video_id, "sent_at": datetime.now(IST)}
        self.user_collection.update_one({"_id": user_id}, {"$push": {"sent_videos": sent_entry}})

    def add_prime_user(self, user_id: int, duration_str: str):
        parts = duration_str.split()
        if len(parts) != 2 or parts[0] not in ("-m", "-d"):
            return False
        try:
            amount = int(parts[1])
            unit = parts[0][-1]
            expiry_date = datetime.now(IST)
            if unit == 'd':
                expiry_date += timedelta(days=amount)
            elif unit == 'm':
                expiry_date += timedelta(days=amount * 30)
        except ValueError:
            return False
        if amount <= 0:
            return False
        expiry_date = expiry_date.replace(hour=23, minute=59, second=59, microsecond=0)
        self.update_user(user_id, {
            "plan": "prime",
            "daily_limit": 50,
            "prime_expiry": expiry_date
        })

    def remove_sent_video(self, user_id: int, video_id: int):
        self.user_collection.update_one(
            {"_id": user_id},
            {"$pull": {"sent_videos": {"video_id": video_id}}}
        )

    def delete_all_videos(self):
        self.video_collection.delete_many({})

    def delete_video_by_id(self, video_id: int):
        self.video_collection.delete_one({"video_id": video_id})
        return True

    def check_prime_expiry(self, user_id: int):
        user = self.get_user(user_id)
        expiry_date = user.get("prime_expiry")
        if expiry_date and expiry_date.tzinfo is None:
            expiry_date = IST.localize(expiry_date)
        if user.get("plan") == "prime" and expiry_date and expiry_date < datetime.now(IST):
            self.update_user(user_id, {
                "plan": "free",
                "daily_limit": FREE_LIMIT,
                "prime_expiry": None
            })
            return False
        elif user.get("plan") == "prime" and expiry_date:return True
        else:return False

    def get_video_count(self):
        return self.video_collection.count_documents({})

    def remove_prime_user(self, user_id: int):
        self.update_user(user_id, {
            "plan": "free",
            "daily_limit": FREE_LIMIT,
            "prime_expiry": None
        })

mdb = Database()