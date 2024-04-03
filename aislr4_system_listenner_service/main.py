import psutil
import datetime
import time
import pymongo
import pydantic
import dataclasses
import random
import requests
import os
import dotenv

dotenv.load_dotenv('./.env')
BOT_TOKEN=os.getenv('BOT_TOKEN')
print(BOT_TOKEN)
class Config(pydantic.BaseModel):

    MONGO_URL: str = "mongodb://localhost:27017"
    CPU_TEMP_CRITICAL: float = 100.00
    GPU_TEMP_CRITICAL: float = 100.00
    CPU_BUSY_CRITICAL: float = 75.00
    GPU_BUSY_CRITICAL: float = 75.00
    RAM_BUSY_CRITICAL: float = 75.00

    class Meta:
        from_attributes = True


@dataclasses.dataclass
class Stat:
    time_stamp: datetime.datetime
    cpu_temp: float
    gpu_temp: float
    cpu_busy: float
    gpu_busy: float
    ram_busy: float


def get_database(CONNECTION_STRING):
    client = pymongo.MongoClient(CONNECTION_STRING)
    return client["server_util_db"]


config = Config()
current_time = datetime.datetime.now()
pseudo_current_time = datetime.datetime(
    year=current_time.year,
    month=current_time.month,
    day=current_time.day,
    hour=current_time.hour,
    minute=current_time.minute,
    second=current_time.second,
    microsecond=0,
)

db = get_database(CONNECTION_STRING=config.MONGO_URL)
is_alerting=False
while True:
    stats = psutil.sensors_temperatures()
    
    try:
        stat={
            'time_stamp':pseudo_current_time.strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    ),
            'cpu_temp':stats["k10temp"][0].current,
            'gpu_temp':stats["amdgpu"][0].current,
            'cpu_busy':float(psutil.cpu_percent()),
            'gpu_busy':float(0),
            'ram_busy':float(psutil.virtual_memory().percent),
        }
        data=  Stat(
                   **stat
                )
      
            
        db["stats"].insert_one(
            dataclasses.asdict(
                data
            )
        )
       
    except:
        # Написано для теста если смотришь на другом ПК
        db["stats"].insert_one(
            dataclasses.asdict(
                Stat(
                    time_stamp=pseudo_current_time.strftime(
                        "%Y-%m-%dT%H:%M:%S.000+00:00"
                    ),
                    cpu_temp=random.random() * random.randint(1, 100),
                    gpu_temp=random.random() * random.randint(1, 100),
                    cpu_busy=random.random() * random.randint(1, 100),
                    gpu_busy=random.random() * random.randint(1, 100),
                    ram_busy=random.random() * random.randint(1, 100),
                )
            )
        )
    if not is_alerting:
            crit= db["critical"].find_one({'type':'params'})['CPU_TEMP_CRITICAL']
            print('crit',type(crit),type(stat['cpu_temp']))
            if stat['cpu_temp'] > crit:
                print('Превышение')
                is_alerting=True
                resp=requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?text=Превышение&chat_id=762835261")
                print(resp)
    pseudo_current_time += datetime.timedelta(seconds=1)
    print("next step")
    time.sleep(1)
