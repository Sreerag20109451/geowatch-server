import os
import pathlib
import unittest

import ee
from dotenv import load_dotenv

from earthengine.auth import EarthEngineAuth


class EarthEngineAuthTests(unittest.TestCase):
    """
    Set up Auth Object
    Read environment paths and read variables
    Read ee credentials

    """
    def setUp(self):
        self.eeAuth = EarthEngineAuth()
        self.envpath =pathlib.Path(__file__).parent.parent.parent / "config"/".env"
        load_dotenv(dotenv_path=self.envpath)
        self.service_account = os.getenv('SERVICE_ACCOUNT')
        self.key_path = pathlib.Path(__file__).parent.parent.parent / 'key.json'

    """
    Check if service account is set correctly
    Check if key path is set correctly
    Check if EE object can be read
    """

    def test_initialization(self):

        self.assertIsNotNone(self.service_account, "SERVICE_ACCOUNT env variable is not set")
        self.assertIn('gserviceaccount.com', self.service_account)
        self.assertTrue(self.key_path.exists(), f"Key file not found at {self.key_path}")
        self.eeAuth.initialize_earth_engine(self.service_account, self.key_path)
        img = ee.Image(1)
        self.assertIsInstance(img, ee.Image)


if __name__ == '__main__':
    unittest.main()
