import os
import json
import pathlib
from dotenv import load_dotenv
from upstash_redis.asyncio import Redis

from dailytasks.newsfeedtools import get_newsData

# Load environment variables once at the module level
# This looks for .env in /config, but won't break if it's missing (like in prod)
BASE_DIR = pathlib.Path(__file__).parent.parent
LOCAL_ENV = BASE_DIR / 'config' / '.env'

if LOCAL_ENV.exists():
    load_dotenv(dotenv_path=LOCAL_ENV)
else:
    load_dotenv() 

class NewsFeed:
    def __init__(self):
        # Simply pull from the environment
        self.redis_url = os.getenv("UPSTASH_REDIS_REST_URL")
        self.token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
        self.gemini_api_key = os.getenv("AIzaSyBebN0FFLJ-WC7fvIVd_QZoYqBPxjf5FaQ")

    async def save_to_redis(newsdata):
        if self.redis_url is None:
            print("no redis url")
            return None
        else:
            redis = Redis(url=self.redis_url, token=self.token)
            await redis.set('daily_news_feed', json.dumps(newsdata))
        pass


    async def get_daily_news_from_redis(self):
        if not self.redis_url or not self.token:
            print("Missing Upstash credentials!")
            return []

        redis = Redis(url=self.redis_url, token=self.token)
        
        data = await redis.get('daily_news_feed')
        if data is None:
            raise  Exception("no data")
        newsdata = json.loads(data)
        if(newsdata["create_dtm"] > datetime.datetime.now()- datetime.timedelta(days=1)):
            newsdata = await get_newsData()
            await self.save_to_redis(newsdata)
        if newsdata is None:
            return []
        return json.loads(newsdata)
        

     