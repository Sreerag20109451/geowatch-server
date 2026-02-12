from dotenv import load_dotenv
import os 
import json
from upstash_redis import Redis

class NewsFeed:

    def __init__(self):
        self.ENV_PATH = pathlib.Path(__file__).parent.parent / 'config' /'.env'
        load_dotenv(dotenv_path=self.ENV_PATH)
        self.redis_url = os.getenv("REDIS_URL")
        self.token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
    
    async def get_daily_news_from_redis():
        redis = Redis(url=self.redis_url, token=self.token)
        newsdata = redis.get('daily_news_feed')
        news_data_json = json.loads(newsdata)
        return news_data_json

