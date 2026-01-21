import os
import pathlib
from unittest.mock import sentinel

from dotenv import load_dotenv
import ee
from ee import collection

from earthengine.auth import EarthEngineAuth
from utility.default_vis_params import sentinel_ndsi_vis_param
from utility.earthengineutilities import create_date_range, create_legend


class SentinelProducts:

    def __init__(self):

        self.reflectance_bands = [
    'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B9', 'B11', 'B12']
        
        self.qa_band= 'QA60'
        
        self._init_ee()
        self.sentinel_msi_collection = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        

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

            key_path = os.path.join(BASE_DIR, "temp_key.json")
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
    def get_recent_sentinel_msi_data(self,region, delta=10, cloud_masking=True):
        date_range = create_date_range(delta)
        start_date = date_range[0]
        end_date = date_range[1]

        match region:
            case 'himalayas':
                regiontobeclipped = self.region.gmba_region("Himalayas")
            case 'alps':
                regiontobeclipped = self.region.gmba_region("Alps")
            case 'greenland':
                regiontobeclipped = self.region.gmba_region("Greenland")
            case 'arctic':
                regiontobeclipped = self.region.gmba_region("Arctic")
            case 'antarctic':
                regiontobeclipped = self.region.lsib_region("Antarctica")

        sentinel_collection = self.sentinel_msi_collection.filter(start_date,end_date).filterBounds(regiontobeclipped)
        return {'collection' : sentinel_collection , 'region_geometry' : regiontobeclipped}


    def get_sentinel_snow_cover_composite(self, region, delta=10, cloud_masking=True):
        vis_param = sentinel_ndsi_vis_param
        sentinel_msi_collection_data = self.get_recent_sentinel_msi_data(region, delta, cloud_masking)
        sentinel_msi_collection = sentinel_msi_collection_data["collection"]
        region_geometry = sentinel_msi_collection["region_geometry"]
        scaled_collection = self.scaleImage(sentinel_msi_collection)
        if cloud_masking is True:
            scaled_collection = self.maskClouds(scaled_collection)
        ndsi_collection = self.ndsi(scaled_collection)
        legend = create_legend(vis_param , "NDSI")
        ndsi_composite =ndsi_collection.select('NDSI').median()
        return  {"image" : ndsi_composite, "vis_param" : vis_param, "legend" : legend}

    

    """

    Scale sentinel imagery to original reflectance
    Args : Sentinel Collection

    Returns : Scaled Sentinel collection
    """

    def scaleImage(self, collection):
        def scaleSentinelImage(image):
            return image.divide(1000)
        for band in self.reflectance_bands:
            image = image.select(band)
            collection.map(scaleSentinelImage)
        return collection

    """
    Masks the cloud and cirrus cover 
    Args : Sentinel Collection
    Returns : Masked Sentinel collection
    """
    
    def maskClouds(self, collection):
        def maskSentinelImage(image):
            qa = image.select(self.qa_band)
            cloud_mask = 1 << 10
            cirrus_mask = 1 << 20
            mask = qa.bitwiseAnd(cloud_mask).eq(0) and qa.bitwiseAnd(cirrus_mask).eq(0)
            return  image.updateMask(mask)
        return collection.map(maskSentinelImage)

    """
    Calculate the NDSI from Sentinel data
    Args : Sentinel Collection  
    Returns : Sentinel collection with NDSI band with corresponding NDSI values
    """
    def ndsi(self, collection):
        def calculate_ndsi(image):
            nominator = image.select('B3').subtract(image.select('B11'))
            denominator = image.select('B3').add(image.select('B11'))
            ndsi = nominator.divide(denominator).rename('NDSI')
            return image.addBands(ndsi)
        return collection.map(calculate_ndsi)
                
                          


            
