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

class CriticalConfig(BaseModel):

    CPU_TEMP_CRITICAL: float = 100.00
    GPU_TEMP_CRITICAL: float = 100.00
    CPU_BUSY_CRITICAL: float = 75.00
    GPU_BUSY_CRITICAL: float = 75.00
    RAM_BUSY_CRITICAL: float = 75.00

    class Meta:
        from_attributes = True

class CryticalSetter(BaseModel):
    CPU_TEMP_CRITICAL: str
    GPU_TEMP_CRITICAL: str
    CPU_BUSY_CRITICAL: str
    GPU_BUSY_CRITICAL: str
    RAM_BUSY_CRITICAL: str

    class Meta:
        from_attributes = True