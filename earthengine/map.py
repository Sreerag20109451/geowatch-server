

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
        mapid = mapidObj["mapid"]
        tile_fetcher = mapidObj["tile_fetcher"]
        url = tile_fetcher.url_format
        return  { "mapid" : mapid, "url" : url, "mapobj" : mapidObj }

    def clip_with_geometry(self, image, geometry):
        return  image.clip(geometry)
