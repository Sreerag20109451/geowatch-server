import os
import pathlib
import tempfile
import json
import ee
from dotenv import load_dotenv
from earthengine.auth import EarthEngineAuth


class EarthEngineRegion:
    def __init__(self):
        pass
        # # Load environment variables
        # self.envpath = pathlib.Path(__file__).parent.parent / "config" / ".env"
        # load_dotenv(dotenv_path=self.envpath)
        # # Read service account and JSON key from env
        # self.service_account = os.getenv("SERVICE_ACCOUNT")
        # key_json_str = os.environ.get("KEY_JSON")
        # print(key_json_str)
        # key_json_dict = json.loads(key_json_str)
        # if not key_json_str:
        #     raise ValueError("KEY_JSON environment variable not set!")
        # key_json_dict = json.loads(key_json_str)
        #
        # # Create a temporary file for EE SDK
        # with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as tmp:
        #     json.dump(key_json_dict, tmp)
        #     self.key_path = tmp.name
        #
        # # Initialize Earth Engine
        # self.eeAuth = EarthEngineAuth()
        # self.eeAuth.initialize_earth_engine(service_account=self.service_account, path_to_key=self.key_path)
        #
        # # Load datasets
        # self.lsib = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")
        # self.gmba = ee.FeatureCollection("projects/geo-watch-483617/assets/gmba")

    def get_regional_boundaries(self, region, dataset="lsib", band=None):
        """
        Get regional boundaries from a dataset
        """
        bands = {
            "lsib": "country_na",
            "gmba": "Name_EN",
        }
        band = band or bands.get(dataset, "country_na")

        fc = self.lsib if dataset == "lsib" else self.gmba
        return fc.filter(ee.Filter.lte(band, region))

    def lsib_region(self, country_na):
        """Get boundaries from LSIB dataset"""
        return self.lsib.filter(ee.Filter.eq("country_na", country_na))

    def gmba_region(self, gmba_na):
        """Get boundaries from GMBA dataset"""
        return self.gmba.filter(ee.Filter.eq("Name_EN", gmba_na))
