import fastapi

from starlette.responses import JSONResponse

from dailytasks.newsfeed import NewsFeed


newsfeedrouter = fastapi.APIRouter()
newsfeed = NewsFeed()

@newsfeedrouter.get("/apiv0/newsfeed/getdailynews")
async def getDailynews():
    try:
        newsdata = await newsfeed.get_daily_news_from_redis()
        if not newsdata or "news" not in newsdata:
            return JSONResponse(status_code=404, content={"message": "No news found", "data": []})
        
        return JSONResponse(status_code=200, content={"message": "success", "data": newsdata["news"]})
    except Exception as e:
        print(f"Error in getDailynews: {e}")
        return JSONResponse(status_code=500, content={"message": f"Error retrieving data: {str(e)}"})

    
