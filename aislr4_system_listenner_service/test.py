# import psutil
# print(psutil.sensors_temperatures())
import datetime
pseudo_current_time=datetime.datetime.now()
time_stamp=pseudo_current_time.strftime(
                        "%Y-%m-%dT%H:%M:%S.000+00:00"
                    )
print(type(time_stamp))
