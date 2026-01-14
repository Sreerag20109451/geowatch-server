import fastapi
from starlette.responses import JSONResponse

from earthengine.map import EarthEngineMaps
from earthengine.snow import ModisProducts
from utility.default_vis_params import snow_cover_global_vis_param



snowrouter  = fastapi.APIRouter()

snowproducts = ModisProducts()
maps = EarthEngineMaps()

@snowrouter.get("/apiv0/snow/global_snow_cover")
async def snow_cover(vis_params=None, region=None, is_png = False, qa_mask="default", snow_class_mask="default"):
    if vis_params is None:
        vis_params = snow_cover_global_vis_param
    if region is not  None:
        region = region.lower()

    try:
        recent_modis_snow_dict = snowproducts.get_modis_snow_cover(vis_params, 10,region = region, is_png = is_png, qa_mask=qa_mask, snow_class_mask=snow_class_mask)
        mapDict = maps.get_mapid(recent_modis_snow_dict["image"],vis_params=vis_params)
      
        legacy_url = mapDict["url"]
        print(legacy_url)

        return  JSONResponse(status_code=200, content= { "url" : legacy_url , "vis_params" : vis_params, "legend" :recent_modis_snow_dict["legend"] })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error" : str(e)})







