import requests
import os
from typing import TypedDict
import pathlib


from dotenv import load_dotenv


class News(TypedDict):
    
    title : str
    image: str
    content: str
    source: str
    href: str


BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()
ENV_PATH = BASE_DIR / "config" / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    load_dotenv() 

# Now os.getenv will work whether the key comes from a file or Railway's UI.
apikey = os.getenv("NEWSDATA_API_KEY")


apikey= os.getenv("NEWSDATA_API_KEY")

news_data_query_builder_url = f'https://newsdata.io/api/1/latest?apikey={apikey}&q=climate%20change&language=en&prioritydomain=top&image=1&removeduplicate=1&size=10'




def get_newsData():
    try:
        data = requests.get(news_data_query_builder_url).json()

        relevant_news = []
        for n in data.get("results", []):
        
            news: News = {
            "title": n.get("title", "No Title"),
            "image": n.get("image_url", ""),
            "content": n.get("description", "No Content"),
            "href": n.get("link", ""), # Fixed typo: 'llink' -> 'link'
            "source": n.get("source_id", "Unknown")
            }
            relevant_news.append(news)

        return relevant_news
    except Exception as e:

        print(e.__traceback__)
        return Exception("Error loading news data")
    





