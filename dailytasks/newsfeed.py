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
        self.gemini_api_key = os.getenv("AIzaSyBebN0FFLJ-WC7fvIVd_QZoYqBPxjf5FaQ")
    
    async def get_daily_news_from_redis(self):
        if not self.redis_url or not self.token:
            print("Missing Upstash credentials!")
            return []

        redis = Redis(url=self.redis_url, token=self.token)
        
        newsdata = await redis.get('daily_news_feed')
        
        if newsdata is None:
            return []
        return json.loads(newsdata)
        
            
        
        return newsdata
    
    def delete_previous_news_from_redis(self):
           if not self.redis_url or not self.token:
            print("Missing Upstash credentials!")
            return []

           redis = Redis(url=self.redis_url, token=self.token)
           if(redis.exists("daily_news_feed")):
              redis.delete("daily_news_feed")
           else:
               pass
    
     