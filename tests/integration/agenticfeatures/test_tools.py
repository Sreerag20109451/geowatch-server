import unittest

import os

from dotenv import load_dotenv

from dailytasks.newsfeedtools import get_newsData
from agenticfeatures.climatecolumns.tools import searchforpapers, search_web


class NewsFeedTests(unittest.IsolatedAsyncioTestCase):

    def setup(self):
        self.envpath = pathlib.Path(__file__).parent.parent.parent.resolve() / "config" / ".env"
        load_dotenv(dotenv_path=self.envpath)
        self.apikey = os.getenv("GEMINI_API_KEY")

        """
    Verify if the newsdata io responds with news objects
    """

    def test_getnews(self):
        print("---Fetching news data -------")
        newses = get_newsData()
        self.assertGreater(len(newses), 2)

        """
    Verify if semantic scholar returns documents
    """

    def test_semantic_scholar_test(self):
        response = searchforpapers.invoke({})
        self.assertEqual(len(response), 10)
    def test_search_web(self):
        response = search_web.invoke({"query" : "climate change"})
        self.assertEqual(len(response), 10)






if __name__ == "__main__":
    unittest.main()
