import unittest

import os

from dotenv import load_dotenv

from dailytasks.newsfeedtools import get_newsData
from dailytasks.newsfeed import NewsFeed


import pathlib
import json

class NewsFeedTests(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.envpath = pathlib.Path(__file__).parent.parent.parent.resolve() / "config" / ".env"
        load_dotenv(dotenv_path=self.envpath)
        self.apikey = os.getenv("NEWSDATA_API_KEY")

    def test_getnews(self):
        print("---Fetching news data -------")
        newses = get_newsData()
        print(newses)
        self.assertGreater(len(newses["news"]), 2)

        """
    Verify redis responds with news objects
    """

    async def test_news_retrival_from_redis(self):
        print("--- Initalising news retrieval from redis--------")
        newsfeeder = NewsFeed()
        newsfeed = await newsfeeder.get_daily_news_from_redis()
        self.assertIsNotNone(newsfeed)
        self.assertGreater(len(newsfeed), 1)



if __name__ == "__main__":
    unittest.main()
    