from langchain.agents import create_agent

from agenticfeatures.climatecolumns.model import model
from agenticfeatures.climatecolumns.tools import  search_web, extract_pages
from typing_extensions import TypedDict, Annotated

import os
import pathlib
from dotenv import load_dotenv
from upstash_redis.asyncio import Redis


BASE_DIR = pathlib.Path(__file__).parent.parent.parent.resolve()
LOCAL_ENV = BASE_DIR / 'config' / '.env'

if LOCAL_ENV.exists():
    load_dotenv(dotenv_path=LOCAL_ENV)
else:
    raise FileNotFoundError()
redis_url = os.getenv('GEMINI_API_KEY')



class NewsDict(TypedDict):
    title: str
    focus: str

class FocusArea(TypedDict):
    area: str
    documents: list[str]
    newses: list[NewsDict]



class FocusAreaList(TypedDict):
    focus_areas: list[FocusArea]

class NewsList(TypedDict):
    newses : list[str]

def generate_newses_for_focus_area(focus_area: FocusArea) -> list[str]:

    writing_assistant_agent = create_agent(
        model=model,
        tools=[search_web, extract_pages],
        system_prompt="""You help write articles based on focus areas.""",
        response_format=NewsList
    )

    prompt = f"""
You must:

1. Generate a precise scientific search query about {focus_area["focus_area"]["area"]} and climate change.
2. Call search_web with the query.
3. Extract URLs from the results.
4. Call extract_pages using EXACTLY this structure:

   {{
       "urllist": ["url1", "url2", "url3"]
   }}

   Do NOT pass a list directly.
   Do NOT pass null.
   The argument must be a dictionary with key "urllist".

5. After extracting content, enter the detailed extracted content into a list, if the page cannot be accessed. use at least the heading and basic content

Return strictly:

{{
    "newses": ["summary1", "summary2", ...]
}}

Do NOT return URLs.
Do NOT return tool outputs.
"""

    response = writing_assistant_agent.invoke(
        {"messages": [{"role": "user", "content": prompt}]}
    )

    return response["structured_response"]["newses"]

def store_to_redis(articles):
    redis_url = os.getenv('UPSTASH_REDIS_REST_URL')
    redis_token = os.getenv('UPSTASH_REDIS_REST_TOKEN')
    redis = Redis(url=redis_url, token=redis_token)
    redis.set("articles", json.dumps(articles))
    return