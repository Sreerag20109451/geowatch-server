import ee
from utility.earthengineutilities import create_date_range



class SnowProducts:
    def __init__(self):
        pass

    """
    Create recent composite of Modis snow cover
    args: delta 
    returns : Recent modis snow cover

     """

    def get_modis_recent_data(self,delta, region=None, is_png = False):
        date_range = create_date_range(delta)
        start_date = date_range[0]
        end_date = date_range[1]
        modis_data = ee.ImageCollection("MODIS/061/MOD10A1")
        modis_data = modis_data.filterDate(start_date, end_date).select(['NDSI_Snow_Cover','NDSI_Snow_Cover_Basic_QA','NDSI_Snow_Cover_Class'])

        match region:
            case 'himalaya':
                modis_data.clip(region)
            case 'alps' :
                modis_data.clip(region)



        return modis_data

    """
    Mask the modis snow cover data 
    
    Args: Modis Image collection, snow cover band (default ='NDSI_snow_cover'), 
    qa band(default ='NDSI_Snow_Cover_Basic_QA') , 
    class band(default =NDSI_Snow_Cover_Class
    
    Return :
    
    Masked image collection
    """

    def maskSnowCover(self,modis_data,snow_band='NDSI_Snow_Cover' ,qa_band='NDSI_Snow_Cover_Basic_QA', class_band='NDSI_Snow_Cover_Class'):
        def mask_image(image):
            image = ee.Image(image)

            # Keep only actual snow (optional threshold)
            snow_mask = image.select(snow_band).gt(2)

            # Best / Good / OK quality
            qa_mask = image.select(qa_band).lt(3)

            # Remove water, ocean, cloud, night, missing
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

        return  modis_data.map(mask_image)








