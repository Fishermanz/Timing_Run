import schedule
import sys

def task():
    print("ok")
    sys.exit(0)


schedule_time = "16:21"
schedule.every().day.at(schedule_time).do(task)
while True:
    schedule.run_pending()