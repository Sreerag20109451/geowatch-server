

class EarthEngineMaps:
    def __init__(self):
        pass
    def get_mapid(self, imagecollection):
        mapidObj = imagecollection.getMapId()
        print(mapidObj)
        mapid = mapidObj["mapid"]
        print(mapid)
        tile_fetcher = mapidObj["tile_fetcher"]  # TileFetcher object
        url = tile_fetcher.url_format
        return  { "mapid" : mapid, "url" : url }
