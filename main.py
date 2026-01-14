import json
import os
import pathlib
from dotenv import load_dotenv
import ee

from api.snow import snowrouter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from earthengine.auth import EarthEngineAuth

app = FastAPI(redirect_slashes=False)

#  Define Paths
BASE_DIR = pathlib.Path(__file__).parent.resolve()
ENV_PATH = BASE_DIR / "config" / ".env"
LOCAL_KEY = BASE_DIR / "key.json"         
RAILWAY_MOUNT = "/services/key.json"      

if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
    print(f"Loaded environment from {ENV_PATH}")
else:
    print("file found; relying on system environment variables")

# Service Credential Logic
service_accnt = os.getenv("SERVICE_ACCOUNT")
key_file_path = None

if LOCAL_KEY.exists():
    key_file_path = str(LOCAL_KEY)
    print(f"Found local key.json at {key_file_path}")

elif os.path.exists(RAILWAY_MOUNT):
    key_file_path = RAILWAY_MOUNT
    print(f"Using Railway Volume at {key_file_path}")

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

# Middlewares 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(snowrouter)

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