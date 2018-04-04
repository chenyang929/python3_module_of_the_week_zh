# collections_chainmap_update_behind.py

import collections

d1 = {'a': 'A', 'c': 'C'}
d2 = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(d1, d2)
print('Before:')
print(m)
print('c={}'.format(m['c']))
d1['c'] = 'C1'
d2['e'] = 'E'
print('After:')
print(m)
print('c={}'.format(m['c']))
