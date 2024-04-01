import os
import fastapi, uvicorn
import schemas
import pydantic
import pymongo
import datetime
from fastapi.middleware.cors import CORSMiddleware
app = fastapi.FastAPI()

origins = [
  "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)
class Config(pydantic.BaseModel):
    MONGO_URL: str = "mongodb://mongodb:27017"

    class Meta:
        from_attributes = True


def get_database(CONNECTION_STRING):
    client = pymongo.MongoClient(CONNECTION_STRING)
    return client["server_util_db"]


def make_stat_list(time_interval: schemas.TimeInterval, db):
    current_time = datetime.datetime.now()
    date_end = (
        datetime.datetime.now()
        - datetime.timedelta(seconds=5)
        + datetime.timedelta(hours=3)
    )
    if time_interval.interval == "hour":

        date_start = date_end - datetime.timedelta(hours=1)
    elif time_interval.interval == "minute":

        date_start = date_end - datetime.timedelta(minutes=1)
    elif time_interval.interval == "day":

        date_start = date_end - datetime.timedelta(days=1)
    elif time_interval.interval == "week":

        date_start = date_end - datetime.timedelta(days=7)
    result = list()
    while date_end != date_start:
        one_stat = db["stats"].find_one(
            {"time_stamp": date_end.strftime("%Y-%m-%dT%H:%M:%S.000+00:00")}
        )
        if one_stat:
            result.append(schemas.GetStat(**one_stat))
            print("->", one_stat)
        else:
            print("NO DATA")
        date_end -= datetime.timedelta(seconds=1)
    return result


config = Config()
db = get_database(config.MONGO_URL)


@app.get("/current_stat", response_model=schemas.GetStat)
async def current_stat():
    current_time = datetime.datetime.now()
    pseudo_current_time = current_time+datetime.timedelta(hours=3)-datetime.timedelta(seconds=5)

    data = db["stats"].find_one(
        {"time_stamp": pseudo_current_time.strftime("%Y-%m-%dT%H:%M:%S.000+00:00")}
    )
    return schemas.GetStat(**data)


@app.post("/time_interval_values", response_model=list[schemas.GetStat])
def get_time_interval_values(time_interval: schemas.TimeInterval):

    return make_stat_list(time_interval=time_interval, db=db)

# @app.post('set_ctitycal/')
#     return {}

uvicorn.run(app=app, host="0.0.0.0")
