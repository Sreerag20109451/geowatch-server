import unittest

import os

from dotenv import load_dotenv

from dailytasks.newsfeedtools import get_newsData
from dailytasks.newsfeed import NewsFeed



class NewsFeedTests(unittest.IsolatedAsyncioTestCase):



    def setup(self):
        self.envpath = pathlib.Path(__file__).parent.parent.parent.resolve() / "config" / ".env"
        load_dotenv(dotenv_path=self.envpath)
        self.apikey = os.getenv("NEWSDATA_API_KEY")

        """
    Verify if the newsdata io responds with news objects
    """

    def test_getnews(self):
        print("---Fetching news data -------")
        newses = get_newsData()
        print(len(newses))
        self.assertGreater(len(newses), 2)

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
    