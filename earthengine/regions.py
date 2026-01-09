import os
import pathlib

from dotenv import load_dotenv
import ee

from earthengine.auth import EarthEngineAuth


class EarthEngineRegion():

    def __init__(self):
        self.eeAuth = EarthEngineAuth()
        self.envpath = pathlib.Path(__file__).parent.parent / "config" / ".env"
        load_dotenv(dotenv_path=self.envpath)
        self.service_account = os.getenv('SERVICE_ACCOUNT')
        self.key_path = pathlib.Path(__file__).parent.parent / 'key.json'
        self.eeAuth.initialize_earth_engine(service_account=self.service_account,path_to_key= self.key_path)
        self.lsib = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")
        self.gmba = ee.FeatureCollection("projects/geo-watch-483617/assets/gmba")
        pass


    """
    
    Get the regional boundaries from datasets
    """
    def get_regional_boundaries(self, region, dataset="lsib",band ='country_na' ):

        bands = {
            self.lsib : 'country_na',
            self.gmba : 'Name_EN',
        }
        if dataset == "lsib":
            dataset = self.lsib
        else :
            dataset = self.gmba

        return  dataset.filter(ee.Filter.lte(bands[dataset],region))

    """
    Get the regional boundaries from the Large Scale International Boundaries dataset
    """

    def lsib_region(self, country_na,):
        return self.lsib.filter(ee.Filter.eq('country_na', country_na))

    """
        Get the regional boundaries from the Global Mountain Boundaries dataset
    """
    def gmba_region(self, gmba_na):
        return  self.gmba.filter(ee.Filter.eq('Name_EN', gmba_na))

