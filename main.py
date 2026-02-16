import json
import os
import redis
import pathlib
from dotenv import load_dotenv
import ee
import sys

from celery import Celery
from celery.schedules import schedule  
from redbeat import RedBeatSchedulerEntry
from api.snow import snowrouter
from api.newsfeed import newsfeedrouter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from earthengine.auth import EarthEngineAuth
from dailytasks.newsfeed import NewsFeed


newsfeedtasks = NewsFeed()

app = FastAPI(redirect_slashes=False)

#  Define Paths
BASE_DIR = pathlib.Path(__file__).parent.resolve()
ENV_PATH = BASE_DIR / "config" / ".env"
LOCAL_KEY = BASE_DIR / "key.json"         
RAILWAY_MOUNT = "/services/key.json"      

if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
    print(f"Loaded environment from ")
else:
    print("file found; relying on system environment variables")

# Service Credential Logic
service_accnt = os.getenv("SERVICE_ACCOUNT")
key_file_path = None





if LOCAL_KEY.exists():
    key_file_path = str(LOCAL_KEY)
    print(f"Found local key.json at")

elif os.path.exists(RAILWAY_MOUNT):
    key_file_path = RAILWAY_MOUNT
    print(f"Using Railway Volume at ")

else:
    key_json_str = os.environ.get("KEY_JSON")
    if key_json_str:
        key_file_path = str(BASE_DIR / "temp_key.json")
        with open(key_file_path, "w") as f:
            f.write(key_json_str)
        print("☁️ Using KEY_JSON environment variable")
    else:
        raise RuntimeError("No key.json found locally OR in /services!")

# Initialize Earth Engine
earthengineAuth = EarthEngineAuth()
earthengineAuth.initialize_earth_engine(service_accnt, key_file_path)


# Initialize celery

celery_app =  Celery('task-scheduler', broker=os.getenv("REDIS_URL"))
reddis_instance = redis.from_url(os.getenv("REDIS_URL"))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
@celery_app.task
def get_daily_news_feed():
    from dailytasks.newsfeedtools import get_newsData
    daily_newsdata = get_newsData()
    reddis_instance.set("daily_news_feed", json.dumps(daily_newsdata))
    return "News feed updated in Redis"

interval = schedule(run_every=6000)  
daily_news_task_path = f"{get_daily_news_feed.__module__}.{get_daily_news_feed.__name__}"
entry = RedBeatSchedulerEntry('get_daily_news_data', daily_news_task_path , interval, args=[], app=celery_app)
entry.save()

# Middlewares 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(snowrouter)
app.include_router(newsfeedrouter)



@celery_app.task
def get_news_data():
    from dailytasks.newsfeed import get_newsData
    news_data = get_news_data()
    return news_data

@app.get("/")
def read_key_info():
    return {"status": "authenticated", "key_source": key_file_path}

@app.get("/testee")
def test_ee():
    try:
        img = ee.Image("MODIS/006/MOD10A1/2020_03_01").select("NDSI_Snow_Cover")
        mapid = img.getMapId({"min": 0, "max": 100, "palette": ["red","yellow","green","blue"]})
        return {"mapid": mapid}
    except Exception as e:
        return {"error": str(e)}

