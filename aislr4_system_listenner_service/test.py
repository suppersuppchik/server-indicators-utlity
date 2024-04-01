import psutil # pip install psutil
import time 
print(psutil.process_iter())
for proc in psutil.process_iter():
        if proc.cpu_percent()>0:
            print(proc.cpu_percent())
            time.sleep(5)
        print ("Process {}  started".format(proc.name()))