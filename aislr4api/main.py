import os
import fastapi, uvicorn
import schemas
import pydantic
import pymongo
import datetime

app = fastapi.FastAPI()


class Config(pydantic.BaseModel):
    MONGO_URL: str = "mongodb://mongodb:27017"

    class Meta:
        from_attributes = True


def get_database(CONNECTION_STRING):
    client = pymongo.MongoClient(CONNECTION_STRING)
    return client["server_util_db"]


config = Config()
db = get_database(config.MONGO_URL)


@app.get("/current_stat", response_model=schemas.GetStat)
async def current_stat():
    current_time = datetime.datetime.now()
    pseudo_current_time = datetime.datetime(
        year=current_time.year,
        month=current_time.month,
        day=current_time.day,
        hour=current_time.hour + 3,
        minute=current_time.minute,
        second=current_time.second - 5,
        microsecond=0,
    )

    data = db["stats"].find_one(
        {"time_stamp": pseudo_current_time.strftime("%Y-%m-%dT%H:%M:%S.000+00:00")}
    )
    return schemas.GetStat(**data)


@app.post("/time_interval_values")
def get_time_interval_values(time_interval: schemas.TimeInterval): 
    if time_interval.interval=='hour':
        date_end=datetime.datetime.now()-datetime.timedelta(seconds=5)
        date_start=date_end-datetime.timedelta(hours=1)
    elif time_interval.interval=='minute':
        date_end=datetime.datetime.now()-datetime.timedelta(seconds=5)
        date_start=date_end-datetime.timedelta(minutes=1)
    
    data=db['stats'].find(
        {"time_stamp":{'$gte':date_start.isoformat(),'$lte':date_end.isoformat()}}
    )
    for i in data:
        print(i)
    return {}




uvicorn.run(app=app, host="0.0.0.0")
