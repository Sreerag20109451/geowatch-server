import fastapi
from pyasn1.type.univ import Boolean
from starlette.responses import JSONResponse
import traceback
from earthengine.map import EarthEngineMaps
from earthengine.modis.snow import ModisProducts
from earthengine.sentinel.sentinel import SentinelProducts
from utility.default_vis_params import snow_cover_global_vis_param, sentinel_ndsi_vis_param

snowrouter  = fastapi.APIRouter()

modisproducts = ModisProducts()
sentinelproducts = SentinelProducts()

maps = EarthEngineMaps()

@snowrouter.get("/apiv0/snow/global_snow_cover")
async def snow_cover(dataset, region=None, is_png = False, qa_mask="default", snow_class_mask="default", sentinel_cloud_mask="False"):
    if  dataset == "modis":
        vis_params = snow_cover_global_vis_param
        if region is not None:
            region = region.lower()

        try:
            recent_modis_snow_dict = modisproducts.get_modis_snow_cover(vis_params, 10, region=region, is_png=is_png,
                                                                       qa_mask=qa_mask, snow_class_mask=snow_class_mask)
            mapDict = maps.get_mapid(recent_modis_snow_dict["image"], vis_params=vis_params)

            legacy_url = mapDict["url"]
            print(legacy_url)

            return JSONResponse(status_code=200, content={"url": legacy_url, "vis_params": vis_params,
                                                          "legend": recent_modis_snow_dict["legend"], "resolution" : "mid"})

        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
    if dataset == "sentinel":
        sentinel_cloud_mask = Boolean(sentinel_cloud_mask)
        vis_params = sentinel_ndsi_vis_param
        if region is not None:
            region = region.lower()
        try:
            recent_sentinel_snow_dict = sentinelproducts.get_sentinel_snow_cover_composite(region, sentnel_cloud_mask=sentinel_cloud_mask)
            mapdict = maps.get_mapid(recent_sentinel_snow_dict["image"], vis_params=vis_params)
            legacy_url = mapdict["url"]
            return JSONResponse(status_code=200, content={"url": legacy_url, "vis_params": vis_params,
                                                          "legend": recent_sentinel_snow_dict["legend"], "resolution" : "high"})
        except Exception as e:
            traceback.print_exc()
            return JSONResponse(status_code=500, content={"error": str(e)})

    return None










