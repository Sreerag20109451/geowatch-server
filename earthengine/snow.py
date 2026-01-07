import ee
from utility.earthengineutilities import create_date_range

"""
Create recent composite of Modis snow cover
args: delta 
returns : Recent modis snow cover

 """

class SnowProducts:
    def __init__(self):
        pass

    def get_modis_recent_data(self,delta):
        date_range = create_date_range(delta)
        modis = ee.ImageCollection("MODIS/061/MOD10A1").select('NDSI_Snow_Cover')
        start_date = date_range[0]
        end_date = date_range[1]
        filtered_modis = modis.filterDate(start_date, end_date).median()
        return filtered_modis






