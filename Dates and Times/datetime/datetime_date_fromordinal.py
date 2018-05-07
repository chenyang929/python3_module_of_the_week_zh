# datetime_date_fromordinal.py

import datetime
import time

o = 736515
print('o              :', o)
print('fromoridinal(o):', datetime.date.fromordinal(o))

t = time.time()
print('t               :', t)
print('fromtimestamp(t):', datetime.date.fromtimestamp(t))
