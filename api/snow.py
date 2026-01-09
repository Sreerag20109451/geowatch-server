import fastapi
from starlette.responses import JSONResponse

from earthengine.map import EarthEngineMaps
from earthengine.snow import SnowProducts
from utility.default_vis_params import snow_cover_global_vis_param

snowrouter  = fastapi.APIRouter()

snowproducts = SnowProducts()
maps = EarthEngineMaps()

@snowrouter.get("/snow/global_snow_cover")
async def snow_cover(vis_params=None, region=None, is_png = False):
    if vis_params is None:
        vis_params = snow_cover_global_vis_param
    if region is not  None:
        region = region.lower()

    try:
        recent_modis_snow = snowproducts.get_modis_recent_data(10, region = region, is_png = is_png)
        mapDict = maps.get_mapid(recent_modis_snow,vis_params=vis_params)
        print(mapDict)

        return {"mapdic" : mapDict["mapobj"], "mapid" : mapDict["mapid"], "url" : mapDict["url"], "vis_params" : vis_params}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error" : str(e)})







