import ee

from earthengine.regions import EarthEngineRegion
from utility.earthengineutilities import create_date_range, create_legend


class ModisProducts:
    def __init__(self):
        self.region = EarthEngineRegion()
        pass

    """
    Get recent modis data with specified bands for a specified time interval (delta, default = 8)
    """

    def get_modis_data(self, delta, threshold=None, qa_mask="default" , snow_class_mask="default", **kwargs ,):
        default_bands = ['NDSI_Snow_Cover', 'NDSI_Snow_Cover_Basic_QA', 'NDSI_Snow_Cover_Class']
        for band in kwargs.items():
            if (band not in default_bands):
                default_bands.append(band)
        date_range = create_date_range(delta)
        start_date = date_range[0]
        end_date = date_range[1]
        modis_data = ee.ImageCollection("MODIS/061/MOD10A1").select(default_bands)
        modis_data = self.maskSnowCover(modis_data, threshold, qa_mask=qa_mask, snow_class_mask=snow_class_mask ).filterDate(start_date, end_date).select(default_bands)
        return modis_data

    """
    Create recent composite of Modis snow cover
    args: visualization_parameters, delta , region , is_png, snow_threshold 
    returns : Recent modis snow cover

     """

    def get_modis_snow_cover(self, vis_params, delta=10, region=None, is_png=False, threshold = None, qa_mask="default" , snow_class_mask="default" ):
        modis_data = self.get_modis_data(delta, threshold, qa_mask, snow_class_mask).select('NDSI_Snow_Cover').median()

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
        legendObj = create_legend(vis_params, 'Modis - NDSI', threshold)
        return {"image" : modis_data , "legend" : legendObj, "vis_param": legendObj["vis_param"] }

    """
    Mask the modis snow cover data 
    
    Args: Modis Image collection, snow cover band (default ='NDSI_snow_cover'), 
    qa band(default ='NDSI_Snow_Cover_Basic_QA') , 
    class band(default =NDSI_Snow_Cover_Class
    
    Return :
    
    Masked image collection
    """

    def maskSnowCover(self, modis_data, threshold=None,
                      snow_band='NDSI_Snow_Cover',
                      qa_band='NDSI_Snow_Cover_Basic_QA',
                      class_band='NDSI_Snow_Cover_Class',
                      qa_mask="default", snow_class_mask="default"):

        def mask_image(image):
            image = ee.Image(image)

            class_image = image.select(class_band)
            class_mask = (
                class_image.neq(200).And(class_image.neq(201))
            )

            image = image.updateMask(class_mask)
            qa_pixel_mask = None
            snow_class_pixel_mask= ee.Image(1)



            if image.bandNames().contains(qa_band) and qa_mask != "default":
                match qa_mask:
                    case 'best':
                        qa_pixel_mask = image.select(qa_band).eq(0)
                    case 'good':
                        qa_pixel_mask = image.select(qa_band).lte(1)
                    case 'ok':
                        qa_pixel_mask = image.select(qa_band).lte(2)
            if qa_pixel_mask is not None:
                image = image.updateMask(qa_pixel_mask)

            if image.bandNames().contains(class_band) and snow_class_mask != "default":
                match snow_class_mask:
                    case 'ocean':
                        snow_class_pixel_mask = image.select(class_band).neq(239)
                    case 'inlandw':
                        snow_class_pixel_mask = image.select(class_band).neq(237)
                    case 'cloud':
                        snow_class_pixel_mask = image.select(class_band).neq(250)
                    case 'night':
                        snow_class_pixel_mask = image.select(class_band).neq(211)
                    case 'saturated':
                        snow_class_pixel_mask = image.select(class_band).neq(254)
                    case 'missing':
                        snow_class_pixel_mask = image.select(class_band).neq(200)
                    case 'nodecision':
                        snow_class_pixel_mask = image.select(class_band).neq(201)
                    case 'all':
                        class_img = image.select(class_band)
                        snow_class_pixel_mask = (
                            class_img.neq(200)  # missing
                            .And(class_img.neq(201))  # no decision
                            .And(class_img.neq(211))  # night
                            .And(class_img.neq(237))  # inland water
                            .And(class_img.neq(239))  # ocean
                            .And(class_img.neq(250))  # cloud
                            .And(class_img.neq(254))  # saturated
                        )

            if snow_class_mask != "default":
                image = image.updateMask(snow_class_pixel_mask)


            # Snow mask

            int_t = float(threshold) if threshold is not None else None

            if image.bandNames().contains(snow_band):
                snow_mask = image.select(snow_band).gt(0 if threshold is None else ee.Image.constant(int_t))
                image = image.updateMask(snow_mask)

            return image

        return modis_data.map(mask_image)

