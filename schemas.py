from pydantic import BaseModel
import datetime
import random


class GetStat(BaseModel):
    time_stamp: str
    cpu_temp: float =  random.randint(1, 100)
    gpu_temp: float = random.randint(1, 100)
    cpu_busy: float =  random.randint(1, 100)
    gpu_busy: float =  random.randint(1, 100)
    ram_busy: float =  random.randint(1, 100)

    class Meta:
        from_attributes = True


class SetStat(BaseModel):
    time_stamp: str
    time_stamp_as_int: int
    cpu_temp: float = random.random() * random.randint(1, 100)
    gpu_temp: float = random.random() * random.randint(1, 100)
    cpu_busy: float = random.random() * random.randint(1, 100)
    gpu_busy: float = random.random() * random.randint(1, 100)
    ram_busy: float = random.random() * random.randint(1, 100)

    class Meta:
        from_attributes = True


class TimeInterval(BaseModel):
    interval: str = "minute"

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
