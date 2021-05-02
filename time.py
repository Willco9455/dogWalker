import datetime 
t = datetime.time(1,1,00)
d = datetime.datetime(2021, 4, 27)

seconds = datetime.timedelta(hours=t.hour, minutes=t.minute,seconds=t.second).total_seconds()
print(seconds)

day = d.weekday()
print(day)