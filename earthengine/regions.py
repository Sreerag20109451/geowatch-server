import os
import pathlib
from dotenv import load_dotenv
import ee
from earthengine.auth import EarthEngineAuth

class EarthEngineRegion:
    _ee_initialized = False

    def __init__(self):
        self._init_ee()

        self.lsib = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")
        self.gmba = ee.FeatureCollection("projects/geo-watch-483617/assets/gmba")



    """Initialize GEE

    Args :None
    Return: None
    
    """
    @classmethod
    def _init_ee(cls):
        if cls._ee_initialized:
            return
        
        BASE_DIR = pathlib.Path(__file__).parent.parent.parent.resolve()
        ENV_PATH = BASE_DIR / "config" / ".env"
        LOCAL_KEY = BASE_DIR / "key.json"         
        RAILWAY_MOUNT = "/services/key.json" 

        if(ENV_PATH.exists()):
            load_dotenv(dotenv_path=ENV_PATH)
        else:
            print("Reading from shared variables in prod")

        service_account = os.getenv("SERVICE_ACCOUNT")
        if not service_account:
            raise RuntimeError("SERVICE_ACCOUNT environment variable not set")

        # Resolve key path
        base_dir = os.path.dirname(__file__)
        local_key = os.path.join(base_dir, "key.json")
        railway_key = "/services/key.json"

        if os.path.exists(local_key):
            key_path = local_key
        elif os.path.exists(railway_key):
            key_path = railway_key
        else:
            key_json = os.getenv("KEY_JSON")
            if not key_json:
                raise RuntimeError("No Earth Engine key found")

            key_path = os.path.join(base_dir, "temp_key.json")
            with open(key_path, "w") as f:
                f.write(key_json)

        ee_auth = EarthEngineAuth()
        ee_auth.initialize_earth_engine(service_account, key_path)

        cls._ee_initialized = True

    def get_regional_boundaries(self, region, dataset="lsib", band=None):
        bands = {
            "lsib": "country_na",
            "gmba": "Name_EN",
        }

        band = band or bands.get(dataset, "country_na")
        fc = self.lsib if dataset == "lsib" else self.gmba

        return fc.filter(ee.Filter.eq(band, region))

    def lsib_region(self, country_na):
        return self.lsib.filter(ee.Filter.eq("country_na", country_na))

    def gmba_region(self, gmba_na):
        return self.gmba.filter(ee.Filter.eq("Name_EN", gmba_na))
