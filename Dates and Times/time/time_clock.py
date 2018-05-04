# time_clock.py

import hashlib
import time

# 用于计算md5校验和的数据
data = open(__file__, 'rb').read()

for i in range(5):
    h = hashlib.sha1()
    print(time.ctime(), ': {:0.3f} {:0.3f}'.format(time.time(), time.clock()))
    for i in range(300000):
        h.update(data)
    cksum = h.digest()
