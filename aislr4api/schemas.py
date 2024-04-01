from pydantic import BaseModel
import datetime


class GetStat(BaseModel):
    time_stamp: datetime.datetime
    cpu_temp: float
    gpu_temp: float
    cpu_busy: float
    gpu_busy: float
    ram_busy: float

    class Meta:
        from_attributes = True


class TimeInterval(BaseModel):
    interval: str = "hour"

    class Meta:
        from_attributes = True
