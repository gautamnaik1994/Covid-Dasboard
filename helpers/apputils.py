import time
import datetime

def date_to_utc(date):
    return time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple())*1000
