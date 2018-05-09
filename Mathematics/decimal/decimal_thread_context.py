# decimal_thread_context.py

import decimal
import threading
from queue import PriorityQueue


class Multiplier(threading.Thread):
    def __init__(self, a, b, prec, q):
        self.a = a
        self.b = b
        self.prec = prec
        self.q = q
        threading.Thread.__init__(self)

    def run(self):
        c = decimal.getcontext().copy()
        c.prec = self.prec
        decimal.setcontext(c)
        self.q.put((self.prec, a * b))


a = decimal.Decimal('3.14')
b = decimal.Decimal('1.234')

q = PriorityQueue()
threads = [Multiplier(a, b, i, q) for i in range(1, 6)]
for t in threads:
    t.start()
for t in threads:
    t.join()
for i in range(5):
    prec, value = q.get()
    print('{} {}'.format(prec, value))

