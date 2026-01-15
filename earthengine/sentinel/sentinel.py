import os
import pathlib

from dotenv import load_dotenv
import ee
from earthengine.auth import EarthEngineAuth
from utility.earthengineutilities import create_date_range


class SentinelProducts:

    def __init__(self):

        self.reflectance_bands = [
    'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B9', 'B11', 'B12']
        
        self.qa_band= 'QA60'
        
        self._init_ee()
        self.sentinel_collection = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        

        pass

    """Initialize Earth Engine"""

    def _init_ee(cls):
        if cls._ee_initialized:
            return
        
        BASE_DIR = pathlib.Path(__file__).parent.parent.parent.resolve()
        ENV_PATH = BASE_DIR / "config" / ".env"

        if(ENV_PATH.exists()):
            load_dotenv(dotenv_path=ENV_PATH)
        else:
            print("Reading from shared variables in prod")

        service_account = os.getenv("SERVICE_ACCOUNT")
        if not service_account:
            raise RuntimeError("SERVICE_ACCOUNT environment variable not set")


        local_key = os.path.join(BASE_DIR, "key.json")
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
        
    
    """
    Get recent sentinel data

    Args : Time delta

    Returns : Sentinel data
    """
    def get_recent_sentinel_data(self,region, delta=10, cloud_masking=True):
        date_range = create_date_range(delta)
        startdate = date_range[0]
        enddate = date_range[1]

        pass
    

    """

    Scale sentinel imagery to original reflectance
    Args : Sentinel Collection

    Returns : Scaled Sentinel collection
    """

    def scaleImage(self, collection,bands):
        def scaleSentinelImage(image):
            return image.divide(1000)
        for band in bands:
            image = image.select(band)
            collection.map(scaleSentinelImage)
        return collection
    
    def maskClouds(self):
        
        pass

    def calculate_indices(self,  collection, index="ndsi", scaled=True):
        match index:
            case "ndsi":

                bands = [ 'B3' , 'B11']
                if scaled is not True:
                    collection = self.scaleImage(collection, bands)
        pass
                
                          


            
