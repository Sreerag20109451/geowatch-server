import os
import unittest
import json
import ee
import pathlib
from dotenv import load_dotenv
from earthengine.auth import EarthEngineAuth

class EarthEngineAuthTests(unittest.TestCase):
    def setUp(self):
        self.eeAuth = EarthEngineAuth()
        
        # 1. Define Paths relative to this file
        # tests/integration/test_eeauth.py -> parents[2] is project root
        self.BASE_DIR = pathlib.Path(__file__).parent.parent.parent.resolve()
        self.ENV_PATH = self.BASE_DIR / "config" / ".env"
        self.LOCAL_KEY = self.BASE_DIR / "key.json"
        self.RAILWAY_MOUNT = pathlib.Path("/services/key.json")

        # 2. Load .env if it exists
        if self.ENV_PATH.exists():
            load_dotenv(dotenv_path=self.ENV_PATH)
        
        # 3. Mirror the Main App Logic for Credential Resolution
        self.service_accnt = os.getenv("SERVICE_ACCOUNT_ID") # Or "SERVICE_ACCOUNT" based on your .env
        self.key_file_path = None

        if self.LOCAL_KEY.exists():
            self.key_file_path = str(self.LOCAL_KEY)
        elif self.RAILWAY_MOUNT.exists():
            self.key_file_path = str(self.RAILWAY_MOUNT)
        else:
            # Fallback to KEY_JSON env var (which contains the raw JSON string)
            key_json_str = os.environ.get("SERVICE_ACCOUNT") # Matches your provided env block
            if key_json_str:
                self.key_file_path = str(self.BASE_DIR / "temp_key.json")
                with open(self.key_file_path, "w") as f:
                    f.write(key_json_str)
            else:
                raise RuntimeError("No credentials found in local files, Railway, or Environment!")

    def test_initialization(self):
        """Tests the EE initialization using the resolved key path."""
        try:
            # Initialize using your custom Auth class
            self.eeAuth.initialize_earth_engine(self.service_accnt, self.key_file_path)

            # Test basic EE object and trigger an API call
            img = ee.Image("MODIS/006/MOD10A1/2020_03_01").select("NDSI_Snow_Cover")
            info = img.getInfo()
            
            self.assertIsNotNone(info)
            self.assertEqual(info['type'], 'Image')
            
        except Exception as e:
            self.fail(f"Earth Engine initialization failed: {e}")

    def tearDown(self):
        # Clean up the temporary key file if we created one during tests
        temp_key = self.BASE_DIR / "temp_key.json"
        if temp_key.exists():
            temp_key.unlink()

if __name__ == "__main__":
    unittest.main()