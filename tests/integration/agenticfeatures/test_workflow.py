import unittest

from agenticfeatures.climatecolumns.agents import generate_articles
from agenticfeatures.climatecolumns.tools import ResearchDocument


class TestClimateColumnWorkflow(unittest.TestCase):
    def setup(self):
        self.envpath = pathlib.Path(__file__).parent.parent.parent.resolve() / "config" / ".env"
        load_dotenv(dotenv_path=self.envpath)
        self.apikey = os.getenv("GEMINI_API_KEY")

    def test_workflow(self):
        print("------------------------Testing workflow---")
        state = generate_articles()
        print(f"The run is {state}")
        self.assertIsInstance(state["documents"], list)
        print("-------------------- Ended testing workflow------------------")




if __name__ == '__main__':
    unittest.main()
