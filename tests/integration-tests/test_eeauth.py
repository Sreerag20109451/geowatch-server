import os
import pathlib
import tempfile
import unittest
import json

import ee
from dotenv import load_dotenv

from earthengine.auth import EarthEngineAuth


class EarthEngineAuthTests(unittest.TestCase):
    """
    Set up Auth Object
    Read environment paths and variables
    Initialize EE credentials from env (no local key.json needed)
    """

    def setUp(self):
        self.eeAuth = EarthEngineAuth()
        # Load .env
        self.envpath = pathlib.Path(__file__).parent.parent.parent / "config" / ".env"
        load_dotenv(dotenv_path=self.envpath)

        # Read service account and key JSON from env
        self.service_account = os.getenv("SERVICE_ACCOUNT")
        key_json_str = os.environ.get("KEY_JSON")
        if not key_json_str:
            raise ValueError("KEY_JSON environment variable not set!")

        key_json_dict = json.loads(key_json_str)

        # Create a temporary file for Earth Engine
        tmp_file = tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False)
        json.dump(key_json_dict, tmp_file)
        tmp_file.flush()
        tmp_file.close()
        self.key_path = pathlib.Path(tmp_file.name)

    def test_initialization(self):
        # Check SERVICE_ACCOUNT
        self.assertIsNotNone(self.service_account, "SERVICE_ACCOUNT env variable is not set")
        self.assertIn("gserviceaccount.com", self.service_account)

        # Check temporary key file
        self.assertTrue(self.key_path.exists(), f"Temporary key file not found at {self.key_path}")

        # Initialize EE
        self.eeAuth.initialize_earth_engine(self.service_account, self.key_path)

        # Test basic EE object
        img = ee.Image(1)
        self.assertIsInstance(img, ee.Image)


if __name__ == "__main__":
    unittest.main()
