import unittest

import os

from dotenv import load_dotenv

from agenticfeatures.tools.newsfeedtools import get_newsData



class NewsFeedTests(unittest.TestCase):
    """
    Verify if the get
    """

    
    def setup(self):
        self.envpath = pathlib.Path(__file__).parent.parent.parent.resolve() / "config" / ".env"
        load_dotenv(dotenv_path=self.envpath)
        self.apikey = os.getenv("NEWSDATA_API_KEY")


    def test_getnews(self):
        print("---Fetching news data -------")
        newses = get_newsData()
        print(len(newses))
        self.assertGreater(len(newses), 2)

if __name__ == "__main__":
    unittest.main()
    