import psutil
import datetime 
import time 
current_time=datetime.datetime.now()
pseudo_current_time=datetime.datetime(year=current_time.year,month=current_time.month,day=current_time.day,hour=current_time.hour,minute=current_time.minute,second=current_time.second,microsecond=0)

while True: 
    pseudo_current_time+=datetime.timedelta(seconds=1)
    print(pseudo_current_time)
    time.sleep(1)
    
