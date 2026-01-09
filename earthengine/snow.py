import ee

from earthengine.regions import EarthEngineRegion
from utility.earthengineutilities import create_date_range


class SnowProducts:
    def __init__(self):
        self.region = EarthEngineRegion()
        pass

    """
    Get recent modis data with specified bands for a specified time interval (delta, default = 8)
    """

    def get_modis_data(self, delta, **kwargs):
        default_bands = ['NDSI_Snow_Cover', 'NDSI_Snow_Cover_Basic_QA', 'NDSI_Snow_Cover_Class']
        for band in kwargs.items():
            if (band not in default_bands):
                default_bands.append(band)
        modis_data = ee.ImageCollection(default_bands)
        date_range = create_date_range(delta)
        start_date = date_range[0]
        end_date = date_range[1]
        modis_data = ee.ImageCollection("MODIS/061/MOD10A1")
        modis_data = self.maskSnowCover(modis_data).filterDate(start_date, end_date).select(default_bands)
        return modis_data

    """
    Create recent composite of Modis snow cover
    args: delta 
    returns : Recent modis snow cover

     """

    def get_modis_snow_cover(self, delta=10, region=None, is_png=False):

        def legend (vis_params):
            return vis_params

        modis_data = self.get_modis_data(delta).select('NDSI_Snow_Cover').median()

        match region:

            case 'himalayas':
                regiontobeclipped = self.region.gmba_region("Himalayas")
                modis_data = modis_data.clip(regiontobeclipped)
            case 'alps':
                regiontobeclipped = self.region.gmba_region("Alps")
                modis_data = modis_data.clip(regiontobeclipped)
            case 'greenland':
                regiontobeclipped = self.region.gmba_region("Greenland")
                modis_data = modis_data.clip(regiontobeclipped)
            case 'arctic':
                regiontobeclipped = self.region.gmba_region("Arctic")
                modis_data = modis_data.clip(regiontobeclipped)
            case 'antarctic':
                regiontobeclipped = self.region.lsib_region("Antarctica")
                modis_data = modis_data.clip(regiontobeclipped)
        return {"image" : modis_data , "legend" : legend }

    """
    Mask the modis snow cover data 
    
    Args: Modis Image collection, snow cover band (default ='NDSI_snow_cover'), 
    qa band(default ='NDSI_Snow_Cover_Basic_QA') , 
    class band(default =NDSI_Snow_Cover_Class
    
    Return :
    
    Masked image collection
    """

    def maskSnowCover(self, modis_data, snow_band='NDSI_Snow_Cover', qa_band='NDSI_Snow_Cover_Basic_QA',
                      class_band='NDSI_Snow_Cover_Class'):
        def mask_image(image):
            image = ee.Image(image)

            snow_mask = image.select(snow_band).gt(2)
            qa_mask = image.select(qa_band).lt(3)
            class_img = image.select(class_band)
            land_mask = (
                class_img.neq(237)  # inland water
                .And(class_img.neq(239))  # ocean
                .And(class_img.neq(250))  # cloud
                .And(class_img.neq(211))  # night
                .And(class_img.neq(200))  # missing
            )

            return (
                image
                .updateMask(snow_mask)
                .updateMask(qa_mask)
                .updateMask(land_mask)
            )

        return modis_data.map(mask_image)
