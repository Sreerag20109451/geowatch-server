
"""
Create date range with the specified delta
Args :Delta
Returns: a date range with the specified delta
"""
import datetime


def create_date_range(delta):
    end_dtm = datetime.datetime.now() - datetime.timedelta(days=1)
    end_date = f"{end_dtm.year}-{end_dtm.month:02d}-{end_dtm.day:02d}"

    start_dtm = end_dtm - datetime.timedelta(days=delta)
    start_date = f"{start_dtm.year}-{start_dtm.month:02d}-{start_dtm.day:02d}"

    return [start_date, end_date]


def create_legend(vis_params, chartname):
    palette = vis_params["palette"]
    min = vis_params["min"]
    max = vis_params["max"]
    unitrange = (max - min) / len(palette)
    legend = {}

    for i, color in enumerate(palette):
        legend[color] = f"{min+(i)*unitrange} - {min + (i+1)*unitrange }"
    return { 'legend' : legend , 'chartname' : chartname}


def create_legacy_tile_url(mapid):

    legacy_url = f"https://earthengine.googleapis.com/v1/{mapid}/tiles/{{z}}/{{x}}/{{y}}"
    return legacy_url





