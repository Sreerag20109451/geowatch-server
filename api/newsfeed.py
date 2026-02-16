import fastapi

from starlette.responses import JSONResponse

from dailytasks.newsfeed import NewsFeed


newsfeedrouter = fastapi.APIRouter()
newsfeed = NewsFeed()

@newsfeedrouter.get("/apiv0/newsfeed/getdailynews")
async def getDailynews():
    try:
        newsdata = await newsfeed.get_daily_news_from_redis()
        print(newsdata)
        return JSONResponse(status_code=200, content={ "message" : "success", "data" : newsdata})
    except Exception as e:
        print(e.__traceback__)
        return JSONResponse(status_code=500, content={ "message" : "Error retrieving data", "data" : news})

    
