import os
import json
import pathlib
from dotenv import load_dotenv
from upstash_redis.asyncio import Redis

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
    
    async def get_daily_news_from_redis(self):
        if not self.redis_url or not self.token:
            print("Missing Upstash credentials!")
            return []

        redis = Redis(url=self.redis_url, token=self.token)
        
        newsdata = await redis.get('daily_news_feed')
        
        if newsdata is None:
            return []
            
        # Upstash-redis usually returns a dict if it was stored as JSON, 
        # but if it's a string, we load it.
        if isinstance(newsdata, str):
            return json.loads(newsdata)
        
        return newsdata