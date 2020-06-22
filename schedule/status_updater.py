import schedule
import time

def job():
    print("Im working")


schedule.every(10).seconds.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
