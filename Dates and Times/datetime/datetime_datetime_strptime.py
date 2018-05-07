# datetime_datetime_strptime.py

import datetime

ft = '%a %b %d %H:%M:%S %Y'

today = datetime.datetime.today()
print('ISO     :', today)

s = today.strftime(ft)
print('strftime:', s)

d = datetime.datetime.strptime(s, ft)
print(d)
print('strptime:', d.strftime(ft))
