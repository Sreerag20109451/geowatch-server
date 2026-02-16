import requests
import pathlib
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain.tools import tool
import os

from agenticfeatures.newsfeed import NewsFeed
from typing import TypedDict


class SummaryTuple(TypedDict):
    title: str
    content: str
    source:str


BASE_DIR = pathlib.Path(__file__).parent.parent
LOCAL_ENV = BASE_DIR / 'config' / '.env'

if LOCAL_ENV.exists():
    load_dotenv(dotenv_path=LOCAL_ENV)
else:
    load_dotenv() 

class LLMTasks:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.newsfeedclass= NewsFeed()
        self.google_model = GoogleGenerativeAI(model='gemini-2.5-flash', google_api_key=self.api_key)

    @tool('get-news-tuples', description ='Get the source, tiltle and description from newsdata')
    async def create_summarization_tuples(self):

        tuples_for_summarisation = []
        newsfeed = await self.newsfeedclass.get_daily_news_from_redis()
        for news in newsfeed:
            tuple = SummaryTuple()
            tuple['title'] = news["title"]
            tuple["content"] = news["content"]
            tuple["source"] = news["content"]
            tuples_for_summarisation.append(tuple)
        
        return SummaryTuple
        


    
