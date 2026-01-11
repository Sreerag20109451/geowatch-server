import ee

from earthengine.regions import EarthEngineRegion
from utility.earthengineutilities import create_date_range, create_legend


class SnowProducts:
    def __init__(self):
        self.region = EarthEngineRegion()
        pass

    """
    Get recent modis data with specified bands for a specified time interval (delta, default = 8)
    """

    def get_modis_data(self, delta, threshold, **kwargs ,):
        default_bands = ['NDSI_Snow_Cover', 'NDSI_Snow_Cover_Basic_QA', 'NDSI_Snow_Cover_Class']
        for band in kwargs.items():
            if (band not in default_bands):
                default_bands.append(band)
        date_range = create_date_range(delta)
        start_date = date_range[0]
        end_date = date_range[1]
        modis_data = ee.ImageCollection("MODIS/061/MOD10A1").select(default_bands)
        modis_data = self.maskSnowCover(modis_data, threshold ).filterDate(start_date, end_date).select(default_bands)
        print(modis_data)
        return modis_data

    """
    Create recent composite of Modis snow cover
    args: visualization_parameters, delta , region , is_png, snow_threshold 
    returns : Recent modis snow cover

     """

    def get_modis_snow_cover(self, vis_params, delta=10, region=None, is_png=False, threshold = 2 ):
        modis_data = self.get_modis_data(delta, threshold).select('NDSI_Snow_Cover').mean()

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
        legendObj = create_legend(vis_params, 'Modis Snow Cover -Ranges')
        return {"image" : modis_data , "legend" : legendObj }

    """
    Mask the modis snow cover data 
    
    Args: Modis Image collection, snow cover band (default ='NDSI_snow_cover'), 
    qa band(default ='NDSI_Snow_Cover_Basic_QA') , 
    class band(default =NDSI_Snow_Cover_Class
    
    Return :
    
    Masked image collection
    """

    def maskSnowCover(self, modis_data, threshold =2, snow_band='NDSI_Snow_Cover', qa_band='NDSI_Snow_Cover_Basic_QA',
                      class_band='NDSI_Snow_Cover_Class'):
        def mask_image(image):
            image = ee.Image(image)

            snow_mask = image.select(snow_band).gt(threshold)
            qa_mask = image.select(qa_band).lt(3)
            class_img = image.select(class_band)
            land_mask = (
                class_img.neq(237)
                .And(class_img.neq(239))
                .And(class_img.neq(250))
                .And(class_img.neq(211))
                .And(class_img.neq(200))
            )

            return (
                image
                .updateMask(snow_mask)
                .updateMask(qa_mask)
                .updateMask(land_mask)
            )

        return modis_data.map(mask_image)
