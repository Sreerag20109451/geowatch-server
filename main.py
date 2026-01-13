import json
import os
import pathlib

from api.snow import snowrouter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from earthengine.auth import EarthEngineAuth

app = FastAPI()

# Load env variables from Railway or .env
env_path = pathlib.Path(__file__).parent / "config" / ".env"
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=env_path)

service_accnt = os.getenv("SERVICE_ACCOUNT")
key_json_str = os.environ.get("KEY_JSON")

if not key_json_str:
    raise RuntimeError("KEY_JSON environment variable not found! Did you set it in Railway for this environment?")

key_json_dict = json.loads(key_json_str)

# Ensure /services exists (Railway volume mount)
volume_path = "/services"
os.makedirs(volume_path, exist_ok=True)

# Write key.json into /services
key_file_path = os.path.join(volume_path, "key.json")
with open(key_file_path, "w") as f:
    json.dump(key_json_dict, f, indent=2)

# Initialize Google Earth Engine using /services/key.json
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

# Routers
app.include_router(snowrouter)

@app.get("/")
def read_root():
    return {"message": "Server is running, key.json written to /services!"}
