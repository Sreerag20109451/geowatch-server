import os
import pathlib
from dotenv import load_dotenv

from api.snow import snowrouter

from fastapi import FastAPI

from earthengine.auth import  EarthEngineAuth

app = FastAPI()



env_path = pathlib.Path(__file__).parent / "config"/".env"
key_path = pathlib.Path(__file__).parent / "key.json"
load_dotenv(dotenv_path=env_path)

service_accnt = os.getenv("SERVICE_ACCOUNT")



"""
Initialize Google Earth Engine
"""
earthengineAuth = EarthEngineAuth()
earthengineAuth.initialize_earth_engine(service_accnt,key_path)
app.include_router(snowrouter)



@app.get("/")
def read_root():
    return {"Hello": "World"}

