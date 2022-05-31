import datetime as dt

utc_0 = dt.datetime.now()
utc_6 = utc_0 + dt.timedelta(hours=6)

print(type(utc_6))
print(str(utc_6))
