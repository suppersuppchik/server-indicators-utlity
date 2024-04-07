import os
import fastapi, uvicorn
import schemas
import pydantic
import pymongo
import datetime
from fastapi.middleware.cors import CORSMiddleware
import time
import threading
import random
import psutil
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
    MONGO_URL: str = "mongodb://localhost:27017"

    class Meta:
        from_attributes = True


def get_database(CONNECTION_STRING):
    client = pymongo.MongoClient(CONNECTION_STRING)
    return client["server_util_db"]


data_storage = dict()
pseudo_current_time: datetime.datetime
DEBUG_MODE = False

SECONDS_STAP = 1
db = get_database(Config().MONGO_URL)
last_current_time_as_int: int


def system_listenner():
    global pseudo_current_time
    global data_storage
    global last_current_time_as_int
    while True:
        pseudo_current_time = datetime.datetime.now()
        pseudo_current_time_str_as_id = pseudo_current_time.strftime("%Y%m%d%H%M%S")
        pseudo_current_time_str_as_time_stamp = pseudo_current_time.strftime(
            "%Y-%m-%dT%H:%M:%S"
        )
        time_stamp_as_int = int(pseudo_current_time_str_as_id)
        if DEBUG_MODE:
            data = schemas.SetStat(
                time_stamp=pseudo_current_time_str_as_time_stamp,
                time_stamp_as_int=time_stamp_as_int,
                cpu_temp=random.uniform(1.00, 100.0),
                gpu_temp=random.uniform(1.00, 100.0),
                cpu_busy=random.uniform(1.00, 100.0),
                gpu_busy=random.uniform(1.00, 100.0),
                ram_busy=random.uniform(1.00, 100.0),
            )
            db["stats"].insert_one(data.model_dump())
        else:
            stats = psutil.sensors_temperatures()
            stat={
            'time_stamp':pseudo_current_time_str_as_time_stamp,
             'time_stamp_as_int':time_stamp_as_int,
            'cpu_temp':stats["k10temp"][0].current,
            'gpu_temp':stats["amdgpu"][0].current,
            'cpu_busy':float(psutil.cpu_percent()),
            'gpu_busy':float(0),
            'ram_busy':float(psutil.virtual_memory().percent),
            }
            data=schemas.SetStat(**stat)
          
            db["stats"].insert_one(data.model_dump())
        last_current_time_as_int = time_stamp_as_int
        print("Работаю ")
        time.sleep(SECONDS_STAP)


def make_stat_list(time_interval):
    global last_current_time_as_int
    global pseudo_current_time

    stats_list = list()
    if time_interval.interval == "hour":
        start_time = pseudo_current_time - datetime.timedelta(
            seconds=3600 / SECONDS_STAP
        )
        start_time_int = int(start_time.strftime("%Y%m%d%H%M%S"))
    elif time_interval.interval == "minute":
        start_time = pseudo_current_time - datetime.timedelta(seconds=60 / SECONDS_STAP)
        start_time_int = int(start_time.strftime("%Y%m%d%H%M%S"))
    elif time_interval.interval == "day":
        start_time = pseudo_current_time - datetime.timedelta(
            seconds=86300 / SECONDS_STAP
        )
        start_time_int = int(start_time.strftime("%Y%m%d%H%M%S"))
    elif time_interval.interval == "week":
        start_time = pseudo_current_time - datetime.timedelta(
            seconds=604800 / SECONDS_STAP
        )
        start_time_int = int(start_time.strftime("%Y%m%d%H%M%S"))
    cursor = db["stats"].find(
        {
            "$and": [
                {"time_stamp_as_int": {"$lte": last_current_time_as_int}},
                {"time_stamp_as_int": {"$gte": start_time_int}},
            ]
        }
    )
    for i in cursor:
        stats_list.append(schemas.GetStat(**i))

    return stats_list


@app.get("/current_stat", response_model=schemas.GetStat)
async def current_stat():
    global last_current_time_as_int
    print(last_current_time_as_int)
    return schemas.GetStat(
        **db["stats"].find_one({"time_stamp_as_int": last_current_time_as_int})
    )


@app.post("/time_interval_values", response_model=list[schemas.GetStat])
def get_time_interval_values(time_interval: schemas.TimeInterval):
    return make_stat_list(time_interval=time_interval)


@app.post("/add_critical")
def add_critical(critical_params: schemas.CryticalSetter):
    res = {"type": "params"}
    for k, v in critical_params.model_dump().items():
        res[k] = float(v)
    db["critical"].drop()
    db["critical"].insert_one(res)
    return {"status": "ok"}


t1 = threading.Thread(target=system_listenner)
t2 = threading.Thread(target=uvicorn.run, kwargs={"app": app, "host": "0.0.0.0"})
t1.start()
t2.start()
t1.join()
t2.join()
