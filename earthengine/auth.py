
import ee


class EarthEngineAuth:
    def __init__(self):
        pass

    """
    Initialize Google Earth Engine

    Args : Service account, Path to credentials
    Return  : None
    """

    def initialize_earth_engine(self,service_account, path_to_key):
        credentials = ee.ServiceAccountCredentials(str(service_account), str(path_to_key))
        ee.Initialize(credentials)
        return






