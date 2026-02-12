import fastapi


newsfeedrouter = fastapi.APIRouter()

@newsfeedrouter.get("/apiv0/newsfeed/getdailynews")
def getDailynews():
    pass
