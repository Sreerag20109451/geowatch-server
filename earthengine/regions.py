from rich.region import Region
import ee


class EarthEngineRegion():

    def __init__(self):
        self.lsib = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")
        pass

    def lsib_region(self, country_na,):
        return self.lsib.filter(ee.Filter.eq('country_na', country_na))

