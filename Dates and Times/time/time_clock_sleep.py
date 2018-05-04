# time_clock_sleep.py

import time

template = '{} - {:0.2f} - {:0.2f}'

print(template.format(time.ctime(), time.time(), time.clock()))

for i in range(3, 0, -1):
    print('Sleeping', i)
    time.sleep(i)
    print(template.format(time.ctime(), time.time(), time.clock()))
