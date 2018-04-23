# collections_counter_elements.py

import collections

c = collections.Counter('extremely')
c['z'] = 0
print(c)
print(list(c.elements()))


