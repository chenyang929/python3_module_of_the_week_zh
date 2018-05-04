# time_monotonic.py

import time

start = time.monotonic()
time.sleep(0.2)
end = time.monotonic()
print('start: {:>9.2f}'.format(start))
print('end  : {:>9.2f}'.format(end))
print('span : {:>9.2f}'.format(end - start))

