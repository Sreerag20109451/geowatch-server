

from utility.earthengineutilities import create_legacy_tile_url


class EarthEngineMaps:
    def __init__(self):
        pass
    """
    
    Get the image's tile url 
    Args : Image collection , Visualization parameters
    
    Return : An object containing mapid and irl
    """
    def get_mapid(self, imagecollection, vis_params):
        mapidObj = imagecollection.getMapId(vis_params)
        legacy_url = create_legacy_tile_url(mapidObj["mapid"])
        return  {  "url" : legacy_url, "mapobj" : mapidObj }

    def clip_with_geometry(self, image, geometry):
        return  image.clip(geometry)
