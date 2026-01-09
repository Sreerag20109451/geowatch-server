

class EarthEngineMaps:
    def __init__(self):
        pass
    def get_mapid(self, imagecollection, vis_params):
        mapidObj = imagecollection.getMapId(vis_params)
        print(mapidObj)
        mapid = mapidObj["mapid"]
        print(mapid)
        tile_fetcher = mapidObj["tile_fetcher"]  # TileFetcher object
        url = tile_fetcher.url_format
        return  { "mapid" : mapid, "url" : url, "mapobj" : mapidObj }

    def clip_with_geometry(self, image, geometry):
        return  image.clip(geometry)
