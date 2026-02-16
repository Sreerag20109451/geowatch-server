import requests
import pathlib
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
import os

from typing import TypedDict




BASE_DIR = pathlib.Path(__file__).parent.parent
LOCAL_ENV = BASE_DIR / 'config' / '.env'

if LOCAL_ENV.exists():
    load_dotenv(dotenv_path=LOCAL_ENV)
else:
    load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

gemini_model = model = ChatGoogleGenerativeAI(
    model="gemini-3-pro-preview",
    api_key=gemini_api_key,
    temperature=1
)


