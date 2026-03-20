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
        if self.redis_url is None:
            print("No redis url configured, fetching fresh data")
            return get_newsData()

        redis = Redis(url=self.redis_url, token=self.token)
        news_data = await redis.get('daily_news_feed')
        print(f"Raw data from redis: {type(news_data)}")

        data = None
        if news_data:
            try:
                if isinstance(news_data, str):
                    data = json.loads(news_data)
                else:
                    data = news_data # Already a dict or other type
            except json.JSONDecodeError:
                print("Failed to parse redis data, fetching fresh")
                data = None

        if data:
            last_created = datetime.datetime.fromisoformat(data["create_dtm"])
            if last_created > (datetime.datetime.now() - datetime.timedelta(days=1)):
                return data
            print("Cache expired: fetching fresh data")

        # Fetch fresh data if cache miss or expired
        data = get_newsData()
        await self.save_to_redis(data)
        return data
        

     