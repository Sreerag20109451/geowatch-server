import fastapi

from starlette.responses import JSONResponse

from agenticfeatures.newsfeed import NewsFeed 


newsfeedrouter = fastapi.APIRouter()
newsfeed = NewsFeed()

@newsfeedrouter.get("/apiv0/newsfeed/getdailynews")
async def getDailynews():
    try:
        news = await newsfeed.newget_daily_news_from_redis()
        return JSONResponse(status_code=200, content={ "message" : "success", "data" : news})
    except Exception as e:
        print(e.__traceback__)
        return JSONResponse(status_code=500, content={ "message" : "Error retrieving data", "data" : news})

    
