import unittest

import os

from dotenv import load_dotenv

from agenticfeatures.climatecolumns.testdata import urllist
from dailytasks.newsfeedtools import get_newsData
from agenticfeatures.climatecolumns.tools import searchforpapers, search_web, extract_pages
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
    """ Verify if the tavily web search retrieves websites"""
    def test_search_web(self):
        print("----------------------- Testing text search----------------------------------")
        response = search_web.invoke({"query" : "climate change"})
        self.assertEqual(len(response), 10)
        print("----------------------- End for Testing text search----------------------------------")
    """ Verify if the tavily web search extracts websites"""
    def test_web_extract(self):
        print("----------------------- Testing text extraction----------------------------------")
        response = extract_pages.invoke({"urllist":urllist})
        self.assertEqual(len(response), len(urllist))
        self.assertIsInstance(response[0], str)
        print(response[0])
        print("----------------------- End for Testing text extraction----------------------------------")








if __name__ == "__main__":
    unittest.main()
