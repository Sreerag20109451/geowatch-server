import os
import json
import pathlib
from dotenv import load_dotenv
from upstash_redis.asyncio import Redis
import  datetime

from dailytasks.newsfeedtools import get_newsData

BASE_DIR = pathlib.Path(__file__).parent.parent
LOCAL_ENV = BASE_DIR / 'config' / '.env'

if LOCAL_ENV.exists():
    load_dotenv(dotenv_path=LOCAL_ENV)
else:
    load_dotenv() 

class NewsFeed:
    def __init__(self):
        self.redis_url = os.getenv("UPSTASH_REDIS_REST_URL")
        self.token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
        self.gemini_api_key = os.getenv("AIzaSyBebN0FFLJ-WC7fvIVd_QZoYqBPxjf5FaQ")

    async def save_to_redis(self,newsdata):
        if self.redis_url is None:
            print("no redis url")
            return None
        else:
            redis = Redis(url=self.redis_url, token=self.token)
            await redis.set('daily_news_feed', json.dumps(newsdata))
        pass

    async def get_daily_news_from_redis(self):
        # ... (credentials check) ...

        redis = Redis(url=self.redis_url, token=self.token)
        raw_data = await redis.get('daily_news_feed')

        # 1. Guard against None (Cache Miss)
        if raw_data is None:
            print("Cache miss: fetching fresh data")
            newsdata = await get_newsData()
            await self.save_to_redis(newsdata)
            return newsdata

        # 2. IMPORTANT: Parse the string from Redis into a Python Dictionary
        data = json.loads(raw_data)

        # 3. Now you can safely access the string key "create_dtm"
        last_created = datetime.datetime.fromisoformat(data["create_dtm"])

        if last_created < (datetime.datetime.now() - datetime.timedelta(days=1)):
            print("Cache expired: fetching fresh data")
            data = await get_newsData()
            await self.save_to_redis(data)

        return data
        

     